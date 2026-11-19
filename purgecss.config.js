module.exports = {
  content: ["_site/**/*.html", "_site/**/*.js"],
  css: ["_site/assets/css/*.css"],
  output: "_site/assets/css/",
  skippedContentGlobs: ["_site/assets/**/*.html"],
  // These classes and attributes are added at runtime (research.js, MathJax) and are absent from the initial HTML.
  safelist: {
    greedy: [/data-theme/, /resolved-theme/, /\[open\]/, /aria-current/, /copy-button/, /toc/, /has-toc/, /mjx/],
  },
};
