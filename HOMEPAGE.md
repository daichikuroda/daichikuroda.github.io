# Daichi Kuroda — homepage

Jekyll site published to https://daichikuroda.github.io by GitHub Actions (`.github/workflows/deploy.yml`).
Public routes: `/`, `/publications/`, `/news/`, `/404.html`, and research pages under `/research/` once published.
The al-folio template files remain in the repository but are excluded from the build.

## Where to edit what

| What                                      | File                                                                            |
| ----------------------------------------- | ------------------------------------------------------------------------------- |
| Name, position, links, portrait, advisors | `_data/profile.yml`                                                             |
| Bio (Markdown, first paragraph is larger) | `_pages/about.md`                                                               |
| Research cards on the homepage            | `_data/themes.yml`                                                              |
| News                                      | `_data/news.yml`                                                                |
| Talks and posters                         | `_data/talks.yml`                                                               |
| Teaching and supervision                  | `_data/teaching.yml`                                                            |
| Publications (newest first)               | `_data/research.json` (+ `_bibliography/papers.bib`)                            |
| Hierarchical clustering page              | `_pages/research/hierarchical-clustering.md`                                    |
| Styles / scripts                          | `assets/css/research.css`, `assets/js/research.js`                              |
| Templates                                 | `_layouts/research.liquid` (shell), `home.liquid`, `topic.liquid`; `_includes/` |

## Drafts and placeholders

- **List entries** (news, talks, teaching) marked `draft: true` are hidden on the live site and shown with a yellow
  "Draft" tag in local previews. Delete the `draft: true` line to publish an entry. The News and Talks & teaching
  sections (and their menu links) appear on the live site as soon as they have at least one published entry.
- **Writing prompts** are paragraphs followed by `{: .todo}`. They show as yellow boxes in previews and are hidden on
  the live site. Replace each with your text and delete the `{: .todo}` line.
- **Portrait**: add a square image as `assets/img/portrait.jpg` (or change `photo:` in `_data/profile.yml`).
  Without the file, the live site shows a small dendrogram illustration in its place.
- **Research page**: `_pages/research/hierarchical-clustering.md` has `published: false`, so it is not built on the
  live site, and its homepage card is not a link. Change it to `published: true` when the text is ready.
  Instructions for math, figures, and definition/theorem boxes are in a comment at the top of that file.
- **Another research page**: copy that file, change `title`, `permalink`, `topic`, and `icon`, add the `page:` URL to
  the matching entry in `_data/themes.yml`, and tag papers with the topic in `_data/research.json`.

## Publications

Each entry in `_data/research.json` can have: `title`, `authors`, `equal` (names to mark with \*, shown as
"\*Equal contribution"), `year`, `label` (badge text), `venue` (full venue line), `preprint: true`, `topics`
(theme ids from `_data/themes.yml`), `summary`, `url` (links to arXiv are labeled "arXiv"), `pdf`, `code`, `bibtex`.

## Local preview

With Ruby 3.3: `bundle install`, then

```
bundle exec jekyll serve --unpublished
```

and open http://127.0.0.1:4000. Previews show drafts and prompts; the production build
(`JEKYLL_ENV=production bundle exec jekyll build`, run by GitHub Actions) hides them.

## Build and deployment

A push to `main` builds the site, runs PurgeCSS (`purgecss.config.js`; keep runtime classes in its safelist), and
deploys `_site` to the `gh-pages` branch. GitHub Pages serves `gh-pages` from its root.

Fonts: Source Serif 4 (SIL Open Font License, `assets/type/OFL.txt`), self-hosted and subset to Latin.
Research pages with `math: true` load MathJax 3 from jsDelivr.
