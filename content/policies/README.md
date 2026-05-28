# Store policies — setup guide

Policies are configured in **Shopify Admin → Settings → Policies** (checkout footer + `/policies/…` URLs). This folder holds **source copy** to paste into Admin. The theme mirrors copy on `templates/page.*.json` (section `default_body`); native `/policies/*` pages use `templates/policy.liquid`.

Work through policies **in order** below. After each one, open the live URL and confirm styling via `templates/policy.liquid` (native policies) or `page.*.json` mirror pages.

**Note:** Full policy HTML is **not** stored in `locales/en.default.json` (Shopify string length limit). Paste from `content/policies/*.html` into Admin, or use theme `default_body` on mirror page templates.

| # | Policy (Admin) | Admin path | Storefront URL | Theme fallback |
|---|----------------|------------|----------------|----------------|
| 1 | Contact information | Policies → Contact information | `/policies/contact-information` | `01-contact-information.md` |
| 2 | Return and refund policy | Policies → Return and refund policy | `/policies/refund-policy` | `02-return-and-refund-policy.html` · `page.refund.json` |
| 3 | Shipping policy | Policies → Shipping policy | `/policies/shipping-policy` | `03-shipping-policy.html` · `page.shipping.json` |
| 4 | Privacy policy | Policies → Privacy policy | `/policies/privacy-policy` | `04-privacy-policy.html` · `page.privacy.json` |
| 5 | Terms of service | Policies → Terms of service | `/policies/terms-of-service` | `05-terms-of-service.html` · `page.terms.json` |
| 6 | Legal notice | Policies → Legal notice | `/policies/legal-notice` | `06-legal-notice.html` · `page.legal-notice.json` |
| — | Return rules (optional) | Policies → Return rules → Manage | Checkout returns | Not theme-managed |

**Optional mirror pages** (same copy, custom URL): create Pages with handles in the table in [admin-checklist.md](../.cursor/context/admin-checklist.md) and assign template suffixes `privacy`, `refund`, `shipping`, `terms`, `legal-notice`.

**Contact (canonical):** `info@bizarretropicals.co.za` · `+27 72 152 7446` · WhatsApp `https://wa.me/27721527446`
