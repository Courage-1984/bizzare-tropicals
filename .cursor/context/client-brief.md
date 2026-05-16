# client-brief.md

# Carnivorous Plants Shopify Store — Client Brief & Build Specification

> **Source:** Original client brief delivered in Afrikaans (WhatsApp). Translated, expanded, and structured for AI-agent-assisted development in Cursor IDE.
> **Stack target:** Shopify Online Store 2.0 (custom theme) · Liquid · Vanilla JavaScript · Vanilla CSS

---

## 1. Project Overview

A South African e-commerce store specializing in **carnivorous plants** and **growing supplies**. The catalogue is organized **by botanical genus**, with one collection page per genus and full species lists rendered on each collection page. Macro photography is a brand priority — product imagery must communicate the texture, mucilage, traps, and colour of each plant.

**Primary user:** Hobbyist and intermediate carnivorous-plant collectors in South Africa.
**Secondary user:** Beginner gardeners buying their first Venus flytrap / Sarracenia.

---

## 2. Technical Constraints (Hard Requirements)

| Constraint | Specification |
|---|---|
| Platform | Shopify Online Store 2.0 (JSON templates, sections-everywhere) |
| Templating | Liquid only |
| JavaScript | **Vanilla JS only.** No React, no Vue, no Alpine, no jQuery. ES modules preferred. |
| CSS | **Vanilla CSS only.** No Tailwind, no Bootstrap, no Sass preprocessors. CSS custom properties + native nesting permitted. |
| Currency | **ZAR (South African Rand)** — single-currency store. Format: `R 1 234,56` (space thousands separator, comma decimal). |
| Performance | Optimise aggressively for **Core Web Vitals** (LCP < 2.5s, INP < 200ms, CLS < 0.1). |
| DOM | Lightweight DOM manipulation. Avoid heavy client-side rendering. Prefer server-rendered Liquid with progressive enhancement. |
| Images | Use Shopify's responsive image filters (`image_url: width: …`) with `srcset` + `sizes`. Lazy-load below-the-fold. |
| Fonts | Self-hosted or `font-display: swap`. No more than 2 font families. |
| Bundling | Native ES modules where supported; minimal build step. No webpack/vite required unless strictly necessary. |
| Accessibility | WCAG 2.1 AA. Semantic HTML, visible focus states, keyboard-navigable mega-menu. |

---

## 3. Site Architecture

### 3.1 Core Pages

- `/` — **Home**
- `/pages/about` — **About**
- `/pages/contact` — **Contact**
- `/pages/shipping` — Shipping & live-plant care policy
- `/pages/care-overview` — High-level "How to grow carnivorous plants" landing page (links into the in-collection care sections)

### 3.2 Collection Structure (Catalogue Taxonomy)

The catalogue is built **strictly by genus**. Each top-level genus is a Shopify Collection. Nepenthes is the only genus split into sub-collections (by elevation/temperature group).


> **Note on `drossophyllum`:** The client brief spells it `Drossophyllum` (with double-s). The botanically correct spelling is *Drosophyllum*. Use `drossophyllum` as the handle to match the client's wording, but display **Drosophyllum** in user-facing text and metafields.

### 3.3 Nepenthes Sub-Collection Logic

Implement Nepenthes sub-collections as **Smart Collections** filtered by the `temperature_group` metafield:

- `nepenthes-highland` → products tagged `genus:nepenthes` AND `temperature_group:highland`
- `nepenthes-intermediate` → products tagged `genus:nepenthes` AND `temperature_group:intermediate`
- `nepenthes-lowland` → products tagged `genus:nepenthes` AND `temperature_group:lowland`

The parent `/collections/nepenthes` page must display all three groups visually (3-card hero) and link into each sub-collection.

---

## 4. Content Rules

### 4.1 Care Instructions — Integrated, Not Separate

**Care content must live ON the genus/collection page itself**, not on isolated "/care" pages.

Each collection page must include these sections in this order:

1. **Hero** — genus banner image + Latin + common name + 1-sentence description
2. **Product grid** — full species/cultivar listing for that genus
3. **Genus overview** — 2–3 paragraphs about origin, habit, what makes the genus distinctive
4. **Trap mechanism** — short explainer with macro image
5. **Care snapshot** — structured table: Light · Water · Soil · Temperature · Humidity · Dormancy
6. **Species/cultivar reference list** — full bullet/grid list (separate from the product grid; lists *all* species in the genus, including those not currently stocked)
7. **FAQ** — 4–6 common questions, structured for FAQPage schema

A single shared `section-genus-care.liquid` and `section-genus-faq.liquid` should accept schema settings so each collection page is fully editable in the Shopify theme editor.

### 4.2 Tone of Voice

- Botanically accurate (always use binomial Latin names, italicised)
- Approachable — written for hobbyists, not academics
- South African context where relevant (e.g. winter dormancy timing for Southern Hemisphere)

---

## 5. Data Structures (Product Metafields)

Define the following metafields under the `custom` namespace. All required on Plant products; supplies use only the supply-specific fields.

| Metafield key | Namespace | Type | Required for | Notes |
|---|---|---|---|---|
| `latin_name` | `custom` | single_line_text | Plants | e.g. *Dionaea muscipula* 'Akai Ryu'. Render italicised in templates. |
| `common_name` | `custom` | single_line_text | Plants | e.g. "Red Dragon Venus Flytrap" |
| `genus` | `custom` | single_line_text | Plants | Lowercase handle, e.g. `dionaea` |
| `difficulty` | `custom` | integer (1–5) | Plants | 1 = beginner, 5 = expert. Render as 5-pip icon scale. |
| `temperature_group` | `custom` | single_line_text (enum) | Plants | One of: `highland`, `intermediate`, `lowland`, `temperate`, `tropical`, `mediterranean` |
| `trap_type` | `custom` | single_line_text (enum) | Plants | One of: `snap`, `pitfall`, `flypaper`, `suction`, `lobster-pot` |
| `dormancy_required` | `custom` | boolean | Plants | Drives a warning banner on PDP for SA winter buyers |
| `temp_min_c` | `custom` | integer | Plants | Minimum safe temperature in °C |
| `temp_max_c` | `custom` | integer | Plants | Maximum safe temperature in °C |
| `cultivar` | `custom` | single_line_text | Plants (optional) | e.g. `Akai Ryu`, `B52`, `Judith Hindle` |
| `pot_size_cm` | `custom` | number_decimal | Plants | Current pot diameter |
| `growth_stage` | `custom` | single_line_text (enum) | Plants | One of: `seedling`, `juvenile`, `mature`, `flowering-size` |
| `cites_listed` | `custom` | boolean | Plants | Flags export-restricted species (e.g. *N. rajah*) |
| `supply_category` | `custom` | single_line_text (enum) | Supplies | One of: `soil`, `pot`, `water`, `lighting`, `climate`, `tool`, `seed`, `book-gift` |
| `volume_litres` | `custom` | number_decimal | Supplies | For soil/water products |
| `wattage` | `custom` | integer | Supplies | For grow lights |

### 5.1 Collection Metafields

| Key | Type | Purpose |
|---|---|---|
| `custom.genus_overview` | rich_text | Body copy for the genus overview section |
| `custom.trap_mechanism` | rich_text | Trap mechanism explainer |
| `custom.care_light` | single_line_text | "Bright direct sun, 6+ hrs" |
| `custom.care_water` | single_line_text | "Tray method, distilled / RO only" |
| `custom.care_soil` | single_line_text | "50/50 peat + perlite" |
| `custom.care_temp` | single_line_text | "21–32 °C summer, 0–10 °C winter" |
| `custom.care_humidity` | single_line_text | "40–60 %" |
| `custom.care_dormancy` | rich_text | Dormancy section, can be `null` |
| `custom.species_list` | rich_text | Full species/cultivar reference list |
| `custom.faqs` | list.metaobject | References to FAQ metaobjects |

### 5.2 Metaobjects

- **`faq`** — `question` (text), `answer` (rich_text)
- **`cultivar`** (optional) — `name`, `parentage`, `registered_year`, `description`

---

## 6. Filtering, Tags, and Search

### 6.1 Storefront Filters (on every collection page)

- Difficulty (1–5)
- Temperature group (Highland / Intermediate / Lowland / Temperate / Tropical / Mediterranean)
- Trap type
- Price range (in ZAR)
- In stock only
- Dormancy required (Yes / No)

Implement using Shopify's native Storefront Filters (Search & Discovery app) tied to the metafields above. No third-party JS filtering library.

### 6.2 Tag Conventions

Use kebab-case, namespaced tags:

- `genus:dionaea`, `genus:nepenthes`, etc.
- `temperature-group:highland`
- `trap-type:snap`
- `difficulty:1` through `difficulty:5`
- `dormancy:yes` / `dormancy:no`
- `cites:yes` for export-restricted species

---

## 7. Page-by-Page Build Notes

### 7.1 Home

- Hero with rotating macro photography (3 slides max, autoplay disabled by default for CLS / reduced-motion)
- 4-card genus shortcut row (Dionaea · Sarracenia · Nepenthes · Drosera)
- Featured products carousel (Shopify-native, no library)
- "New arrivals" + "Beginner-friendly" sections
- Care-tip / blog teaser
- Newsletter signup

### 7.2 Collection (Genus) Page Template

Single reusable template `templates/collection.json` with sections:

1. `collection-hero`
2. `collection-product-grid` (with filter sidebar)
3. `genus-overview` (pulls from collection metafield)
4. `genus-trap-mechanism`
5. `genus-care-snapshot` (table layout)
6. `genus-species-list`
7. `genus-faq`
8. `related-collections`

### 7.3 Product (PDP) Template

- Image gallery (zoomable; pinch-zoom on mobile via CSS `touch-action`)
- Title · Latin name (italic) · cultivar
- Price in ZAR
- Difficulty pips, trap-type icon, temperature-group badge
- "Dormancy required" warning banner (conditional on metafield)
- "CITES-listed" notice (conditional)
- Quick care card (light/water/soil/temp pulled from collection-level metafields, overridable per product)
- Variants: pot size, age/maturity
- Add-to-cart
- Description (rich text)
- Shipping & live-plant care accordion
- Cross-sell: "Pair with…" growing-supplies products

### 7.4 Growing Supplies Collection

Sub-tabs (rendered as in-page filter chips, not separate URLs):

- Soil & Media
- Pots & Containers
- Water & Watering
- Lighting
- Climate Control
- Tools & Accessories
- Seeds & Propagation
- Books & Gifts

---

## 8. Genus Reference Data

Pre-populate collection metafields with this data:

### Drosera (Sundews)
- Trap: flypaper · ~250 species worldwide
- Popular: *D. capensis*, *D. spatulata*, *D. binata*, *D. aliciae*, *D. regia*, *D. adelae*, *D. filiformis*, *D. burmannii*, *D. rotundifolia*

### Nepenthes
- Trap: pitfall · ~179 species · split by elevation
- **Highland:** *N. rajah*, *N. lowii*, *N. villosa*, *N. edwardsiana*, *N. veitchii*, *N. macrophylla*, *N. spathulata*
- **Intermediate:** *N. ventricosa*, *N. ventrata*, *N. miranda*, *N. sanguinea*, *N. maxima*, *N. fusca*
- **Lowland:** *N. ampullaria*, *N. rafflesiana*, *N. mirabilis*, *N. bicalcarata*, *N. albomarginata*, *N. gracilis*, *N. northiana*

### Pinguicula (Butterworts)
- Trap: flypaper · ~126 species · Mexican / Warm Temperate / Cold Temperate
- Popular: *P. moranensis*, *P. gigantea*, *P. agnata*, *P. cyclosecta*, *P. esseriana*, *P. moctezumae*, *P. laueana*, *P. primuliflora*, *P. vulgaris*

### Heliamphora (Sun Pitchers)
- Trap: pitfall · ~24 species · tepuis of South America · highland conditions
- Popular: *H. minor*, *H. nutans*, *H. heterodoxa*, *H. pulchella*, *H. tatei*, *H. ionasi*, *H. chimantensis*

### Cephalotus (Albany Pitcher Plant)
- Trap: pitfall · monotypic (one species: *C. follicularis*)
- Cultivars: 'Hummer's Giant', 'Eden Black', 'Czech Giant', 'Brewer's Red', 'Big Boy'

### Utricularia (Bladderworts)
- Trap: suction · ~230 species · Terrestrial / Epiphytic / Aquatic
- Popular: *U. sandersonii*, *U. livida*, *U. bisquamata*, *U. longifolia*, *U. calycifida*, *U. nelumbifolia*, *U. reniformis*, *U. gibba*

### Darlingtonia (Cobra Lily)
- Trap: pitfall · monotypic (*D. californica*) · cool-root requirement
- Locality clones: Oregon, California, 'Othello'

### Byblis (Rainbow Plants)
- Trap: flypaper · 8 species · Australia + New Guinea
- Popular: *B. liniflora*, *B. gigantea*, *B. filifolia*, *B. aquatica*, *B. rorida*

### Drosophyllum (Dewy Pine)
- Trap: flypaper · monotypic (*D. lusitanicum*) · Mediterranean / dry-grower
- Mostly sold as seed or seed-grown seedlings (variant: `seed` vs `live-plant`)

### Sarracenia (Trumpet Pitchers)
- Trap: pitfall · 8–11 species + 100s of hybrids/cultivars · dormancy required
- Species: *S. purpurea*, *S. flava*, *S. leucophylla*, *S. psittacina*, *S. rubra*, *S. alata*, *S. oreophila*, *S. minor*, *S. rosea*
- Cultivars: 'Adrian Slack', 'Judith Hindle', 'Doodle Bug', 'Scarlet Belle', 'Leah Wilkerson', 'Bug Bat'

### Dionaea (Venus Flytrap)
- Trap: snap · monotypic (*D. muscipula*) · dormancy required
- Cultivars: 'Akai Ryu', 'B52', 'Bohemian Garnet', 'Dente', 'Jaws', 'Sawtooth', 'Piranha', 'Ginormous', 'Alien', 'King Henry', 'Maroon Monster'

### Other
- Catch-all: *Genlisea*, *Aldrovanda vesiculosa*, *Brocchinia reducta*, *Catopsis berteroniana*, *Roridula*, *Triphyophyllum*, *Stylidium*

### Growing Supplies
- Soil: peat, long-fibre sphagnum, live sphagnum, perlite, silica sand, pumice, vermiculite, pre-mixed
- Pots, water/TDS meters, LED grow lights, humidifiers, terrariums, hygrometers, tweezers, labels, seed packets, books, gift cards

---

## 9. Performance Budget

| Metric | Target |
|---|---|
| LCP | < 2.5s |
| INP | < 200ms |
| CLS | < 0.1 |
| Total JS (parsed) | < 100 KB |
| Total CSS | < 60 KB |
| Hero image | < 150 KB (WebP/AVIF) |
| Third-party scripts | Only essentials (analytics + Shopify-native chat) |

---

## 10. Out of Scope (Phase 1)

- Multi-currency / multi-language
- Subscription / recurring orders
- Customer wishlists (Phase 2)
- Live chat (use Shopify Inbox only)
- Loyalty programme

---

## 11. Glossary for the AI Agent

- **Genus** — botanical grouping above species (e.g. *Dionaea*)
- **Species** — e.g. *Dionaea muscipula*
- **Cultivar** — a cultivated variety with a registered name, e.g. *D. muscipula* 'Akai Ryu'
- **PDP** — Product Detail Page
- **Pitfall trap** — passive trap that drowns prey (Nepenthes, Sarracenia, Heliamphora, Cephalotus, Darlingtonia)
- **Snap trap** — active closing trap (Dionaea, Aldrovanda)
- **Flypaper trap** — sticky mucilage trap (Drosera, Pinguicula, Byblis, Drosophyllum)
- **Suction trap** — bladder vacuum trap (Utricularia)
- **Dormancy** — required cold rest period for some temperate genera

---

**End of brief. Build accordingly.**

