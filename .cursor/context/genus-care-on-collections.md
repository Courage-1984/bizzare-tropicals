# Genus care on collection pages — advice

## Current state

| Piece | Status |
|-------|--------|
| `templates/collection.json` | `main-collection-banner` → `nepenthes-collection-hub` (parent only) → `growing-supplies-filter-chips` (supplies only) → product grid |
| `sections/collection-hero.liquid` | **Not on catalog** — care lives on PDP via `snippets/product-care-dossier.liquid` |
| Client brief §4.1 | Wants overview, trap mechanism, care table, species list, FAQ **on each genus collection** |

## Option A — Quick win: wire `collection-hero` (recommended first)

Add `collection-hero` **below** the anatomy banner (or **replace** banner on non-pitcher genera — merchant choice).

**Pros:** Already styled; parses `<ul><li><strong>Light:</strong> …` in collection description; fallback care rows if description empty.  
**Cons:** Does not include trap explainer, species reference list, or FAQ schema; single “dossier” block only.

**Merchant workflow:** Paste structured HTML into **Collection → Description** in Admin:

```html
<p>Intro paragraph about the genus…</p>
<ul>
  <li><strong>Light:</strong> Bright direct sun, 6+ hours.</li>
  <li><strong>Water:</strong> Tray method, distilled or RO only.</li>
  <li><strong>Substrate:</strong> 50/50 peat and perlite.</li>
  <li><strong>Humidity:</strong> 40–60%.</li>
  <li><strong>Dormancy:</strong> Cool winter rest for temperate species.</li>
  <li><strong>Feeding:</strong> Do not fertilize; insects only.</li>
</ul>
```

**Catalog:** Collection descriptions can still hold genus intro copy (shown in anatomy banner area if configured). Per-specimen care belongs on the **product page** (`product-care-dossier`).

**PDP care priority:** `custom.care_guide` metafield → product description → metafield grid (light, water, substrate, humidity, temp, dormancy) → theme fallback → default rows.

## Option B — Full brief (medium build)

New sections + collection metafields from brief:

| Section | Metafield / source |
|---------|-------------------|
| Genus overview | `custom.genus_overview` (rich text) |
| Trap mechanism | `custom.trap_mechanism` |
| Care snapshot table | `custom.care_light`, `care_water`, etc. |
| Species list | `custom.species_list` |
| FAQ | `custom.faqs` (metaobject list) + FAQPage JSON-LD |

**Pros:** Matches brief; editor-friendly per collection.  
**Cons:** More dev + Admin metafield setup + content entry for every genus.

## Option C — Hybrid

- Wire **collection-hero** now (Option A).  
- Add **FAQ** section + metaobjects later.  
- Keep anatomy banner for pitcher genera only (conditional in Liquid on `collection.handle`).

## Nepenthes parent collection

Brief wants `/collections/nepenthes` to show **3 cards** → highland / intermediate / lowland.

- Create manual collection `nepenthes` with short description + optional `page`-style content.  
- **Dev:** Small section `nepenthes-hub.liquid` shown when `collection.handle == 'nepenthes'` (3 linked cards).  
- Sub-collections remain the shop targets in nav (`catalog-genus-handles.liquid` already uses sub-handles, not parent).

## Recommendation

1. **Launch:** Option A + collection descriptions with 6 care bullets.  
2. **Phase 2:** FAQ section + Nepenthes hub cards.  
3. **Phase 3:** Full metafield-driven blocks if client wants Theme Editor fields instead of HTML in descriptions.
