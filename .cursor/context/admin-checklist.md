# Shopify Admin Setup Checklist

Manual configuration required in the Shopify Admin and Theme Editor for the Bizarre Tropicals custom theme. Complete every section before launch on the official store.

**Store:** `bizzare-tropicals.myshopify.com`  
**Theme path:** Online Store → Themes → Customize

---

## 1. Store settings

- [ ] **Favicon:** In the Theme Editor → **Theme settings** → **Brand**, upload a square PNG (32×32 or larger) under **Favicon image**. The theme outputs it in `layout/theme.liquid`.
- [ ] **Currency:** Set the store default currency to **ZAR (South African Rand)** in **Settings → Store details**.
- [ ] **Markets:** Confirm South Africa is the primary market (single-currency store for Phase 1).
- [ ] **Checkout:** Review shipping zones, live-plant policies, and order notification emails.

---

## 2. Navigation

- [ ] **Main menu:** Go to **Online Store → Navigation → Main menu** and ensure links include: **Home**, **Catalog** (or shop-all collection), **About Us**, **Contact**.
- [ ] **Header:** In the Theme Editor → **Header** section, assign **Desktop menu** (and optional **Mobile menu**). Upload a **Logo image** or rely on the typographic fallback (“Bizarre Tropicals”). Confirm **Search** and **Cart** icons work; cart opens the AJAX drawer (`data-cart-drawer-open`).
- [ ] **Footer menu (optional):** In the Theme Editor → **Footer** section, assign a menu under **Menu** if you want curated quick links; otherwise the theme falls back to default shop/about/care/contact links.

---

## 3. Pages and templates

- [ ] **About page:** Create an **About Us** page in **Online Store → Pages**.
- [ ] **Assign template:** On the About page, set **Theme template** to **`about`** (not *Default page*).
- [ ] **Contact page:** Create a **Contact** page with handle `contact` (`/pages/contact`) so footer and navigation links resolve.
- [ ] **Contact template:** On the Contact page, set **Theme template** to **`contact`** (split form, FAQ accordion blocks, social links).
- [ ] **About template:** Set **Theme template** to **`about`** (laboratory, curator bio, conservatory pillars — all editable in the section).
- [ ] **Care overview (optional):** Create `/pages/care-overview` if you want the footer “Care” link to land on a dedicated overview page.

---

## 4. Custom metafields (products)

Go to **Settings → Custom data → Products**. Create definitions in the **`custom`** namespace using these **exact keys** (the theme reads `product.metafields.custom.<key>`).

### 4.1 Required by theme templates (create first)

| Admin label | Namespace & key | Type | Used on |
|-------------|-----------------|------|---------|
| Latin name | `custom.latin_name` | Single line text | PDP, product cards |
| Difficulty | `custom.difficulty` | Integer (1–5) | PDP, product cards |
| Genus | `custom.genus` | Single line text | Product cards (placeholder images) |
| Temperature group | `custom.temperature_group` | Single line text | PDP |
| Trap type | `custom.trap_type` | Single line text | PDP |
| Dormancy required | `custom.dormancy_required` | True or false | PDP |

- [ ] **Latin name** — `custom.latin_name`
- [ ] **Difficulty** — `custom.difficulty` (integer **1–5**; 1 = beginner, 5 = expert)
- [ ] **Genus** — `custom.genus` (lowercase handle, e.g. `dionaea`, `nepenthes`)
- [ ] **Temperature group** — `custom.temperature_group`
- [ ] **Trap type** — `custom.trap_type`
- [ ] **Dormancy required** — `custom.dormancy_required`

### 4.2 Allowed values (PDP badges and labels)

**`custom.temperature_group`** — use one of:

`highland` · `intermediate` · `lowland` · `temperate` · `tropical` · `mediterranean`

**`custom.trap_type`** — use one of:

`snap` · `pitfall` · `flypaper` · `suction` · `lobster-pot`

### 4.3 Recommended for catalog growth (not yet rendered in Liquid)

From the build spec; add when you import or filter at scale:

`custom.common_name` · `custom.temp_min_c` · `custom.temp_max_c` · `custom.cultivar` · `custom.pot_size_cm` · `custom.growth_stage` · `custom.cites_listed` · supply fields (`custom.supply_category`, etc.)

---

## 5. Collections (genera)

Go to **Products → Collections** and create manual (or smart) collections with these **handles**:

- [ ] `drosera` · `nepenthes` · `pinguicula` · `heliamphora` · `cephalotus` · `utricularia` · `darlingtonia` · `byblis` · `drossophyllum` · `sarracenia` · `dionaea` · `other` · `growing-supplies`

### 5.1 Nepenthes sub-collections

- [ ] **`nepenthes-highland`** — smart collection: genus Nepenthes + `temperature_group` = `highland`
- [ ] **`nepenthes-intermediate`** — smart collection: genus Nepenthes + `temperature_group` = `intermediate`
- [ ] **`nepenthes-lowland`** — smart collection: genus Nepenthes + `temperature_group` = `lowland`

Use product tags and/or metafields per your Search & Discovery filter setup.

### 5.2 Collection images

- [ ] Upload a high-quality **macro** image as each collection’s **Collection image** (used in the collection hero when present).

### 5.3 Cultivation dossier (collection description)

The **Collection hero** section renders care content from the collection **Description** field. A **bulleted list** in that field triggers the theme’s **2-column Cultivation Dossier** layout (`collection-hero.liquid`).

- [ ] **Formatting:** Enter the description as a **bulleted list** (not plain paragraphs) so the dossier grid activates on desktop.
- [ ] **Required topics:** Each genus list should include all six care dimensions:
  - **Light**
  - **Water**
  - **Substrate** (soil/media)
  - **Humidity**
  - **Dormancy**
  - **Feeding**
- [ ] **Label style:** Use **bold** list labels (e.g. `**Light:**` …) so they match dossier heading styles.

**Example (paste into Collection → Description):**

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

- [ ] **Care heading (optional):** In **Theme Editor → Collection pages → Collection hero**, adjust **Care guide heading** (default: “Care guide”) if needed.

---

## 6. Theme global and section settings

### 6.1 Footer — contact information

**Theme Editor → Footer** (footer group). Update:

- [ ] **Address** — Gauteng address (default: `Gauteng, South Africa (By Appointment Only)`)
- [ ] **Email** — `info@bizarretropicals.co.za`
- [ ] **Phone** — WhatsApp number (default placeholder: `+27 (WhatsApp Preferred)`)

### 6.2 Social media

Facebook and Instagram appear in the **Footer** brand column. The theme currently links to:

- Facebook: `https://www.facebook.com/bizarretropicals/`
- Instagram: `https://www.instagram.com/bizarretropicals/`

- [ ] **Verify profiles:** Confirm these URLs match the official Bizarre Tropicals accounts after store transfer.
- [ ] **Theme settings (if added):** If **Theme settings → Social media** fields are present in your theme version, enter Facebook and Instagram URLs there; otherwise confirm the footer defaults above.

### 6.3 Homepage — hero slider

**Theme Editor → Home page → Homepage hero** (`homepage-hero`, max **5** slide blocks).

- [ ] Add up to **5 slides** (block type **Slide**).
- [ ] Per slide: upload a **high-resolution botanical** image, set **Heading**, **Subheading**, **Button label**, and **Button link** (e.g. `/collections/drosera`).
- [ ] Adjust **Overlay opacity** if text contrast needs tuning.

### 6.4 Homepage — featured collection

**Theme Editor → Home page → Featured collection**.

- [ ] **Collection:** Select a collection (e.g. **Featured** or **New Arrivals**) for the dark-gradient product carousel.
- [ ] **Products to show:** Set count (4–12; default 8).
- [ ] **Heading / Subheading / View all label:** Align copy with merchandising (defaults: “Featured plants”, etc.).

### 6.5 Homepage — genus shortcuts

**Theme Editor → Home page → Shop by genus**.

- [ ] Confirm each genus block points to the correct collection URL.
- [ ] Reorder or add blocks for additional genera as the catalogue grows.

---

## 7. Products and merchandising

- [ ] **Metafields:** Populate `latin_name`, `difficulty`, `genus`, and PDP fields (`temperature_group`, `trap_type`, `dormancy_required`) for every live plant SKU.
- [ ] **Images:** Use macro product photography; first image = featured image for cards and PDP gallery.
- [ ] **Pricing:** Enter prices in ZAR; theme formats via `zar-price` snippet.
- [ ] **Tags (recommended):** `genus:<handle>`, `temperature-group:<value>`, `trap-type:<value>`, `difficulty:1`–`5`, `dormancy:yes` / `dormancy:no` for Search & Discovery filters.

---

## 8. Payments

The footer always shows a **Yoco** badge when **Show payment icons** is enabled. Shopify-native card icons appear when gateways are active.

- [ ] **Yoco:** Install and configure the **Yoco** payment gateway in **Settings → Payments** so checkout accepts ZAR card payments.
- [ ] **Payment icons:** In **Theme Editor → Footer**, keep **Show payment icons** enabled to display Yoco and enabled payment types in the footer.
- [ ] **Test checkout:** Place a test order to confirm icons and checkout match live gateway configuration.

---

## 9. Apps and discovery (recommended)

- [ ] **Search & Discovery:** Configure storefront filters for difficulty, temperature group, trap type, price, in stock, and dormancy (tied to metafields/tags above).
- [ ] **Shopify Inbox:** Enable if using native chat (Phase 1 scope).

---

## 10. Pre-launch QA

- [ ] Home: hero slides, genus shortcuts, and featured collection show real products (not placeholders).
- [ ] Collection page: hero image, dossier grid, and product grid load for each genus.
- [ ] PDP: Latin name, difficulty pips, temperature badge, trap type, dormancy line, ZAR price, add to cart (opens AJAX cart drawer).
- [ ] Cart drawer: header icon and PDP add-to-cart open slide-out drawer; quantity +/- updates via Cart API; checkout link works.
- [ ] Footer: address, email, phone, social links, payment icons.
- [ ] About page uses the `about` template and editable pillar blocks.
- [ ] Mobile: dossier collapses to one column; hero and carousel remain usable.

---

## 11. New store migration

Complete after transferring the theme and data to the **official** Shopify account:

- [ ] **Domain:** Connect the production domain in **Settings → Domains** and set it as primary.
- [ ] **SSL:** Confirm HTTPS is active on the primary domain.
- [ ] **Staff access:** Ensure the **Logi-Ink** collaborator/staff account has **Themes** and **Products** (and **Settings** as needed for metafields/payments).
- [ ] **Billing & payments:** Reconnect Yoco and verify payout/business details on the new store.
- [ ] **Theme publish:** Publish the Bizarre Tropicals theme on the live store.
- [ ] **Repeat this checklist:** Re-run sections 1–10 on the production store; theme editor content does not always migrate with code-only pushes.
- [ ] **Remove dev placeholders:** Replace Commons/Wikimedia placeholder images with client photography (see `.cursor/context/placeholder-images.md`).

---

---

## 12. Merchant customization

Every section on the homepage, about page, and contact page is modular. You can add, hide, or reorder these sections and their internal blocks directly in the Theme Editor (Customize).

Theme sections also expose merchant-editable settings so content can change without code deploys:

- [ ] **Homepage hero:** Upload slide images or set per-slide / default placeholder URLs; adjust overlay opacity.
- [ ] **Genus shortcuts:** Pick a **Collection** per card (title/link optional); set section and per-card placeholder URLs.
- [ ] **Featured collection:** Choose collection, copy, product count, view-all label, and gradient background colors.
- [ ] **Collection hero:** Set care heading, placeholder image URL, and sticky dossier toggle; write care copy in each collection’s **Description** (HTML list for the dossier grid).
- [ ] **Contact page:** Toggle FAQ, social links, and sticky sidebar; edit panel image/placeholder, contact rows, FAQ **Question** blocks, and social URLs/handles (URL fields have no schema default—set them in the template or Theme Editor; defaults live in `page.contact.json` and `footer-group.json`).
- [ ] **About page:** Edit overlines, science vs nature split/lab copy, curator signature, placeholder URLs, and pillar blocks (icon, heading, text, placeholder).
- [ ] **Footer:** Brand story (HTML), social URLs, show-social toggle, copyright and designer link, contact fields, menu, newsletter, payment icons.

---

*Last aligned with theme files: `layout/theme.liquid`, `config/settings_schema.json`, `sections/header.liquid`, `about-template.liquid`, `contact-template.liquid`, `collection-hero.liquid`, `featured-collection.liquid`, `footer.liquid`, `genus-shortcuts.liquid`, `homepage-hero.liquid`, `page.about.json`, `page.contact.json`, `index.json`, `en.default.schema.json`.*
