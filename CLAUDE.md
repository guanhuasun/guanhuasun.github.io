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
- The navigation order is Publications (external Google Scholar link) → Projects → CV/Statements → Veritas China. Keep external links external in `_data/navigation.yml` rather than creating stub pages.
- `_pages/projects.md` uses `layout: archive` and hand-rolls project entries as Markdown — it is not driven by the `_portfolio/` collection. Add new projects directly in that file.
- Site author metadata (name, email, avatar, Google Scholar link, GitHub handle) lives in `_config.yml` under `author:`. The sidebar author card (`_includes/author-profile.html`) reads from there.
- The site uses the `google-universal` analytics provider but no tracking ID is set — leave as-is unless the user supplies one.

## Things to avoid
- Don't edit `CHANGELOG.md` — it's upstream theme history, kept for patch-tracking against the academicpages template (see README).
- Don't commit `Gemfile.lock` fixes blindly; the README explicitly says to delete it when `bundle install` errors or when a security advisory fires.
- Don't hand-edit `assets/js/main.min.js` — regenerate via `npm run build:js` after editing the unminified sources listed in `package.json`'s `uglify` script.
