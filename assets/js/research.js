/* Progressive enhancements. The site is fully readable without JavaScript. */
(() => {
  const root = document.documentElement;
  const system = window.matchMedia("(prefers-color-scheme: dark)");

  /* Appearance toggle ---------------------------------------------------- */
  const button = document.querySelector(".theme-toggle");
  const isDark = () => (root.dataset.theme ? root.dataset.theme === "dark" : system.matches);
  const sync = () => {
    const dark = isDark();
    root.dataset.resolvedTheme = dark ? "dark" : "light";
    if (button) {
      button.setAttribute("aria-pressed", String(dark));
      button.setAttribute("aria-label", dark ? "Light appearance" : "Dark appearance");
    }
  };
  if (button) {
    button.hidden = false;
    button.addEventListener("click", () => {
      const next = isDark() ? "light" : "dark";
      root.dataset.theme = next;
      try {
        localStorage.setItem("appearance", next);
      } catch (_) {
        /* Storage is optional. */
      }
      sync();
    });
  }
  system.addEventListener("change", sync);
  sync();

  /* Copy buttons for BibTeX --------------------------------------------- */
  if (navigator.clipboard) {
    document.querySelectorAll(".bibtex").forEach((box) => {
      const code = box.querySelector("code");
      if (!code) return;
      const copy = document.createElement("button");
      copy.type = "button";
      copy.className = "copy-button";
      copy.textContent = "Copy";
      copy.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(code.textContent);
          copy.textContent = "Copied";
        } catch (_) {
          copy.textContent = "Press ⌘C";
        }
        setTimeout(() => (copy.textContent = "Copy"), 1600);
      });
      box.appendChild(copy);
    });
  }

  /* Table of contents on research pages --------------------------------- */
  const toc = document.querySelector(".toc[data-toc]");
  const prose = document.querySelector(".prose");
  if (toc && prose) {
    const headings = [...prose.querySelectorAll("h2[id]")];
    if (headings.length >= 2) {
      const inner = document.createElement("div");
      inner.className = "toc-inner";
      const label = document.createElement("p");
      label.className = "eyebrow";
      label.id = "toc-label";
      label.textContent = "On this page";
      const list = document.createElement("ol");
      const links = headings.map((h) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = `#${h.id}`;
        a.textContent = h.textContent;
        li.appendChild(a);
        list.appendChild(li);
        return a;
      });
      inner.append(label, list);
      toc.appendChild(inner);
      toc.setAttribute("aria-labelledby", "toc-label");
      toc.closest(".topic-body")?.classList.add("has-toc");
      if ("IntersectionObserver" in window) {
        const current = new Map();
        const io = new IntersectionObserver(
          (entries) => {
            entries.forEach((e) => current.set(e.target.id, e.isIntersecting));
            const active = headings.find((h) => current.get(h.id));
            if (!active) return;
            links.forEach((a) =>
              a.getAttribute("href") === `#${active.id}` ? a.setAttribute("aria-current", "true") : a.removeAttribute("aria-current")
            );
          },
          { rootMargin: "0px 0px -70% 0px" }
        );
        headings.forEach((h) => io.observe(h));
      }
    }
  }
})();
