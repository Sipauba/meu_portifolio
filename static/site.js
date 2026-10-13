/* Progressive enhancement: content, project URLs and contact work without JS. */
(() => {
  "use strict";
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [
    ...root.querySelectorAll(selector),
  ];
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function setupNavigation() {
    const toggle = $(".menu-toggle");
    const nav = $("#primary-nav");
    if (!toggle || !nav) return;
    const mobile = window.matchMedia("(max-width: 800px)");
    const setOpen = (open, restoreFocus = false) => {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
      nav.classList.toggle("open", open);
      if (restoreFocus) toggle.focus();
    };
    toggle.hidden = false;
    document.documentElement.classList.add("nav-ready");
    toggle.addEventListener("click", () =>
      setOpen(toggle.getAttribute("aria-expanded") !== "true"),
    );
    nav.addEventListener("click", (event) => {
      const link = event.target.closest("a");
      if (!link) return;
      const wasOpen = nav.classList.contains("open");
      setOpen(false);
      if (wasOpen && link.hash && link.pathname === location.pathname) {
        const target = document.getElementById(link.hash.slice(1));
        if (target) {
          target.setAttribute("tabindex", "-1");
          target.focus({ preventScroll: true });
        }
      }
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && nav.classList.contains("open"))
        setOpen(false, true);
    });
    document.addEventListener("click", (event) => {
      if (!event.target.closest(".topbar")) setOpen(false);
    });
    document.addEventListener("focusin", (event) => {
      if (!event.target.closest(".topbar")) setOpen(false);
    });
    mobile.addEventListener("change", () => setOpen(false));
    if (!("IntersectionObserver" in window)) return;
    const links = $$("a[data-section]", nav);
    const sections = links
      .map((link) => document.getElementById(link.dataset.section))
      .filter(Boolean);
    const visible = new Set();
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) =>
          entry.isIntersecting
            ? visible.add(entry.target)
            : visible.delete(entry.target),
        );
        const active = sections
          .filter((section) => visible.has(section))
          .at(-1);
        links.forEach((link) => {
          if (active?.id === link.dataset.section)
            link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      },
      { rootMargin: "-15% 0px -35% 0px" },
    );
    sections.forEach((section) => observer.observe(section));
  }

  function setupCatalog() {
    const toolbar = $(".project-toolbar");
    const grid = $(".project-grid");
    if (!toolbar || !grid) return;
    const cards = $$(".project-card", grid);
    const filters = $$(".filter");
    const search = $("#project-search");
    const count = $(".project-count");
    const collection = $("#collection-label");
    const collectionLabel = collection.textContent;
    const empty = $(".empty-state");
    const normalize = (text) =>
      text
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLocaleLowerCase("pt-BR");
    const index = new Map(
      cards.map((card) => [card, normalize(card.dataset.search)]),
    );
    const params = new URLSearchParams(location.search);
    let selected = filters.some(
      (filter) => filter.dataset.filter === params.get("categoria"),
    )
      ? params.get("categoria")
      : "Todos";
    search.value = (params.get("busca") || "").slice(0, 120);
    const apply = (save = true) => {
      const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
      let total = 0;
      cards.forEach((card) => {
        const matches =
          (selected === "Todos" ||
            card.dataset.filters.split("|").includes(selected)) &&
          terms.every((term) => index.get(card).includes(term));
        card.hidden = !matches;
        if (matches) total++;
      });
      filters.forEach((filter) => {
        const active = filter.dataset.filter === selected;
        filter.classList.toggle("active", active);
        filter.setAttribute("aria-pressed", String(active));
      });
      count.textContent = `${total} ${total === 1 ? "projeto" : "projetos"}${total !== cards.length ? ` de ${cards.length}` : ""}`;
      empty.hidden = total > 0;
      const filtered = selected !== "Todos" || terms.length > 0;
      grid.classList.toggle("is-filtered", filtered);
      collection.textContent = filtered
        ? "RESULTADOS DA SELEÇÃO"
        : collectionLabel;
      if (save) {
        const url = new URL(location.href);
        if (selected === "Todos") url.searchParams.delete("categoria");
        else url.searchParams.set("categoria", selected);
        if (search.value.trim())
          url.searchParams.set("busca", search.value.trim());
        else url.searchParams.delete("busca");
        history.replaceState(null, "", url);
      }
    };
    filters.forEach((filter) =>
      filter.addEventListener("click", () => {
        selected = filter.dataset.filter;
        apply();
      }),
    );
    let timer;
    search.addEventListener("input", () => {
      clearTimeout(timer);
      timer = setTimeout(apply, 120);
    });
    $("#reset-filters").addEventListener("click", () => {
      clearTimeout(timer);
      selected = "Todos";
      search.value = "";
      apply();
      search.focus();
    });
    apply(false);
    toolbar.hidden = false;
  }

  function setupDialog() {
    const dialog = $("#project-dialog");
    const source = $("#projects-data");
    if (!dialog || !source || typeof dialog.showModal !== "function") return;
    let projects;
    try {
      projects = new Map(
        JSON.parse(source.textContent).map((project) => [
          project.slug,
          project,
        ]),
      );
    } catch {
      return;
    } // Direct case-study links remain available if data is invalid.
    let opener;
    const text = (selector, value) => {
      $(selector, dialog).textContent = value;
    };
    $$(".summary-trigger").forEach((button) => {
      const project = projects.get(button.dataset.projectSlug);
      if (!project) return;
      button.hidden = false;
      button.addEventListener("click", () => {
        opener = button;
        text("#dialog-category", project.category);
        text("#dialog-title", project.name);
        text("#dialog-summary", project.summary);
        text("#dialog-problem", project.problem);
        text("#dialog-impact", project.impact);
        $("#dialog-workflow", dialog).replaceChildren(
          ...project.workflow.map((step, i) => {
            const li = document.createElement("li");
            const number = document.createElement("span");
            number.textContent = String(i + 1).padStart(2, "0");
            number.setAttribute("aria-hidden", "true");
            const description = document.createElement("p");
            description.textContent = step;
            li.append(number, description);
            return li;
          }),
        );
        $("#dialog-stack", dialog).replaceChildren(
          ...project.stack.map((item) => {
            const li = document.createElement("li");
            li.textContent = item;
            return li;
          }),
        );
        $("#dialog-github", dialog).href = project.repo;
        $("#dialog-case", dialog).href = $(
          ".case-link",
          button.closest(".project-card"),
        ).href;
        dialog.showModal();
        document.body.classList.add("modal-open");
        $(".dialog-scroll", dialog).scrollTop = 0;
        $(".dialog-close", dialog).focus({ preventScroll: true });
      });
    });
    $(".dialog-close", dialog).addEventListener("click", () => dialog.close());
    dialog.addEventListener("keydown", (event) => {
      if (event.key !== "Tab") return;
      const focusable = $$('button, a[href], [tabindex="0"]', dialog);
      const first = focusable[0];
      const last = focusable.at(-1);
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
    // Only a pointer that starts AND ends outside closes the backdrop.
    const outside = (event) => {
      const r = dialog.getBoundingClientRect();
      return (
        event.clientX < r.left ||
        event.clientX > r.right ||
        event.clientY < r.top ||
        event.clientY > r.bottom
      );
    };
    let backdropStart = false;
    dialog.addEventListener("pointerdown", (event) => {
      backdropStart = event.target === dialog && outside(event);
    });
    dialog.addEventListener("click", (event) => {
      if (backdropStart && event.target === dialog && outside(event))
        dialog.close();
      backdropStart = false;
    });
    dialog.addEventListener("close", () => {
      document.body.classList.remove("modal-open");
      if (opener?.isConnected && !opener.closest("[hidden]"))
        opener.focus({ preventScroll: true });
    });
  }

  function setupMap() {
    const map = $(".integration-map");
    if (!map) return;
    const descriptions = {
      origin: "Sistemas, APIs e dados: o ponto de partida de uma integração.",
      process:
        "Python e n8n orquestram as etapas. A IA apoia a interpretação e transformação dos dados.",
      output:
        "O fluxo se traduz em ações: integrações, alertas e relatórios para a operação.",
    };
    const buttons = $$("[data-map-step]", map);
    buttons.forEach((button) =>
      button.addEventListener("click", () => {
        const step = button.dataset.mapStep;
        buttons.forEach((item) =>
          item.setAttribute("aria-pressed", String(item === button)),
        );
        $$(".map-nodes", map).forEach((node) =>
          node.classList.toggle(
            "map-selected",
            node.classList.contains(`map-${step}`),
          ),
        );
        $("#map-caption").textContent = descriptions[step];
      }),
    );
    $$(".map-origin", map).forEach((node) =>
      node.classList.add("map-selected"),
    );
    $(".map-controls", map).hidden = false;
  }

  function setupReveals() {
    if (motion.matches || !("IntersectionObserver" in window)) return;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-entering");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.15 },
    );
    $$("[data-reveal]").forEach((element) => observer.observe(element));
    motion.addEventListener("change", (event) => {
      if (event.matches) {
        observer.disconnect();
        $$(".is-entering").forEach((element) =>
          element.classList.remove("is-entering"),
        );
      }
    });
  }

  setupNavigation();
  setupCatalog();
  setupDialog();
  setupMap();
  setupReveals();
})();
