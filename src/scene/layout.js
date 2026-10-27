// Composition geometry.
//
// Proportions follow the red studio reference, with a viewport-based mobile fit.

import { renderScale } from '../lib/render-scale.js';

import { TARGET_RATIO } from './type.js';

export const REF = {
  wordWidth: 0.78,     // fraction of viewport width
  capHeight: 0.44,     // fraction of viewport height
  vCentre: 0.473,       // vertical centre of the cap box
  legend: { x: 0.869, y: 0.265, h: 0.0422 },
  artist: { x: 0.077, y: 0.586, h: 0.0367 },
  dotsBR: { x: 0.967, y: 0.905 },
  arrows: { left: 0.023, right: 0.967, top: 0.369, bottom: 0.607, count: 5 },
};

export function computeLayout(w, h) {
  const portrait = h / w > 1.05;
  const narrow = w < 760;

  // fit the word by whichever axis binds first, preserving its proportions
  const byWidth = (REF.wordWidth * w) / TARGET_RATIO;
  const byHeight = REF.capHeight * h;
  let capH = Math.min(byWidth, byHeight);

  // On a phone the word is width-bound and ends up short, leaving a dead band of
  // empty screen. Letting it grow taller there keeps the composition dense
  // instead of stranding the type in the middle of nowhere.
  if (portrait) capH = Math.min(byWidth * 1.0, h * 0.30);

  const wordW = capH * TARGET_RATIO;
  const cx = w * 0.5;
  const vCentre = portrait ? h * 0.50 : h * REF.vCentre;
  const capTop = vCentre - capH * 0.5;
  const baseline = vCentre + capH * 0.5;

  const word = {
    x: cx - wordW * 0.5,
    y: capTop,
    w: wordW,
    h: capH,
    capH,
    baseline,
  };

  // The foreground figure rises above the letters and meets the lit floor.
  let heroH = capH * 1.42;
  let feet = baseline + capH * 0.33;

  if (portrait) {
    // on a phone the word is width-bound and short, so tying the man to it would
    // shrink him to a bystander; he is scaled to the viewport instead and the
    // wordmark crosses his torso
    heroH = h * 0.54;
    feet = h * 0.885;
  }

  return {
    w,
    h,
    dpr: renderScale(w, h),
    portrait,
    narrow,
    word,
    hero: { h: heroH, cx, feet },
    // clear of the header band and clear of his head; it renders in front of
    // the typography, so it stays readable wherever it lands
    welcomeY: portrait ? (feet - heroH) - h * 0.075 : h * 0.19,
    legend: portrait
      ? { x: w * 0.955, y: capTop - h * 0.052, h: 20, alignRight: true }
      : { x: w * REF.legend.x, y: h * REF.legend.y,
          h: Math.max(18, h * REF.legend.h) },
    artist: portrait
      ? { x: w * 0.045, y: baseline + h * 0.055, h: 19 }
      : { x: w * REF.artist.x, y: h * REF.artist.y,
          h: Math.max(16, h * REF.artist.h) },
    ember: { x: 0.5, y: vCentre / h },
  };
}

/**
 * Place a clip so the SUBJECT (not the video rectangle) lands where we want.
 * The tracks baked into the manifest give the subject's box per frame, so a
 * figure can be anchored by his feet and held at a chosen height even though he
 * walks toward the camera and grows through the shot.
 */
export function fitSubject(track, frameAspect, opts) {
  const [x0, y0, x1, y1] = track;
  const subH = Math.max(y1 - y0, 1e-3);
  const subCX = (x0 + x1) * 0.5;

  const quadH = opts.height / subH;          // video height needed
  const quadW = quadH * frameAspect;

  const footY = opts.feet !== undefined ? opts.feet : opts.top + opts.height;
  return {
    x: opts.cx - quadW * subCX,
    y: footY - quadH * y1,
    w: quadW,
    h: quadH,
  };
}
