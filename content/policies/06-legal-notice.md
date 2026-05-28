# 6. Legal notice

## Shopify Admin steps

1. **Settings → Policies → Legal notice**.
2. Paste the HTML from [`06-legal-notice.html`](./06-legal-notice.html).
3. **Save**.

## Optional mirror page (theme)

1. **Online Store → Pages → Add page**
2. **Title:** Legal notice
3. **Handle:** `legal-notice`
4. **Theme template:** `page.legal-notice`
5. Leave body empty for theme fallback, or paste the same HTML.

Storefront URL: `/policies/legal-notice`

## When you have registration details

Update `06-legal-notice.html` (and re-paste in Admin) with:

- Registered legal entity name (if different from trading name)
- Company registration number (e.g. CK / registration number)
- VAT vendor number (if applicable)

## Verify

- [ ] Admin no longer shows “No policy set” for Legal notice.
- [ ] `/policies/legal-notice` renders with theme styling.
- [ ] All six written policies are complete in Admin.

## Policies checklist (all six)

| Policy | Admin |
|--------|--------|
| Contact information | Form fields + save |
| Return and refund | HTML pasted |
| Shipping | HTML pasted |
| Privacy | HTML pasted (custom, not automated only) |
| Terms of service | HTML pasted |
| Legal notice | HTML pasted |

Optional: **Return rules** under Policies → Return rules (separate from written refund policy).
