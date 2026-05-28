# Collections & smart collections — setup guide

Use this when completing Admin checklist §5. Handles must match `snippets/catalog-genus-handles.liquid` and the mega menu.

## 1. Manual collections (create first)

**Products → Collections → Create collection → Manual**

| Handle | Title (example) | Notes |
|--------|-----------------|--------|
| `all` | All products | Often auto; ensure it exists for homepage sections |
| `growing-supplies` | Growing supplies | Soil, pots, lights, etc. |
| `other` | Other carnivores | Catch-all genus |
| `dionaea` | Dionaea | |
| `sarracenia` | Sarracenia | |
| `drosera` | Drosera | |
| `pinguicula` | Pinguicula | |
| `cephalotus` | Cephalotus | |
| `heliamphora` | Heliamphora | |
| `utricularia` | Utricularia | |
| `darlingtonia` | Darlingtonia | |
| `byblis` | Byblis | |
| `drossophyllum` | Drosophyllum | Display spelling; handle stays `drossophyllum` per brief |

Optional parent (for marketing URL only; **not** in dynamic genus nav):

| Handle | Title | Notes |
|--------|-------|--------|
| `nepenthes` | Nepenthes | Parent landing; link to 3 sub-collections below |

## 2. Smart collections — Nepenthes elevation groups

**Products → Collections → Create → Automated**

### `nepenthes-highland`

- **Conditions (all must match):**
  - Product tag **equals** `genus:nepenthes` **OR** metafield `custom.genus` equals `nepenthes`
  - **AND** Product tag **equals** `temperature-group:highland` **OR** metafield `custom.temperature_group` equals `highland`

### `nepenthes-intermediate`

- Same pattern with `temperature-group:intermediate` / `intermediate`

### `nepenthes-lowland`

- Same pattern with `temperature-group:lowland` / `lowland`

> Prefer **one** rule style (tags only is simplest for CSV import). Example tag set per product: `genus:nepenthes`, `temperature-group:highland`, `difficulty:2`.

## 3. Product tags (recommended convention)

| Tag | Purpose |
|-----|---------|
| `genus:dionaea` | Genus smart collections & filters |
| `temperature-group:highland` | Nepenthes + Search & Discovery |
| `trap-type:pitfall` | Filters |
| `difficulty:1` | Easy care badge (1–5) |
| `dormancy:yes` | PDP banner + filters |
| `Rare` | Wax seal badge |
| `In-House` | Lab propagated badge |
| `cites:yes` | CITES notice (when implemented on PDP) |

## 4. Search & Discovery filters

**Shopify Admin → Apps → Search & Discovery → Filters**

Enable storefront filters that map to metafields/tags you actually populate:

- Availability  
- Price  
- `custom.genus` or tag-based genus  
- `custom.difficulty`  
- `custom.temperature_group`  
- `custom.trap_type`  
- Dormancy (boolean metafield or tag)

## 5. Collection content (merchant)

For each genus collection:

1. **Image** — hero / card imagery (replace Wikimedia in theme)  
2. **Description** — can use HTML `<ul><li><strong>Light:</strong> …</strong></li>…` for dossier grid on PDP; for full genus care sections see [genus-care-on-collections.md](./genus-care-on-collections.md)

## 6. Verify in theme

- [ ] Mega menu lists in-stock genera (excludes empty collections)  
- [ ] Homepage genus strip shows expected handles  
- [ ] `/collections/nepenthes-highland` (etc.) show correct products  
- [ ] Filters return results on a collection page  
