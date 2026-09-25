from __future__ import annotations

import io
import pathlib
import time
import urllib.request
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]

ASSETS = [
    ('image/pass-13.webp', 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/42bd81a4-abb1-4de4-bfc6-ea9fba2ffc23/%EB%AA%A8%ED%97%98%EA%B0%80%ED%8C%A8%EC%8A%A4%EA%B2%8C%EC%8B%9C%EB%AC%BC%EC%9D%B4%EB%AF%B8%EC%A7%80900x750.png', 'https://mabinogimobile.nexon.com/News/Notice/3545050'),
    ('image/lucky-37.webp', 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/65bf6c16-9ba6-44b9-82eb-2cc0f16aacb7/%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C%EB%9E%98%EB%AF%B8%ED%8C%A8%EC%85%98%EB%9F%AD%ED%82%A4%EB%B0%95%EC%8A%A4%EA%B2%8C%EC%8B%9C%EA%B8%80%EC%9D%B4%EB%AF%B8%EC%A7%80900x750.png', 'https://mabinogimobile.nexon.com/News/Notice/3545054'),
    ('image/lucky-38.webp', 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/3b9f6fff-1e65-49cc-a895-9e77ee9ea298/%EB%A3%A8%EC%84%BC%ED%8A%B8%EC%98%A4%EC%8A%A4%ED%8C%A8%EC%85%98%EB%9F%AD%ED%82%A4%EB%B0%95%EC%8A%A4%EA%B2%8C%EC%8B%9C%EA%B8%80%EC%9D%B4%EB%AF%B8%EC%A7%80900x750.png', 'https://mabinogimobile.nexon.com/News/Notice/3545054'),
    ('image/package-7.webp', 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/c6e12ff5-645e-4736-b1b9-8879859a33ec/%ED%86%A0%ED%83%88%ED%8C%A8%ED%82%A4%EC%A7%80%EA%B2%8C%EC%8B%9C%EB%AC%BC%EC%9D%B4%EB%AF%B8%EC%A7%80900x750B.png', 'https://mabinogimobile.nexon.com/News/Notice/3545055'),
    ('image/pet-20.webp', 'https://dszw1qtcnsa5e.cloudfront.net/community/20260916/9864aedd-648e-41a3-9d9e-74e5103a9859/%EC%9E%89%EA%B8%80%EB%A6%AC%EC%8B%9C%EC%89%BD%EB%8F%85%EA%B2%8C%EC%8B%9C%EA%B8%80%EC%9D%B4%EB%AF%B8%EC%A7%80900x750.png', 'https://mabinogimobile.nexon.com/News/Notice/3545053'),
    ('image/legend-7.webp', 'https://dszw1qtcnsa5e.cloudfront.net/community/20260917/693fc379-8b1e-4d02-b3d4-294477c66576/%ED%95%98%EB%B2%A0%EC%8A%A4%ED%8B%B0%EC%95%84%EB%B8%94%EB%A0%88%EC%8B%B1%EC%95%A1%ED%84%B0.png', 'https://mabinogimobile.nexon.com/News/Notice/3545058'),
    ('image/legend-7-robe.webp', 'https://dszw1qtcnsa5e.cloudfront.net/community/20260917/25c95e5c-cd2c-4d55-9714-94c552ad5860/%ED%95%98%EB%B2%A0%EC%8A%A4%ED%8B%B0%EC%95%84%EB%B8%94%EB%A0%88%EC%8B%B1%EC%95%A1%ED%84%B0%EB%A1%9C%EB%B8%8C.png', 'https://mabinogimobile.nexon.com/News/Notice/3545058'),
]


def download(url: str, referer: str) -> bytes:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/136 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Referer': referer,
    }
    last_error = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
            if len(data) < 3000:
                raise RuntimeError(f'image payload too small: {len(data)} bytes')
            return data
        except Exception as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(2 ** attempt)
    raise RuntimeError(f'failed to download {url}: {last_error}')


def save_webp(raw: bytes, destination: pathlib.Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        # Preserve transparency for the legend previews.
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
        im.save(destination, 'WEBP', quality=90, method=6)



def patch_index() -> bool:
    path = ROOT / 'index.html'
    text = path.read_text(encoding='utf-8')
    changed = False

    kr_tag = '<script defer src="data/catalog-update-20260917.js"></script>'
    kr_anchor = '<script defer src="data/pets.js"></script>'
    if kr_tag not in text:
        if kr_anchor not in text:
            raise RuntimeError('cannot patch index.html: data/pets.js loader not found')
        text = text.replace(kr_anchor, kr_anchor + '\n' + kr_tag, 1)
        print('OK   index.html (inserted 2026-09-17 KR data loader)')
        changed = True
    else:
        print('SKIP index.html (KR update loader already present)')

    tw_tag = '<script defer src="data/tw-update-20260925.js"></script>'
    tw_anchor = '<script defer src="data/site-config.js"></script>'
    if tw_tag not in text:
        if tw_anchor not in text:
            raise RuntimeError('cannot patch index.html: data/site-config.js loader not found')
        text = text.replace(tw_anchor, tw_anchor + '\n' + tw_tag, 1)
        print('OK   index.html (inserted 2026-09-25 TW status loader)')
        changed = True
    else:
        print('SKIP index.html (TW update loader already present)')

    if changed:
        path.write_text(text, encoding='utf-8')
    return changed


def main() -> None:
    patch_index()
    for relpath, url, referer in ASSETS:
        destination = ROOT / relpath
        if destination.exists() and destination.stat().st_size > 3000:
            print(f'SKIP {relpath} ({destination.stat().st_size} bytes)')
            continue
        raw = download(url, referer)
        save_webp(raw, destination)
        print(f'OK   {relpath} ({destination.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
