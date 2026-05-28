# 4. Privacy policy

Your Admin currently shows **Automated** for Privacy policy (Shopify-generated). For a policy tailored to Bizarre Tropicals and POPIA, switch to your custom copy below.

## Shopify Admin steps

1. **Settings → Policies → Privacy policy**.
2. If you see **Automated**, choose to **edit** or **replace** the automated policy (wording varies; look for *Edit*, *Customize*, or *Create from template*).
3. Paste the HTML from [`04-privacy-policy.html`](./04-privacy-policy.html) (merged Shopify template + POPIA + Bizarre Tropicals contact details; last updated May 28, 2026).
4. **Save** — status should show as a custom/written policy (not only “Automated”).

> **Note:** Shopify may still offer automated updates or suggestions. After pasting custom copy, review any Admin prompts so your published policy is the version you intend.

## Optional mirror page (theme)

1. **Online Store → Pages → Add page**
2. **Title:** Privacy policy
3. **Handle:** `privacy-policy`
4. **Theme template:** `page.privacy`
5. Leave body empty for theme fallback, or paste the same HTML.

Footer “Privacy” prefers `/pages/privacy-policy` if that page exists; otherwise `/policies/privacy-policy` when the Admin policy is set.

## Verify

- [ ] `/policies/privacy-policy` shows your custom copy (not generic Shopify-only text).
- [ ] Footer privacy link works.
- [ ] Cookie banner / Customer privacy settings in Admin align with what you describe (Shopify **Settings → Customer privacy**).
