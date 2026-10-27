// The loading title card. Progress is driven by the real asset loads in
// main.js; this only smooths the counter so it reads like a film leader
// rather than jumping between three discrete steps.

const LINES = ['Setting the stage', 'Lighting the scene', 'Rolling the film', 'Welcome to my world'];
const MIN_SHOW = 1900;   // long enough for the wordmark to finish arriving
const SETTLE = 450;      // time for the counter to land on 100 before the exit

export function createBootScreen({ root, fill, count, line, steps }) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const shownAt = performance.now();
  let done = 0;
  let target = 0;
  let shown = 0;
  let raf = 0;
  let finished = false;

  const render = () => {
    const rounded = Math.round(shown);
    count.textContent = String(rounded).padStart(2, '0');
    fill.style.width = `${shown}%`;
  };

  const frame = () => {
    // Ease toward whichever is lower: the assets actually loaded, or how far
    // through the minimum display time we are. Local/cached assets then still
    // read as one continuous climb instead of a jump to 100 that idles.
    const paced = Math.min(100, ((performance.now() - shownAt) / MIN_SHOW) * 100);
    const goal = Math.min(target, paced);
    shown += (goal - shown) * (reduced ? 1 : 0.12);
    if (!finished && target < 100 && shown < target + 6) shown += 0.05;   // slow creep while a step stalls
    shown = Math.min(shown, 100);
    render();
    if (finished && shown > 99.6) { shown = 100; render(); return; }
    raf = requestAnimationFrame(frame);
  };

  const setLine = (text) => {
    if (line.textContent === text) return;
    if (reduced) { line.textContent = text; return; }
    line.classList.add('is-swapping');
    setTimeout(() => { line.textContent = text; line.classList.remove('is-swapping'); }, 300);
  };

  render();
  raf = requestAnimationFrame(frame);

  return {
    // one asset group ready; the counter heads to the next milestone
    step() {
      done = Math.min(done + 1, steps);
      target = (done / steps) * 92;
      setLine(LINES[Math.min(done, LINES.length - 2)]);
    },
    // resolves once the card has been on screen long enough and the counter reads 100
    async finish() {
      if (finished) return;
      finished = true;
      target = 100;
      setLine(LINES[LINES.length - 1]);
      const remaining = reduced ? 0 : Math.max(0, MIN_SHOW - (performance.now() - shownAt));
      await wait(remaining + (reduced ? 0 : SETTLE));
      cancelAnimationFrame(raf);
      shown = 100; render();
      root.classList.add('is-done');
    },
    // immediate exit for the no-WebGL / no-media fallback
    abort() {
      finished = true;
      cancelAnimationFrame(raf);
      root.classList.add('is-done');
    },
  };
}

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
