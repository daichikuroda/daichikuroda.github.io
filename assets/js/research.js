(() => {
  const root = document.documentElement;
  const button = document.querySelector(".theme-toggle");
  const system = window.matchMedia("(prefers-color-scheme: dark)");
  let choice = null;
  try {
    choice = localStorage.getItem("appearance");
  } catch (_) {
    /* Storage is optional. */
  }
  if (choice === "light" || choice === "dark") root.dataset.theme = choice;
  const isDark = () => (root.dataset.theme ? root.dataset.theme === "dark" : system.matches);
  const update = () => {
    button.setAttribute("aria-pressed", String(isDark()));
  };
  if (button) {
    button.hidden = false;
    update();
    button.addEventListener("click", () => {
      const next = isDark() ? "light" : "dark";
      root.dataset.theme = next;
      try {
        localStorage.setItem("appearance", next);
      } catch (_) {
        /* Storage is optional. */
      }
      update();
    });
    system.addEventListener("change", update);
  }
})();
