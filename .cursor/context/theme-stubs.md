# Theme stubs — do not use in templates

These files remain in the repo for reference but are **excluded from Shopify CLI push** via `.shopifyignore`. Live storefront uses the `main-*` and branded sections instead.

| File | Replacement |
|------|-------------|
| `sections/homepage-hero.liquid` | `home-slider.liquid` |
| `sections/collection.liquid` | `main-collection-product-grid.liquid` |
| `sections/product.liquid` | `main-product.liquid` |
| `sections/404.liquid` | `main-404.liquid` |
| `sections/cart.liquid` | `main-cart-page.liquid` + cart drawer |
| `sections/hello-world.liquid` | — (remove from theme editor if present) |
| `sections/custom-section.liquid` | — |

**Kept for future use (not ignored):**

| File | Notes |
|------|--------|
| `sections/collection-hero.liquid` | Unused on catalog; PDP uses `snippets/product-care-dossier.liquid` instead |
| `sections/blog.liquid`, `article.liquid` | Starter layouts; blog hidden from nav until restyled |

**Blog / care link:** `footer.link_care` removed from locales. No blog in main menu. Add care overview page when `page.care-overview` exists.
