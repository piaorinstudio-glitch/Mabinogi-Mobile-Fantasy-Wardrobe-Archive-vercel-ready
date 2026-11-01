#!/usr/bin/env python3
"""Temporarily disable the Deka action-box section without deleting assets.
Run from the root of Mabinogi-Mobile-Fantasy-Wardrobe-Archive-vercel-ready.
"""
from pathlib import Path

index = Path(__file__).resolve().parent / 'index.html'
if not index.is_file():
    raise SystemExit('錯誤：請先切換到網站 GitHub 儲存庫的根目錄（必須能找到 index.html）。')

source = index.read_bytes()
removals = [
    '<button class="category" data-type="action"><span class="cat-zh">動作箱</span><span class="cat-en">ACTION</span></button>',
    '<script defer src="data/actions.js?v=20261015"></script>',
    '<script defer src="assets/js/action-gallery.js?v=20261015"></script>',
]

removals = [s.encode('utf-8') for s in removals]

if all(s not in source for s in removals):
    print('動作箱已關閉，無須重複處理。')
    raise SystemExit(0)

missing = [s for s in removals if source.count(s) != 1]
if missing:
    raise SystemExit('無法安全修改：index.html 與 2026-11-02 檢查版本不同，請先核對檔案。\n' + '\n'.join(s.decode('utf-8') for s in missing))

result = source
for value in removals:
    result = result.replace(value, b'', 1)
index.write_bytes(result)
print('已修改 index.html：隱藏動作箱分類，且不再載入動作資料及預覽程式。')
print('沒有刪除 image/actions/ 中的 PNG、GIF，也沒有修改其他分類。')
