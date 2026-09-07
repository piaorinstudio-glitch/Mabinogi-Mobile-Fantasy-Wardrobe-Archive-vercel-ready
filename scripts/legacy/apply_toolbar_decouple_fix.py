from pathlib import Path
import re

p = Path('index.html')
if not p.exists():
    raise SystemExit('index.html not found')
text = p.read_text(encoding='utf-8')

# 1) Move predict/offline/sort out of sticky toolbar into main section head actions.
old_toolbar = '''<div class="toolbar-shell">
  <div class="wrap toolbar">
    <nav class="category-nav" aria-label="圖鑑分類">
      <button class="category active" data-type="pass">通行證</button>
      <button class="category" data-type="lucky">幸運箱</button>
      <button class="category" data-type="package">全套套組</button>
      <button class="category" data-type="pet">寵物</button>
      <button class="category" data-type="abyss">深淵副本時裝</button>
      <button class="category" data-type="raid">團隊副本時裝</button>
    </nav>
    <button class="predict-btn" id="openPrediction" type="button"><span class="predict-dot"></span>台版下批預測</button>
    <button class="offline-pet-btn" id="offlinePetBtn" type="button">⬇ 建立寵物離線版</button>
    <select class="sort" id="sort" aria-label="排序">
      <option value="old" selected>舊到新</option>
      <option value="new">新到舊</option>
    </select>
  </div>
</div>'''
new_toolbar = '''<div class="toolbar-shell">
  <div class="wrap toolbar">
    <nav class="category-nav" aria-label="圖鑑分類">
      <button class="category active" data-type="pass">通行證</button>
      <button class="category" data-type="lucky">幸運箱</button>
      <button class="category" data-type="package">全套套組</button>
      <button class="category" data-type="pet">寵物</button>
      <button class="category" data-type="abyss">深淵副本時裝</button>
      <button class="category" data-type="raid">團隊副本時裝</button>
    </nav>
  </div>
</div>'''
if old_toolbar in text:
    text = text.replace(old_toolbar, new_toolbar, 1)
else:
    # Fallback: remove only action controls from toolbar if previous patch changed whitespace.
    text = re.sub(r'\s*<button class="predict-btn" id="openPrediction"[\s\S]*?</button>', '', text, count=1)
    text = re.sub(r'\s*<button class="offline-pet-btn" id="offlinePetBtn"[\s\S]*?</button>', '', text, count=1)
    text = re.sub(r'\s*<select class="sort" id="sort"[\s\S]*?</select>', '', text, count=1)

old_head = '''<div class="section-head">
    <div><div class="section-title" id="sectionTitle">通行證</div><div class="section-note" id="sectionNote">點圖片可放大查看</div></div>
  </div>'''
new_head = '''<div class="section-head">
    <div class="section-heading-block"><div class="section-title" id="sectionTitle">通行證</div><div class="section-note" id="sectionNote">點圖片可放大查看</div></div>
    <div class="section-actions" aria-label="目前分類操作">
      <button class="predict-btn" id="openPrediction" type="button"><span class="predict-dot"></span>台版下批預測</button>
      <button class="offline-pet-btn" id="offlinePetBtn" type="button">⬇ 建立寵物離線版</button>
      <select class="sort" id="sort" aria-label="排序">
        <option value="old" selected>舊到新</option>
        <option value="new">新到舊</option>
      </select>
    </div>
  </div>'''
if old_head in text:
    text = text.replace(old_head, new_head, 1)
elif 'class="section-actions"' not in text:
    text = text.replace('<div class="section-head">', '<div class="section-head">', 1)
    text = re.sub(r'(<div class="section-head">\s*<div[^>]*><div class="section-title" id="sectionTitle">.*?</div><div class="section-note" id="sectionNote">.*?</div></div>)', r'\1\n    <div class="section-actions" aria-label="目前分類操作">\n      <button class="predict-btn" id="openPrediction" type="button"><span class="predict-dot"></span>台版下批預測</button>\n      <button class="offline-pet-btn" id="offlinePetBtn" type="button">⬇ 建立寵物離線版</button>\n      <select class="sort" id="sort" aria-label="排序">\n        <option value="old" selected>舊到新</option>\n        <option value="new">新到舊</option>\n      </select>\n    </div>', text, count=1, flags=re.S)

# 2) Override toolbar layout CSS. Keep categories sticky; actions are normal content below.
css_marker = '/* decouple section actions from sticky category toolbar */'
css = r'''

/* decouple section actions from sticky category toolbar */
.toolbar-shell{
  position:sticky;
  top:0;
  z-index:20;
}
.toolbar{
  display:block;
  padding:10px 0;
}
.category-nav{
  display:flex;
  gap:7px;
  flex-wrap:wrap;
  width:100%;
}
.section-head{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:14px;
  margin:2px 0 14px;
}
.section-heading-block{min-width:0;}
.section-actions{
  display:flex;
  align-items:center;
  justify-content:flex-end;
  gap:8px;
  flex-wrap:wrap;
  margin-left:auto;
}
.section-actions .predict-btn,
.section-actions .offline-pet-btn,
.section-actions .sort{
  position:static;
  flex:0 0 auto;
}
.section-actions .sort{margin-left:0;}
.pet-filter-bar{
  flex-basis:100%;
  margin-left:0;
  margin-top:4px;
}
@media(max-width:900px){
  .toolbar{padding:9px 0;}
  .category-nav{
    flex-wrap:nowrap;
    overflow-x:auto;
    overscroll-behavior-x:contain;
    padding-bottom:4px;
    scrollbar-width:thin;
  }
  .category{flex:0 0 auto;white-space:nowrap;}
  .section-head{
    display:grid;
    grid-template-columns:1fr auto;
    align-items:center;
    gap:10px 12px;
    margin-top:2px;
  }
  .section-actions{
    grid-column:2;
    grid-row:1;
    margin-left:0;
    justify-content:flex-end;
    flex-wrap:nowrap;
  }
  .pet-filter-bar.show{
    grid-column:1 / -1;
    grid-row:2;
    display:flex;
    width:100%;
    flex-wrap:nowrap;
    overflow-x:auto;
    padding-bottom:5px;
    scrollbar-width:thin;
  }
}
@media(max-width:620px){
  main{padding-top:16px;}
  .section-head{
    grid-template-columns:1fr;
    align-items:start;
    margin-bottom:12px;
  }
  .section-actions{
    grid-column:1;
    grid-row:2;
    width:100%;
    justify-content:space-between;
    gap:8px;
  }
  .section-actions .predict-btn.show{display:inline-flex;}
  .section-actions .predict-btn:not(.show){display:none;}
  .section-actions .sort{margin-left:auto;max-width:128px;height:38px;}
  .pet-filter-bar.show{
    grid-column:1;
    grid-row:3;
    margin-top:0;
  }
}
@media(max-width:420px){
  .section-actions{gap:6px;}
  .section-actions .sort{max-width:116px;font-size:11px;}
  .section-actions .predict-btn{font-size:11px;padding:0 9px;}
}
'''
if css_marker not in text:
    text = text.replace('\n</style>', css + '\n</style>', 1)

# Version marker for cache busting / confirmation.
text = re.sub(r'<!-- toolbar .*? -->\n?', '', text)
text = text.replace('</html>', '<!-- toolbar decoupled 2026-09-05 -->\n</html>')

p.write_text(text, encoding='utf-8', newline='\n')
print('Toolbar actions moved out of sticky category list')
