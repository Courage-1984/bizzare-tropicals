# Launch TODO tracker

| # | Task | Status |
|---|------|--------|
| 1 | Footer translation missing (terms, legal, contact) | Done |
| 2 | Collections setup guide | Done — [collections-setup-guide.md](./collections-setup-guide.md) |
| 3 | Genus care / collection-hero advice | Done — [genus-care-on-collections.md](./genus-care-on-collections.md) |
| 4 | Four more contact FAQs | Done — `templates/page.contact.json` |
| 5 | Supplies / CITES / care overview advice | Done — [feature-roadmap-advice.md](./feature-roadmap-advice.md) |
| 6a | Skip link, `/cart` → drawer, remove `link_care` | Done |
| 6b | Stubs ignored, settings_schema renamed | Done — [theme-stubs.md](./theme-stubs.md) |
| 7 | Upload errors (locales, policy.liquid, whatsapp_url) | Done |
| 8 | Nepenthes hub + supply chips on collection | Done — `collection-hero` removed from catalog; care on PDP |
| 9 | CITES + pair-with on PDP | Done — `main-product.liquid` + snippets |
| 10 | Care overview page | Done — `templates/page.care-overview.json` |
| 11 | Pretoria address in footer/contact | Done — theme defaults updated |

## Merchant follow-up (Admin)

- [ ] Create page **Care overview** with handle `care-overview` and assign template **care-overview**
- [ ] Paste policies in **Settings → Policies** from `content/policies/`
- [ ] Tag supply SKUs with `supply:soil` etc. or set `custom.supply_category` metafield
- [ ] Set `custom.cites_listed` or tag `cites:yes` on regulated products
- [ ] Add collection descriptions with care `<ul>` bullets for genus pages (see genus-care doc)
