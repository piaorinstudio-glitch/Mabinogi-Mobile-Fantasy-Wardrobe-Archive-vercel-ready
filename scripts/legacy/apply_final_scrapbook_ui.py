from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Run this workflow from repository root.')
text = INDEX.read_text(encoding='utf-8')

# Replace/force theme class.
if re.search(r'<html[^>]*class="[^"]*"', text):
    text = re.sub(r'<html([^>]*)class="[^"]*"', r'<html\1class="mabi-scrapbook-final"', text, count=1)
else:
    text = text.replace('<html lang="zh-Hant">', '<html lang="zh-Hant" class="mabi-scrapbook-final">', 1)

# Cleaner search label icon instead of a second text button.
text = text.replace('<span>搜尋</span>\n        <input id="archiveSearch"', '<span aria-hidden="true">⌕</span>\n        <input id="archiveSearch"')

labels = {
    'pass': ('通 行 證', 'PASS'),
    'lucky': ('幸 運 箱', 'LUCKY BOX'),
    'package': ('全 套 套 組', 'SET ITEM'),
    'dye': ('染 色 預 覽', 'DYE PREVIEW'),
    'pet': ('寵 物', 'PET'),
    'abyss': ('深 淵 副 本 時 裝', 'ABYSS'),
    'raid': ('團 隊 副 本 時 裝', 'RAID'),
}
for key, (zh, en) in labels.items():
    pattern = re.compile(r'(<button class="category[^"]*" data-type="'+re.escape(key)+r'">)(.*?)(</button>)')
    def repl(m):
        if 'cat-zh' in m.group(2):
            return m.group(0)
        return f'{m.group(1)}<span class="cat-zh">{zh}</span><span class="cat-en">{en}</span>{m.group(3)}'
    text = pattern.sub(repl, text, count=1)

marker = '/* mabi scrapbook final layout */'
css = r'''

/* mabi scrapbook final layout */
:root{
  --mabi-bg:#f6f1e6;
  --mabi-paper:#fffdf7;
  --mabi-ink:#4f4742;
  --mabi-muted:#8d8178;
  --mabi-line:#e7dac4;
  --mabi-green:#78ad88;
  --mabi-shadow:0 16px 34px rgba(100,83,61,.13);
}
html.mabi-scrapbook-final body{
  color:var(--mabi-ink);
  background:
    radial-gradient(circle at 4% 7%,rgba(139,188,197,.22) 0 8px,transparent 9px),
    radial-gradient(circle at 8% 3%,rgba(239,197,135,.23) 0 7px,transparent 8px),
    radial-gradient(circle at 91% 8%,rgba(149,188,142,.22) 0 8px,transparent 9px),
    linear-gradient(180deg,#f6f1e6 0%,#fbf6eb 42%,#f5efe2 100%);
  background-attachment:fixed;
  font-family:"Noto Serif TC","Noto Sans TC","Microsoft JhengHei",serif;
}
html.mabi-scrapbook-final body::before{
  content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.34;
  background-image:linear-gradient(90deg,rgba(92,76,57,.035) 1px,transparent 1px),linear-gradient(180deg,rgba(92,76,57,.03) 1px,transparent 1px);
  background-size:32px 32px;
}
.mabi-scrapbook-final .wrap{width:min(1220px,calc(100% - 70px));}

/* wide paper header */
.mabi-scrapbook-final .hero{
  color:#5e5550;margin:0;padding:34px 0 26px;border:0;border-radius:0;overflow:hidden;
  background:linear-gradient(90deg,rgba(197,216,200,.58),transparent 18%,transparent 82%,rgba(207,220,205,.58)),radial-gradient(ellipse at 50% 18%,rgba(255,255,255,.90),rgba(255,250,239,.82) 55%,rgba(242,233,216,.70));
  box-shadow:0 10px 28px rgba(113,92,65,.10);
}
.mabi-scrapbook-final .hero::before{
  content:"Stories\A in Erinn";white-space:pre;display:block;position:absolute;left:42px;top:34px;width:235px;height:145px;
  border:14px solid rgba(255,255,255,.82);background:linear-gradient(rgba(112,153,129,.16),rgba(112,153,129,.16)),linear-gradient(135deg,#dcebdd,#b9d6d2 48%,#edf3df);
  color:#81766f;font:italic 22px/1.05 Georgia,serif;padding:12px 0 0 18px;box-shadow:0 13px 26px rgba(104,84,60,.16);transform:rotate(-6deg);opacity:.95;
}
.mabi-scrapbook-final .hero::after{
  content:"在艾琳，\A遇見更喜歡的自己。";white-space:pre;display:block;position:absolute;right:48px;top:35px;width:250px;min-height:104px;padding:24px 24px 14px;
  background:rgba(255,252,241,.88);color:#71665f;border:1px solid rgba(225,210,187,.78);box-shadow:0 13px 24px rgba(104,84,60,.12);transform:rotate(4deg);font-size:18px;line-height:1.7;
}
.mabi-scrapbook-final .hero-top{width:min(850px,calc(100% - 420px));margin:auto;display:block;text-align:center;position:relative;z-index:1;}
.mabi-scrapbook-final .eyebrow{display:block;color:#807872;background:transparent;border:0;box-shadow:none;letter-spacing:.08em;font-size:24px;font-weight:500;text-transform:none;padding:0;font-family:Georgia,"Noto Serif TC",serif;}
.mabi-scrapbook-final .eyebrow::before{display:none;}
.mabi-scrapbook-final h1{display:inline-block;position:relative;margin:7px 0 10px;color:#3f3835;text-shadow:none;font-size:clamp(42px,4.8vw,64px);line-height:1.08;letter-spacing:.02em;font-family:"Noto Serif TC","Source Han Serif TC",Georgia,serif;}
.mabi-scrapbook-final h1::before{content:"";position:absolute;left:50%;top:-10px;width:122px;height:32px;transform:translateX(-50%) rotate(-1.5deg);background:rgba(233,174,189,.38);border-radius:7px;z-index:-1;}
.mabi-scrapbook-final h1::after{content:"Fantasy Wardrobe Archive";display:block;margin-top:8px;color:#8b817a;font:italic 23px/1.1 Georgia,serif;letter-spacing:.12em;}
.mabi-scrapbook-final .subtitle{display:block!important;color:#6f665f;font-size:17px;letter-spacing:.22em;margin:14px 0 0;}
.mabi-scrapbook-final .subtitle::before{content:"收 集 每 一 個，屬 於 你 的 風 格";}
.mabi-scrapbook-final .source-btn{position:absolute;right:0;top:2px;height:50px;padding:0 26px;background:rgba(255,253,246,.76);color:#655b55;border:1px solid #dfd0b9;border-radius:12px;box-shadow:0 12px 24px rgba(102,84,61,.12);font-weight:900;}

/* category stickers */
.mabi-scrapbook-final .toolbar-shell{position:sticky;top:0;z-index:20;margin-top:0;background:rgba(255,250,238,.78);border-top:1px solid rgba(230,217,195,.75);border-bottom:1px solid rgba(224,210,186,.85);backdrop-filter:blur(16px);box-shadow:0 8px 20px rgba(107,89,64,.06);}
.mabi-scrapbook-final .toolbar{display:block;padding:15px 0;}
.mabi-scrapbook-final .category-nav{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:12px;width:100%;}
.mabi-scrapbook-final .category{height:60px;border:0;border-radius:7px;padding:0 12px;color:#5a504a;box-shadow:0 8px 16px rgba(96,79,57,.10),inset 0 1px 0 rgba(255,255,255,.42);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;position:relative;overflow:visible;font-family:"Noto Serif TC","Noto Sans TC",serif;}
.mabi-scrapbook-final .category::before{font-size:24px;line-height:1;opacity:.68;position:absolute;left:14px;top:50%;transform:translateY(-50%);}
.mabi-scrapbook-final .category[data-type="pass"]{background:#79b58c;color:white}.mabi-scrapbook-final .category[data-type="pass"]::before{content:"🎟";opacity:.86}
.mabi-scrapbook-final .category[data-type="lucky"]{background:#efd3da}.mabi-scrapbook-final .category[data-type="lucky"]::before{content:"🎁"}
.mabi-scrapbook-final .category[data-type="package"]{background:#f1dfb8}.mabi-scrapbook-final .category[data-type="package"]::before{content:"👕"}
.mabi-scrapbook-final .category[data-type="dye"]{background:#dfd2ed}.mabi-scrapbook-final .category[data-type="dye"]::before{content:"🎨"}
.mabi-scrapbook-final .category[data-type="pet"]{background:#c9e3ef}.mabi-scrapbook-final .category[data-type="pet"]::before{content:"🐾"}
.mabi-scrapbook-final .category[data-type="abyss"]{background:#d7e7e0}.mabi-scrapbook-final .category[data-type="abyss"]::before{content:"⛰"}
.mabi-scrapbook-final .category[data-type="raid"]{background:#ead5d0}.mabi-scrapbook-final .category[data-type="raid"]::before{content:"🛡"}
.mabi-scrapbook-final .category.active{transform:translateY(-2px);box-shadow:0 12px 22px rgba(85,68,47,.16),inset 0 1px 0 rgba(255,255,255,.45);outline:2px solid rgba(255,255,255,.75);outline-offset:-4px;}
.mabi-scrapbook-final .category.active::after{content:"";position:absolute;left:18%;right:18%;top:-8px;height:14px;background:rgba(250,230,174,.60);border-radius:3px;transform:rotate(-2deg);}
.mabi-scrapbook-final .cat-zh{font-size:18px;font-weight:900;letter-spacing:.08em;line-height:1}.mabi-scrapbook-final .cat-en{font-size:10px;font-family:Georgia,serif;letter-spacing:.18em;opacity:.75;line-height:1}

/* title and tools */
.mabi-scrapbook-final main.wrap{padding-top:34px;}
.mabi-scrapbook-final .section-head{display:grid;grid-template-columns:minmax(320px,1fr) auto;align-items:center;gap:22px;margin:0 0 22px;padding:0;background:transparent;border:0;box-shadow:none;}
.mabi-scrapbook-final .section-heading-block{position:relative;min-height:92px;display:flex;align-items:center;gap:24px;}
.mabi-scrapbook-final .section-heading-block::before{content:"";width:240px;height:76px;background:rgba(255,253,246,.86);border:1px solid rgba(229,215,192,.80);box-shadow:0 12px 24px rgba(102,84,61,.10);transform:rotate(-2deg);flex:none;}
.mabi-scrapbook-final .section-heading-block::after{content:"踏上旅程，\A收集途中閃耀的風景。";white-space:pre;color:#6f665f;font-size:19px;line-height:1.75;letter-spacing:.12em;padding-left:24px;border-left:1px solid #d8cbb8;}
.mabi-scrapbook-final .section-title{position:absolute;left:34px;top:50%;transform:translateY(-50%);z-index:2;color:#352f2c;font-size:44px;font-weight:950;letter-spacing:.12em;font-family:"Noto Serif TC","Source Han Serif TC",Georgia,serif;}
.mabi-scrapbook-final .section-title::before{display:none}.mabi-scrapbook-final .section-title::after{content:"PASS";display:block;margin-top:4px;font-size:16px;letter-spacing:.35em;font-family:Georgia,serif;color:#6f665f;text-align:right;}
.mabi-scrapbook-final .section-note{display:none!important}.mabi-scrapbook-final .section-actions{display:flex;align-items:center;justify-content:flex-end;gap:12px;margin:0;}
.mabi-scrapbook-final .sort,.mabi-scrapbook-final .predict-btn,.mabi-scrapbook-final .offline-pet-btn{height:56px;border:0!important;border-radius:28px!important;background:rgba(255,255,255,.72)!important;color:#655b55!important;box-shadow:0 9px 18px rgba(90,73,52,.10),inset 0 1px 0 rgba(255,255,255,.75)!important;padding:0 24px;font-weight:900;font-size:15px;}
.mabi-scrapbook-final .predict-btn.show{display:inline-flex!important;background:linear-gradient(180deg,#86b995,#6aa87c)!important;color:white!important;}
.mabi-scrapbook-final .archive-tools{display:grid;grid-template-columns:minmax(320px,1fr) auto;align-items:center;gap:24px;margin:-8px 0 30px;}
.mabi-scrapbook-final .archive-search-wrap{height:64px;display:flex;align-items:center;gap:0;border-radius:999px;background:rgba(255,255,255,.72);border:3px solid rgba(205,223,202,.95);box-shadow:0 10px 20px rgba(96,79,57,.09),inset 0 1px 0 rgba(255,255,255,.85);overflow:hidden;}
.mabi-scrapbook-final .archive-search-wrap span{width:74px;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(210,230,211,.70);color:#6a6a63;font-size:35px;font-family:Arial,sans-serif;font-weight:400;}
.mabi-scrapbook-final #archiveSearch{flex:1;width:100%;height:100%;min-height:0!important;border:0!important;background:transparent!important;box-shadow:none!important;outline:0!important;padding:0 22px!important;color:#5c544e;font-size:18px;font-weight:700;}.mabi-scrapbook-final #archiveSearch::placeholder{color:#958c84;}
.mabi-scrapbook-final .archive-count{font-size:17px;color:#6f665f;font-weight:900;white-space:nowrap;}.mabi-scrapbook-final .archive-count::before{content:"› ";color:#d3c7b4;margin-right:10px;}

/* polaroid card grid */
.mabi-scrapbook-final .feed{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px 26px;align-items:start;}
.mabi-scrapbook-final .entry{display:block!important;min-height:0!important;border:0!important;border-radius:9px!important;overflow:visible!important;background:transparent!important;box-shadow:none!important;transform:none!important;transition:.18s ease;position:relative;}
.mabi-scrapbook-final .entry:hover{transform:translateY(-4px)!important;box-shadow:none!important}.mabi-scrapbook-final .entry::before{content:"";position:absolute;left:34%;right:34%;top:-11px;height:22px;z-index:4;border:0!important;border-radius:4px;background:rgba(171,205,221,.58);box-shadow:0 2px 7px rgba(94,77,55,.08);transform:rotate(-2deg);}
.mabi-scrapbook-final .entry:nth-child(4n+2)::before{background:rgba(231,172,186,.45);transform:rotate(2deg)}.mabi-scrapbook-final .entry:nth-child(4n+3)::before{background:rgba(241,217,151,.55);transform:rotate(-1deg)}.mabi-scrapbook-final .entry:nth-child(4n)::before{background:rgba(174,207,179,.55);transform:rotate(2.4deg)}
.mabi-scrapbook-final .entry::after{display:none!important}.mabi-scrapbook-final .image-wrap{width:100%!important;aspect-ratio:1.48/1!important;min-height:0!important;height:auto!important;border:13px solid rgba(255,255,255,.93)!important;border-bottom:0!important;border-radius:8px 8px 0 0!important;background:#f1eadc!important;box-shadow:0 14px 25px rgba(94,77,55,.12)!important;cursor:zoom-in;}
.mabi-scrapbook-final .image-wrap img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(.98) contrast(.99)}.mabi-scrapbook-final .image-wrap::after{display:none!important}
.mabi-scrapbook-final .entry-info{min-height:110px!important;margin:0!important;padding:15px 18px 17px!important;display:block!important;background:rgba(255,253,247,.94)!important;border:0!important;border-radius:0 0 8px 8px!important;box-shadow:0 16px 25px rgba(94,77,55,.11)!important;text-align:left!important;}
.mabi-scrapbook-final .entry-meta{margin:0!important;display:block!important}.mabi-scrapbook-final .issue{position:absolute;right:18px;bottom:82px;z-index:3;border-radius:3px!important;background:rgba(244,234,215,.92)!important;color:#6d625c!important;font-size:15px!important;font-weight:500!important;padding:9px 13px!important;box-shadow:0 3px 7px rgba(93,75,54,.10)!important;}
.mabi-scrapbook-final .date{display:none!important}.mabi-scrapbook-final .name{position:relative;display:block;padding-left:28px;color:#342f2c;font-size:24px!important;line-height:1.25!important;letter-spacing:.08em!important;font-weight:800!important;font-family:"Noto Serif TC","Source Han Serif TC",serif;margin:0 0 4px;}
.mabi-scrapbook-final .name::before{content:"";position:absolute;left:0;top:.48em;width:15px;height:15px;border-radius:50%;background:#78b1b5}.mabi-scrapbook-final .entry:nth-child(4n+2) .name::before{background:#e8b1a6}.mabi-scrapbook-final .entry:nth-child(4n+3) .name::before{background:#beb6a8}.mabi-scrapbook-final .entry:nth-child(4n) .name::before{background:#bca6a0}
.mabi-scrapbook-final .ko{margin:0 0 0 28px!important;color:#7f7973!important;font-size:17px!important;line-height:1.35!important;letter-spacing:.05em;font-family:"Noto Serif TC","Noto Sans KR",serif}.mabi-scrapbook-final .tw-pass-row,.mabi-scrapbook-final .pet-variants{display:none!important}.mabi-scrapbook-final .empty{grid-column:1/-1;border:1px dashed #d9cbb4;background:rgba(255,253,246,.82)}

@media(max-width:1120px){.mabi-scrapbook-final .wrap{width:min(100% - 42px,1120px)}.mabi-scrapbook-final .hero::before,.mabi-scrapbook-final .hero::after{opacity:.42}.mabi-scrapbook-final .hero-top{width:min(760px,100% - 220px)}.mabi-scrapbook-final .category-nav{grid-template-columns:repeat(4,minmax(0,1fr))}.mabi-scrapbook-final .feed{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:820px){.mabi-scrapbook-final .wrap{width:min(100% - 24px,980px)}.mabi-scrapbook-final .hero{padding:30px 0 24px}.mabi-scrapbook-final .hero::before,.mabi-scrapbook-final .hero::after{display:none}.mabi-scrapbook-final .hero-top{width:min(100% - 24px,760px)}.mabi-scrapbook-final .source-btn{position:static;margin-top:18px;width:100%}.mabi-scrapbook-final .category-nav{display:flex;overflow-x:auto;gap:10px;padding:2px 2px 8px;scrollbar-width:thin}.mabi-scrapbook-final .category{flex:0 0 150px;height:56px}.mabi-scrapbook-final .section-head{grid-template-columns:1fr;gap:12px}.mabi-scrapbook-final .section-heading-block{min-height:82px}.mabi-scrapbook-final .section-heading-block::before{width:210px;height:68px}.mabi-scrapbook-final .section-heading-block::after{font-size:15px;letter-spacing:.08em;padding-left:14px}.mabi-scrapbook-final .section-title{font-size:35px;left:26px}.mabi-scrapbook-final .section-actions{justify-content:flex-start;flex-wrap:wrap}.mabi-scrapbook-final .archive-tools{grid-template-columns:1fr;gap:12px;margin-top:0}.mabi-scrapbook-final .archive-count{justify-self:end}.mabi-scrapbook-final .feed{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 18px}}
@media(max-width:540px){.mabi-scrapbook-final h1{font-size:34px}.mabi-scrapbook-final h1::after{font-size:16px;letter-spacing:.08em}.mabi-scrapbook-final .subtitle{font-size:13px;letter-spacing:.12em}.mabi-scrapbook-final .cat-zh{font-size:16px}.mabi-scrapbook-final .section-heading-block{display:block;min-height:84px}.mabi-scrapbook-final .section-heading-block::before{display:block;width:220px;height:70px}.mabi-scrapbook-final .section-heading-block::after{display:none}.mabi-scrapbook-final .section-title{font-size:34px}.mabi-scrapbook-final .section-actions{display:grid;grid-template-columns:1fr 1fr;width:100%}.mabi-scrapbook-final .section-actions .predict-btn.show{grid-column:1/-1;justify-content:center}.mabi-scrapbook-final .sort,.mabi-scrapbook-final .predict-btn,.mabi-scrapbook-final .offline-pet-btn{height:48px;font-size:13px;padding:0 16px}.mabi-scrapbook-final .archive-search-wrap{height:56px}.mabi-scrapbook-final .archive-search-wrap span{width:58px;font-size:28px}.mabi-scrapbook-final #archiveSearch{font-size:15px}.mabi-scrapbook-final .feed{grid-template-columns:1fr;gap:24px}.mabi-scrapbook-final .issue{bottom:86px;font-size:13px!important}}
'''
if marker in text:
    text = re.sub(r'\n/\* mabi scrapbook final layout \*/[\s\S]*?\n(?=</style>)', css + '\n', text, count=1)
else:
    text = text.replace('\n</style>', css + '\n</style>', 1)

text = re.sub(r'\n<!-- mabi scrapbook final layout [^>]*-->', '', text)
text = text.replace('</html>', '\n<!-- mabi scrapbook final layout 2026-09-06 -->\n</html>')
INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Applied Mabinogi scrapbook final UI layout.')
