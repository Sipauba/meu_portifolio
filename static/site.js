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

const panel = document.querySelector('.hero-panel');
const canvas = document.querySelector('.network-canvas');
if (panel && canvas) {
  const context = canvas.getContext('2d');
  if (context) {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const labels = ['RPA', 'API', 'ERP', 'IA', 'GLPI', 'DADOS', 'IoT'];
    const nodes = [
      { x: .50, y: .48, label: 'AUTOMAÇÃO', main: true },
      { x: .21, y: .28, label: labels[0] },
      { x: .76, y: .22, label: labels[1] },
      { x: .82, y: .55, label: labels[2] },
      { x: .65, y: .79, label: labels[3] },
      { x: .24, y: .74, label: labels[4] },
      { x: .12, y: .51, label: labels[5] },
      { x: .52, y: .16, label: labels[6] },
    ];
    let width = 0;
    let height = 0;
    let tick = 0;
    let frame = 0;
    let active = false;
    let pointer = { x: -1000, y: -1000 };
    let phase = 0;
    const resize = () => {
      const box = panel.getBoundingClientRect();
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      width = box.width;
      height = box.height;
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      draw();
    };
    const position = (node, index) => {
      const drift = reducedMotion.matches ? 0 : Math.sin(tick + index * 1.7) * 5;
      return { x: node.x * width + drift, y: node.y * height + drift * .6 };
    };
    const draw = () => {
      context.clearRect(0, 0, width, height);
      const points = nodes.map(position);
      const center = points[0];
      const glow = context.createRadialGradient(center.x, center.y, 0, center.x, center.y, width * .55);
      glow.addColorStop(0, '#3cbacb32');
      glow.addColorStop(1, '#3cbacb00');
      context.fillStyle = glow;
      context.fillRect(0, 0, width, height);
      points.slice(1).forEach((point, index) => {
        const distance = Math.hypot(pointer.x - point.x, pointer.y - point.y);
        const nearby = distance < 60;
        context.beginPath();
        context.moveTo(center.x, center.y);
        context.lineTo(point.x, point.y);
        context.strokeStyle = nearby ? '#99f5f3' : '#5bc2ce8a';
        context.lineWidth = nearby ? 2 : 1;
        context.stroke();
        if (index < points.length - 2) {
          const next = points[index + 2];
          context.beginPath();
          context.moveTo(point.x, point.y);
          context.lineTo(next.x, next.y);
          context.strokeStyle = '#4e9daf4d';
          context.lineWidth = 1;
          context.stroke();
        }
        const pulse = reducedMotion.matches ? .5 : (Math.sin(tick * 2 + index + phase) + 1) / 2;
        const x = center.x + (point.x - center.x) * pulse;
        const y = center.y + (point.y - center.y) * pulse;
        context.beginPath();
        context.arc(x, y, 2.3, 0, Math.PI * 2);
        context.fillStyle = '#c4ffff';
        context.fill();
      });
      points.forEach((point, index) => {
        const node = nodes[index];
        const hovered = Math.hypot(pointer.x - point.x, pointer.y - point.y) < (node.main ? 55 : 35);
        const radius = node.main ? 38 : hovered ? 22 : 17;
        context.beginPath();
        context.arc(point.x, point.y, radius + 7, 0, Math.PI * 2);
        context.strokeStyle = hovered ? '#9fffff88' : '#65cbd533';
        context.stroke();
        context.beginPath();
        context.arc(point.x, point.y, radius, 0, Math.PI * 2);
        context.fillStyle = node.main ? '#1b5566' : hovered ? '#24677a' : '#173a4c';
        context.fill();
        context.strokeStyle = hovered ? '#b8fffc' : '#6fc9d5';
        context.stroke();
        context.fillStyle = '#ecffff';
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.font = `${node.main ? 'bold 13px' : '11px'} Manrope, sans-serif`;
        context.fillText(node.label, point.x, point.y);
      });
    };
    const animate = () => {
      if (!active || reducedMotion.matches) return;
      tick += .012;
      draw();
      frame = window.requestAnimationFrame(animate);
    };
    new ResizeObserver(resize).observe(panel);
    new IntersectionObserver(entries => {
      active = entries[0].isIntersecting;
      window.cancelAnimationFrame(frame);
      if (active) animate();
    }).observe(panel);
    panel.addEventListener('pointermove', event => {
      const box = panel.getBoundingClientRect();
      pointer = { x: event.clientX - box.left, y: event.clientY - box.top };
      if (reducedMotion.matches) draw();
    });
    panel.addEventListener('pointerleave', () => {
      pointer = { x: -1000, y: -1000 };
      if (reducedMotion.matches) draw();
    });
    panel.querySelector('.network-reset').addEventListener('click', () => {
      phase += Math.PI / 2;
      nodes.slice(1).forEach((node, index) => {
        const angle = (index / (nodes.length - 1)) * Math.PI * 2 + phase;
        node.x = .5 + Math.cos(angle) * .34;
        node.y = .48 + Math.sin(angle) * .31;
      });
      draw();
    });
    reducedMotion.addEventListener('change', () => {
      window.cancelAnimationFrame(frame);
      if (active) animate();
      draw();
    });
    resize();
  }
}
