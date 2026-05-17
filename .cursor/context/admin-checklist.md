# Shopify Admin Setup Checklist

Manual configuration required in the Shopify Admin and Theme Editor for the **Bizarre Tropicals** custom theme. Complete every section before launch on the official store.

**Store:** `bizzare-tropicals.myshopify.com`  
**Theme path:** Online Store → Themes → Customize  
**Codebase root:** Shopify Online Store 2.0 theme (`sections/`, `templates/`, `snippets/`, `layout/theme.liquid`)

---

## How data flows (dynamic vs manual)

| Area | Source | Notes |
|------|--------|--------|
| **Catalog mega menu** | Live `collections` | Auto-lists in-stock genus collections (`snippets/header-catalog-mega-menu.liquid`). Thumbnails: block upload → collection image → first product image → placeholder. |
| **Shop by genus** (homepage) | Live collections **or** manual blocks | Default: **Use live Shopify collections** (`use_dynamic_genera`). Same genus rules as mega menu. Turn off to use manual **Genus card** blocks. |
| **Botanical discovery strip** | Per-block collection picker | Up to 4 cards; image fallback: override → collection image → first product image. |
| **Newly cataloged** | Collection picker + `created_at` sort | Default collection: **All** (`all`). Newest products first in Liquid. |
| **Featured plants** | Collection picker | Falls back to `collections.all` on homepage; on PDP falls back to product’s first collection. |
| **Featured specimen** | Product picker + optional overrides | Pick a product for live image, title (Latin metafield), and URL. |
| **Collection grid** | `collection.products` + Search & Discovery filters | AJAX filters + load more; dedupes product IDs. |
| **Product cards / PDP** | `product` + `custom.*` metafields | Mock/placeholder only in theme preview or empty catalog. |
| **Cart / checkout** | Shopify Cart API + hosted checkout | Cart drawer is theme-side; checkout is Shopify-hosted. |
| **Customer account link** | Theme `/account` + login | Avoids 401 from hosted profile URL on theme dev. |

**Launch rule:** Replace Wikimedia / Unsplash placeholder URLs with uploaded Shopify Files or product photography (see `.cursor/context/placeholder-images.md`). Placeholders hurt performance and SEO.

---

## Template registry

Assign each **Page** in Admin → **Online Store → Pages** to the matching template suffix.

| Template file | Type | Purpose | Section(s) |
|---------------|------|---------|------------|
| `templates/index.json` | Home | Homepage | `home-slider`, `genus-shortcuts`, `botanical-discovery-strip`, `new-specimens`, `featured-specimen`, `conservatory-standards`, `featured-collection` |
| `templates/collection.json` | Collection | All genus / catalog grids | `main-collection-banner`, `main-collection-product-grid` |
| `templates/product.json` | Product | Specimen PDP | `main-product`, `featured-collection` (related) |
| `templates/cart.json` | Cart | Full cart page | Theme cart section |
| `templates/search.json` | Search | Search results | `search` |
| `templates/list-collections.json` | List collections | Collection index | `collections` |
| `templates/blog.json` | Blog | Blog index | `blog` |
| `templates/article.json` | Article | Blog post | `article` |
| `templates/404.json` | 404 | Not found | `main-404` |
| `templates/password.json` | Password | Store password | `password` |
| `templates/gift_card.liquid` | Gift card | Gift card | Liquid gift card |
| `templates/page.json` | Page (default) | Generic rich page | `page` |
| `templates/page.about.json` | Page | About | `about-template` |
| `templates/page.contact.json` | Page | Contact | `contact-template` |
| `templates/page.privacy.json` | Page | Privacy policy | `main-policy-page` |
| `templates/page.refund.json` | Page | Refund policy | `main-policy-page` |
| `templates/page.shipping.json` | Page | Shipping policy | `main-policy-page` |
| `templates/customers/login.json` | Customer | Login | `main-login` |
| `templates/customers/register.json` | Customer | Register | `main-register` |
| `templates/customers/account.json` | Customer | Account hub | `main-account` |
| `templates/customers/order.json` | Customer | Order detail (JSON) | `main-order` |
| `templates/customers/order.liquid` | Customer | Order detail (Liquid) | `main-order` — **do not enable both**; repo keeps `.liquid` for Theme Editor certificate preview |

**Section groups**

| File | Renders |
|------|---------|
| `sections/header-group.json` | Announcement bar, header, search overlay |
| `sections/footer-group.json` | Footer |

**Legacy / unused on storefront (safe to ignore in admin)**

| File | Note |
|------|------|
| `sections/homepage-hero.liquid` | Duplicate of `home-slider`; not referenced in `index.json` |
| `sections/collection.liquid`, `sections/product.liquid`, `sections/404.liquid` | Starter stubs; live templates use `main-*` sections |

---

## Development essentials (do these first)

### Theme Editor — brand, contact, and social

Social URLs and contact details are configured in the **Footer** section (footer group):

- [ ] **Address** — Gauteng address (`contact_address`).
- [ ] **Email** — `info@bizarretropicals.co.za` (`contact_email`).
- [ ] **Phone / WhatsApp** — Live number (`contact_phone`).
- [ ] **Facebook / Instagram URLs** — Official profiles (`facebook_url`, `instagram_url`).
- [ ] **Show social links** — Enable `show_social`.

### Main navigation

- [ ] **Main menu** (`main-menu` in `header-group.json`): Home, **Catalog**, About, Contact.
- [ ] **Catalog** link opens mega menu → **All products** (`/collections/all`).
- [ ] Mega menu auto-shows in-stock genera; optional **Mega menu item** blocks override thumbnails/labels.

### Homepage layout (`templates/index.json`)

- [ ] **Home slider** (`home-slider.liquid`) — Up to **5** slides. Upload macro images (not Wikimedia URLs). First slide loads with `fetchpriority: high`. Autoplay + Ken Burns; pauses when tab hidden.
- [ ] **Shop by genus** (`genus-shortcuts.liquid`) — Enable **Use live Shopify collections** (recommended). Or manual genus blocks with collection per card. Carousel: autoplay, loop, arrow wrap.
- [ ] **Botanical discovery strip** (`botanical-discovery-strip.liquid`) — 4 collection cards; anchor heading in Bizarre red. Assign collections in blocks.
- [ ] **New specimen ledger** (`new-specimens.liquid`) — Collection **All** (or New Arrivals); sorted newest first; autoplay + loop.
- [ ] **Featured specimen** (`featured-specimen.liquid`) — Pick a **Featured product** for live image/link; override copy as needed.
- [ ] **Conservatory standards** — Pillar blocks; replace placeholder thumbnails.
- [ ] **Featured plants** (`featured-collection.liquid`) — Select collection (defaults to **All** in code if empty). Autoplay + loop.

### Catalog hero — Anatomy of a predator

**Collection banner** (`main-collection-banner.liquid`):

- [ ] Upload **Illustration image** (transparent PNG) or set fallback URL.
- [ ] Collection **title** and optional **description** from Admin → Collections.

### The “Dossier” rule (in-page care content)

Bulleted HTML (`<ul><li>…</li></ul>`) in collection or product descriptions activates the 2-column cultivation grid on PDP.

- [ ] Six dimensions: Light, Water, Substrate, Humidity, Dormancy, Feeding — bold labels per line.

---

## Performance checklist (for merchants & dev)

Report slow loads to your developer if these are not done:

### Critical (biggest impact)

- [ ] **Replace external placeholder images** — Wikimedia/Unsplash URLs on homepage, genus cards, and hero force large off-domain downloads. Upload to **Settings → Files** or product/collection images.
- [ ] **Compress macro photography** — WebP/JPEG, reasonable dimensions (hero ≤ 2400px wide).
- [ ] **Limit homepage slides** to 3–5 with real uploads (not 5× duplicate-weight placeholders).
- [ ] **Search & Discovery** — Only enable filters you need; many filters slow collection AJAX.

### Theme behaviour (already in code)

- [ ] First hero slide: `loading="eager"` + `fetchpriority="high"`.
- [ ] Other images: lazy loading via `image_tag` / `loading="lazy"`.
- [ ] Carousels pause autoplay when browser tab is hidden (`document.hidden`).
- [ ] Below-fold sections use `content-visibility: auto` on desktop (see `assets/base.css`).
- [ ] Scripts: `global.js`, `theme.js`, `cart-drawer.js` are **deferred** in `layout/theme.liquid`.
- [ ] Section CSS/JS is bundled per section by Shopify (no jQuery/React).

### Shopify Admin

- [ ] **Apps** — Remove unused apps (inject scripts into `content_for_header`).
- [ ] **Markets / analytics** — Keep only required tracking.
- [ ] Run **Shopify Theme Check** and **PageSpeed** on production URL after placeholders removed.

### Theme dev proxy

- [ ] `shopify theme dev` is slower than production CDN; judge performance on the published `.myshopify.com` or live domain.

---

## 1. Store settings

- [ ] **Favicon:** Theme settings → Brand (`layout/theme.liquid`).
- [ ] **Currency:** ZAR default.
- [ ] **Checkout:** Shipping zones, live-plant policies.
- [ ] **Newsletter:** Shopify Email + **Field Notes** modal (`newsletter-modal.liquid`).

---

## 2. Navigation

- [ ] **Main menu** — Home, Catalog, About, Contact.
- [ ] **Header group:** Announcement bar, Header (logo, menus, mega menu blocks), Search overlay genus quick links.
- [ ] **Predictive search:** Search & Discovery app → `/search/suggest.json`.
- [ ] **Footer menu** (optional).

---

## 3. Pages and templates

Create pages in Admin and assign templates:

| Page | Handle (suggested) | Template suffix |
|------|-------------------|-----------------|
| About | `about` | `about` |
| Contact | `contact` | `contact` |
| Privacy | `privacy-policy` | `privacy` |
| Refund | `refund-policy` | `refund` |
| Shipping | `shipping-policy` | `shipping` |
| Care overview (optional) | `care-overview` | `page` (default) or custom |

- [ ] **404:** Theme Editor → 404 → `main-404` (CTA default `/collections/all`).

---

## 4. Custom metafields (products)

**Settings → Custom data → Products**, namespace **`custom`**.

### 4.1 Theme usage

| Metafield key | Used in |
|---------------|---------|
| `custom.latin_name` | PDP, product cards, cart drawer |
| `custom.difficulty` | PDP, cards, badges (1 = Easy care) |
| `custom.genus` | Product cards, placeholder genus art |
| `custom.temperature_group` | PDP badge |
| `custom.trap_type` | PDP badge |
| `custom.dormancy_required` | PDP notice |
| `custom.care_guide` | PDP **Botanical husbandry** accordion |

### 4.2 Required definitions

- [ ] `custom.latin_name` — Single line text  
- [ ] `custom.difficulty` — Integer 1–5  
- [ ] `custom.genus` — Single line (handle, e.g. `drosera`)  
- [ ] `custom.temperature_group` — Single line text  
- [ ] `custom.trap_type` — Single line text  
- [ ] `custom.dormancy_required` — Boolean  
- [ ] `custom.care_guide` — Rich text  

### 4.3 Allowed values

**`temperature_group`:** `highland` · `intermediate` · `lowland` · `temperate` · `tropical` · `mediterranean`  

**`trap_type`:** `snap` · `pitfall` · `flypaper` · `suction` · `lobster-pot`

### 4.4 Product tags (badges)

- [ ] `Rare` → Rare specimen seal  
- [ ] `In-House` → Lab propagated  
- [ ] `custom.difficulty` = 1 → Easy care  

---

## 5. Collections (genera)

- [ ] Handles: `drosera`, `nepenthes`, `pinguicula`, `heliamphora`, `cephalotus`, `utricularia`, `darlingtonia`, `byblis`, `drossophyllum`, `sarracenia`, `dionaea`, `other`, `growing-supplies`, `all`
- [ ] **Nepenthes sub-collections:** `nepenthes-highland`, `nepenthes-intermediate`, `nepenthes-lowland` (smart collections on metafields/tags)
- [ ] **Collection image** + bulleted dossier **description** per genus

---

## 6. Theme Editor sections (reference)

### 6.1 Header / mega menu

- [ ] **Catalog** in desktop menu.  
- [ ] **Mega menu item** blocks: optional label, link, thumbnail (else live collection/product/placeholder).

### 6.2 Homepage sections

| Section file | Key settings |
|--------------|--------------|
| `home-slider.liquid` | Slide blocks, overlay opacity, images |
| `genus-shortcuts.liquid` | **Use live Shopify collections**, hide empty blocks, heading |
| `botanical-discovery-strip.liquid` | Anchor heading/color, 4 discovery cards |
| `new-specimens.liquid` | Collection, product limit, copy |
| `featured-specimen.liquid` | **Product**, image override, CTA |
| `conservatory-standards.liquid` | Pillar blocks |
| `featured-collection.liquid` | Collection, count, gradient |

### 6.3 About page (`page.about.json`)

- [ ] **About page** section: hero, story, laboratory, curator, **Scientific plate** blocks.

### 6.4 Policy pages

- [ ] Privacy / Refund / Shipping → `main-policy-page` with fallback body copy in template JSON.

---

## 7. Products and merchandising

- [ ] All §4.2 metafields on live plant SKUs.  
- [ ] Featured image = primary macro photo.  
- [ ] ZAR pricing.  
- [ ] Tags: `genus:<handle>`, `temperature-group:<value>`, `trap-type:<value>`, `difficulty:1`–`5`, `dormancy:yes` / `no`.

---

## 8. Payments

- [ ] **Yoco** in Settings → Payments.  
- [ ] Footer payment icons enabled.  
- [ ] Test checkout on staging.

---

## 9. Search & Discovery (catalog filters)

- [ ] Storefront filters: Availability, Price, Genus, Difficulty, Temperature, Trap type (as needed).  
- [ ] Collection grid: desktop filter bar + mobile drawer; **Load more specimens** (no numbered pagination).

---

## 10. Pre-launch QA

- [ ] Home: real images, dynamic genus strip, discovery strip links, newly cataloged from live products, featured collection not mock cards.  
- [ ] Catalog: no duplicate products in grid; filters work; load more works.  
- [ ] PDP: metafields, cart drawer add, cultivation accordion.  
- [ ] Account icon → login or `/account` (no 401).  
- [ ] Mobile: carousels swipe; reduced motion respected.  
- [ ] PageSpeed / Lighthouse on production after placeholder removal.

---

## 10.1 Order fulfillment

- [ ] Pack **Specimen Log** printout from customer order page (`main-order.liquid`).  
- [ ] Cart drawer **Botanical dispatch** copy matches schedule (`cart-drawer-dispatch.liquid`).

---

## 11. New account transfer (production store)

- [ ] Domain + SSL.  
- [ ] Recreate metafields **before** CSV import.  
- [ ] Reconnect Yoco.  
- [ ] Publish theme; re-run Theme Editor sections 1–10.  
- [ ] Replace all placeholder imagery.

---

## 12. Theme Editor — global overlays

These sections are included in `layout/theme.liquid` (not on `index.json`). In **Customize**, open the left sidebar and select:

| Section | What the client can edit |
|---------|-------------------------|
| **Field Notes newsletter modal** | Heading, subtext, button, illustration, trigger, delay — preview opens when the section is selected |
| **Cart drawer** | Drawer title, empty-cart copy, dispatch note toggle |

All homepage sections (`home-slider`, `genus-shortcuts`, `botanical-discovery-strip`, etc.) expose text, images, and collection pickers when clicked.

**Shop by genus:** enable **Use live Shopify collections** to auto-list in-stock genera (recommended).

---

## 13. Customer accounts

- [ ] **Classic accounts:** Theme templates under `templates/customers/`.  
- [ ] **New customer accounts:** Header uses theme login; logged-in users go to `/account` (not hosted profile URL) to avoid dev/proxy 401 errors.  
- [ ] Enable customer accounts in **Settings → Customer accounts**.

---

## Code map (quick reference)

```
layout/theme.liquid          → header-group, cart-drawer, newsletter, footer-group, deferred JS
sections/header-group.json   → announcement-bar, header, search-overlay
sections/footer-group.json   → footer
snippets/header-catalog-mega-menu.liquid  → dynamic genus list
snippets/genus-shortcuts-dynamic-strip.liquid → homepage genus carousel (dynamic)
snippets/customer-account-link-url.liquid → account/login URLs
sections/main-collection-product-grid.liquid → catalog + filters + load more
sections/main-product.liquid → PDP
assets/base.css              → global styles + content-visibility
assets/global.js             → reduced motion + tab visibility
assets/theme.js              → scroll reveal
```

---

*Last aligned with theme: `newsletter-modal.liquid`, `cart-drawer.liquid`, `page.liquid`, `genus-shortcuts.liquid` (dynamic genera), `botanical-discovery-strip.liquid`, `genus-shortcuts.liquid` (dynamic genera), `featured-collection.liquid`, `new-specimens.liquid`, `featured-specimen.liquid` (product picker), `main-collection-product-grid.liquid`, `customer-account-link-url.liquid`, `templates/index.json`, `templates/product.json`, policy templates, `assets/base.css`, `assets/global.js`.*
