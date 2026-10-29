// Observe individual elements so long mobile sections reveal as they are read.
const groups = [
  '.experience__heading, .experience__note, .experience__mobile-hint',
  '.cert-room__intro, .cert-room__script--top, .cert-room__wall-heading, .cert-room__milestone-title, .cert-room__milestones > article, .cert-room__script--bottom, .cert-room__footer',
  '.contact__portrait, .contact__top, .contact h2, .contact__script, .contact__intro, .contact__card, .contact__rail, .contact__closing, .contact__location',
];

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('closing-revealed');
      observer.unobserve(entry.target);
    }
  }, { threshold: .12 });

  for (const selector of groups) {
    document.querySelectorAll(selector).forEach((element, index) => {
      element.classList.add('closing-reveal');
      element.style.setProperty('--closing-delay', `${(index % 4) * 80}ms`);
      observer.observe(element);
    });
  }
}
