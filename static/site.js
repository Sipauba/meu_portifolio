const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#primary-nav');
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  nav.classList.toggle('open', open);
});
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Abrir menu');
}));
const cards = [...document.querySelectorAll('.project-card')];
const count = document.querySelector('.project-count');
const empty = document.querySelector('.empty-state');
document.querySelectorAll('.filter').forEach(button => button.addEventListener('click', () => {
  const filter = button.dataset.filter;
  document.querySelectorAll('.filter').forEach(item => {
    const active = item === button;
    item.classList.toggle('active', active);
    item.setAttribute('aria-pressed', String(active));
  });
  let visible = 0;
  cards.forEach(card => {
    const matches = filter === 'Todos' || card.dataset.filters.split('|').includes(filter);
    card.hidden = !matches;
    if (matches) visible++;
  });
  count.textContent = `${visible} ${visible === 1 ? 'projeto' : 'projetos'}`;
  empty.hidden = visible > 0;
}));
window.addEventListener('scroll', () => document.querySelector('.topbar').classList.toggle('scrolled', window.scrollY > 12), { passive: true });
