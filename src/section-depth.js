// Event delegation also covers Skills cards mounted asynchronously by React.
const motion = matchMedia('(min-width: 901px) and (hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)');
const cardSelector = '.contact__card, .cert-room__frame, .cert-room__milestones article, .journey__card, .skill-card';
const sections = document.querySelectorAll('#contact, #certifications, #experience, .skills-scene');
const controllers = [];

for (const section of sections) {
  let frame = 0;
  let pointer = null;
  let activeCard = null;
  const clearCard = () => {
    if (!activeCard) return;
    activeCard.style.removeProperty('--card-rx');
    activeCard.style.removeProperty('--card-ry');
    activeCard.classList.remove('depth-active');
    activeCard = null;
  };
  const reset = () => {
    cancelAnimationFrame(frame);
    frame = 0;
    pointer = null;
    clearCard();
    section.style.removeProperty('--depth-rx');
    section.style.removeProperty('--depth-ry');
  };
  const paint = () => {
    frame = 0;
    if (!pointer || !motion.matches || document.querySelector('dialog[open]')) return reset();
    const box = section.getBoundingClientRect();
    const x = Math.max(-1, Math.min(1, (pointer.x - box.left) / box.width * 2 - 1));
    const y = Math.max(-1, Math.min(1, (pointer.y - box.top) / box.height * 2 - 1));
    section.style.setProperty('--depth-rx', `${-y * 1.2}deg`);
    section.style.setProperty('--depth-ry', `${x * 1.8}deg`);
    const card = pointer.target.closest(cardSelector);
    if (card !== activeCard) clearCard();
    if (!card) return;
    activeCard = card;
    const bounds = card.getBoundingClientRect();
    const cx = Math.max(-1, Math.min(1, (pointer.x - bounds.left) / bounds.width * 2 - 1));
    const cy = Math.max(-1, Math.min(1, (pointer.y - bounds.top) / bounds.height * 2 - 1));
    card.style.setProperty('--card-rx', `${-cy * 5}deg`);
    card.style.setProperty('--card-ry', `${cx * 6}deg`);
    card.classList.add('depth-active');
  };
  section.addEventListener('pointermove', event => {
    if (!motion.matches || event.pointerType === 'touch') return;
    pointer = { x: event.clientX, y: event.clientY, target: event.target };
    if (!frame) frame = requestAnimationFrame(paint);
  }, { passive: true });
  section.addEventListener('pointerleave', reset);
  section.addEventListener('pointercancel', reset);
  section.addEventListener('click', reset);
  controllers.push(reset);
  new IntersectionObserver(([entry]) => { if (!entry.isIntersecting) reset(); }).observe(section);
}
const resetAll = () => controllers.forEach(reset => reset());
motion.addEventListener('change', resetAll);
window.addEventListener('blur', resetAll);
document.addEventListener('visibilitychange', () => { if (document.hidden) resetAll(); });
