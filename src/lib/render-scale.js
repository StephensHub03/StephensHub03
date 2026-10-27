// Bound full-screen shader cost independently of display resolution.
export function renderScale(w, h) {
  const mobile = matchMedia('(pointer: coarse)').matches;
  const budget = mobile ? 1500000 : 2500000;
  return Math.min(window.devicePixelRatio || 1, mobile ? 1.25 : 1.5,
    Math.sqrt(budget / Math.max(1, w * h)));
}
