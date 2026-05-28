# Feature roadmap — supplies, PDP, care overview

## 1. Growing supplies — sub-filter chips (`supply_category`)

### Goal

On `/collections/growing-supplies`, in-page chips filter by supply type without separate URLs (per client brief).

### Prerequisites (Admin)

1. **Metafield** `custom.supply_category` (single line text or list) on products  
   Allowed values: `soil`, `pot`, `water`, `lighting`, `climate`, `tool`, `seed`, `book-gift`  
2. Tag each supply SKU, e.g. `supply:soil`, or set metafield on each product.

### Theme approach

| Approach | Effort | Notes |
|----------|--------|--------|
| **Search & Discovery subcollections** | Low (Admin) | Create child collections `growing-supplies-soil`, etc. — **different URLs**, not chips |
| **Client-side filter chips** | Medium | Section on `collection.json` when handle is `growing-supplies`; filter cards by `data-supply-category` on product cards |
| **Shopify filters** | Low | Add `supply_category` as storefront filter — sidebar/drawer, not chips |

**Recommended:** Medium-term build `sections/growing-supplies-chips.liquid` + extend `product-card.liquid` with `data-supply-category="{{ product.metafields.custom.supply_category }}"`. Chips toggle visibility via JS (no new URLs). Reuse collection grid below.

---

## 2. PDP — CITES notice + “Pair with” cross-sell

### CITES notice

**Prerequisites:** `custom.cites_listed` (boolean) and/or tag `cites:yes`.

**Theme:** In `main-product.liquid`, above add-to-cart:

```liquid
{% if product.metafields.custom.cites_listed == true or product.tags contains 'cites:yes' %}
  … banner: export restrictions, SA compliance …
{% endif %}
```

**Effort:** Small (~1 hour).

### Pair with growing supplies

**Prerequisites:** Related products via:

- Shopify **product recommendations** (complementary), or  
- Manual **collection** `growing-supplies` + filter by tags on PDP genus, or  
- Metafield **list of product references** (heavy Admin).

**Theme:** New block or accordion “Pair with…” using `collection.products` from `growing-supplies` (limit 4) or `recommendations.products` API.

**Effort:** Medium (~half day).

---

## 3. Care overview page (`/pages/care-overview`)

### Goal

High-level “How to grow carnivorous plants” linking into genus collections (brief §3.1).

### Options

| Option | Effort | Notes |
|--------|--------|--------|
| **Generic page** | None | Create page in Admin, assign `page.json`, write content in page body |
| **`page.care-overview.json`** | Small | Section with intro + grid of genus links from `catalog-genus-handles` snippet |
| **Blog article** | Low | Single pinned article — not ideal for nav structure |

**Recommended:** Add `templates/page.care-overview.json` + `sections/care-overview-template.liquid`:

- Hero + 3–4 pillars (water, light, dormancy, substrate)  
- Auto-linked genus cards (reuse genus-shortcut card snippet)  
- CTA to contact / catalog  

**Effort:** Small–medium (~half day). No blog required.

---

## Priority order

1. CITES banner (compliance, small)  
2. Care overview page (SEO + education)  
3. Wire collection-hero / genus descriptions (see genus-care doc)  
4. Pair with supplies cross-sell  
5. Growing-supplies chips  
