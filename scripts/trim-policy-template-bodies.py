#!/usr/bin/env python3
"""Shorten default_body in page.* policy JSON templates (Admin is source of truth)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHORT = (
    "<p>Full policy text belongs in <strong>Settings → Policies</strong> in Shopify Admin. "
    "Paste from <code>content/policies/</code> in the theme repository.</p>"
)

for name in ("privacy", "terms", "legal-notice"):
    path = ROOT / "templates" / f"page.{name}.json"
    if not path.exists():
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    for section in data.get("sections", {}).values():
        if "default_body" in section.get("settings", {}):
            section["settings"]["default_body"] = SHORT
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("trimmed", path.name)
