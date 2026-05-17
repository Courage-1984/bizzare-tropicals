#!/usr/bin/env python3
"""
Discover and verify Wikimedia Commons image URLs for Shopify product CSVs.

Patterns from csv_products/original/001.csv and verified batches:
  https://commons.wikimedia.org/wiki/Special:FilePath/{filename}?width=1024
  - Spaces in Commons filenames become underscores in the URL path.
  - Optional ?width=1024 for Shopify-sized thumbs (Special:FilePath scales on the fly).
  - upload.wikimedia.org thumb URLs from imageinfo are the most reliable for verification.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import OrderedDict
from pathlib import Path
from urllib.parse import quote, unquote

import requests

ROOT = Path(__file__).resolve().parent
ORIGINAL_DIR = ROOT / "csv_products" / "original"
MERGED_CSV = ROOT / "csv_products" / "merged_products.csv"
MASTER_LINKS_PATH = ROOT / "master_links_export.json"
VERIFIED_JSON = ROOT / "verified_images.json"
REPORT_JSON = ROOT / "botanical_links_report.json"

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
HEADERS = {
    "User-Agent": "BizarreTropicalsBot/12.0 (https://github.com/Courage-1984/bizzare-tropicals; product-image-audit)"
}

TARGET_IMAGES = 5
REQUEST_PAUSE = 0.35
IMAGE_EXT = re.compile(r"\.(jpe?g|png|gif|webp)$", re.IGNORECASE)
SKIP_IN_TITLE = re.compile(
    r"(distribution|range\s*map|phylogen|cladogram|icon|logo|stamp|currency|"
    r"herbarium\s*sheet|line\s*drawing\s*only|diagram\s*only|map\s*of\s*the)",
    re.IGNORECASE,
)
GENUS_FALLBACK_SKIP = re.compile(
    r"(asteroid|asteroid shape|bouguereau|caunus|caunos|virgil\s+solis|mytholog|"
    r"orbital|overflow|salar jung|lightcurve inversion|biblis|and\s+byblis|"
    r"byblis\s+and|frère|frere|solais)",
    re.IGNORECASE,
)
ALWAYS_SKIP = re.compile(
    r"(caunos|caunus|overflow|asteroid|bouguereau|mytholog|biblis|fontaine|"
    r"changée|changee|btv1b|virgil|solais|frère|frere)",
    re.IGNORECASE,
)
SPECIAL_FILEPATH = re.compile(
    r"commons\.wikimedia\.org/wiki/Special:FilePath/([^?#]+)", re.IGNORECASE
)
UPLOAD_PATH = re.compile(
    r"upload\.wikimedia\.org/wikipedia/commons/(?:thumb/)?[^/]+/[^/]+/(.+?)(?:\?|$)",
    re.IGNORECASE,
)
LATIN_COL = "Latin Name (product.metafields.custom.latin_name)"
IMAGE_COL = "Product image URL"
HANDLE_COL = "URL handle"
POS_COL = "Image position"
CATEGORY_COL = "Product category"
# Shopify Standard Product Taxonomy (2024-10) — "Live Plants" is not a valid node.
SHOPIFY_PRODUCT_CATEGORY = (
    "Home & Garden > Plants > Indoor & Outdoor Plants > Potted Houseplants"
)
INVALID_PRODUCT_CATEGORIES = frozenset(
    {
        "",
        "Plants",
        "Home & Garden > Plants > Live Plants",
    }
)

MERGE_FILE_ORDER = [
    "001.csv",
    "002.csv",
    "003.csv",
    "004.csv",
    "005.csv",
    "006.csv",
]

GENUS_TYPOS: dict[str, tuple[str, ...]] = {
    "heliamphora": ("heliamhora",),
}


def log(message: str = "") -> None:
    try:
        print(message, flush=True)
    except UnicodeEncodeError:
        safe = message.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(
            sys.stdout.encoding or "utf-8", errors="replace"
        )
        print(safe, flush=True)


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.replace("_", " ")).strip().lower()


def compact(name: str) -> str:
    return re.sub(r"[\s_'.()-]+", "", name.lower())


def species_slug(latin: str) -> str:
    tokens = re.findall(r"[A-Za-z]+", latin or "")
    if len(tokens) < 2:
        return ""
    return f"{tokens[0].lower()}-{tokens[1].lower()}"


def taxon_from_product(product: dict) -> tuple[str, str, list[str]]:
    """Return (genus, epithet, extra_match_tokens) from latin name, title, and handle."""
    latin = product.get("latin") or ""
    handle = product["handle"]
    title = product.get("title") or ""

    genus_m = re.match(r"([A-Za-z]+)", latin)
    genus = (genus_m.group(1) if genus_m else handle.split("-")[0]).lower()

    extra: list[str] = []
    epithet = ""

    handle_parts = handle.split("-")
    if len(handle_parts) >= 2:
        epithet = handle_parts[1].lower()
        extra.extend(p.lower() for p in handle_parts[2:] if len(p) > 2)

    base_latin = re.sub(r"\([^)]*\)", "", latin).strip()
    latin_parts = re.findall(r"[a-zA-Z]+", base_latin)
    if len(latin_parts) >= 2 and latin_parts[1].lower() not in ("x", "subsp", "var"):
        if not epithet:
            epithet = latin_parts[1].lower()
        elif latin_parts[1].lower() != epithet:
            extra.append(latin_parts[1].lower())

    cultivar = re.search(r"'([^']+)'", title) or re.search(r"'([^']+)'", latin)
    if cultivar:
        extra.append(cultivar.group(1).lower())
        if not epithet:
            epithet = cultivar.group(1).lower()

    if " x " in latin.lower():
        for side in latin.lower().split(" x "):
            for token in re.findall(r"[a-z]+", side):
                if token != genus and token not in extra:
                    extra.append(token)

    extra = [t for t in extra if t != genus]
    return genus, epithet, extra


def file_url(filename: str, width: int = 1024) -> str:
    path = filename.replace(" ", "_")
    encoded = quote(path, safe="/!'()")
    return (
        f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded}"
        f"?width={width}"
    )


def parse_commons_url(url: str) -> str | None:
    if not url:
        return None
    match = SPECIAL_FILEPATH.search(url)
    if match:
        return unquote(match.group(1)).replace("_", " ")
    match = UPLOAD_PATH.search(url)
    if match:
        name = unquote(match.group(1))
        if "/thumb/" in url or re.search(r"/\d+px-", url):
            name = re.sub(r"/\d+px-", ".", name, count=1)
        return name.replace("_", " ")
    return None


def handle_to_binomial(handle: str) -> str:
    parts = handle.split("-", 1)
    genus = parts[0].capitalize()
    epithet = parts[1].replace("-", " ") if len(parts) > 1 else ""
    return f"{genus} {epithet}".strip()


def _is_genus_plant_image(product: dict, filename: str) -> bool:
    """Genus fallback: another species in the same genus (binomial or CamelCase filename)."""
    if GENUS_FALLBACK_SKIP.search(filename) or ALWAYS_SKIP.search(filename):
        return False
    if SKIP_IN_TITLE.search(filename):
        return False
    genus, _, _ = taxon_from_product(product)
    if not genus_in_filename(genus, filename):
        return False
    if IMAGE_EXT.search(filename):
        binomial = re.search(rf"{genus}[\s_]+[a-z][a-z0-9-]+", filename, re.IGNORECASE)
        camel = re.search(rf"{genus}[A-Z][a-z]+", filename)
        return bool(binomial or camel)
    return False


def genus_in_filename(genus: str, filename: str) -> bool:
    low = filename.lower()
    if genus in low:
        return True
    for typo in GENUS_TYPOS.get(genus, ()):
        if typo in low:
            return True
    return False


def epithet_in_filename(epithet: str, extra: list[str], filename: str) -> bool:
    if not epithet and not extra:
        return True
    low = filename.lower()
    compact_file = compact(filename)
    checks = [epithet] + extra if epithet else extra
    for token in checks:
        if not token:
            continue
        if token in low or token in compact_file:
            return True
    return False


def _read_product_blocks(path: Path) -> list[tuple[str, list[dict[str, str]]]]:
    blocks: list[tuple[str, list[dict[str, str]]]] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        current_handle: str | None = None
        block: list[dict[str, str]] = []
        for row in reader:
            handle = (row.get(HANDLE_COL) or "").strip() or current_handle
            if not handle:
                continue
            if handle != current_handle:
                if current_handle and block:
                    blocks.append((current_handle, block))
                current_handle = handle
                block = []
            block.append({k: (row.get(k) or "") for k in fieldnames})
        if current_handle and block:
            blocks.append((current_handle, block))
    return blocks


def normalize_product_categories(
    rows: list[dict[str, str]], fieldnames: list[str]
) -> int:
    """Set valid Shopify taxonomy on product rows; propagate to same-handle rows."""
    if CATEGORY_COL not in fieldnames:
        return 0
    by_handle: dict[str, str] = {}
    for row in rows:
        handle = (row.get(HANDLE_COL) or "").strip()
        if not handle:
            continue
        cat = (row.get(CATEGORY_COL) or "").strip()
        if cat and cat not in INVALID_PRODUCT_CATEGORIES:
            by_handle[handle] = cat
    changed = 0
    for row in rows:
        handle = (row.get(HANDLE_COL) or "").strip()
        if not handle:
            continue
        current = (row.get(CATEGORY_COL) or "").strip()
        target = by_handle.get(handle, SHOPIFY_PRODUCT_CATEGORY)
        if current in INVALID_PRODUCT_CATEGORIES or (
            (row.get("Title") or "").strip() and current != target
        ):
            if current != target:
                row[CATEGORY_COL] = target
                changed += 1
                by_handle[handle] = target
    return changed


def fix_csv_product_categories(csv_path: Path = MERGED_CSV) -> int:
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    changed = normalize_product_categories(rows, fieldnames)
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    log(f"Normalized {changed} category cells in {csv_path}")
    return changed


def merge_original_csvs(
    source_dir: Path = ORIGINAL_DIR,
    output_path: Path = MERGED_CSV,
) -> Path:
    paths: list[Path] = []
    for name in MERGE_FILE_ORDER:
        candidate = source_dir / name
        if candidate.exists():
            paths.append(candidate)
    for extra in sorted(source_dir.glob("*.csv")):
        if extra not in paths:
            paths.append(extra)

    all_columns: list[str] = []
    seen_columns: set[str] = set()
    blocks_by_handle: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    handle_order: list[str] = []

    for path in paths:
        with path.open(encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames:
                for col in reader.fieldnames:
                    if col not in seen_columns:
                        seen_columns.add(col)
                        all_columns.append(col)
        for handle, block in _read_product_blocks(path):
            if handle not in blocks_by_handle:
                handle_order.append(handle)
            blocks_by_handle[handle] = block

    final_rows: list[dict[str, str]] = []
    for handle in handle_order:
        final_rows.extend(blocks_by_handle[handle])

    normalize_product_categories(final_rows, all_columns)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=all_columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(final_rows)

    log(
        f"Merged {len(paths)} files -> {output_path} "
        f"({len(handle_order)} products, {len(final_rows)} rows)"
    )
    return output_path


def load_products_from_csv(csv_path: Path) -> dict[str, dict]:
    products: dict[str, dict] = {}
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            handle = (row.get(HANDLE_COL) or "").strip()
            if not handle:
                continue
            if handle not in products:
                products[handle] = {
                    "handle": handle,
                    "title": (row.get("Title") or "").strip(),
                    "latin": (row.get(LATIN_COL) or "").strip(),
                    "urls": [],
                    "filenames": [],
                }
            latin = (row.get(LATIN_COL) or "").strip()
            if latin:
                products[handle]["latin"] = latin
            title = (row.get("Title") or "").strip()
            if title:
                products[handle]["title"] = title
            img_url = (row.get(IMAGE_COL) or "").strip()
            if img_url and img_url not in products[handle]["urls"]:
                products[handle]["urls"].append(img_url)
                fn = parse_commons_url(img_url)
                if fn:
                    products[handle]["filenames"].append(fn)
    return products


def load_master_links(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _has_suspicious_filenames(filenames: list[str]) -> bool:
    return any(ALWAYS_SKIP.search(f) for f in filenames)


def load_results_cache() -> dict[str, dict]:
    """Load prior filenames/urls per handle from report + verified JSON."""
    cache: dict[str, dict] = {}
    if REPORT_JSON.exists():
        with REPORT_JSON.open(encoding="utf-8") as fh:
            report = json.load(fh)
        for handle, data in report.get("results", {}).items():
            filenames = list(data.get("filenames") or [])
            urls = list(data.get("urls") or [])
            if filenames and urls:
                cache[handle] = {
                    "filenames": filenames,
                    "urls": urls,
                    "verified_thumb_urls": data.get("verified_thumb_urls") or [],
                }
            elif filenames:
                cache[handle] = {
                    "filenames": filenames,
                    "urls": [file_url(f) for f in filenames],
                    "verified_thumb_urls": [],
                }

    if VERIFIED_JSON.exists():
        with VERIFIED_JSON.open(encoding="utf-8") as fh:
            verified = json.load(fh)
        for handle, urls in verified.items():
            if (
                handle in cache
                and len(cache[handle].get("filenames", [])) >= TARGET_IMAGES
            ):
                continue
            filenames = [parse_commons_url(u) for u in urls]
            filenames = [f for f in filenames if f]
            if len(filenames) >= TARGET_IMAGES:
                cache[handle] = {
                    "filenames": filenames[:TARGET_IMAGES],
                    "urls": urls[:TARGET_IMAGES],
                    "verified_thumb_urls": [],
                }
    return cache


class CommonsClient:
    def __init__(self, pause: float = REQUEST_PAUSE):
        self.session = requests.Session()
        self.pause = pause
        self._exist_cache: dict[str, bool] = {}
        self._info_cache: dict[str, dict] = {}

    def _get(self, url: str, params: dict, retries: int = 5) -> dict:
        for attempt in range(retries):
            time.sleep(self.pause)
            response = self.session.get(url, params=params, headers=HEADERS, timeout=25)
            if response.status_code == 429:
                wait = min(45, 2 ** (attempt + 2))
                log(f"  (rate limited, waiting {wait}s...)")
                time.sleep(wait)
                continue
            response.raise_for_status()
            return response.json()
        response.raise_for_status()
        return {}

    def search_images(self, query: str, limit: int = 40) -> list[dict]:
        data = self._get(
            COMMONS_API,
            {
                "action": "query",
                "generator": "search",
                "gsrsearch": f"{query} filetype:bitmap",
                "gsrnamespace": 6,
                "gsrlimit": limit,
                "prop": "imageinfo",
                "iiprop": "url|thumburl|mime|size|extmetadata",
                "iiurlwidth": 1024,
                "format": "json",
            },
        )
        results = []
        for page in data.get("query", {}).get("pages", {}).values():
            title = page.get("title", "")
            if not title.startswith("File:"):
                continue
            info = (page.get("imageinfo") or [{}])[0]
            if not info.get("thumburl") and not info.get("url"):
                continue
            results.append(
                {
                    "filename": title[5:],
                    "thumburl": info.get("thumburl") or info.get("url"),
                    "url": info.get("url"),
                    "size": info.get("size") or 0,
                }
            )
        return results

    def category_files(self, category: str, limit: int = 50) -> list[dict]:
        data = self._get(
            COMMONS_API,
            {
                "action": "query",
                "generator": "categorymembers",
                "gcmtitle": f"Category:{category}",
                "gcmtype": "file",
                "gcmlimit": limit,
                "prop": "imageinfo",
                "iiprop": "url|thumburl|mime|size",
                "iiurlwidth": 1024,
                "format": "json",
            },
        )
        results = []
        for page in data.get("query", {}).get("pages", {}).values():
            title = page.get("title", "")
            if not title.startswith("File:"):
                continue
            info = (page.get("imageinfo") or [{}])[0]
            results.append(
                {
                    "filename": title[5:],
                    "thumburl": info.get("thumburl") or info.get("url"),
                    "url": info.get("url"),
                    "size": info.get("size") or 0,
                }
            )
        return results

    def files_exist(self, filenames: list[str]) -> set[str]:
        unknown = [f for f in filenames if f not in self._exist_cache]
        for i in range(0, len(unknown), 50):
            chunk = unknown[i : i + 50]
            if not chunk:
                continue
            titles = "|".join(f"File:{name}" for name in chunk)
            data = self._get(
                COMMONS_API,
                {"action": "query", "titles": titles, "format": "json"},
            )
            found = set()
            for page in data.get("query", {}).get("pages", {}).values():
                if page.get("missing") or page.get("invalid"):
                    continue
                title = page.get("title", "")
                if title.startswith("File:"):
                    found.add(title[5:])
            for name in chunk:
                self._exist_cache[name] = name in found
        return {name for name in filenames if self._exist_cache.get(name)}

    def imageinfo_for_files(self, filenames: list[str]) -> dict[str, dict]:
        unknown = [f for f in filenames if f not in self._info_cache]
        for i in range(0, len(unknown), 50):
            chunk = unknown[i : i + 50]
            if not chunk:
                continue
            titles = "|".join(f"File:{n}" for n in chunk)
            data = self._get(
                COMMONS_API,
                {
                    "action": "query",
                    "titles": titles,
                    "prop": "imageinfo",
                    "iiprop": "url|thumburl|mime|size",
                    "iiurlwidth": 1024,
                    "format": "json",
                },
            )
            for page in data.get("query", {}).get("pages", {}).values():
                if page.get("missing"):
                    continue
                title = page.get("title", "")
                if title.startswith("File:"):
                    info = (page.get("imageinfo") or [{}])[0]
                    self._info_cache[title[5:]] = info
        return {
            name: self._info_cache[name]
            for name in filenames
            if name in self._info_cache
        }

    def wikidata_commons_files(self, latin: str, limit: int = 10) -> list[str]:
        search = self._get(
            WIKIDATA_API,
            {
                "action": "wbsearchentities",
                "search": latin,
                "language": "en",
                "type": "item",
                "limit": 3,
                "format": "json",
            },
        )
        entity_ids = [
            item.get("id") for item in search.get("search", []) if item.get("id")
        ]
        if not entity_ids:
            return []

        claims = self._get(
            WIKIDATA_API,
            {
                "action": "wbgetentities",
                "ids": "|".join(entity_ids[:2]),
                "props": "claims",
                "format": "json",
            },
        )
        filenames: list[str] = []
        for ent in claims.get("entities", {}).values():
            for claim in ent.get("claims", {}).get("P18", []):
                mainsnak = claim.get("mainsnak", {})
                if mainsnak.get("snaktype") != "value":
                    continue
                value = mainsnak.get("datavalue", {}).get("value", "")
                if value:
                    filenames.append(value)
            if len(filenames) >= limit:
                break
        return filenames[:limit]


def build_search_queries(product: dict) -> list[str]:
    latin = product.get("latin") or ""
    handle = product["handle"]
    queries: list[str] = []
    genus, epithet, extra = taxon_from_product(product)

    if latin:
        queries.append(latin)
        base = re.sub(r"\([^)]*\)", "", latin).strip()
        if base and base != latin:
            queries.append(base)
        if " x " in latin.lower():
            queries.append(latin.split(" x ")[0].strip())
    if genus and epithet:
        queries.append(f"{genus.capitalize()} {epithet}")
    queries.append(handle_to_binomial(handle))

    title = product.get("title") or ""
    cultivar = re.search(r"'([^']+)'", title)
    if cultivar:
        queries.append(f"{genus.capitalize()} '{cultivar.group(1)}'")

    seen: set[str] = set()
    unique: list[str] = []
    for q in queries:
        q = q.strip()
        if q and q.lower() not in seen:
            seen.add(q.lower())
            unique.append(q)
    return unique


def is_relevant(
    product: dict,
    filename: str,
    *,
    strict: bool = True,
    genus_only: bool = False,
) -> bool:
    if not IMAGE_EXT.search(filename):
        return False
    if SKIP_IN_TITLE.search(filename) or ALWAYS_SKIP.search(filename):
        return False
    if genus_only and GENUS_FALLBACK_SKIP.search(filename):
        return False

    genus, epithet, extra = taxon_from_product(product)
    if not genus_in_filename(genus, filename):
        return False

    if genus_only:
        return _is_genus_plant_image(product, filename)

    return epithet_in_filename(epithet, extra, filename)


def discover_candidates(
    client: CommonsClient,
    product: dict,
    existing: set[str],
    *,
    strict: bool = True,
    genus_only: bool = False,
) -> list[dict]:
    have = {normalize_name(n) for n in existing}
    seen_files: set[str] = set()
    candidates: list[dict] = []

    def add_entry(entry: dict) -> None:
        fn = entry["filename"]
        key = normalize_name(fn)
        if key in have or key in seen_files:
            return
        if not is_relevant(product, fn, strict=strict, genus_only=genus_only):
            return
        seen_files.add(key)
        candidates.append(entry)

    latin = product.get("latin", "")
    if not genus_only:
        for fn in client.wikidata_commons_files(latin):
            add_entry({"filename": fn, "thumburl": None, "url": None, "size": 0})

        if latin:
            parts = re.findall(r"[A-Za-z]+", re.sub(r"\([^)]*\)", "", latin))
            cats = [latin]
            if len(parts) >= 2:
                cats.append(f"{parts[0]} {parts[1]}")
            for cat in cats:
                try:
                    for entry in client.category_files(cat, limit=30):
                        add_entry(entry)
                except requests.RequestException:
                    pass

    queries = build_search_queries(product)
    if genus_only:
        genus, _, _ = taxon_from_product(product)
        g = genus.capitalize()
        queries = [f"{g} carnivorous plant", f"{g} plant", g]

    for query in queries:
        try:
            for entry in client.search_images(query, limit=40):
                add_entry(entry)
        except requests.RequestException as exc:
            log(f"  search error ({query}): {exc}")

    candidates.sort(key=lambda e: e.get("size") or 0, reverse=True)
    return candidates


def url_from_imageinfo(info: dict | None, filename: str) -> str | None:
    """Trust Commons imageinfo thumb/url (no HTTP HEAD)."""
    if not info:
        return None
    return info.get("thumburl") or info.get("url") or file_url(filename)


def process_product(
    client: CommonsClient,
    product: dict,
    seed_filenames: list[str],
    cached: dict | None = None,
    *,
    verify_http: bool = False,
) -> tuple[list[str], list[str], bool]:
    """
    Return (filenames, thumb_urls, used_genus_fallback).
    Starts from cache; only discovers missing slots.
    """
    names: list[str] = []
    urls: list[str] = []
    norm_seen: set[str] = set()
    used_genus_fallback = False

    if cached:
        for fn, shop_url in zip(
            cached.get("filenames", [])[:TARGET_IMAGES],
            cached.get("urls", [])[:TARGET_IMAGES],
        ):
            names.append(fn)
            urls.append(shop_url)
            norm_seen.add(normalize_name(fn))

    def try_add(
        filename: str, prefer_url: str | None = None, info: dict | None = None
    ) -> bool:
        if len(names) >= TARGET_IMAGES:
            return False
        key = normalize_name(filename)
        if key in norm_seen:
            return False
        if filename not in client.files_exist([filename]):
            return False
        if not info:
            info = client.imageinfo_for_files([filename]).get(filename)
        if not info and not prefer_url:
            return False
        thumb = prefer_url or url_from_imageinfo(info, filename)
        if not thumb:
            return False
        if verify_http:
            try:
                r = client.session.head(
                    thumb, headers=HEADERS, allow_redirects=True, timeout=10
                )
                if r.status_code != 200:
                    return False
            except requests.RequestException:
                return False
        names.append(filename)
        urls.append(file_url(filename))
        norm_seen.add(key)
        return True

    if len(names) >= TARGET_IMAGES:
        return names[:TARGET_IMAGES], urls[:TARGET_IMAGES], used_genus_fallback

    needed = TARGET_IMAGES - len(names)
    raw_seeds = list(dict.fromkeys(seed_filenames + product.get("filenames", [])))
    all_seeds = [
        f
        for f in raw_seeds
        if normalize_name(f) not in norm_seen and is_relevant(product, f, strict=False)
    ]
    if all_seeds:
        info_batch = client.imageinfo_for_files(all_seeds)
        for fn in all_seeds:
            if len(names) >= TARGET_IMAGES:
                break
            if try_add(fn, info=info_batch.get(fn)):
                log(f"  + seed OK: {fn}")
            else:
                log(f"  - seed fail: {fn}")

    if len(names) >= TARGET_IMAGES:
        return names[:TARGET_IMAGES], urls[:TARGET_IMAGES], used_genus_fallback

    existing = set(names)

    for strict, genus_only in ((True, False), (False, False), (False, True)):
        if len(names) >= TARGET_IMAGES:
            break
        if genus_only:
            used_genus_fallback = True
            log("  ~ genus-level fallback (few species images on Commons)...")
        for entry in discover_candidates(
            client, product, existing, strict=strict, genus_only=genus_only
        ):
            if len(names) >= TARGET_IMAGES:
                break
            fn = entry["filename"]
            if try_add(fn, prefer_url=entry.get("thumburl")):
                log(f"  + found: {fn}")
                existing.add(fn)
            time.sleep(0.15)

    return names[:TARGET_IMAGES], urls[:TARGET_IMAGES], used_genus_fallback


def update_csv_images(csv_path: Path, results: dict[str, dict]) -> None:
    rows: list[dict[str, str]] = []
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        for row in reader:
            handle = (row.get(HANDLE_COL) or "").strip()
            if handle in results:
                pos = (row.get(POS_COL) or "").strip()
                try:
                    idx = int(float(pos)) - 1
                except (ValueError, TypeError):
                    idx = -1
                urls = results[handle].get("urls", [])
                if 0 <= idx < len(urls):
                    row[IMAGE_COL] = urls[idx]
                elif idx >= TARGET_IMAGES:
                    row[IMAGE_COL] = ""
            rows.append(row)

    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run_audit(
    csv_path: Path,
    limit: int | None = None,
    skip_merge: bool = False,
    only_incomplete: bool = False,
    force: bool = False,
    handles_filter: list[str] | None = None,
) -> int:
    if not skip_merge:
        merge_original_csvs()
    else:
        fix_csv_product_categories(csv_path)

    master = load_master_links(MASTER_LINKS_PATH)
    products = load_products_from_csv(csv_path)
    cache = load_results_cache()
    handles = sorted(products.keys())

    if handles_filter:
        wanted = {h.strip() for h in handles_filter if h.strip()}
        handles = [h for h in handles if h in wanted]
        log(f"Filter handles: {len(handles)} products")
    elif only_incomplete:
        incomplete_handles: set[str] = set()
        if REPORT_JSON.exists():
            with REPORT_JSON.open(encoding="utf-8") as fh:
                rep = json.load(fh)
            incomplete_handles = set(rep.get("incomplete", []))
            for h, data in rep.get("results", {}).items():
                if len(data.get("filenames", [])) < TARGET_IMAGES:
                    incomplete_handles.add(h)
                elif data.get("genus_fallback") or _has_suspicious_filenames(
                    data.get("filenames", [])
                ):
                    incomplete_handles.add(h)
        for h in products:
            if len(cache.get(h, {}).get("filenames", [])) < TARGET_IMAGES:
                incomplete_handles.add(h)
        handles = [h for h in handles if h in incomplete_handles]
        log(f"Only incomplete: {len(handles)} products to process")

    if limit:
        handles = handles[:limit]

    client = CommonsClient()
    results: dict[str, dict] = dict(cache)
    incomplete: list[str] = []
    skipped = 0

    log(f"\n{'HANDLE':<40} | {'STATUS':<12} | DETAIL")
    log("-" * 90)

    for handle in sorted(products.keys()):
        product = products[handle]
        if handle not in handles:
            if len(cache.get(handle, {}).get("filenames", [])) >= TARGET_IMAGES:
                skipped += 1
            continue

        prior = cache.get(handle, {})
        if (
            not force
            and len(prior.get("filenames", [])) >= TARGET_IMAGES
            and len(prior.get("urls", [])) >= TARGET_IMAGES
        ):
            log(f"{handle:<40} | SKIP (cached) | {TARGET_IMAGES}/{TARGET_IMAGES}")
            results[handle] = {
                "latin": product.get("latin"),
                "filenames": prior["filenames"][:TARGET_IMAGES],
                "urls": prior["urls"][:TARGET_IMAGES],
                "verified_thumb_urls": prior.get("verified_thumb_urls", []),
                "genus_fallback": prior.get("genus_fallback", False),
            }
            continue

        slug = species_slug(product.get("latin", ""))
        seeds = list(master.get(slug, []))
        if not seeds:
            for key, files in master.items():
                if key in handle or handle.startswith(key):
                    seeds = list(files)
                    break

        log(f"\n{handle} ({product.get('latin', '')})")
        names, shop_urls, genus_fallback = process_product(
            client,
            product,
            seeds,
            cached=prior if not force else None,
            verify_http=False,
        )
        count = len(names)
        status = "COMPLETE" if count >= TARGET_IMAGES else "INCOMPLETE"
        if count < TARGET_IMAGES:
            incomplete.append(handle)
        note = " (genus fallback)" if genus_fallback and count >= TARGET_IMAGES else ""
        log(f"{handle:<40} | {status:<12} | {count}/{TARGET_IMAGES}{note}")
        results[handle] = {
            "latin": product.get("latin"),
            "filenames": names,
            "urls": shop_urls,
            "verified_thumb_urls": [],
            "genus_fallback": genus_fallback or count < TARGET_IMAGES,
        }

    for handle in sorted(products.keys()):
        if handle not in results:
            prior = cache.get(handle, {})
            if prior:
                results[handle] = {
                    "latin": products[handle].get("latin"),
                    "filenames": prior.get("filenames", []),
                    "urls": prior.get("urls", []),
                    "verified_thumb_urls": prior.get("verified_thumb_urls", []),
                    "genus_fallback": prior.get("genus_fallback", False),
                }
                if len(prior.get("filenames", [])) < TARGET_IMAGES:
                    incomplete.append(handle)

    incomplete = sorted(set(incomplete))
    complete = sum(
        1
        for h in products
        if len(results.get(h, {}).get("filenames", [])) >= TARGET_IMAGES
    )

    verified = {h: r["urls"] for h, r in results.items() if r.get("urls")}
    with VERIFIED_JSON.open("w", encoding="utf-8") as fh:
        json.dump(verified, fh, indent=2)

    export: dict[str, list[str]] = {}
    for h, r in results.items():
        key = species_slug(r.get("latin") or "") or h
        if key not in export or len(r.get("filenames", [])) > len(export.get(key, [])):
            export[key] = r.get("filenames", [])
    with MASTER_LINKS_PATH.open("w", encoding="utf-8") as fh:
        json.dump(export, fh, indent=2)

    report = {
        "total": len(products),
        "complete": complete,
        "incomplete": [
            h
            for h in products
            if len(results.get(h, {}).get("filenames", [])) < TARGET_IMAGES
        ],
        "skipped_cached": skipped,
        "results": results,
    }
    with REPORT_JSON.open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    update_csv_images(csv_path, results)

    log("-" * 90)
    log(
        f"DONE: {report['complete']}/{report['total']} products at {TARGET_IMAGES}/{TARGET_IMAGES} images "
        f"({skipped} skipped from cache)."
    )
    if report["incomplete"]:
        log(f"Still incomplete: {', '.join(report['incomplete'])}")
    log(
        f"Wrote: {VERIFIED_JSON.name}, {MASTER_LINKS_PATH.name}, {REPORT_JSON.name}, updated CSV"
    )
    return 0 if not report["incomplete"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify and discover Commons images for products."
    )
    parser.add_argument(
        "--csv", type=Path, default=MERGED_CSV, help="Merged product CSV path"
    )
    parser.add_argument(
        "--merge-only", action="store_true", help="Only merge original CSVs"
    )
    parser.add_argument(
        "--fix-categories",
        action="store_true",
        help="Normalize Product category to Shopify taxonomy in --csv",
    )
    parser.add_argument("--skip-merge", action="store_true", help="Skip merge step")
    parser.add_argument(
        "--limit", type=int, default=None, help="Process first N handles only"
    )
    parser.add_argument(
        "--only-incomplete",
        action="store_true",
        help="Only process products missing 5/5 images",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-process all products even if cache has 5/5",
    )
    parser.add_argument(
        "--handles",
        type=str,
        default=None,
        help="Comma-separated URL handles to process (implies --force for those)",
    )
    args = parser.parse_args()

    if args.fix_categories:
        fix_csv_product_categories(args.csv)
        return 0
    if args.merge_only:
        merge_original_csvs()
        return 0
    handles_filter = None
    if args.handles:
        handles_filter = [h.strip() for h in args.handles.split(",") if h.strip()]
    return run_audit(
        args.csv,
        limit=args.limit,
        skip_merge=args.skip_merge,
        only_incomplete=args.only_incomplete,
        force=args.force or bool(handles_filter),
        handles_filter=handles_filter,
    )


if __name__ == "__main__":
    sys.exit(main())
