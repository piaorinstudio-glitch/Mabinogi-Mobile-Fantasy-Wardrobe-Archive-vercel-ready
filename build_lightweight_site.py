#!/usr/bin/env python3
"""Build a static-site folder without large Deka action GIFs.
Put this file in the GitHub repository root and run:
    python build_lightweight_site.py
Then deploy the generated site-dist/ folder to a static host.
This does NOT delete any original image or Git file.
"""
from pathlib import Path
from shutil import copy2, copytree, rmtree

root = Path(__file__).resolve().parent
out = root / 'site-dist'
if not (root / 'index.html').is_file():
    raise SystemExit('請把腳本放在包含 index.html 的儲存庫根目錄。')
if out.exists():
    rmtree(out)
out.mkdir()

for fname in ['index.html', 'about.html', 'privacy.html', 'contact.html',
              'ads.txt', 'robots.txt', 'sitemap.xml', 'favicon.svg']:
    source = root / fname
    if source.is_file():
        copy2(source, out / fname)

for folder in ['assets', 'data', 'image']:
    source = root / folder
    if not source.is_dir():
        raise SystemExit(f'缺少網站必要資料夾：{folder}')
    def skip(p, names, folder=folder):
        if folder == 'image' and Path(p) == source:
            return ['actions'] if 'actions' in names else []
        if folder == 'data' and Path(p) == source:
            return ['actions.js'] if 'actions.js' in names else []
        return []
    copytree(source, out / folder, ignore=skip)

index = out / 'index.html'
b = index.read_bytes()
needles = [
    '<button class="category" data-type="action"><span class="cat-zh">動作箱</span><span class="cat-en">ACTION</span></button>',
    '<script defer src="data/actions.js?v=20261015"></script>',
    '<script defer src="assets/js/action-gallery.js?v=20261015"></script>',
]
for needle in needles:
    raw = needle.encode('utf-8')
    if b.count(raw) != 1:
        raise SystemExit(f'首頁格式不符合預期，未能確保關閉動作箱：{needle}')
    b = b.replace(raw, b'', 1)
index.write_bytes(b)
# Not referenced by the closed section; remove its JS from this published folder.
preview_js = out / 'assets/js/action-gallery.js'
if preview_js.exists():
    preview_js.unlink()
size = sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
print(f'完成：{out}；部署檔案總大小約 {size/1024/1024:.1f} MiB。')
print('原始 image/actions/ GIF、PNG 與資料均未刪除。')
