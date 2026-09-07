#!/usr/bin/env python3
from __future__ import annotations
import json, re, time, ssl
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'image_manifest.json'
REPORT = ROOT / 'image_download_report.txt'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36'
CTX = ssl.create_default_context()

def headers_for(url: str):
    if 'cloudfront.net' in url:
        ref = 'https://mabinogimobile.nexon.com/'
    elif 'inven.co.kr' in url:
        ref = 'https://www.inven.co.kr/'
    elif 'dcinside.com' in url:
        ref = 'https://gall.dcinside.com/'
    else:
        ref = 'https://namu.moe/'
    return {
        'User-Agent': UA,
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Referer': ref,
        'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
    }

def get(url: str, timeout=60):
    req = Request(url, headers=headers_for(url))
    with urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read(), r.headers.get('Content-Type', '')

def valid(data: bytes, ct=''):
    sig = data.startswith((b'\x89PNG\r\n\x1a\n', b'\xff\xd8\xff', b'RIFF', b'GIF8'))
    return len(data) > 3000 and (ct.startswith('image/') or sig)

def resolve_namu(filename: str):
    found = []
    q = quote('파일:' + filename, safe='')
    for host in ('https://namu.moe/w/', 'https://m.namu.moe/w/', 'https://dark.namu.moe/w/'):
        try:
            raw, _ = get(host + q)
            txt = raw.decode('utf-8', 'ignore').replace('&amp;', '&')
            found += re.findall(r'https://file\.namu\.moe/file/[0-9a-fA-F]+', txt)
            if found:
                break
        except Exception:
            pass
    return list(dict.fromkeys(found))

def main():
    assets = json.loads(MANIFEST.read_text(encoding='utf-8'))['assets']
    failures, successes, skipped = [], [], []
    for x in assets:
        dest = ROOT / x['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and dest.stat().st_size > 3000:
            skipped.append(x['path'])
            print('✓ 已存在', x['path'])
            continue

        urls = list(x.get('urls', []))
        if x.get('namu_filename'):
            urls += resolve_namu(x['namu_filename'])
        urls = list(dict.fromkeys(urls))

        ok = False
        last_error = ''
        for attempt in range(1, 4):
            for u in urls:
                try:
                    data, ct = get(u)
                    if valid(data, ct):
                        dest.write_bytes(data)
                        print('✓ 下載', x['path'], len(data), 'bytes')
                        successes.append(x['path'])
                        ok = True
                        break
                    last_error = f'內容不是有效圖片 ({len(data)} bytes, {ct})'
                except Exception as e:
                    last_error = repr(e)
                    print('! 失敗', x['name'], 'attempt', attempt, u, e)
                time.sleep(.5)
            if ok:
                break
            time.sleep(2 * attempt)
        if not ok:
            failures.append((x['name'], x['path'], last_error))

    lines = [
        'Mabinogi Mobile Wardrobe image localization report',
        f'success={len(successes)} skipped={len(skipped)} failed={len(failures)}',
        '',
    ]
    if successes:
        lines += ['Downloaded:'] + [f'  {p}' for p in successes] + ['']
    if failures:
        lines += ['Failed:'] + [f'  {name} -> {path} :: {err}' for name, path, err in failures] + ['']
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print('\n' + '\n'.join(lines))
    # 不因單張外站擋圖而中止，讓 GitHub Action 仍能 commit 已成功下載的圖片。
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
