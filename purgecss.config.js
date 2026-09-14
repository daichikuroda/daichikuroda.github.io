module.exports = {
  content: ["_site/**/*.html", "_site/**/*.js"],
  css: ["_site/assets/css/*.css"],
  output: "_site/assets/css/",
  skippedContentGlobs: ["_site/assets/**/*.html"],
  // These attributes change at runtime and are absent from the initial HTML.
  safelist: { greedy: [/data-theme/, /\[open\]/] },
};
