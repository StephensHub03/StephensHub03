// Scene two's lifecycle — the supplied artwork, presented.
//
// The section IS the reference image. What this file adds is presentation:
// the artwork arrives from black when the section is reached.
//
// The procedural WebGL version of this room (universe.js, ribbon.js,
// particles.js, shaders2.js) is parked, not deleted — swap this module's
// implementation back if the live, pointer-reactive variant is ever wanted.

export async function initUniverse() {
  const section = document.getElementById('universe');
  const image = document.getElementById('uniImage');
  const veil = document.getElementById('uniVeil');
  if (!section || !image || !veil) return null;

  const state = { entered: false };

  new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) {
        if (!state.entered) {
          state.entered = true;
          section.classList.add('is-on');
          veil.style.opacity = '0';
        }
      }
    }
  }, { threshold: 0.30 }).observe(section);

  image.addEventListener('error', () => section.classList.add('is-fallback'),
    { once: true });

  return { image, section };
}
