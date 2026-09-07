from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from the repository root.')

text = INDEX.read_text(encoding='utf-8')
text = re.sub(r'<html lang="zh-Hant"[^>]*>', '<html lang="zh-Hant" class="mabi-scrapbook-final">', text, count=1)
for version in ['v5','v4','v3','v2']:
    text = re.sub(r'\n?/\* hero images final layout fix ' + version + r' \*/[\s\S]*?(?=\n</style>)', '', text, count=1)
text = re.sub(r'\n?<script id="hero-images-final-layout-fix">[\s\S]*?</script>\s*', '\n', text, count=1)
text = text.replace('value="undefined"', 'value=""')
text = text.replace('placeholder="undefined"', 'placeholder="搜尋中文名 / 韓文名"')
text = re.sub(r'placeholder="[^"]*中文名[^"]*韓文名[^"]*"', 'placeholder="搜尋中文名 / 韓文名"', text, count=1)

new_header = '''<header class="hero">
  <div class="wrap hero-top hero-layout-final">
    <figure class="hero-photo hero-photo-main" aria-label="玩家營火合照">
      <img src="image/hero-campfire.png" alt="瑪奇 Mobile 玩家營火合照" loading="eager" decoding="async">
    </figure>
    <div class="hero-title-card">
      <h1><span class="mabi-title-small">瑪奇Mobile</span><span class="mabi-title-main">韓服外觀圖鑑</span></h1>
    </div>
    <figure class="hero-photo hero-photo-sub" aria-label="三人合照">
      <img src="image/hero-friends.png" alt="瑪奇 Mobile 三人合照" loading="eager" decoding="async">
    </figure>
    <button class="source-btn" id="openSources">資料來源</button>
  </div>
</header>'''
text = re.sub(r'<header class="hero">[\s\S]*?</header>', new_header, text, count=1)

labels = {
    'pass': ('通行證', 'PASS'),
    'lucky': ('幸運箱', 'LUCKY BOX'),
    'package': ('全套套組', 'SET ITEM'),
    'pet': ('寵物', 'PET'),
    'abyss': ('深淵副本時裝', 'ABYSS'),
    'raid': ('團隊副本時裝', 'RAID'),
    'dye': ('染色預覽', 'EXTRA TOOL'),
}
for key, (zh, en) in labels.items():
    pat = re.compile(r'(<button class="category[^"]*" data-type="' + re.escape(key) + r'">)[\s\S]*?(</button>)')
    text = pat.sub(lambda m, zh=zh, en=en: f'{m.group(1)}<span class="cat-zh">{zh}</span><span class="cat-en">{en}</span>{m.group(2)}', text, count=1)

# Put dye preview at the very end of category buttons.
nav_match = re.search(r'(<nav class="category-nav"[\s\S]*?>)([\s\S]*?)(</nav>)', text)
if nav_match:
    buttons = re.findall(r'\s*<button class="category[\s\S]*?</button>', nav_match.group(2))
    by_type = {}
    for button in buttons:
        m = re.search(r'data-type="([^"]+)"', button)
        if m:
            by_type[m.group(1)] = button.strip()
    order = ['pass','lucky','package','pet','abyss','raid','dye']
    rebuilt = '\n      ' + '\n      '.join(by_type[t] for t in order if t in by_type) + '\n    '
    text = text[:nav_match.start(2)] + rebuilt + text[nav_match.end(2):]

# Rebuild the title/search/sort area as one stable grid row.
section_block = '''<div class="section-head">
    <div class="section-heading-block"><div class="section-title" id="sectionTitle">通行證</div><div class="section-note" id="sectionNote"></div></div>
    <div class="archive-tools" id="archiveTools">
      <label class="archive-search-wrap" for="archiveSearch">
        <span aria-hidden="true"></span>
        <input id="archiveSearch" class="archive-search" type="search" placeholder="搜尋中文名 / 韓文名" autocomplete="off">
      </label>
      <div class="archive-count" id="archiveCount" aria-live="polite"></div>
    </div>
    <div class="section-actions" aria-label="目前分類操作">
      <button class="predict-btn" id="openPrediction" type="button">台版下批預測</button>
      <button class="offline-pet-btn" id="offlinePetBtn" type="button">建立寵物離線版</button>
      <select class="sort" id="sort" aria-label="排序">
        <option value="old" selected>舊到新</option>
        <option value="new">新到舊</option>
      </select>
    </div>
  </div>
  <section class="feed" id="feed"></section>'''
text = re.sub(r'<div class="section-head">[\s\S]*?<section class="feed" id="feed"></section>', section_block, text, count=1)

css = r'''
/* hero images final layout fix v5 */
html.mabi-scrapbook-final body{overflow-x:hidden !important;}
html.mabi-scrapbook-final .hero::before,
html.mabi-scrapbook-final .hero::after,
html.mabi-scrapbook-final .hero-top::before,
html.mabi-scrapbook-final .hero-top::after,
html.mabi-scrapbook-final .section-heading-block::before,
html.mabi-scrapbook-final .section-heading-block::after{content:none !important;display:none !important;}
html.mabi-scrapbook-final .eyebrow,
html.mabi-scrapbook-final .subtitle,
html.mabi-scrapbook-final .section-note{display:none !important;}

html.mabi-scrapbook-final .wrap{width:min(1320px,calc(100% - 44px)) !important;}
html.mabi-scrapbook-final .hero{padding:22px 0 20px !important;min-height:0 !important;overflow:hidden !important;color:#332e2b !important;background:linear-gradient(90deg,rgba(201,226,214,.74) 0%,rgba(255,252,244,.94) 22%,rgba(255,252,244,.96) 78%,rgba(211,230,218,.74) 100%) !important;box-shadow:0 8px 22px rgba(111,93,72,.08) !important;}
html.mabi-scrapbook-final .hero-layout-final{position:relative !important;display:grid !important;grid-template-columns:350px minmax(380px,1fr) 230px !important;align-items:center !important;justify-content:center !important;gap:24px !important;min-height:250px !important;padding:0 !important;}
html.mabi-scrapbook-final .hero-title-card{position:relative !important;z-index:2 !important;justify-self:center !important;padding:28px 40px 24px !important;min-width:min(580px,100%) !important;text-align:center !important;background:rgba(255,253,247,.86) !important;border:1px solid rgba(226,211,185,.74) !important;border-radius:18px !important;box-shadow:0 14px 32px rgba(105,86,63,.09) !important;}
html.mabi-scrapbook-final .hero h1{display:flex !important;flex-direction:column !important;align-items:center !important;gap:6px !important;margin:0 !important;color:#332e2b !important;line-height:1.04 !important;letter-spacing:-.03em !important;text-shadow:none !important;}
html.mabi-scrapbook-final .mabi-title-small{display:block !important;font-size:clamp(28px,3vw,40px) !important;font-weight:850 !important;}
html.mabi-scrapbook-final .mabi-title-main{display:block !important;font-size:clamp(48px,5.4vw,82px) !important;font-weight:950 !important;}
html.mabi-scrapbook-final .hero-photo{position:relative !important;z-index:1 !important;margin:0 !important;padding:12px 12px 28px !important;background:rgba(255,255,255,.92) !important;border-radius:8px !important;box-shadow:0 16px 30px rgba(103,85,62,.15) !important;}
html.mabi-scrapbook-final .hero-photo::before{content:"" !important;position:absolute !important;left:50% !important;top:-11px !important;width:96px !important;height:20px !important;transform:translateX(-50%) rotate(-2deg) !important;background:rgba(183,211,194,.62) !important;border-radius:3px !important;z-index:3 !important;}
html.mabi-scrapbook-final .hero-photo-main{transform:rotate(-4deg) !important;}
html.mabi-scrapbook-final .hero-photo-sub{transform:rotate(4deg) !important;}
html.mabi-scrapbook-final .hero-photo-main img{display:block !important;width:100% !important;height:210px !important;object-fit:cover !important;border-radius:4px !important;}
html.mabi-scrapbook-final .hero-photo-sub img{display:block !important;width:100% !important;height:138px !important;object-fit:cover !important;border-radius:4px !important;}
html.mabi-scrapbook-final .source-btn{position:absolute !important;right:0 !important;top:4px !important;z-index:4 !important;height:46px !important;padding:0 20px !important;color:#6d625b !important;background:rgba(255,253,247,.90) !important;border:1px solid #e4d4b9 !important;border-radius:999px !important;box-shadow:0 10px 20px rgba(111,94,72,.10) !important;}

html.mabi-scrapbook-final .toolbar-shell{position:sticky !important;top:0 !important;z-index:20 !important;margin-top:0 !important;padding:12px 0 !important;background:rgba(255,250,239,.88) !important;border-top:1px solid #eadcc2 !important;border-bottom:1px solid #eadcc2 !important;backdrop-filter:blur(12px) !important;}
html.mabi-scrapbook-final .toolbar{display:block !important;padding:0 !important;}
html.mabi-scrapbook-final .toolbar-actions{display:none !important;}
html.mabi-scrapbook-final .category-nav{display:grid !important;grid-template-columns:repeat(7,minmax(120px,1fr)) !important;gap:12px !important;align-items:stretch !important;justify-content:center !important;width:100% !important;}
html.mabi-scrapbook-final .category::before{content:none !important;display:none !important;}
html.mabi-scrapbook-final .category{display:flex !important;flex-direction:column !important;align-items:center !important;justify-content:center !important;gap:2px !important;min-width:0 !important;height:58px !important;padding:0 12px !important;border:0 !important;border-radius:8px !important;color:#655b53 !important;box-shadow:0 7px 16px rgba(108,89,62,.08), inset 0 1px 0 rgba(255,255,255,.55) !important;transform:none !important;position:relative !important;overflow:visible !important;}
html.mabi-scrapbook-final .category[data-type="pass"]{background:#7fbd97 !important;color:#fff !important;}
html.mabi-scrapbook-final .category[data-type="lucky"]{background:#f1c8d3 !important;}
html.mabi-scrapbook-final .category[data-type="package"]{background:#efd9aa !important;}
html.mabi-scrapbook-final .category[data-type="pet"]{background:#c8e4ee !important;}
html.mabi-scrapbook-final .category[data-type="abyss"]{background:#cfe7dc !important;}
html.mabi-scrapbook-final .category[data-type="raid"]{background:#ead0d0 !important;}
html.mabi-scrapbook-final .category[data-type="dye"]{background:#d9c8ed !important;box-shadow:0 7px 16px rgba(127,96,175,.11), inset 0 1px 0 rgba(255,255,255,.55) !important;}
html.mabi-scrapbook-final .category[data-type="dye"]::after{content:"額外工具" !important;position:absolute !important;top:-9px !important;right:10px !important;height:20px !important;padding:0 7px !important;border-radius:999px !important;background:#8c73b9 !important;color:#fff !important;font-size:10px !important;font-weight:900 !important;letter-spacing:.08em !important;display:inline-flex !important;align-items:center !important;justify-content:center !important;box-shadow:0 6px 12px rgba(99,83,133,.18) !important;}
html.mabi-scrapbook-final .category.active{outline:3px solid rgba(255,255,255,.82) !important;box-shadow:0 0 0 3px rgba(104,174,134,.55),0 10px 20px rgba(108,89,62,.10) !important;}
html.mabi-scrapbook-final .category[data-type="dye"].active{box-shadow:0 0 0 3px rgba(140,115,185,.42),0 10px 20px rgba(99,83,133,.16) !important;}
html.mabi-scrapbook-final .category .cat-zh{font-size:15px !important;line-height:1.05 !important;letter-spacing:.08em !important;font-weight:950 !important;}
html.mabi-scrapbook-final .category .cat-en{font-size:10px !important;line-height:1 !important;letter-spacing:.18em !important;opacity:.78 !important;font-weight:900 !important;}

html.mabi-scrapbook-final main.wrap{padding-top:28px !important;}
html.mabi-scrapbook-final .section-head{display:grid !important;grid-template-columns:minmax(245px,auto) minmax(360px,1fr) auto !important;gap:18px !important;align-items:center !important;margin:0 0 24px !important;padding:0 !important;background:transparent !important;border:0 !important;box-shadow:none !important;}
html.mabi-scrapbook-final .section-heading-block{display:flex !important;align-items:center !important;min-height:0 !important;grid-column:1 !important;grid-row:1 !important;}
html.mabi-scrapbook-final .section-title{min-width:0 !important;min-height:0 !important;padding:16px 28px !important;background:rgba(255,253,247,.88) !important;border:1px solid #e5d6bd !important;box-shadow:0 12px 26px rgba(111,93,72,.08) !important;color:#332e2b !important;font-size:clamp(30px,3.4vw,48px) !important;line-height:1 !important;letter-spacing:.08em !important;transform:none !important;white-space:nowrap !important;}
html.mabi-scrapbook-final .section-title::before{display:none !important;}
html.mabi-scrapbook-final .section-title::after{content:attr(data-en) !important;margin-left:18px !important;color:#786a61 !important;font-size:.42em !important;letter-spacing:.26em !important;font-family:Georgia,"Times New Roman",serif !important;font-weight:850 !important;}
html.mabi-scrapbook-final .archive-tools{display:flex !important;align-items:center !important;gap:14px !important;width:100% !important;min-width:0 !important;margin:0 !important;grid-column:2 !important;grid-row:1 !important;}
html.mabi-scrapbook-final .archive-search-wrap{display:flex !important;align-items:center !important;gap:12px !important;flex:1 1 auto !important;width:100% !important;max-width:none !important;height:56px !important;padding:0 18px !important;border-radius:999px !important;border:2px solid #bfd7c5 !important;background:rgba(255,255,255,.90) !important;box-shadow:0 10px 24px rgba(113,96,74,.08), inset 0 1px 0 rgba(255,255,255,.86) !important;position:relative !important;}
html.mabi-scrapbook-final .archive-search-wrap::before,html.mabi-scrapbook-final .archive-search-wrap::after{content:none !important;display:none !important;}
html.mabi-scrapbook-final .archive-search-wrap > span{display:inline-flex !important;align-items:center !important;justify-content:center !important;width:40px !important;min-width:40px !important;height:40px !important;border-radius:999px !important;background:#dce9df !important;color:#6b675d !important;font-size:0 !important;position:relative !important;}
html.mabi-scrapbook-final .archive-search-wrap > span::before{content:'⌕' !important;font-size:26px !important;line-height:1 !important;display:block !important;}
html.mabi-scrapbook-final .archive-search-wrap > span::after{content:none !important;display:none !important;}
html.mabi-scrapbook-final .archive-search{width:100% !important;min-width:0 !important;border:0 !important;outline:0 !important;background:transparent !important;color:#514943 !important;font-size:15px !important;font-weight:900 !important;text-align:left !important;padding:0 !important;}
html.mabi-scrapbook-final .archive-search::placeholder{color:#8f877f !important;opacity:1;text-align:left !important;}
html.mabi-scrapbook-final .archive-count{flex:0 0 auto !important;white-space:nowrap !important;color:#6c625b !important;font-size:15px !important;font-weight:900 !important;}
html.mabi-scrapbook-final .section-actions{display:flex !important;align-items:center !important;justify-content:flex-end !important;gap:12px !important;margin:0 !important;width:auto !important;grid-column:3 !important;grid-row:1 !important;}
html.mabi-scrapbook-final .section-actions .sort,html.mabi-scrapbook-final .section-actions .predict-btn{height:52px !important;padding:0 22px !important;border:0 !important;border-radius:999px !important;background:rgba(255,255,255,.82) !important;color:#655b53 !important;box-shadow:0 10px 24px rgba(104,86,63,.10) !important;}
html.mabi-scrapbook-final .section-actions .predict-btn.show{display:inline-flex !important;align-items:center !important;}
html.mabi-scrapbook-final .section-actions .offline-pet-btn{display:none !important;}
html.mabi-scrapbook-final .section-actions .predict-dot{display:none !important;}

html.mabi-scrapbook-final .mabi-pet-kind-filters{display:flex !important;gap:10px !important;flex-wrap:wrap !important;margin:-4px 0 22px !important;}
html.mabi-scrapbook-final .mabi-pet-kind-filters button{height:42px !important;padding:0 18px !important;border-radius:999px !important;border:1px solid rgba(220,204,178,.9) !important;background:rgba(255,255,255,.86) !important;color:#655b53 !important;font-size:14px !important;font-weight:900 !important;box-shadow:0 6px 14px rgba(107,93,74,.07) !important;cursor:pointer !important;}
html.mabi-scrapbook-final .mabi-pet-kind-filters button.active{color:#fff !important;border-color:transparent !important;}
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="all"].active{background:linear-gradient(180deg,#95c9a8,#6aa98b) !important;}
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="常駐"],html.mabi-scrapbook-final .mabi-kind-chip.regular{background:linear-gradient(180deg,#95c9a8,#6aa98b) !important;color:#fff !important;}
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="限定"],html.mabi-scrapbook-final .mabi-kind-chip.limited{background:linear-gradient(180deg,#e3c07b,#c99943) !important;color:#fff !important;}
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="聯動"],html.mabi-scrapbook-final .mabi-kind-chip.collab{background:linear-gradient(180deg,#b7a2db,#8f74c1) !important;color:#fff !important;}

html.mabi-scrapbook-final .feed{display:grid !important;grid-template-columns:repeat(3,minmax(0,1fr)) !important;gap:28px !important;}
html.mabi-scrapbook-final .entry{overflow:visible !important;border:1px solid rgba(228,216,193,.78) !important;border-radius:13px !important;background:#fffdf7 !important;box-shadow:0 12px 28px rgba(103,88,69,.11) !important;transform:none !important;}
html.mabi-scrapbook-final .entry::before{left:36%;right:36%;top:-10px;height:19px;background:rgba(179,209,222,.68);border:0;border-radius:4px;display:block !important;}
html.mabi-scrapbook-final .entry::after{display:none !important;}
html.mabi-scrapbook-final .image-wrap{position:relative !important;aspect-ratio:1.92 / 1 !important;min-height:0 !important;height:auto !important;border-radius:10px 10px 0 0 !important;overflow:visible !important;background:#f6efe4 !important;}
html.mabi-scrapbook-final .image-wrap::after{display:none !important;}
html.mabi-scrapbook-final .image-wrap img{width:calc(100% - 18px) !important;height:calc(100% - 18px) !important;margin:9px !important;display:block !important;object-fit:cover !important;border-radius:4px !important;}
html.mabi-scrapbook-final .entry-info{min-height:0 !important;margin:0 !important;padding:12px 18px 13px !important;display:block !important;background:#fffdf7 !important;border:0 !important;box-shadow:none !important;}
html.mabi-scrapbook-final .entry-meta,html.mabi-scrapbook-final .date{display:none !important;}
html.mabi-scrapbook-final .name{margin:0 !important;color:#4d4540 !important;font-size:18px !important;line-height:1.22 !important;letter-spacing:-.01em !important;}
html.mabi-scrapbook-final .ko{margin-top:3px !important;color:#776e67 !important;font-size:12px !important;line-height:1.35 !important;}
html.mabi-scrapbook-final .mabi-num-badge{position:absolute !important;right:10px !important;bottom:-18px !important;z-index:4 !important;display:inline-flex !important;align-items:center !important;justify-content:center !important;min-width:64px !important;height:54px !important;padding:8px 10px !important;border-radius:6px !important;background:#efe5d3 !important;color:#655a4f !important;font-size:14px !important;font-weight:900 !important;box-shadow:0 8px 18px rgba(104,86,63,.12) !important;}
html.mabi-scrapbook-final .mabi-kind-chip{display:inline-flex !important;align-items:center !important;justify-content:center !important;height:26px !important;padding:0 10px !important;border-radius:999px !important;color:#fff !important;font-size:12px !important;font-weight:900 !important;margin:0 0 7px !important;}
html.mabi-scrapbook-final .pet-variants{margin-top:8px !important;padding-top:8px !important;}
html.mabi-scrapbook-final .pet-variant{font-size:10px !important;padding:5px 7px !important;}

@media(max-width:1180px){
  html.mabi-scrapbook-final .hero-layout-final{grid-template-columns:280px minmax(300px,1fr) 190px !important;}
  html.mabi-scrapbook-final .feed{grid-template-columns:repeat(3,minmax(0,1fr)) !important;}
  html.mabi-scrapbook-final .category-nav{grid-template-columns:repeat(4,minmax(130px,1fr)) !important;}
  html.mabi-scrapbook-final .section-head{grid-template-columns:1fr auto !important;}
  html.mabi-scrapbook-final .section-heading-block{grid-column:1 !important;}
  html.mabi-scrapbook-final .section-actions{grid-column:2 !important;}
  html.mabi-scrapbook-final .archive-tools{grid-column:1 / -1 !important;grid-row:2 !important;}
}
@media(max-width:900px){
  html.mabi-scrapbook-final .wrap{width:min(100% - 24px,980px) !important;}
  html.mabi-scrapbook-final .hero-layout-final{grid-template-columns:1fr !important;gap:12px !important;min-height:0 !important;}
  html.mabi-scrapbook-final .hero-photo-sub{display:none !important;}
  html.mabi-scrapbook-final .hero-photo-main{max-width:420px !important;justify-self:center !important;}
  html.mabi-scrapbook-final .hero-photo-main img{height:210px !important;}
  html.mabi-scrapbook-final .hero-title-card{min-width:0 !important;width:100% !important;padding:24px 18px 20px !important;}
  html.mabi-scrapbook-final .source-btn{position:static !important;margin:12px auto 0 !important;display:inline-flex !important;}
  html.mabi-scrapbook-final .category-nav{display:flex !important;justify-content:flex-start !important;overflow-x:auto !important;flex-wrap:nowrap !important;padding:2px 2px 8px !important;}
  html.mabi-scrapbook-final .category{flex:0 0 132px !important;}
  html.mabi-scrapbook-final .section-head{grid-template-columns:1fr !important;gap:12px !important;}
  html.mabi-scrapbook-final .section-heading-block,html.mabi-scrapbook-final .archive-tools,html.mabi-scrapbook-final .section-actions{grid-column:1 !important;grid-row:auto !important;}
  html.mabi-scrapbook-final .section-actions{justify-content:flex-start !important;flex-wrap:wrap !important;}
  html.mabi-scrapbook-final .archive-tools{flex-wrap:wrap !important;}
  html.mabi-scrapbook-final .archive-count{width:100% !important;}
  html.mabi-scrapbook-final .feed{grid-template-columns:repeat(2,minmax(0,1fr)) !important;}
}
@media(max-width:560px){
  html.mabi-scrapbook-final .mabi-title-main{font-size:clamp(38px,12vw,54px) !important;}
  html.mabi-scrapbook-final .hero-photo-main img{height:176px !important;}
  html.mabi-scrapbook-final .archive-search-wrap{height:56px !important;}
  html.mabi-scrapbook-final .archive-search{font-size:15px !important;}
  html.mabi-scrapbook-final .feed{grid-template-columns:1fr !important;}
}
'''

js = '''
<script id="hero-images-final-layout-fix">
(()=>{
  const TYPE_EN={pass:'PASS',lucky:'LUCKY BOX',package:'SET ITEM',pet:'PET',abyss:'ABYSS',raid:'RAID',dye:'DYE TOOL'};
  const TYPE_ZH={pass:'通行證',lucky:'幸運箱',package:'全套套組',pet:'寵物',abyss:'深淵副本時裝',raid:'團隊副本時裝',dye:'染色預覽'};
  let petKindFilter='all';
  const q=(s,r=document)=>r.querySelector(s);
  const qa=(s,r=document)=>Array.from(r.querySelectorAll(s));
  const normalizeKind=k=>k==='常規'?'常駐':(k||'常駐');
  function itemFromEntry(entry){const id=q('.image-wrap',entry)?.dataset?.image;return (typeof DATA!=='undefined'&&Array.isArray(DATA))?DATA.find(x=>x.id===id):null;}
  function issueText(item){if(!item)return '';if(item.type==='package')return `第 ${item.number} 代`;if(item.type==='abyss'||item.type==='raid')return `第 ${item.number} 套`;return `第 ${item.number} 期`;}
  function kindClass(kind){kind=normalizeKind(kind);if(kind==='限定')return 'limited';if(kind==='聯動')return 'collab';return 'regular';}
  function fixHeader(){
    const h1=q('.hero h1');
    if(h1)h1.innerHTML='<span class="mabi-title-small">瑪奇Mobile</span><span class="mabi-title-main">韓服外觀圖鑑</span>';
    q('.eyebrow')?.remove();
    q('.subtitle')?.remove();
    const title=q('#sectionTitle');
    const type=(typeof state!=='undefined'&&state.type)||q('.category.active')?.dataset?.type||'pass';
    if(title) title.dataset.en=TYPE_EN[type]||'';
    const note=q('#sectionNote'); if(note) note.textContent='';
  }
  function fixCats(){
    const nav=q('.category-nav');
    if(nav){const dye=q('.category[data-type="dye"]',nav); if(dye) nav.appendChild(dye);}
    qa('.category').forEach(btn=>{const type=btn.dataset.type;if(type) btn.innerHTML=`<span class="cat-zh">${TYPE_ZH[type]||btn.textContent.trim()}</span><span class="cat-en">${TYPE_EN[type]||''}</span>`;});
  }
  function fixSearch(){
    const input=q('#archiveSearch');
    if(input){input.placeholder='搜尋中文名 / 韓文名'; if(input.value==='undefined'||input.value==='null') input.value='';}
    const lab=q('.archive-search-wrap > span'); if(lab) lab.textContent='';
  }
  function decorateEntry(entry){
    const item=itemFromEntry(entry); if(!item)return;
    const imgWrap=q('.image-wrap',entry);
    if(imgWrap&&!q('.mabi-num-badge',imgWrap)){const b=document.createElement('span');b.className='mabi-num-badge';imgWrap.appendChild(b);}
    const b=q('.mabi-num-badge',imgWrap); if(b) b.textContent=issueText(item);
    const meta=q('.entry-meta',entry); if(meta) meta.style.display='none';
    const info=q('.entry-info',entry);
    if(info){let chip=q('.mabi-kind-chip',info);if(item.type==='pet'){if(!chip){chip=document.createElement('div');info.insertBefore(chip,info.firstChild);}const kind=normalizeKind(item.kind);chip.className=`mabi-kind-chip ${kindClass(kind)}`;chip.textContent=kind;}else if(chip){chip.remove();}}
  }
  function countVisible(){return qa('#feed .entry').filter(el=>getComputedStyle(el).display!=='none').length;}
  function updateCount(){const count=q('#archiveCount'); if(count) count.textContent=`共 ${countVisible()} 筆`;}
  function ensurePetFilter(){
    const main=q('main.wrap'); if(!main)return;
    let bar=q('#mabiPetKindFilters');
    const isPet=(typeof state!=='undefined'&&state.type==='pet')||q('.category.active')?.dataset?.type==='pet';
    if(!isPet){if(bar)bar.remove();return;}
    if(!bar){bar=document.createElement('div');bar.id='mabiPetKindFilters';bar.className='mabi-pet-kind-filters';const anchor=q('.section-head')||q('.archive-tools');if(anchor)anchor.insertAdjacentElement('afterend',bar);['all','常駐','限定','聯動'].forEach(kind=>{const btn=document.createElement('button');btn.type='button';btn.dataset.kind=kind;btn.textContent=kind==='all'?'全部':kind;btn.addEventListener('click',()=>{petKindFilter=kind;applyPetFilter();});bar.appendChild(btn);});}
    applyPetFilter();
  }
  function applyPetFilter(){
    const bar=q('#mabiPetKindFilters'); if(bar)qa('button',bar).forEach(btn=>btn.classList.toggle('active',btn.dataset.kind===petKindFilter));
    const isPet=(typeof state!=='undefined'&&state.type==='pet')||q('.category.active')?.dataset?.type==='pet'; if(!isPet)return;
    qa('#feed .entry').forEach(entry=>{const item=itemFromEntry(entry);const kind=normalizeKind(item?.kind);entry.style.display=(petKindFilter==='all'||kind===petKindFilter)?'':'none';});
    updateCount();
  }
  function refresh(){fixHeader();fixCats();fixSearch();qa('#feed .entry').forEach(decorateEntry);ensurePetFilter();updateCount();}
  const feed=q('#feed'); if(feed)new MutationObserver(()=>setTimeout(refresh,0)).observe(feed,{childList:true,subtree:true});
  document.addEventListener('DOMContentLoaded',()=>setTimeout(refresh,80));
  window.addEventListener('hashchange',()=>setTimeout(refresh,90));
  document.addEventListener('click',e=>{if(e.target.closest('.category'))setTimeout(refresh,120);});
  document.addEventListener('input',e=>{if(e.target.id==='archiveSearch')setTimeout(updateCount,30);});
  setTimeout(refresh,120);
})();
</script>
'''

if '\n</style>' not in text:
    raise SystemExit('Could not find </style>')
text = text.replace('\n</style>', '\n' + css + '\n</style>', 1)
if '</body>' in text:
    text = text.replace('</body>', js + '\n</body>', 1)
else:
    text += '\n' + js
text = re.sub(r'\n<!-- hero images final layout fix 2026-09-06[^>]*-->', '', text)
text = text.replace('</html>', '\n<!-- hero images final layout fix 2026-09-06 v5 -->\n</html>')
INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Applied pet button + 3 column + smaller text fix v5.')
