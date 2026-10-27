// Boot, orchestration, the frame loop.
//
// Order of operations matters here: the page must sit on TRUE black until the
// critical assets are ready, with bounded waits so slow media cannot trap
// visitors behind the loading screen.

import { Stage } from './gl/stage.js';
import { Clip } from './lib/clip.js';
import { computeLayout } from './scene/layout.js';
import { buildWord, fontsReady } from './scene/type.js';
import { Furniture } from './scene/furniture.js';
import { sample, letterOrder, CUES, T } from './scene/timeline.js';
import { damp, clamp } from './lib/ease.js';
import { initChrono } from './scene3/boot3.js';
import { createBootScreen } from './boot-screen.js';

// a cinematic page manages its own positions; the browser restoring an old
// scroll offset mid-boot yanks the visitor (and any scripted anchor) around
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

const MEDIA = 'public/media/';

const root = document.documentElement;
const boot = document.getElementById('boot');
const bootScreen = createBootScreen({
  root: boot,
  fill: document.getElementById('bootFill'),
  count: document.getElementById('bootCount'),
  line: document.getElementById('bootLine'),
  steps: 3,
});

const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

const app = {
  stage: null,
  furniture: null,
  clips: {},
  layout: null,
  word: null,
  order: [],
  t0: 0,
  fired: new Set(),
  pointer: { x: 0, y: 0, tx: 0, ty: 0 },
  running: false,
  raf: 0,
  heroOnScreen: true,
};

// --------------------------------------------------------------------------

async function main() {
  const canvas = document.getElementById('stage');
  app.stage = new Stage(canvas);
  app.furniture = new Furniture(document);

  if (!app.stage.ok) return degrade('WebGL unavailable');

  let manifest;
  try {
    manifest = await fetch(`${MEDIA}manifest.json`, { signal: AbortSignal.timeout(8000) }).then((r) => r.json());
  } catch {
    return degrade('media manifest missing');
  }

  const tick = () => bootScreen.step();

  await Promise.race([Promise.all([
    fontsReady().then(tick),
    app.stage.loadTextures({
      grunge: 'public/tex/grunge.png',
      grain: 'public/tex/grain.png',
      floor: 'public/media/hero-wet-floor.png',
    }).then(tick),
  ]), wait(8000).then(() => { throw new Error('startup timed out'); })]);

  const mk = (name, loopFade) => {
    const c = manifest.clips[name];
    return new Clip({
      src: [
        { url: MEDIA + c.webm, type: 'video/webm' },
        { url: MEDIA + c.mp4, type: 'video/mp4' },
      ],
      poster: MEDIA + c.poster,
      w: c.w, h: c.h, track: c.track, format: c.format, loopFade,
    });
  };
  app.clips.hero = mk('hero', 0.7);
  const sound = document.getElementById('heroSound');
  const video = app.clips.hero.el;
  let soundWanted = true;
  let restoredSoundAt = 0;
  video.muted = false;
  video.defaultMuted = false;
  video.volume = 1;
  const syncSound = () => {
    const enabled = soundWanted;
    sound.textContent = enabled ? 'Sound on' : 'Sound off';
    sound.setAttribute('aria-pressed', String(enabled));
    sound.setAttribute('aria-label', enabled ? 'Mute video sound' : 'Enable video sound');
  };
  const enableSoundFromGesture = async () => {
    if (!soundWanted) return false;
    video.muted = false;
    video.volume = 1;
    syncSound();
    const ok = await app.clips.hero.play();
    if (ok) restoredSoundAt = performance.now();
    return ok;
  };
  sound.hidden = false;
  syncSound();
  video.addEventListener('volumechange', syncSound);
  sound.addEventListener('click', async () => {
    if (performance.now() - restoredSoundAt < 300) return;
    if (soundWanted && video.muted) {
      await enableSoundFromGesture();
      return;
    }
    soundWanted = !soundWanted;
    video.muted = !soundWanted;
    syncSound();
    if (soundWanted && !await app.clips.hero.play()) {
      soundWanted = false;
      video.muted = true;
      syncSound();
    }
  });

  layout();
  window.addEventListener('resize', debounce(layout, 140));
  window.addEventListener('orientationchange', () => setTimeout(layout, 220));

  await app.clips.hero.whenReady();
  tick();

  // Prepare the next scene near the viewport without delaying the hero.
  const section = document.getElementById('chrono');
  const observer = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;
    observer.disconnect();
    initChrono().then((c) => { app.chrono = c; })
      .catch((e) => console.warn('[stephen] chrono unavailable:', e.message));
  }, { rootMargin: '600px' });
  if (section) observer.observe(section);

  await begin();

  if (reduced || !app.heroOnScreen || document.hidden) return;
  let playing = await app.clips.hero.play();
  if (!playing && soundWanted) {
    video.muted = true;
    playing = await app.clips.hero.play();
    const restoreSound = async () => {
      await enableSoundFromGesture();
      window.removeEventListener('pointerdown', restoreSound);
      window.removeEventListener('keydown', restoreSound);
    };
    window.addEventListener('pointerdown', restoreSound, { once: true, capture: true });
    window.addEventListener('keydown', restoreSound, { once: true });
  }
}

async function begin() {
  // let the title card land on 100 and clear before the sequence starts on black
  await bootScreen.finish();
  root.classList.remove('is-booting');
  app.t0 = performance.now();
  app.running = true;
  bindPointer();

  // ?t=4.2 starts the sequence part-way through, and ?t=end lands on the
  // settled composition. Purely a review aid for tuning a single beat without
  // sitting through the whole opening each time.
  const q = new URLSearchParams(location.search).get('t');
  if (q !== null) {
    const at = q === 'end' ? T.settled : parseFloat(q);
    if (Number.isFinite(at)) {
      app.t0 = performance.now() - at * 1000;
      for (const [when, name] of CUES) {
        if (at >= when) { app.fired.add(name); root.classList.add(`is-${name}`); }
      }
    }
  }
  if (reduced) {
    // honour the preference fully: land on the finished composition and hold it
    // still - no build-up, no looping walk, no drifting grain
    app.t0 = performance.now() - T.settled * 1000;
    for (const [, name] of CUES) root.classList.add(`is-${name}`);
    const c = app.clips.hero;
    const still = () => {
      c.pause();
      c.needsUpload = true;
      renderStill();
      window.addEventListener('resize', debounce(renderStill, 160));
    };
    renderStill();
    c.el.addEventListener('seeked', still, { once: true });
    c.el.currentTime = Math.min(6, (c.duration || 8) * 0.6);
    return;
  }
  if (app.heroOnScreen && !document.hidden) app.raf = requestAnimationFrame(frame);
}

// --------------------------------------------------------------------------

function layout() {
  const w = window.innerWidth;
  const h = window.innerHeight;
  const L = computeLayout(w, h);
  app.layout = L;
  app.stage.resize(L);

  const capPx = Math.round(L.word.capH * L.dpr);
  if (!app.word || Math.abs(app.word.capPx - capPx) > 2) {
    const word = buildWord(capPx, app.stage.maxTexture);
    word.capPx = capPx;
    app.word = word;
    app.stage.setWord(word);
    app.order = letterOrder(word.letters);
  }
  app.furniture.apply(L);
}

function bindPointer() {
  if (reduced || matchMedia('(pointer: coarse)').matches) return;
  window.addEventListener('pointermove', (e) => {
    // normalised to -1..1, then damped in the frame loop; the response is
    // deliberately small — depth, not a toy
    app.pointer.tx = (e.clientX / window.innerWidth) * 2 - 1;
    app.pointer.ty = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });
  window.addEventListener('pointerleave', () => {
    app.pointer.tx = 0;
    app.pointer.ty = 0;
  });
}

let last = 0;
function frame(now) {
  app.raf = 0;
  if (!app.running || document.hidden || !app.heroOnScreen) return;
  const t = (now - app.t0) / 1000;
  const dt = Math.min(0.05, (now - last) / 1000 || 0.016);
  last = now;

  for (const [at, name] of CUES) {
    if (t >= at && !app.fired.has(name)) {
      app.fired.add(name);
      root.classList.add(`is-${name}`);
    }
  }

  const p = app.pointer;
  p.x = damp(p.x, p.tx, 3.1, dt);
  p.y = damp(p.y, p.ty, 3.1, dt);
  // parallax only comes alive once the composition has settled
  const gate = clamp((t - T.settled + 0.9) / 1.2);
  app.stage.parallax.x = p.x * gate;
  app.stage.parallax.y = p.y * gate;

  const state = sample(t, app.word.letters.length, app.order);

  // after the intro the wordmark breathes very slightly, so the frame never
  // becomes a static image
  if (state.settled) {
    const b = Math.sin(t * 0.42) * 0.5 + Math.sin(t * 0.27 + 1.3) * 0.5;
    for (const l of state.letters) l.dy = b * 0.0035;
  }

  app.stage.render(state, t, app.clips);
  app.raf = requestAnimationFrame(frame);
}

// --------------------------------------------------------------------------

function degrade(reason) {
  console.warn('[stephen] falling back:', reason);
  root.classList.remove('is-booting');
  root.classList.add('is-fallback');
  bootScreen.abort();
  for (const [, name] of CUES) root.classList.add(`is-${name}`);
  document.querySelector('.stage-wrap').insertAdjacentHTML('afterbegin',
    '<div class="fallback"><p>STEPHEN</p>'
    + '<small>Welcome to my world</small></div>');
}

function renderStill() {
  layout();
  const state = sample(T.settled + 1, app.word.letters.length, app.order);
  app.stage.render(state, T.settled + 1, app.clips);
}

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

function debounce(fn, ms) {
  let id;
  return (...a) => { clearTimeout(id); id = setTimeout(() => fn(...a), ms); };
}

// mobile menu
const burger = document.getElementById('burger');
const menu = document.getElementById('menu');
menu?.querySelectorAll('a').forEach((a, i) => a.style.setProperty('--i', i));
function setMenu(open) {
  burger.setAttribute('aria-expanded', String(open));
  root.classList.toggle('is-menu', open);
  if (open) menu.hidden = false;
  else setTimeout(() => { if (!root.classList.contains('is-menu')) menu.hidden = true; }, 500);
}
burger?.addEventListener('click', () =>
  setMenu(burger.getAttribute('aria-expanded') !== 'true'));
menu?.addEventListener('click', (e) => {
  if (e.target.closest('a')) setMenu(false);
});
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && root.classList.contains('is-menu')) setMenu(false);
});

// Stop both GPU work and decoding while the hero cannot be seen.
function syncHeroPlayback() {
  const visible = app.heroOnScreen && !document.hidden;
  const clip = app.clips.hero;
  if (!visible) {
    cancelAnimationFrame(app.raf);
    app.raf = 0;
    clip?.pause();
  } else if (app.running && !reduced) {
    if (clip?.el.paused) clip.play();
    if (!app.raf) {
      last = performance.now();
      app.raf = requestAnimationFrame(frame);
    }
  }
}
const heroWrap = document.querySelector('.stage-wrap');
const spacer = document.querySelector('.hero-spacer');
if (heroWrap && spacer && 'IntersectionObserver' in window) {
  new IntersectionObserver(([entry]) => {
    app.heroOnScreen = entry.isIntersecting;
    document.getElementById('heroSound').hidden = !entry.isIntersecting;
    heroWrap.style.visibility = entry.isIntersecting ? '' : 'hidden';
    syncHeroPlayback();
  }).observe(spacer);
}
document.addEventListener('visibilitychange', syncHeroPlayback);

// Review hook. Draws one frame on demand and reads the framebuffer in the SAME
// task, because the context is created without preserveDrawingBuffer. Rendering
// here rather than piggy-backing on the animation loop means it still works when
// the tab is hidden and rAF is throttled to a stop.
window.__shot = async (name = 'shot', at = null) => {
  if (!app.word) return 'not ready';
  const t = at !== null ? at : (performance.now() - app.t0) / 1000;
  app.stage.render(sample(t, app.word.letters.length, app.order), t, app.clips);
  const url = app.stage.canvas.toDataURL('image/png');
  await fetch(`/__shot?name=${encodeURIComponent(name)}`,
    { method: 'POST', body: url });
  return `${app.stage.canvas.width}x${app.stage.canvas.height} @ t=${t.toFixed(2)}`;
};

// live tuning of the letter surface while matching the reference art
window.__tune = (k, v) => { app.stage[k] = v; return app.stage[k]; };

main().catch((e) => degrade(e.message));
