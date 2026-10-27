const section = document.getElementById('certifications');
const frames = [...section.querySelectorAll('.cert-room__frame')];
const previous = document.getElementById('certRoomPrev');
const next = document.getElementById('certRoomNext');
const dialog = document.getElementById('certRoomDialog');
let page = 0;

function showPage(value) {
  page = Math.max(0, Math.min(Math.ceil(frames.length / 6) - 1, value));
  frames.forEach((frame, index) => { frame.hidden = Math.floor(index / 6) !== page; });
  document.getElementById('certRoomCount').textContent = `${String(page * 6 + 1).padStart(2, '0')} — ${String(Math.min((page + 1) * 6, frames.length)).padStart(2, '0')} / ${frames.length}`;
  previous.disabled = page === 0;
  next.disabled = (page + 1) * 6 >= frames.length;
  if (document.activeElement === next && next.disabled) previous.focus({ preventScroll: true });
  else if (document.activeElement === previous && previous.disabled) next.focus({ preventScroll: true });
}
previous.addEventListener('click', () => showPage(page - 1));
next.addEventListener('click', () => showPage(page + 1));
frames.forEach(frame => frame.addEventListener('click', () => {
  const image = frame.querySelector('img');
  const full = document.getElementById('certRoomFull');
  full.src = image.src;
  full.alt = image.alt;
  document.getElementById('certRoomDialogTitle').textContent = frame.dataset.title;
  document.getElementById('certRoomIssuer').textContent = frame.dataset.issuer;
  document.getElementById('certRoomOriginal').href = image.src;
  dialog.showModal();
}));
dialog.addEventListener('click', event => {
  const bounds = dialog.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
});
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    if (entries.some(entry => entry.isIntersecting)) {
      section.classList.add('is-visible');
      observer.disconnect();
    }
  }, { threshold: .12 });
  observer.observe(section);
}
