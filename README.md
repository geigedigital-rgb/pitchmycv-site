# Pitch My CV — Landing

Conversion-focused landing page for an AI resume optimization product (Rezi/Enhancv style).

## Principles

- **One thought, one pain, one action** — single CTA: "Optimize my resume"
- **Funnel:** Pain → Why (ATS) → Solution → Trust
- **Design:** Minimal, util-tool feel — system fonts, lots of whitespace, one accent (dark CTA), no illustrations/gradients

## Structure

- `index.html` — Main landing page (`/`)
- `examples/`, `tools/`, `about/`, `blog/`, etc. — Clean routes via `index.html` files in folders
- `css/style.css` — Styling and design system
- `css/examples-resume-assets.css` — Styles for resume preview/download block on role example pages
- `js/main.js` — Interactions (Drag & Drop)
- `assets/` — Image assets
- `scripts/generate_resume_examples.py` — Offline generator for per-role PDF/PNG resume examples

## Run locally

Open the project in a browser via a static server:

```bash
npx serve .
# or
python3 -m http.server 8000
```

## Generate role resume samples (offline)

Run once locally or in CI to refresh static resume example files:

```bash
python3 -m pip install --upgrade reportlab pillow
python3 scripts/generate_resume_examples.py
```

Generated files:

- `assets/examples/<role>/sample.pdf`
- `assets/examples/<role>/preview.png`

## SEO

- Semantic HTML5 (`header`, `main`, `section`, `h1`/`h2`)
- Unique `title` and `meta description`
- Canonical URL, Open Graph, Twitter Card
- JSON-LD `SoftwareApplication` schema

## Next steps

- Replace `#cta` links with real flow (e.g. upload CV / start optimization)
- Add analytics on CTA click
- Optionally add a second page (e.g. pricing) after the conversion step
