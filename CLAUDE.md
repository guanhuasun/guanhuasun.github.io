# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Guanhua Sun's personal academic website (`guanhuasun.github.io`), built on the **academicpages** fork of the **Minimal Mistakes** Jekyll theme. It is deployed via GitHub Pages directly from the `master` branch — there is no build step on push; GitHub Pages runs Jekyll server-side.

Content is almost all Markdown under `_pages/` and the collection directories. Code edits are rare; most changes are content edits or theme/layout tweaks.

## Local development

```bash
bundle install                    # first-time setup; if it errors, delete Gemfile.lock and retry
bundle exec jekyll liveserve      # serve at http://localhost:4000 with live-reload
# or equivalently:
bundle exec jekyll serve --config _config.yml,_config.dev.yml
```

Use a Ruby version compatible with the GitHub Pages bundle. Its vendored Ruby Sass 3.7 importer does not resolve absolute Windows paths under Ruby 3.4, so that local runtime combination fails before the site's Sass is evaluated.

`_config.dev.yml` overrides `url` to `http://localhost:4000` and disables analytics for local runs. Note: Jekyll does **not** auto-reload `_config.yml` changes — restart the server after editing it.

There are no tests and no lint. `package.json` exists only to uglify the theme's JS bundle (`npm run build:js` → `assets/js/main.min.js`); you generally don't need it unless editing files under `assets/js/_main.js` or `assets/js/plugins/`.

## Architecture

### Jekyll collections drive the site structure
`_config.yml` defines four collections — `teaching`, `publications`, `portfolio`, `talks` — each rendered from its own `_<collection>/` directory with permalink `/:collection/:path/`. The `defaults:` block in `_config.yml` assigns a layout and front-matter defaults per collection, so individual content files rarely need to specify `layout:`.

Top-level navigable pages live in `_pages/` (included via the `include:` list in `_config.yml`, since `_pages` is not a standard Jekyll directory). The nav bar itself is driven by `_data/navigation.yml` — add/remove menu entries there, not in layouts.

### Layout / include hierarchy
- `_layouts/` — page templates (`single.html`, `archive.html`, `talk.html`, `splash.html`, etc.). `compress.html` is the HTML-minifying wrapper referenced by `compress_html` in `_config.yml`.
- `_includes/` — reusable partials (author profile, masthead, SEO, analytics, comments, social share). Layouts compose these; prefer editing includes over layouts when changing shared UI.
- `_sass/` + `assets/css/main.scss` — Sass is compiled by Jekyll (`sass_dir: _sass`, `style: compressed`). Touch `_sass/` for styling changes, not the generated CSS.

### Content generators (optional tooling)
`markdown_generator/` contains Jupyter notebooks and plain-Python equivalents (`publications.py`, `talks.py`, `pubsFromBib.py`) that convert `publications.tsv` / `talks.tsv` / a BibTeX file into per-item Markdown under `_publications/` and `_talks/`. Use these only if bulk-generating from a spreadsheet; hand-written Markdown in the collection directories works fine too.

`talkmap.py` / `talkmap.ipynb` geocode talk locations into an interactive map rendered at `_pages/talkmap.html`. Disabled by default via `talkmap_link: false` in `_config.yml`.

## Editing conventions specific to this site
- The navigation order is Publications → Projects → Teaching → CV/Statements → Veritas China. Publications is a local page; Google Scholar is linked from the home header and Publications page. Keep genuinely external links external in `_data/navigation.yml` rather than creating stub pages.
- `_pages/projects.md` uses `layout: archive` and hand-rolls project entries as Markdown — it is not driven by the `_portfolio/` collection. Add new projects directly in that file.
- Site author metadata (name, email, avatar, Google Scholar link, GitHub handle) lives in `_config.yml` under `author:`. The sidebar author card (`_includes/author-profile.html`) reads from there.
- Analytics is disabled because no tracking ID is configured. Only enable a supported analytics provider when the user supplies the required identifier.

## Design system

The site was redesigned around an **IBM Carbon × academic** look — concise, elegant, modern. Any styling change should stay within these constraints unless the user explicitly asks for a new direction.

### Principles
- **Concise over decorative.** The site is a reference document, not a marketing page. No hero sections, no pull-quotes, no gradients, no drop shadows, no hover-lift animations.
- **Single narrow column.** All content sits in a 960px centered column (`$narrow-width` in `_sass/_layout-narrow.scss`). The Susy grid and the sidebar author card are both disabled under `body.layout-narrow` — do not reintroduce them.
- **Sharp corners everywhere.** `border-radius: 0` is a Carbon hallmark. Buttons, cards, images-in-content, form fields — all square. The only rounded element is the circular profile photo on the home page (`border-radius: 50%`, intentional).
- **Typography does the work.** Hierarchy comes from font, weight, and size — not from color blocks or boxes. Cards and list rows are separated by 1px rules in `$border-color`, nothing heavier.
- **Colors the user likes:** off-white, blue, black, grey. **Colors to avoid:** green, yellow, brown. Don't introduce accent colors outside the Carbon palette.

### Tokens (defined in `_sass/skins/_modern-plex.scss`)
- Background: `#ffffff` (pure white). The off-whites `#fafaf8`, `#f4f4f4`, `#faf7f2`, `#f2f0ef` were evaluated and rejected — do not propose them again without being asked.
- Text: `#161616` (IBM Gray 100) body; `#525252` (Gray 70) metadata; `#a8a8a8` (Gray 50) captions.
- Links: `#0f62fe` (IBM Blue 60) default, `#0043ce` (Blue 70) hover. Underline only on hover, `text-underline-offset: 2px`.
- Rules / borders: `#e0e0e0` (Gray 20). Code block background: `#f4f4f4` (Gray 10).
- Spacing scale: multiples of 4 (4/8/16/24/32/48/64 px). Don't introduce odd values.

### Typography
- Active skin: `modern-plex` (set in `_config.yml`). Body = IBM Plex Serif, UI/nav/headings = IBM Plex Sans, metadata = IBM Plex Mono. Loaded from Google Fonts in `_includes/head/custom.html`.
- An alternate `modern-helvetica` skin (Helvetica Neue + Charter) exists as a comparison point but is not the active default. Don't swap the active skin unless the user asks.
- Base size 16px, line-height 1.6. Headings are 600 weight with `letter-spacing: -0.01em`.

### Layout specifics
- Home page uses `_includes/home-header.html` (120px circular photo + name + inline Email / Github / Scholar links) followed by `## About`, `## Research`, `## Education`, and `## Other Interests` sections. Keep the presentation compact without imposing a one-viewport limit on the biographical content.
- Publications use a hybrid layout: a "Featured" card grid (`pub-grid`, `repeat(auto-fit, minmax(280px, 1fr))`) for items with `featured: true`, followed by a dense numbered list grouped by year (`pub-list`) with `pdf / arxiv / doi / link` chips inline after each title — not on a separate row.
- The Calder video (`images/calder-bg-loop.mp4` / `.webm`) renders fixed in the bottom-right via `.video-background { z-index: -1 }`. If you ever paint a body background, set it on `html` instead and give `.layout-narrow` `isolation: isolate` so the video stays visible.
- Footer is absolute-positioned at bottom right (`© 2026 Guanhua Sun`). Do not re-enable the theme's full-width footer panel.

## Things to avoid
- Don't edit `CHANGELOG.md` — it's upstream theme history, kept for patch-tracking against the academicpages template (see README).
- Don't commit `Gemfile.lock` fixes blindly; the README explicitly says to delete it when `bundle install` errors or when a security advisory fires.
- Don't hand-edit `assets/js/main.min.js` — regenerate via `npm run build:js` after editing the unminified sources listed in `package.json`'s `uglify` script.
