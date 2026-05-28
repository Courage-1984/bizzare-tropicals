# 5. Terms of service

## Shopify Admin steps

1. **Settings → Policies → Terms of service**.
2. Paste the HTML from [`05-terms-of-service.html`](./05-terms-of-service.html).
3. **Save**.

## Optional mirror page (theme)

1. **Online Store → Pages → Add page**
2. **Title:** Terms of service
3. **Handle:** `terms-of-service`
4. **Theme template:** `page.terms`
5. Leave body empty for theme fallback, or paste the same HTML.

Storefront URL: `/policies/terms-of-service`

## Related policies

Ensure these are also published in Admin (same `content/policies/` folder):

- Privacy policy → links back to these Terms
- Shipping policy
- Return and refund policy

## Verify

- [ ] Admin no longer shows “No policy set” for Terms of service.
- [ ] `/policies/terms-of-service` renders with theme styling.
- [ ] Privacy policy “Terms of Service” link resolves correctly.
