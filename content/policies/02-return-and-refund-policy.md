# 2. Return and refund policy

## Shopify Admin steps

1. **Settings → Policies → Return and refund policy**.
2. Open the policy editor and **paste the HTML** from [`02-return-and-refund-policy.html`](./02-return-and-refund-policy.html) (or use Shopify’s template and merge the bullet points below).
3. **Save**.

## Optional mirror page (theme)

For a branded URL at `/pages/refund-policy`:

1. **Online Store → Pages → Add page**
2. **Title:** Return and refund policy  
3. **Handle:** `refund-policy`  
4. **Theme template:** `page.refund`  
5. Leave body **empty** to use theme fallback copy, or paste the same HTML as Admin.

Footer “Refund policy” links to `/policies/refund-policy` when this Admin policy is set.

## Return rules (optional)

**Settings → Policies → Return rules → Manage** is separate from this written policy. For live plants, many merchants leave Return rules **off** and handle cases manually via this refund policy. Enable Return rules only if you want self-serve returns in checkout for eligible SKUs (e.g. unopened supplies).

## Verify

- [ ] Admin no longer shows “No policy set” for Return and refund policy.
- [ ] `https://[store].myshopify.com/policies/refund-policy` shows themed layout and correct copy.
- [ ] Footer refund link resolves to the same URL.
