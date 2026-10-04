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

// Cards keep their URLs as a fallback; ordinary clicks open an accessible dialog.
const projectDialog = document.querySelector('#project-dialog');
const projectData = document.querySelector('#projects-data');
if (projectDialog && projectData && typeof projectDialog.showModal === 'function') {
  const projects = new Map(JSON.parse(projectData.textContent).map(project => [project.slug, project]));
  const closeButton = projectDialog.querySelector('.dialog-close');
  let opener = null;
  const setText = (selector, value) => {
    projectDialog.querySelector(selector).textContent = value;
  };
  const closeDialog = () => projectDialog.close();
  document.querySelectorAll('.card-cover-link[data-project-slug]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const project = projects.get(link.dataset.projectSlug);
      if (!project) return;
      event.preventDefault();
      opener = link;
      setText('#dialog-category', project.category);
      setText('#dialog-title', project.name);
      setText('#dialog-summary', project.summary);
      setText('#dialog-problem', project.problem);
      setText('#dialog-impact', project.impact);
      const workflow = projectDialog.querySelector('#dialog-workflow');
      workflow.replaceChildren(...project.workflow.map((step, index) => {
        const row = document.createElement('li');
        const number = document.createElement('span');
        number.textContent = String(index + 1).padStart(2, '0');
        const description = document.createElement('p');
        description.textContent = step;
        row.append(number, description);
        return row;
      }));
      const stack = projectDialog.querySelector('#dialog-stack');
      stack.replaceChildren(...project.stack.map(item => {
        const tag = document.createElement('span');
        tag.textContent = item;
        return tag;
      }));
      projectDialog.querySelector('#dialog-github').href = project.repo;
      projectDialog.showModal();
      document.body.classList.add('modal-open');
      closeButton.focus();
    });
  });
  projectDialog.querySelectorAll('.dialog-close, .dialog-back').forEach(button => button.addEventListener('click', closeDialog));
  projectDialog.addEventListener('click', event => {
    if (event.target === projectDialog) closeDialog();
  });
  projectDialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    if (opener?.isConnected) opener.focus();
  });
}

// Reveal content once as it enters the viewport; show everything for reduced motion.
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window && !reducedMotion.matches) {
  const revealTargets = [...document.querySelectorAll(
    '.hero-copy, .hero-panel, .about-layout, .section-heading, .area-card, .featured-card, .project-toolbar, .project-card, .stack-group, .contact-section'
  )];
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -24px 0px' });
  document.querySelectorAll('.areas-grid, .featured-grid, .project-grid, .stack-grid').forEach(grid => {
    [...grid.children].forEach((element, index) => {
      element.style.setProperty('--reveal-delay', `${(index % 3) * 70}ms`);
    });
  });
  revealTargets.forEach(element => {
    element.classList.add('reveal-item');
    observer.observe(element);
  });
  document.documentElement.classList.add('has-reveal');
  reducedMotion.addEventListener('change', event => {
    if (!event.matches) return;
    document.documentElement.classList.remove('has-reveal');
    observer.disconnect();
  }, { once: true });
}
