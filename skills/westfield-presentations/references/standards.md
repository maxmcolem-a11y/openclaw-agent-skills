# Westfield presentation standards

## Proven learnings from the Timber Ridge project

- Work directly on the live HTML deck and publish iterative revisions fast.
- Keep the live URL stable unless Max asks for a new deck slug.
- Favor a calm, direct, client-facing design-review voice. Avoid prompt-y labels and avoid "humanized" fluff.
- On interaction-heavy decks, make slideshow dots clickable, support keyboard navigation where it helps, and match lightbox behavior across related slides.
- Center zoomed images. Do not let single-image lightboxes drift left or right.
- Keep repeated slide archetypes visually consistent, especially three-image progression pages.
- Treat bilingual support as prebaked content, not runtime translation. Store both language dictionaries in-page and localize image assets offline when the images themselves contain text.
- Store language preference locally so the deck reopens in the last-used language.
- Publish only intended files. Avoid dragging screenshots, scratch files, or unrelated repo noise into the commit.
- When GitHub Pages caching gets in the way, share a cache-busted review URL.

## Current canonical template deck

Until a neutral base template is extracted, the strongest starting point is:

- `artifacts/westfield-presentations/timber-ridge-daypack-development-clean/`

This deck already includes:

- a minimal cover slide
- a STEP/model viewer pattern
- standardized three-image progression slides
- hero slideshow + lightbox + spec sheet modal patterns
- EN/ZH language toggle infrastructure
- a closing confidentiality slide
- top-right cover logo slot

Replace project-specific copy, logos, and assets early when cloning from it.

## Standard slide modules

### 1. Cover slide

Use a minimal title slide with:

- deck title
- mandate / position or equivalent summary
- optional top-right brand logo slot

### 2. Technical exploration slide

Use when showing many candidate forms or models.

Patterns:

- thumbnail chooser or viewer
- on-demand heavy asset loading
- preload lightweight previews first

### 3. Three-image progression slide

Use for concept evolution, print-to-sketch, or before/after storytelling.

Rules:

- keep image sizing consistent across all three-image slides in the deck
- keep titles below the images
- make the images zoomable
- keep whitespace intentional, not excessive

### 4. Final-result slideshow slide

Use for polished concept presentation.

Patterns:

- hero slideshow
- clickable dots
- zoomed slideshow navigation
- optional full spec sheet modal

### 5. Closing slide

Use for deck closure and handoff.

Include when appropriate:

- confidentiality notice
- ownership statement
- author
- last edited date
- brand logos

## Interaction standards

- Exclude non-essential thumbnails from fullscreen if fullscreen would be noisy.
- Group related slideshow images in the lightbox so next/previous works naturally.
- Keep zoomed images centered.
- Keep arrows and close buttons obvious but unobtrusive.
- If the deck has paged spec sheets, localize the page indicator too.

## Translation standards

If the deck is bilingual:

- use `data-i18n` bindings for text
- keep an in-page `translations` object
- translate UI chrome too, not just slide copy
- create localized image variants for text-heavy visual assets
- switch localized assets instantly on toggle

## Publishing checklist

- confirm the exact target deck folder
- edit only the relevant files
- run a narrow `git diff`
- stage only intended assets
- push to `origin main`
- return the live URL
- mention the specific change in one sentence

## Formalization plan

1. Extract a neutral Westfield base deck from the Timber Ridge template.
2. Move brand-specific values into a small config block: title, subtitle, logos, author, date, confidentiality text, language support.
3. Keep reusable slide archetypes intact: cover, exploration, progression, final-result, closing.
4. Preserve proven interaction patterns: centered lightbox, grouped slideshow navigation, spec modal, bilingual switching.
5. Add a bootstrap step so a new deck can be cloned quickly without copying repo clutter.
6. Reuse the same publish checklist for every Westfield deck.
