import json
import re
import time
import requests

# Verified filenames per product handle (Commons File: titles)
master_links = {
    "drosera-capensis": [
        "Drosera_capensis_bend.JPG",
        "Drosera capensis (carnivorous-plant-142084).jpg",
        "Drosera capensis leaf.jpg",
        "Drosera capensis 2.jpg",
        "Drosera capensis Luc Viatour.jpg",
    ],
    "nepenthes-edwardsiana": [
        "Nepenthes edwardsiana Macfarlane illustration.jpg",
        "Nepenthes edwardsiana entire ASR 052007 tambu.jpg",
        "Nepenthes edwardsiana ASR 052007 tambu.jpg",
        "N.edwardsiana IP.jpg",
        "Nepenthes edwardsiana - Transactions of the Linnean Society of London (1859).jpg",
    ],
    "nepenthes-burbidgeae": [
        "Nepenthes burbidgeae.jpg",
        "Nepenthes burbidgeae 066.jpg",
        "Pig Hill Kinabalu N. burbidgeae.jpg",
        "Nepenthes burbidgeae.png",
        "Pig Hill Kinabalu N. burbidgeae site two 2.jpg",
    ],
    "nepenthes-bicalcarata": [
        "Nepenthes bicalcarata.jpg",
        "Nepenthesbicalcarata1.jpg",
        "Nepenthes bicalcarata (cultivated1).jpg",
        "Nepenthes bicalcarata Macfarlane illustration.jpg",
        "Nepenthes bicalcarata Kebun Raya Bogor.jpg",
    ],
    "pinguicula-aphrodite": [
        "Pinguicula 'Aphrodite'.jpg",
        "Pinguicula 'Aphrodite' 1.jpg",
        "Pinguicula 'Aphrodite' 2.jpg",
        "Pinguicula 'Aphrodite' flower.jpg",
        "Pinguicula 'Aphrodite' habit.jpg",
    ],
    "heliamphora-minor": [
        "Heliamphora minor Auyan-tepui.jpg",
        "Heliamphora minor2.jpg",
        "Heliamphora minor - Atlanta Botanical Garden.JPG",
        "Heliamphora minor kz01.jpg",
        "Heliamphora minor var minor.jpg",
    ],
    "cephalotus-follicularis": [
        "Cephalotus follicularis 0001.JPG",
        "Cephalotus_follicularis_002.jpg",
        "Cephalotus follicularis 01.jpg",
        "Cephalotus follicularis Hennern 3.jpg",
        "Cephalotus follicularis001.jpg",
    ],
    "utricularia-alpina": [
        "Utricularia alpina.jpg",
        "Utricularia alpina traps Darwiniana.jpg",
        "Utricularia alpina cultivated flower.jpg",
        "Utricularia alpina kz01.jpg",
        "Utricularia alpina flower closeup.jpg",
    ],
    "darlingtonia-californica": [
        "Darlingtonia californica, by Mary Vaux Walcott.jpg",
        "Darlingtonia Macfarlane illustration.jpg",
        "Darlingtonia californica.jpg",
        "Darlingtonia californica 3.jpg",
        "Darlingtonia californica ne1.JPG",
    ],
    "byblis-liniflora": [
        "Byblis liniflora 3 flowering.jpg",
        "ByblisLinifloraFlora.JPG",
        "ByblisLinifloraHabitus.JPG",
        "Byblis liniflora capsule1.JPG",
        "Byblis liniflora capsule2.JPG",
    ],
    "drosophyllum-lusitanicum": [
        "Drosophyllum_lusitanicum_a.JPG",
        "Drosophyllum_lusitanicum_ne.jpg",
        "Drosophyllum lusitanicum kz06.jpg",
        "Drosophyllum lusitanicum kz03.jpg",
        "Drosophyllum lusitanicum kz01.jpg",
    ],
    "sarracenia-flava": [
        "Sarracenia_flava.JPG",
        "Sarracenia flava (19317814192).jpg",
        "Sarracenia flava 2zz.jpg",
        "Sarracenia_flava_001.jpg",
        "Sarraceniaceae Sarracenia flava 3.jpg",
    ],
    "dionaea-muscipula": [
        "01 Venusfliegenfalle.jpg",
        "Dionaea muscipula.jpg",
        "Dionaea muscipula 1.jpg",
        "Dionaea muscipula 001.JPG",
        "Dionaea_muscipula_2.jpg",
    ],
}

# Extra Commons search queries when the handle is a cultivar or needs broader search
SEARCH_QUERIES = {
    "pinguicula-aphrodite": ["Pinguicula Aphrodite", "Pinguicula moranensis"],
    "nepenthes-edwardsiana": ["Nepenthes edwardsiana"],
}

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "BizarreTropicalsBot/10.0 (https://github.com/; local-dev)"}
TARGET_PER_GENUS = 5
REQUEST_PAUSE = 1.25
IMAGE_EXT = re.compile(r"\.(jpe?g|png|gif|webp)$", re.IGNORECASE)
SKIP_IN_TITLE = re.compile(
    r"(distribution|range map|phylogen|cladogram|icon|logo|stamp|currency|"
    r"diagram only|line drawing only)",
    re.IGNORECASE,
)


def log(message=""):
    print(message, flush=True)


def handle_to_binomial(handle):
    parts = handle.split("-", 1)
    genus = parts[0].capitalize()
    epithet = parts[1].replace("-", " ") if len(parts) > 1 else ""
    return f"{genus} {epithet}".strip()


def file_url(filename):
    path = filename.replace(" ", "_")
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{path}?width=1024"


def normalize_name(name):
    return re.sub(r"\s+", " ", name.replace("_", " ")).strip().lower()


class CommonsClient:
    def __init__(self):
        self.session = requests.Session()

    def _get(self, params, retries=5):
        for attempt in range(retries):
            time.sleep(REQUEST_PAUSE)
            response = self.session.get(
                COMMONS_API, params=params, headers=HEADERS, timeout=20
            )
            if response.status_code == 429:
                wait = min(30, 2 ** (attempt + 1))
                log(f"  (rate limited, waiting {wait}s...)")
                time.sleep(wait)
                continue
            response.raise_for_status()
            return response.json()
        response.raise_for_status()

    def search_files(self, query, limit=30):
        data = self._get(
            {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srnamespace": 6,
                "srlimit": limit,
                "format": "json",
            }
        )
        return [hit["title"][5:] for hit in data["query"]["search"]]

    def files_exist(self, filenames):
        if not filenames:
            return set()
        titles = "|".join(f"File:{name}" for name in filenames)
        data = self._get(
            {
                "action": "query",
                "titles": titles,
                "format": "json",
            }
        )
        found = set()
        for page in data.get("query", {}).get("pages", {}).values():
            if page.get("missing") or page.get("invalid"):
                continue
            title = page.get("title", "")
            if title.startswith("File:"):
                found.add(title[5:])
        return found

    def verify_url(self, url):
        try:
            response = self.session.head(
                url, headers=HEADERS, allow_redirects=True, timeout=12
            )
            return response.status_code == 200
        except requests.RequestException:
            return False


def is_relevant(handle, filename):
    genus, epithet = handle.split("-", 1)
    low = filename.lower()
    epithet_spaced = epithet.replace("-", " ")

    if not IMAGE_EXT.search(filename):
        return False
    if SKIP_IN_TITLE.search(filename):
        return False
    if genus not in low:
        return False

    # Cultivar handles: require cultivar name or genus+epithet in title
    if "'" in filename or "aphrodite" in handle:
        if "aphrodite" not in low:
            return False
    elif epithet_spaced not in low and epithet not in low:
        return False

    return True


def discover_for_handle(client, handle, existing_names):
    queries = SEARCH_QUERIES.get(handle, [handle_to_binomial(handle)])
    have = {normalize_name(n) for n in existing_names}
    seen = set()
    candidates = []

    for query in queries:
        try:
            results = client.search_files(query)
        except requests.RequestException as exc:
            log(f"{handle:<25} | SEARCH ERROR   | {query}: {exc}")
            continue

        for name in results:
            if name in seen:
                continue
            seen.add(name)
            if normalize_name(name) in have:
                continue
            if not is_relevant(handle, name):
                continue
            candidates.append(name)

    return candidates


def verify_and_expand():
    client = CommonsClient()
    working_data = {}
    filenames_by_handle = {
        handle: list(files) for handle, files in master_links.items()
    }

    log(f"{'GENUS':<25} | {'STATUS':<15} | {'DETAIL'}")
    log("-" * 75)

    for handle, files in filenames_by_handle.items():
        working_data[handle] = [file_url(f) for f in files]

    short = [h for h in working_data if len(working_data[h]) < TARGET_PER_GENUS]
    log(f"Filling {len(short)} genera to {TARGET_PER_GENUS} images via Commons search...")

    all_ok = True
    for handle in filenames_by_handle:
        names = filenames_by_handle[handle]
        urls = working_data[handle]
        existing_norm = {normalize_name(n) for n in names}

        if len(urls) >= TARGET_PER_GENUS:
            log(f"{handle:<25} | COMPLETE       | {len(urls)}/{TARGET_PER_GENUS}")
            continue

        needed = TARGET_PER_GENUS - len(urls)
        log(f"{handle:<25} | SEARCHING      | need {needed} more...")

        candidates = discover_for_handle(client, handle, names)
        added = 0

        for cand in candidates:
            if added >= needed:
                break
            if normalize_name(cand) in existing_norm:
                continue

            if cand not in client.files_exist([cand]):
                continue

            url = file_url(cand)
            if url in urls:
                continue
            if not client.verify_url(url):
                log(f"{handle:<25} | SKIP (404)     | {cand}")
                continue

            log(f"{handle:<25} | NEW SUCCESS    | {cand}")
            names.append(cand)
            urls.append(url)
            existing_norm.add(normalize_name(cand))
            added += 1
            time.sleep(0.5)

        count = len(urls)
        status = "COMPLETE" if count >= TARGET_PER_GENUS else "INCOMPLETE"
        if count < TARGET_PER_GENUS:
            all_ok = False
        log(f"{handle:<25} | {status:<14} | {count}/{TARGET_PER_GENUS} images")

    filenames_by_handle = {
        h: filenames_by_handle[h] for h in filenames_by_handle
    }
    working_data = {h: [file_url(f) for f in filenames_by_handle[h]] for h in working_data}

    with open("verified_images.json", "w", encoding="utf-8") as f:
        json.dump(working_data, f, indent=4)

    with open("master_links_export.json", "w", encoding="utf-8") as f:
        json.dump(filenames_by_handle, f, indent=4)

    log("-" * 75)
    if all_ok:
        log("DONE. All genera have 5/5 verified images.")
    else:
        log("DONE with gaps. Re-run later or add filenames to master_links.")
    log("Updated: verified_images.json, master_links_export.json")


if __name__ == "__main__":
    verify_and_expand()
