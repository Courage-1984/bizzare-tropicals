#!/usr/bin/env python3
"""Remove oversized policies.*_body keys from locales/en.default.json."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALE = ROOT / "locales" / "en.default.json"

text = LOCALE.read_text(encoding="utf-8")
header_m = re.match(r"(/\*.*?\*/\s*)", text, re.S)
header = header_m.group(1) if header_m else ""
body = text[header_m.end() :] if header_m else text
body = re.sub(
    r'\n  "policies": \{.*?\n  \},\n  "search":',
    '\n  "search":',
    body,
    count=1,
    flags=re.S,
)
data = json.loads(body)
data.pop("policies", None)
data.setdefault("sections", {}).setdefault("main_policy_page", {})[
    "admin_fallback_hint"
] = (
    "Paste this policy in Shopify Admin under Settings > Policies. "
    "Source HTML is in the theme repo under content/policies/."
)
LOCALE.write_text(
    header + json.dumps(data, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print("Wrote", LOCALE, "- policies removed:", "policies" not in data)
