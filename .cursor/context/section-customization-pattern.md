# Section customization pattern

Use this checklist whenever we add or refactor a storefront section so the client can edit copy and imagery in the **Shopify theme editor** (left settings panel) without breaking layout or logic. Pair with [admin-checklist.md](./admin-checklist.md) for store-wide setup.

---

## Goals

- **Fallbacks always work** — Empty catalog, missing uploads, or first-time theme preview still show sensible images and text.
- **Merchant control** — Non-developers change headings, body copy, images, links, and collections from the editor.
- **Layout stability** — Custom content (long titles, missing images, zero products) must not break grids, carousels, or navigation.

---

## The five steps (per section)

### 1. Audit

Before changing code, document:

| Question | Notes |
|----------|--------|
| What is hardcoded in Liquid vs driven by `section.settings` / `block.settings`? | |
| What fallbacks exist today? | Placeholders, mock copy, `request.design_mode`, collection/product images |
| What breaks if the client clears a field? | |
| Which snippets does this section `render`? | Shared fallback snippets? |

**Output:** Short list of gaps (e.g. “title has no default”, “image only works if collection has products”).

---

### 2. Schema (theme editor)

Expose merchant-facing controls in `{% schema %}`:

- **Settings** — Section-wide: heading, colors, toggles, default collection, etc.
- **Blocks** — Repeatable items (slides, cards, pillars) when the section is modular.
- **Defaults** — Every important field gets a `default` so new installs and presets look complete.
- **Labels & info** — Clear `label`; use `info` for “Uses collection image when empty” style hints.
- **Types** — Prefer `image_picker`, `text`, `textarea`, `richtext`, `collection`, `product`, `url`, `color`, `range` over free-form HTML in Liquid.

**Locale:** User-facing strings in `locales/en.default.json`; editor strings in `locales/en.default.schema.json` (keys under `t:` in schema).

**Do not** duplicate JSON keys in locale files (e.g. two `"collections"` roots — last one wins and breaks translations).

---

### 3. Fallback chain (images & copy)

Define and implement **one explicit order** in Liquid. Example for a card image:

1. Block/section **uploaded image** (`image_picker`)
2. **Placeholder URL** setting (development / until client uploads)
3. **Collection image** → first **product** featured image
4. Shared snippet default (e.g. `genus-placeholder-url`, `discovery-card-placeholder-url`)
5. CSS **empty state** (gradient block) — never a broken `<img>`

For **text**:

1. Block/section setting
2. Related object (e.g. `collection.title` via `collection-display-title` when we override admin titles)
3. Translation key `{{ 'sections.*' | t }}`
4. Hardcoded default only as last resort in Liquid (`| default: '…'`)

**Rule:** If a setting overrides display text (e.g. formatted genus names), do not let stale block labels from the editor override unless the merchant explicitly set them.

---

### 4. Layout safety

- **Required to render:** Only output a card/link/grid cell when minimum data exists (e.g. `title` + `link`). Skip silently in loop, do not render empty anchors.
- **Images:** Fixed aspect via `object-fit: cover`, min-heights on cards, placeholder class when no `src`.
- **Long copy:** `truncate` or `line-clamp` only where design requires; otherwise allow wrap without overflow breaking flex/grid.
- **Carousels / grids:** Empty block list → show section empty message (`empty` translation), not a collapsed section.
- **Design mode:** Optional mock data when `request.design_mode` and catalog is empty — clearly separated from live storefront logic.
- **No Liquid logic in `{% stylesheet %}` / `{% javascript %}`** — settings cannot be read there; pass via `data-*` attributes if needed.

---

### 5. Client notes (admin checklist)

After the section is done, update [admin-checklist.md](./admin-checklist.md) (or a subsection) with:

- Where to find the section in **Customize** (homepage / header group / etc.)
- Which settings the client should touch first
- Fallback behavior in plain language (“If you leave image empty, we use the collection’s first product photo”)
- Links/handles they must create in Admin (collections, pages like `about-us`)
- Launch reminder: replace Wikimedia placeholder URLs with **Settings → Files** or native uploads

---

## Code conventions (this theme)

| Pattern | Use |
|---------|-----|
| CSS variables for single properties | `style="--gap: {{ section.settings.gap }}px"` |
| CSS classes for multi-property layout | `class="section {{ section.settings.layout }}"` |
| Display titles | `{% render 'collection-display-title', collection: c %}` |
| Genus nav order | `{% render 'catalog-genus-handles' %}` |
| Placeholder URLs | Document in [placeholder-images.md](./placeholder-images.md); verify URLs (404s break cards) |
| User-facing copy | `{{ 'key' | t }}` only — no raw English in templates |
| Section attributes | `{{ section.shopify_attributes }}` / `{{ block.shopify_attributes }}` on editable wrappers |

---

## Definition of done (per section)

- [ ] Audit notes captured (in PR, chat, or a line in admin-checklist)
- [ ] Schema defaults match current storefront appearance
- [ ] Fallback chain documented in a `{% doc %}` header or this file’s section list
- [ ] Tested: all fields blank, placeholder only, live collection, client upload
- [ ] Theme editor preview does not show “Translation missing”
- [ ] admin-checklist updated for merchants

---

## Section queue

Track progress as we go through the site (check when complete):

| Section | File(s) | Done |
|---------|---------|------|
| Announcement bar | `sections/announcement-bar.liquid` | ✓ |
| Header / mega menu | `sections/header.liquid`, `snippets/header-catalog-mega-menu.liquid` | ✓ |
| Search overlay | `sections/search-overlay.liquid` | ✓ |
| Home slider | `sections/home-slider.liquid` | ✓ |
| Shop by genus | `sections/genus-shortcuts.liquid` | ✓ |
| Botanical discovery strip | `sections/botanical-discovery-strip.liquid` | ✓ |
| Newly cataloged | `sections/new-specimens.liquid` | ✓ |
| Featured specimen | `sections/featured-specimen.liquid` | ✓ |
| Conservatory standards | `sections/conservatory-standards.liquid` | ✓ |
| Featured collection | `sections/featured-collection.liquid` | ✓ |
| Collection banner | `sections/main-collection-banner.liquid` | ✓ |
| Collection grid | `sections/main-collection-product-grid.liquid` | ✓ |
| Product PDP | `sections/main-product.liquid` | ✓ |
| Footer | `sections/footer.liquid` | ✓ |
| About / Contact / Policy pages | `sections/about-template.liquid`, etc. | ✓ |
| Newsletter popup | `sections/newsletter-modal.liquid` | ✓ — Customer email signup (not blog); see [admin-checklist.md](./admin-checklist.md#newsletter-signups-not-blog-posts) |
| Cart drawer | `sections/cart-drawer.liquid` | ✓ |

---

*When starting work on a section, say which row in the queue — apply steps 1–5 in order.*
