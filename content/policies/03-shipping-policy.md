# 3. Shipping policy

## Shopify Admin steps

1. **Settings → Policies → Shipping policy**.
2. Paste the HTML from [`03-shipping-policy.html`](./03-shipping-policy.html).
3. **Save**.

Also confirm **Settings → Shipping and delivery** has your live rates and zones configured for South Africa (this policy describes how you ship; rates come from shipping settings).

## Optional mirror page (theme)

1. **Online Store → Pages → Add page**
2. **Title:** Shipping policy (or *Shipping & live plant care*)
3. **Handle:** `shipping-policy`
4. **Theme template:** `page.shipping`
5. Leave body empty for theme fallback, or paste the same HTML.

Footer “Shipping” links to `/policies/shipping-policy` when this Admin policy is set.

## Verify

- [ ] Admin no longer shows “No policy set” for Shipping policy.
- [ ] `/policies/shipping-policy` shows themed layout and correct copy.
- [ ] Footer shipping link resolves to the same URL.
- [ ] Checkout shipping rates match what customers expect from this policy.
