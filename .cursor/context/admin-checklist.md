# Shopify Admin Setup Checklist

Manual configuration required in the Shopify Admin and Theme Editor for the Bizarre Tropicals custom theme. Complete every section before launch on the official store.

**Store:** `bizzare-tropicals.myshopify.com`  
**Theme path:** Online Store → Themes → Customize

---

## Development essentials (do these first)

Steps discovered during theme build that are easy to miss:

### Theme Editor — brand, contact, and social

Social URLs and contact details are configured in the **Footer** section (not global Theme settings). Open **Theme Editor → Footer** (footer group):

- [ ] **Address** — Enter the Gauteng address (default placeholder: `Gauteng, South Africa (By Appointment Only)`). Setting ID: `contact_address`.
- [ ] **Email** — `info@bizarretropicals.co.za` (setting: `contact_email`).
- [ ] **Phone / WhatsApp** — Live WhatsApp number (setting: `contact_phone`; default placeholder: `+27 (WhatsApp Preferred)`).
- [ ] **Facebook URL** — Official page (setting: `facebook_url`; schema default in `footer-group.json`: `https://www.facebook.com/bizarretropicals/`).
- [ ] **Instagram URL** — Official profile (setting: `instagram_url`; schema default: `https://www.instagram.com/bizarretropicals/`).
- [ ] **Show social links** — Enable `show_social` so icons render in the brand column.

### Main navigation

- [ ] **Catalog mega menu:** Ensure the desktop menu includes a top-level link titled **Catalog** (case-insensitive). It routes to **All products** (`/collections/all`) and opens the genus mega menu on hover. Populate genus thumbnails via **Mega menu item** blocks in the Header section (see **§6 Theme Editor**).

### Homepage layout

- [ ] **Hero slider:** **Theme Editor → Home page → Homepage hero** (`homepage-hero.liquid`, max **5** slide blocks). Per slide: upload botanical **macro** imagery, set bespoke **Heading**, **Subheading**, **Button label**, and **Button link**. Tune **Overlay opacity** for text contrast.
- [ ] **Featured collection:** **Theme Editor → Home page → Featured collection** (`featured-collection.liquid`). Select a **Featured** (or equivalent) collection for the dark-gradient carousel; set product count, heading, subheading, and view-all label.
- [ ] **Featured specimen:** **Theme Editor → Home page → Featured specimen** — see **§6.2**.
- [ ] **Conservatory standards:** **Theme Editor → Home page → Conservatory standards** — see **§6.3**.
- [ ] **Genus shortcuts:** Confirm each **Shop by genus** card points to the correct collection handle.

### The “Dossier” rule (collections)

**IMPORTANT:** The **Cultivation Dossier** 2-column grid in `collection-hero.liquid` only activates when the collection **Description** contains a **bulleted list** (`<ul>`). Plain paragraphs render as a single column.

- [ ] Enter each genus collection description as a **bulleted list** (HTML `<ul><li>…</li></ul>` or the rich-text bullet control in admin).
- [ ] Include all six care dimensions in every genus dossier:
  - **Light**
  - **Water**
  - **Substrate** (soil/media)
  - **Humidity**
  - **Dormancy**
  - **Feeding**
- [ ] Use **bold** labels on each line (e.g. `**Light:**`) so they match dossier heading styles.

**Example (Collection → Description):**

```html
<ul>
  <li><strong>Light:</strong> Bright direct sun, 6+ hours daily.</li>
  <li><strong>Water:</strong> Tray method; distilled or RO water only.</li>
  <li><strong>Substrate:</strong> 50/50 peat and perlite, no fertiliser.</li>
  <li><strong>Humidity:</strong> 40–60% for most windowsill species.</li>
  <li><strong>Dormancy:</strong> Not required for tropical sundews.</li>
  <li><strong>Feeding:</strong> Optional; let plants catch insects naturally.</li>
</ul>
```

- [ ] **Collection hero (optional):** Adjust **Care guide heading** and **Enable sticky dossier** in **Theme Editor → Collection pages → Collection hero**.

---

## 1. Store settings

- [ ] **Favicon:** **Theme Editor → Theme settings → Brand** — upload **Favicon image** (`layout/theme.liquid`).
- [ ] **Currency:** **Settings → Store details** — default **ZAR (South African Rand)**.
- [ ] **Markets:** South Africa as primary market (single-currency, Phase 1).
- [ ] **Checkout:** Shipping zones, live-plant policies, order notifications.
- [ ] **Newsletter:** Configure **Shopify Email** for subscribers from the **Field Notes** modal (`sections/newsletter-modal.liquid`). Tags: `newsletter`, `field-notes`. **Theme Editor → Field Notes newsletter modal** — trigger, delay, cookie duration (default 7 days).

---

## 2. Navigation

- [ ] **Main menu:** **Online Store → Navigation → Main menu** — Home, Catalog, About Us, Contact.
- [ ] **Header group** (**Theme Editor → Header**):
  - **Announcement bar** — Message blocks; rotation interval; dismiss stored in `localStorage` (`bt-announcement-<section-id>`).
  - **Header** — Desktop/mobile menus; logo; **Mega menu item** blocks for Catalog dropdown; **Search** opens overlay (`data-search-overlay-open`); **Cart** opens drawer (`data-cart-drawer-open`).
  - **Search overlay** — Genus quick-link blocks (defaults: `/collections/drosera`, etc.).
- [ ] **Predictive search:** **Search & Discovery** app enabled for `/search/suggest.json`.
- [ ] **Footer menu (optional):** **Theme Editor → Footer → Menu** for curated quick links.

---

## 3. Pages and templates

- [ ] **About** — Page created; template **`about`** (`page.about.json`).
- [ ] **Contact** — Handle `contact`; template **`contact`** (`page.contact.json`).
- [ ] **Care overview (optional):** `/pages/care-overview` for footer “Care” link.

---

## 4. Custom metafields (products)

Create in **Settings → Custom data → Products**, namespace **`custom`**. Keys must match Liquid exactly (`product.metafields.custom.<key>`).

### 4.1 Code cross-check (theme usage)

| Metafield key | Read in Liquid | Used for |
|---------------|--------------|----------|
| `custom.latin_name` | `sections/main-product.liquid`, `snippets/product-card.liquid`, `snippets/cart-drawer-contents.liquid` | PDP title line, card subtitle, cart line |
| `custom.difficulty` | `sections/main-product.liquid`, `snippets/product-card.liquid`, `snippets/product-card-badges.liquid` | Difficulty pips; **Easy care** wax seal when value = **1** |
| `custom.genus` | `snippets/product-card.liquid` | Genus handle / placeholder image selection |
| `custom.temperature_group` | `sections/main-product.liquid` | PDP temperature badge |
| `custom.trap_type` | `sections/main-product.liquid` | PDP trap-type badge |
| `custom.dormancy_required` | `sections/main-product.liquid` | PDP dormancy notice |

### 4.2 Required definitions (create before product import)

- [ ] **`custom.latin_name`** — Single line text
- [ ] **`custom.difficulty`** — Integer **1–5** (1 = beginner; triggers **Easy care** badge at 1)
- [ ] **`custom.genus`** — Single line text (lowercase handle, e.g. `dionaea`)
- [ ] **`custom.temperature_group`** — Single line text
- [ ] **`custom.trap_type`** — Single line text
- [ ] **`custom.dormancy_required`** — True or false

### 4.3 Allowed values

**`custom.temperature_group`:** `highland` · `intermediate` · `lowland` · `temperate` · `tropical` · `mediterranean`

**`custom.trap_type`:** `snap` · `pitfall` · `flypaper` · `suction` · `lobster-pot`

### 4.4 Recommended later (not rendered in current Liquid)

`custom.common_name` · `custom.temp_min_c` · `custom.temp_max_c` · `custom.cultivar` · `custom.pot_size_cm` · `custom.growth_stage` · `custom.cites_listed` · supply fields (`custom.supply_category`, etc.)

### 4.5 Product card badges (tags, not metafields)

Configured in `snippets/product-card-badges.liquid`:

- [ ] Tag **`Rare`** → **Rare specimen** wax seal
- [ ] Tag **`In-House`** → **Lab propagated** label
- [ ] **`custom.difficulty` = 1** → **Easy care** wax seal

---

## 5. Collections (genera)

- [ ] Handles: `drosera` · `nepenthes` · `pinguicula` · `heliamphora` · `cephalotus` · `utricularia` · `darlingtonia` · `byblis` · `drossophyllum` · `sarracenia` · `dionaea` · `other` · `growing-supplies`

### 5.1 Nepenthes sub-collections

- [ ] `nepenthes-highland` · `nepenthes-intermediate` · `nepenthes-lowland` (smart collections on `temperature_group` + genus tags)

### 5.2 Collection images and dossier

- [ ] **Collection image** — macro hero per genus.
- [ ] **Description** — bulleted dossier list (see **Development essentials → Dossier rule**).

---

## 6. Theme Editor (Customize) management

Use **Online Store → Themes → Customize** to control homepage, header, and About content without code. Every section below uses **blocks** or **settings** in the theme editor; development placeholders (Wikimedia URLs) apply until you upload production macro assets.

### 6.1 Header / mega menu

**Path:** **Theme Editor → Header** (header group) → select the **Header** section.

- [ ] Confirm the **Desktop menu** includes a top-level link titled **Catalog** (case-insensitive). Hover opens the genus mega menu.
- [ ] Under **Catalog mega menu**, add or edit **Mega menu item** blocks (up to 12). Each block controls one genus column:
  - **Genus label** — Display name (e.g. `Drosera`).
  - **Collection link** — URL to the genus collection (e.g. `/collections/drosera`).
  - **Thumbnail image** — Square macro upload (recommended). If empty, the **Placeholder thumbnail URL** is used until launch photography is ready.
- [ ] Drag blocks to reorder columns in the dropdown.
- [ ] Remove blocks for genera you do not stock yet.

### 6.2 Homepage — Featured specimen

**Path:** **Theme Editor → Home page → Featured specimen**.

- [ ] **Background color** — Dark panel behind copy (default forest charcoal).
- [ ] **Macro image** — Hero specimen photo; if empty, **Placeholder image URL** is shown.
- [ ] **Subheading**, **Heading** (Latin binomial), **Button label**, **Button link** — CTA to a product or collection.

### 6.3 Homepage — Conservatory standards

**Path:** **Theme Editor → Home page → Conservatory standards**.

- [ ] Set section **Subheading** and **Heading**.
- [ ] Add, remove, or reorder **Pillar** blocks (up to 4). Per pillar: **Thumbnail image** (or placeholder URL), **Pillar heading**, **Body text**.
- [ ] Replace Wikimedia placeholder URLs with uploaded 50×50 macro thumbnails before launch.

### 6.4 About page — Scientific plates

**Path:** **Theme Editor → Pages → About** (template **about**) → **About page** section.

- [ ] **Hero**, **Story**, **Laboratory**, and **The curator** groups — edit overlines, headings, rich text, portrait, and asymmetrical story/lab images (or placeholder URLs).
- [ ] **Conservatory** — set the section heading; then manage **Scientific plate** blocks:
  - **Plate image** — 4:5 botanical plate macro.
  - **Reference ID** — Label on the plate (e.g. `REF. QC-01`).
  - **Plate title** and **Plate description**.
  - **Placeholder image URL** — Development fallback per plate.
- [ ] Drag plates to reorder the conservatory grid.

---

## 7. Products and merchandising

- [ ] Populate all **§4.2** metafields on every live plant SKU before relying on PDP/cards.
- [ ] Macro photography; first image = featured image.
- [ ] Prices in **ZAR** (`snippets/zar-price.liquid`).
- [ ] Tags for filters: `genus:<handle>`, `temperature-group:<value>`, `trap-type:<value>`, `difficulty:1`–`5`, `dormancy:yes` / `no`.

---

## 8. Payments

- [ ] **Yoco** — **Settings → Payments**.
- [ ] **Footer → Show payment icons** — Yoco + enabled gateways.
- [ ] Test checkout on staging.

---

## 9. Apps and discovery (required for catalog filters)

- [ ] **Search & Discovery** — enable **Storefront filters** on collection pages for:
  - `custom.genus` (label: **Genus**)
  - `custom.difficulty` (label: **Difficulty**)
  - `custom.temperature_group` (label: **Temperature**)
  - `custom.trap_type` (label: **Trap type**)
- [ ] Optional additional filters: price, availability, dormancy (`custom.dormancy_required`).
- [ ] **Collection product grid** (`main-collection-product-grid.liquid`) — **Filter by cultivation** opens a left slide-out drawer; filters apply via AJAX without a full page reload.
- [ ] **Shopify Inbox** (optional, Phase 1).

---

## 10. Pre-launch QA

- [ ] Home: hero, genus shortcuts, featured specimen, conservatory standards (pillar blocks), featured collection (real products and macro imagery, not placeholders).
- [ ] About: curator portrait, laboratory image, scientific plates with REF IDs and plate imagery.
- [ ] Header: Catalog mega menu items (labels, links, thumbnails).
- [ ] Collection: hero, **2-column dossier** (bulleted description), product grid, **Filter by cultivation** drawer (genus, difficulty, temperature, trap type).
- [ ] PDP: `latin_name`, difficulty, `temperature_group`, `trap_type`, dormancy, ZAR price, cart drawer.
- [ ] Footer: address, email, WhatsApp, social, payments.
- [ ] Announcement bar, search overlay, Field Notes modal (if enabled).
- [ ] Product badges: `Rare`, `In-House`, difficulty **1**.
- [ ] Mobile: dossier single column; hero and carousels usable.

---

## 11. New account transfer

Complete when moving the theme to the **official** production Shopify store:

- [ ] **Domain:** **Settings → Domains** — connect the official domain; set as primary; confirm SSL/HTTPS.
- [ ] **Metafields first:** Re-create **all** product metafield definitions in **§4.2** (**Settings → Custom data → Products**) **before** importing product CSVs. Imported rows will not populate undefined metafields.
- [ ] **Staff access:** Ensure the **Logi-Ink** collaborator account has **Themes** and **Products** permissions (and **Settings** for metafields/payments as needed).
- [ ] **Billing & payments:** Reconnect **Yoco**; verify payout/business details.
- [ ] **Theme publish:** Publish this theme on the live store.
- [ ] **Re-run this checklist:** Theme Editor content (hero slides, mega menu blocks, footer URLs, featured collection) does not always migrate with code-only deploys — reconfigure sections **1–10** on production.
- [ ] **Replace placeholders:** Client macro photography per `.cursor/context/placeholder-images.md`.

---

## 12. Merchant customization (Theme Editor)

Modular sections — add, hide, or reorder without code:

- [ ] **Homepage hero** — slides, placeholders, overlay opacity.
- [ ] **Genus shortcuts** — collection per card, placeholders.
- [ ] **Featured collection** — collection, copy, count, gradient colors.
- [ ] **Collection hero** — care heading, placeholder URL, sticky dossier; dossier copy in collection **Description** (bulleted list).
- [ ] **Contact template** — FAQ blocks, social URLs.
- [ ] **About template** — curator, laboratory, scientific plates (see **§6.4**).
- [ ] **Footer** — brand story, contact fields, social URLs, menu, newsletter, payment icons.
- [ ] **Header group** — announcement bar, mega menu items, search overlay quick links.
- [ ] **Field Notes modal** — enable, trigger, copy, illustration.

---

*Last aligned with theme files: schema audit — `sections/header.liquid`, `sections/header-group.json`, `snippets/header-catalog-mega-menu.liquid`, `snippets/site-nav.liquid`, `snippets/site-nav-item.liquid`, `sections/featured-specimen.liquid`, `sections/conservatory-standards.liquid`, `sections/about-template.liquid`, `templates/page.about.json`, `locales/en.default.schema.json`, plus `layout/theme.liquid`, `sections/main-collection-product-grid.liquid`, `snippets/cultivation-filter-drawer.liquid`, `page.contact.json`, `index.json`, `footer-group.json`, `en.default.json`.*
