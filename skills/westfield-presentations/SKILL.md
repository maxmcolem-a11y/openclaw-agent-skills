---
name: westfield-presentations
description: Build, revise, publish, or template Westfield Outdoors HTML presentation decks in `artifacts/westfield-presentations`, especially when Max asks for frontend slide work, live GitHub Pages deck updates, slide copy/layout tweaks, image or lightbox behavior, bilingual EN/ZH deck support, logo placement, closing disclaimers, or reusable Westfield presentation standards.
---

# Westfield Presentations

Use this skill for Westfield deck work that lives in the GitHub Pages presentations repo.

## Core workflow

1. Read `references/standards.md` before changing a deck.
2. If starting a new deck, read `references/kickoff.md` and collect missing inputs.
3. If creating a new deck from the current strongest template, run `scripts/bootstrap_deck.py <new-slug>`.
4. Edit the target deck directly in `artifacts/westfield-presentations/<deck-slug>/`.
5. Publish only the intended files, push, and return the live URL.

## Defaults

- Keep the same live URL when the user is iterating on an existing deck.
- Prefer calm, direct, credible design-review language.
- Treat `index.html` as the main surface unless the task clearly requires new assets or scripts.
- Verify interaction-heavy changes with static checks when browser preview is inconvenient.
- If review may be affected by cache, offer a cache-busted URL.

## Starting a new deck

- Use `references/kickoff.md` to gather the brief.
- Use the current canonical template deck until a more neutral Westfield base deck exists.
- Replace project-specific copy, logos, and assets early so stale content does not leak into review.
- Confirm whether the deck needs bilingual support, spec-sheet modals, STEP/model viewers, or a confidentiality closing slide.

## Revising an existing deck

- Read the live deck file before editing.
- Match existing slide patterns unless the user asks to refactor them.
- Keep three-image slides visually consistent across the whole deck.
- Keep zoom/lightbox behavior centered and predictable.
- When adding logos or brand marks, use transparent assets when possible.

## Publishing

- Run a narrow diff before commit.
- Stage only the intended deck files and assets.
- Commit with a descriptive message.
- Push to `origin main` in `artifacts/westfield-presentations`.
- Reply with the live URL and a short note on what changed.
