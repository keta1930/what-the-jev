# Documentation site

Next.js 16 and Fumadocs serve the repository's English and Chinese documentation. The repository Markdown files remain the only editable content source.

## Run

Requires Node.js 22.13+ and npm. From `site/`:

```bash
npm ci
npm run dev
```

Open <http://localhost:20242> or <http://localhost:20242/zh>. Development listens on `0.0.0.0:20242` and watches the source documents and their images. `PORT` can override the port after confirming its allocation. Do not start a second server on an occupied port.

```bash
npm test
npm run check
npm run build
npm start
```

`build` synchronizes content before producing the production build. Next.js 16.2.10 uses `.next/dev` for development and `.next` for production; the production cleanup preserves the `dev` directory. A build can run alongside development. Stop the development server before using `start` on the same port. Production requires a rebuild after source changes. Set `SITE_URL` to the eventual public origin before building; its local default is `http://localhost:20242`. No deployment is configured.

## Content

| Source | English route |
| --- | --- |
| `README.md`, `README.zh.md` | `/about` |
| `example/INDEX*.md`, `example/*/README*.md` | `/examples`, `/examples/<name>` |
| `experiments/INDEX*.md`, `experiments/*/report/REPORT*.md` | `/experiments`, `/experiments/<name>` |
| `resource/README*.md`, `resource/<category>/*.md` | `/resources`, `/resources/<category>/<name>` |

Chinese routes use `/zh`; English routes have no language prefix. Resource category pages derive from the resource index. Add articles and their index entries using the repository's existing conventions. The `docs/jev` agent knowledge base is excluded from pages, navigation, search, and RSS; `/docs` and `/zh/docs` return 404. Public articles retain links to that knowledge base as GitHub source links. Reserved `AGENTS.md`, `CLAUDE.md`, `TODO.md`, experiment preparation material, and raw data are excluded. The game directory currently contains planning material only and does not appear as a completed game.

`npm run sync` scans these sources, extracts metadata and index summaries, validates relative links and fragments, renders Markdown, and copies referenced images. Generated files live in `.generated/`, `public/repo-assets/`, and `public/search/`; do not edit them. Missing files, duplicate routes, and unindexed examples, experiments or resources fail synchronization with the source path.

Markdown keeps GFM tables, highlighted code, Unicode math, and literal angle-bracket placeholders. It does not execute HTML or MDX, or interpret dollar amounts as math. Local images preserve their original paths. Data, scripts, configurations and license links point to the repository at the build commit.

## Reading and shortcuts

The homepage contains a centered introduction and navigation. Directories use grouped article lists with thin dividers. Search loads only the current language's index on demand and matches words or Chinese phrases across titles and document text.

Cormorant Garamond, Inter, and JetBrains Mono are self-hosted as Latin variable WOFF2 files in `public/fonts/`, with their OFL licenses. They were sourced from the respective `@fontsource-variable` 5.3.0 packages. CSS loads them locally; neither builds nor page views require a font CDN. Chinese characters use local system font fallbacks. Keep the font files and licenses with the site.

| Shortcut | Action |
| --- | --- |
| Cmd/Ctrl+K | Search |
| D | Toggle light/dark mode |
| L | Open the corresponding translation |
| H | Current language's homepage |
| M | Copy the article's original Markdown |
| Escape | Close a dialog |

Use `?` in the header for help and to disable single-letter shortcuts. Inputs, composition events and open dialogs do not trigger those shortcuts. Buttons remain available. Themes follow the system initially and persist the user's choice.

## RSS

`/rss.xml` and `/zh/rss.xml` each include every published source document, including the project introduction and source indexes. A document's GUID includes its language, route identity and a hash of its source text, index summary/group, and referenced image bytes. Text or image changes produce a new GUID even if the author leaves the frontmatter date unchanged; rebuilding unchanged input does not create a new GUID.

Dates use UTC-normalized Git modification times for committed files, filesystem modification times for local edits, and declared frontmatter dates. Referenced image and source-index modification dates participate in the latest update date. Generation does not use the build clock or a persistent revision cache.

The feeds expose the latest revision of each current document, not a historical event archive. Several edits between reader polls may appear as one update; reverting to identical content reuses that content's GUID. Uncommitted previews use local modification times, so Git is required for reproducible dates across machines. Removing a document removes its feed item and search result after synchronization.
