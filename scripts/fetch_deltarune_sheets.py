"""Download the Deltarune sprite sheets that the character GIFs are built from.

Sources and credits live in docs/deltarune-assets.md. This fetches the raw
full sheets from The Spriters Resource into a local (gitignored) folder so the
media can be rebuilt from the original web resources.

    python3 scripts/fetch_deltarune_sheets.py

The Spriters Resource stores each sheet under a sharded path that is not
derivable from the asset id, so we scrape the asset page for the real image
URL rather than guessing it.
"""

from __future__ import annotations

import argparse
import re
import urllib.request
from pathlib import Path

# character -> Spriters Resource asset id (see docs/deltarune-assets.md)
ASSETS = {
    'kris': 110448,
    'lancer': 110484,
    'ralsei': 110469,
    'noelle': 110612,
    'susie': 110471,
    'spamton': 162176,
    'jevil': 110456,
    'tenna': 273063,
}

# Animated previews the build reuses for characters that have no walk cycle on
# their static sheet. source filename -> (asset id, preview gif number).
PREVIEW_GIFS = {
    'jevil-dance.gif': (110456, 2131),   # 8-frame bounce
    'spamton-walk.gif': (162176, 5182),  # 4-frame march
    'spamton-laugh.gif': (162176, 5183),  # laugh / glitch
    'spamton-glitch.gif': (162176, 5181),
}

BASE = 'https://www.spriters-resource.com'
ASSET_PAGE = BASE + '/pc_computer/deltarune/asset/{id}/'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'


def _get(url: str, referer: str = BASE) -> bytes:
    request = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': referer})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def _asset_html(asset_id: int) -> str:
    return _get(ASSET_PAGE.format(id=asset_id)).decode('utf-8', 'replace')


def sheet_url(asset_id: int, html: str) -> str:
    match = re.search(rf'/media/assets/\d+/{asset_id}\.png', html)
    if not match:
        raise RuntimeError(f'No sheet image for asset {asset_id}')
    return BASE + match.group(0)


def preview_url(asset_id: int, number: int, html: str) -> str:
    match = re.search(rf'/media/gifs/\d+/{asset_id}-{number}\.gif', html)
    if not match:
        raise RuntimeError(f'No preview gif {asset_id}-{number}')
    return BASE + match.group(0)


def fetch(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    html_cache: dict[int, str] = {}
    for name, asset_id in ASSETS.items():
        html = html_cache.setdefault(asset_id, _asset_html(asset_id))
        url = sheet_url(asset_id, html)
        data = _get(url, referer=ASSET_PAGE.format(id=asset_id))
        (out_dir / f'{name}.png').write_bytes(data)
        print(f'{name}.png: {len(data):>8} bytes  <- {url}')
    for filename, (asset_id, number) in PREVIEW_GIFS.items():
        html = html_cache.setdefault(asset_id, _asset_html(asset_id))
        url = preview_url(asset_id, number, html)
        data = _get(url, referer=ASSET_PAGE.format(id=asset_id))
        (out_dir / filename).write_bytes(data)
        print(f'{filename}: {len(data):>8} bytes  <- {url}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=Path('tmp/deltarune-sources'))
    fetch(parser.parse_args().out_dir)


if __name__ == '__main__':
    main()
