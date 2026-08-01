import argparse
import csv
import json
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
}


def fetch(url, delay=1.0, timeout=15):
    time.sleep(delay)
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp


def extract_table(soup):
    rows = []
    for tr in soup.select("table tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    return rows


def extract_json_blocks(soup):
    blocks = []
    for script in soup.find_all("script"):
        text = script.string or ""
        text = text.strip()
        if text.startswith(("{", "[")):
            try:
                blocks.append(json.loads(text))
            except json.JSONDecodeError:
                continue
    return blocks


def flatten(item, prefix=""):
    if isinstance(item, dict):
        out = {}
        for k, v in item.items():
            key = f"{prefix}.{k}" if prefix else k
            out.update(flatten(v, key))
        return out
    if isinstance(item, list):
        out = {}
        for i, v in enumerate(item):
            key = f"{prefix}.{i}" if prefix else str(i)
            out.update(flatten(v, key))
        return out
    return {prefix: item}


def to_csv(rows, out):
    records = [flatten(r) for r in rows]
    keys = []
    for r in records:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)
    return len(records)


def main():
    parser = argparse.ArgumentParser(
        description="Scraper: extrae tablas, JSON embebido o APIs y exporta a CSV."
    )
    parser.add_argument("url", help="URL a extraer")
    parser.add_argument("-o", "--output", default="datos.csv", help="Archivo CSV de salida")
    parser.add_argument("--delay", type=float, default=1.0, help="Segundos entre peticiones")
    parser.add_argument("--paginar", action="store_true", help="Seguir enlaces de paginacion")
    args = parser.parse_args()

    rows = []
    resp = fetch(args.url, delay=args.delay)
    content_type = resp.headers.get("Content-Type", "")
    text = resp.text

    if "json" in content_type or text.lstrip().startswith(("[", "{")):
        try:
            data = json.loads(text)
            rows = data if isinstance(data, list) else [data]
        except json.JSONDecodeError:
            pass

    if not rows:
        soup = BeautifulSoup(text, "html.parser")
        rows = extract_table(soup)
        if not rows:
            for block in extract_json_blocks(soup):
                rows.extend(block if isinstance(block, list) else [block])

    if args.paginar:
        soup = BeautifulSoup(text, "html.parser")
        seen = set()
        while True:
            link = None
            for a in soup.select("a"):
                if any(p in a.get_text().lower() for p in ("siguiente", "next", "sig")):
                    link = a
                    break
            if not link:
                break
            url = urljoin(args.url, link.get("href"))
            if url in seen:
                break
            seen.add(url)
            resp = fetch(url, delay=args.delay)
            soup = BeautifulSoup(resp.text, "html.parser")
            more = extract_table(soup)
            rows.extend(more)
            if not more:
                break

    if not rows:
        print("No se encontro ningun dato util en la pagina.", file=sys.stderr)
        sys.exit(1)

    total = to_csv(rows, args.output)
    print(f"OK: {total} registros guardados en {args.output}")


if __name__ == "__main__":
    main()
