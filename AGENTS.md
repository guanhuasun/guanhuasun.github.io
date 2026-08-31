# Repository Guide for Coding Agents

## Project overview

This repository is Guanhua Sun's personal academic website at
`guanhuasun.github.io`. It is a Jekyll site derived from Academic Pages and the
Minimal Mistakes theme. GitHub Pages builds the `master` branch directly; there
is no repository-owned deployment workflow.

Most routine work is content editing in Markdown or YAML. Theme, layout, and
JavaScript changes are less common and should preserve the site's compact
academic design.

## Working safely

- Preserve unrelated tracked and untracked files. The repository may contain
  local CV sources, media, build artifacts, and editor settings that are not
  committed.
- Do not edit `CHANGELOG.md`; it records upstream theme history.
- Do not hand-edit `assets/js/main.min.js`. Edit the source files and regenerate
  the bundle with `npm run build:js`.
- Do not delete sample or legacy pages merely because they are not linked from
  the main navigation. Report them and ask before removing them.
- Use root-relative links for assets served by this site and HTTPS links for
  external resources.

## Local development and validation

Install Ruby dependencies when needed:

```bash
bundle install
```

Serve locally with the development override:

```bash
bundle exec jekyll serve --config _config.yml,_config.dev.yml
```

Validate content, Liquid, and Sass changes with:

```bash
bundle exec jekyll build --config _config.yml,_config.dev.yml
```

Use a Ruby version compatible with the GitHub Pages bundle. The vendored Ruby
Sass 3.7 importer does not resolve absolute Windows paths under Ruby 3.4; that
runtime combination fails before the site's Sass is evaluated.

Jekyll does not reload `_config.yml` automatically while serving. Restart the
server after changing either configuration file. There is no automated test or
lint suite.

## Site architecture

### Configuration and data

- `_config.yml` contains site metadata, author information, collections,
  defaults, Sass settings, plugins, and production behavior.
- `_config.dev.yml` overrides the local URL, disables analytics, and emits
  expanded CSS for development.
- `_data/navigation.yml` is the source of the main menu after the hard-coded
  Home link.
- `_data/cv.yml` is the structured source for the native CV page.
- `_data/publication_themes.yml` contains publication-theme metadata.

The current main navigation is: Home, Publications, Projects, Teaching,
CV/Statements, and Veritas China. Google Scholar is linked from the home header
and Publications page rather than replacing the local Publications page.

### Content

- `_pages/about.md` is the homepage. It includes `_includes/home-header.html`
  and contains About, Research, Education, and Other Interests sections.
- `_pages/publications.md` renders featured publication cards and a complete
  year-grouped publication list from `_publications/`.
- `_pages/projects.md` is a hand-written project list; it does not use the
  `_portfolio/` collection.
- `_pages/teaching.html` splits `_teaching/` records into college and outreach
  tables using the `level` field.
- `_pages/cv.md` combines `_data/cv.yml`, `_publications/`, and `_teaching/`, and
  links to `files/CV.pdf`.
- `_talks/`, `_portfolio/`, `_posts/`, and several non-menu pages retain legacy
  Academic Pages examples. They may still be built at direct URLs.

The configured output collections are `teaching`, `publications`, `portfolio`,
and `talks`. Collection defaults in `_config.yml` provide layouts and shared
front matter.

### Rendering pipeline

The normal layout chain is:

```text
content -> single/archive -> default -> compress
```

- `_layouts/default.html` builds the document shell, masthead, optional Calder
  video, footer, and scripts.
- `_layouts/single.html` renders individual pages and collection entries.
- `_layouts/archive.html` renders list-style top-level pages.
- `_layouts/compress.html` minifies production HTML.
- `_includes/` contains reusable navigation, metadata, author, publication,
  footer, analytics, and script fragments. Prefer changing an include over
  duplicating shared markup in layouts.

### Styling and scripts

- `assets/css/main.scss` is the Sass entry point compiled by Jekyll.
- `_sass/skins/_modern-plex.scss` is the active skin and defines IBM Plex fonts
  and IBM Carbon-inspired color tokens.
- `_sass/_layout-narrow.scss` applies the active 960px centered, sidebar-free
  layout and the compact home header.
- `_sass/_publications.scss` controls featured cards and dense publication
  lists.
- `_sass/_video-background.scss` controls the fixed Calder mobile video.
- `assets/js/_main.js` and `assets/js/plugins/` are bundled into
  `assets/js/main.min.js` by `npm run build:js`.

## Design constraints

- Maintain a concise academic reference-document feel.
- Keep the single centered column and hidden theme sidebar.
- Use IBM Plex Serif for body copy, IBM Plex Sans for interface/headings, and
  IBM Plex Mono for metadata where defined.
- Use the existing Carbon palette: white, near-black, gray, and blue.
- Avoid new gradients, shadows, hover lifts, decorative hero sections, and
  unrelated accent colors.
- Keep corners square. The circular homepage portrait is the intentional
  exception.
- Use spacing based on the existing 4px scale and 1px gray separators.
- Preserve the bottom-right Calder animation on the homepage. Its negative
  stacking order depends on the background being painted on `html` and
  `.layout-narrow` creating an isolated stacking context.

## Content conventions

- Publication items live in `_publications/`. Use `puburl` for the publisher or
  canonical landing page and `paperurl` only for a direct paper/PDF URL. Optional
  `arxiv` and `doi` fields produce their own link chips. Set `featured: true` to
  include an item in the featured grid.
- Teaching records require `title`, `type`, `venue`, `date`, and `semester`.
  Add `level: high-school` for outreach entries. The Teaching tables link each
  title to its collection page, so a full syllabus can live directly in the
  corresponding `_teaching/` item.
- Update `_data/cv.yml` for structured CV sections instead of hard-coding those
  entries into `_pages/cv.md`.
- Put downloadable documents in `files/` and images/video in `images/`.
- The optional generators in `markdown_generator/` are for bulk imports. Direct
  Markdown edits are preferred for small changes.

## Final checks

Before handing off a change:

1. Review `git diff` and confirm unrelated files were not modified.
2. Run a Jekyll build for changes to content, configuration, Liquid, layouts,
   includes, or Sass.
3. Regenerate and inspect the JavaScript bundle if its sources changed.
4. For visual changes, inspect the homepage plus Publications, Teaching, CV,
   and a narrow mobile viewport.
5. Report any legacy sample content or configuration warnings separately rather
   than silently deleting or suppressing them.
