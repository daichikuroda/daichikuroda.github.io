# Daichi Kuroda — homepage

This redesign keeps the existing Jekyll project and GitHub Pages deployment workflow. The public routes are `/`, `/publications/`, and `/404.html`. Template examples remain in source but are excluded from the build.

## Editing

- `_pages/about.md`: introduction and contact details.
- `_data/research.json`: publication list, newest first. Both pages use this list; the homepage shows the first four entries. `bibtex` contains the expandable citation. Label unpublished work with `preprint: true`.
- `_bibliography/papers.bib`: matching bibliography for the retained al-folio tooling. Keep it aligned if that tooling is used again.
- `_layouts/research.liquid`: shared navigation, document metadata, and footer.
- `_includes/research-papers.liquid`: paper entries shared by both pages.
- `assets/css/research.css`: layout, responsive rules, light/dark colors, and print styling.
- `assets/js/research.js`: optional local appearance preference. Reading the site and citations works without JavaScript.

No portrait, degree history, CV, awards, or private project material has been added.

## Build and deployment

Use Ruby 3.3 and the existing Gemfile/lockfile. Run `bundle install`, then `JEKYLL_ENV=production bundle exec jekyll build`. Output is written to `_site`. The existing GitHub workflow also runs PurgeCSS and deploys `_site` to the `gh-pages` branch after a push to the default branch. Review a feature branch before merging. GitHub Pages must be configured to serve the `gh-pages` branch from its root.

The stylesheet has dynamic theme attributes; preserve these in the PurgeCSS safelist.

## Content sources, checked September 14, 2026

- Profile, affiliation, email: https://people.epfl.ch/daichi.kuroda?lang=en
- Advisor/co-advisor: https://memento.epfl.ch/event/hierarchical-community-detection/
- New preprint, also supplied by Daichi: https://arxiv.org/abs/2609.11173
- JASA: https://doi.org/10.1080/01621459.2025.2569711 (final journal publication: 2026; earlier manuscript: 2025)
- Hierarchical linkage preprint: https://arxiv.org/abs/2511.18056
- ACM SIGMETRICS PER: https://doi.org/10.1145/3725536.3725541
- Frontiers in Physics: https://doi.org/10.3389/fphy.2023.1166219
- Scientific Reports: https://doi.org/10.1038/s41598-022-15343-y
- ORCID linked by the JASA publisher: https://orcid.org/0009-0004-3467-5177

## Validation

Production Jekyll build; both routes; four recent/six total paper entries; expandable BibTeX; dark/light appearance and persistence; 320–1440px widths; enlarged text; local assets; and browser error checks. See the task's preview screenshots for the reviewed appearance.
