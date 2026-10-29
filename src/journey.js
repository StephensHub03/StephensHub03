const links = [...document.querySelectorAll('[data-nav]')];
const sections = [...new Set(links.map(link => link.hash))]
  .map(hash => document.getElementById(hash.slice(1)))
  .filter(Boolean);
const experienceSection = document.getElementById('experience');
const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');

function updateExperienceMotion() {
  if (!experienceSection) return;
  if (motionPreference.matches) {
    experienceSection.style.removeProperty('--experience-slide');
    return;
  }
  // Match the Skills entrance timing, arriving from the opposite side.
  const top = experienceSection.getBoundingClientRect().top;
  const progress = Math.max(0, Math.min(1,
    (window.innerHeight - top) / (window.innerHeight * .82)));
  const eased = progress * progress * (3 - 2 * progress);
  experienceSection.style.setProperty('--experience-slide', `${-(1 - eased) * 100}%`);
}

function updateNavigation() {
  document.documentElement.classList.toggle('is-scrolled', window.scrollY > 40);
  const marker = window.innerHeight * 0.3;
  let current = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= marker) current = section;
  }
  for (const link of links) {
    const active = link.hash === `#${current.id}`;
    link.classList.toggle('is-active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
}

let pending = false;
function scheduleUpdate() {
  if (pending) return;
  pending = true;
  requestAnimationFrame(() => {
    pending = false;
    updateNavigation();
    updateExperienceMotion();
  });
}
window.addEventListener('scroll', scheduleUpdate, { passive: true });
window.addEventListener('resize', scheduleUpdate);
window.addEventListener('load', scheduleUpdate);
window.addEventListener('hashchange', scheduleUpdate);
motionPreference.addEventListener('change', scheduleUpdate);
updateNavigation();
updateExperienceMotion();

// Reveal each timeline entry independently, including on the stacked mobile layout.
if (experienceSection && 'IntersectionObserver' in window) {
  const items = experienceSection.querySelectorAll(
    '.journey__intro, .journey__history > blockquote, .journey__milestone, .journey__stats > div'
  );
  const reveals = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('journey-revealed');
      reveals.unobserve(entry.target);
    }
  }, { threshold: .18 });
  items.forEach((item, index) => {
    item.classList.add('journey-reveal');
    item.style.setProperty('--reveal-delay', `${Math.min(index % 6, 4) * 75}ms`);
    reveals.observe(item);
  });
}
