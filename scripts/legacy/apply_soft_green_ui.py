from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from the repository root.')

text = INDEX.read_text(encoding='utf-8')

# Update search placeholder to the user's preferred concise wording if a search input exists.
text = re.sub(
    r'placeholder="[^"]*中文名\s*/\s*韓文名[^"]*"',
    'placeholder="搜尋中文名 / 韓文名"',
    text
)
text = re.sub(
    r'placeholder="[^"]*(?:搜尋|search)[^"]*"',
    'placeholder="搜尋中文名 / 韓文名"',
    text,
    flags=re.I
)

# Add a soft, cute presentation-inspired visual layer. Keep it as an end-of-style override so it does not
# rely on fragile line numbers from earlier patches.
marker = '/* soft green presentation UI redesign v1 */'
css = r'''

/* soft green presentation UI redesign v1 */
:root{
  --bg:#dfead2;
  --bg-2:#f5f8ee;
  --surface:#fffef8;
  --surface-2:#f3f8eb;
  --ink:#635651;
  --muted:#8a8176;
  --line:#d9e7c4;
  --line-2:#a8cf91;
  --green:#72bf8a;
  --green-2:#89d0a0;
  --green-3:#e8f5da;
  --gold:#b8d46b;
  --gold-2:#93bd55;
  --berry:#8b726b;
  --shadow:0 14px 28px rgba(96,126,79,.13);
  --shadow-deep:0 24px 60px rgba(92,119,80,.20);
}

body{
  color:var(--ink);
  background:
    radial-gradient(circle at 8% 7%, rgba(255,255,255,.72) 0 0.8px, transparent 1px) 0 0/22px 22px,
    radial-gradient(circle at 82% 18%, rgba(158,215,160,.24), transparent 28%),
    radial-gradient(circle at 16% 82%, rgba(195,226,137,.28), transparent 30%),
    linear-gradient(180deg,#dce8cf 0%,#eef6e5 46%,#f7f3e8 100%);
}

.wrap{width:min(1100px,calc(100% - 34px));}

.hero{
  margin:24px auto 0;
  width:min(1100px,calc(100% - 34px));
  border-radius:34px;
  overflow:hidden;
  color:#675752;
  padding:28px 0;
  background:
    radial-gradient(ellipse at 6% 5%, rgba(156,220,133,.58) 0 18%, transparent 19%),
    radial-gradient(ellipse at 94% 8%, rgba(130,203,153,.50) 0 16%, transparent 17%),
    radial-gradient(ellipse at 14% 96%, rgba(143,211,167,.42) 0 18%, transparent 19%),
    radial-gradient(ellipse at 83% 93%, rgba(188,227,127,.50) 0 16%, transparent 17%),
    linear-gradient(180deg,#fffffb 0%,#fbfff4 100%);
  border:12px solid rgba(233,242,216,.96);
  box-shadow:0 20px 55px rgba(95,130,76,.16);
}
.hero::before,.hero::after{display:none;}
.hero .wrap{width:min(980px,calc(100% - 36px));}
.hero-top{
  align-items:center;
  gap:24px;
}
.hero-text{
  position:relative;
  flex:1;
  text-align:center;
  padding:18px min(7vw,86px) 16px;
}
.hero-text::before,
.hero-text::after{
  content:"";
  position:absolute;
  width:132px;
  height:30px;
  border-radius:999px;
  opacity:.75;
  pointer-events:none;
}
.hero-text::before{left:2%;top:0;background:repeating-linear-gradient(90deg,#a3d89f 0 9px,#ffffff 9px 16px);transform:rotate(-4deg)}
.hero-text::after{right:1%;bottom:2px;background:radial-gradient(circle,#fff 0 2px,transparent 3px) 0 0/15px 15px,#bde979;transform:rotate(3deg)}
.eyebrow{
  background:#8b746f;
  color:#fff;
  border:0;
  box-shadow:0 7px 0 rgba(100,80,75,.16);
  border-radius:999px 999px 18px 18px;
  letter-spacing:.08em;
  text-transform:none;
}
h1{
  color:#6b5b55;
  text-shadow:none;
  font-family:"Noto Serif TC","Noto Sans TC","Microsoft JhengHei",serif;
  font-weight:950;
  letter-spacing:-.045em;
}
.sub{
  color:#8a8076;
  font-weight:800;
}
.source-btn{
  background:#fffdf7;
  color:#6f625c;
  border:2px solid #dce8c5;
  box-shadow:0 8px 0 rgba(155,190,126,.16);
}
.source-btn:hover{background:#f9fff0;border-color:#acd391;}

.toolbar-shell{
  background:rgba(230,241,213,.86);
  border-bottom:1px solid rgba(185,214,147,.55);
  backdrop-filter:blur(14px);
}
.toolbar{padding:12px 0;}
.category-nav{gap:9px;}
.category{
  color:#7a6a63;
  background:rgba(255,255,250,.72);
  border:2px solid rgba(207,226,181,.88);
  border-radius:999px;
  box-shadow:0 4px 0 rgba(139,190,119,.10);
}
.category:hover{background:#fbfff3;border-color:#acd995;transform:translateY(-1px);}
.category.active{
  color:#fff;
  background:linear-gradient(180deg,#8bd89f,#62bd83);
  border-color:#75c889;
  box-shadow:0 7px 0 rgba(76,150,96,.18);
}

main.wrap{padding-top:22px;}
.section-head{
  gap:14px;
  align-items:center;
  margin:0 0 18px;
  padding:16px 18px;
  background:rgba(255,255,250,.72);
  border:2px solid rgba(214,230,190,.9);
  border-radius:24px;
  box-shadow:var(--shadow);
}
.section-title{
  display:inline-flex;
  align-items:center;
  gap:8px;
  color:#6a5b55;
  font-family:"Noto Serif TC","Noto Sans TC",serif;
}
.section-title::before{content:"🌿";font-size:.82em;}
.section-note{color:#9a9287;}

.search-wrap,.search-area,.search-box-wrap,.archive-search,.search-panel{
  background:transparent !important;
}
input[type="search"], .search-input, #searchInput{
  min-height:42px;
  color:#665852;
  background:linear-gradient(180deg,#fffefa,#f7f3e6) !important;
  border:2px solid #dce9c6 !important;
  border-radius:999px !important;
  padding:0 42px 0 17px !important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 5px 0 rgba(164,195,127,.10) !important;
  outline:none;
}
input[type="search"]::placeholder,.search-input::placeholder,#searchInput::placeholder{color:#aaa196;}
input[type="search"]:focus,.search-input:focus,#searchInput:focus{
  border-color:#9ed38d !important;
  box-shadow:0 0 0 4px rgba(147,205,126,.18),inset 0 1px 0 rgba(255,255,255,.9) !important;
}
.sort{
  color:#6f625c;
  background:linear-gradient(180deg,#fffefa,#f5f2e6);
  border:2px solid #d9e8c0;
  border-radius:999px;
  box-shadow:0 5px 0 rgba(155,190,126,.12);
}
.predict-btn,.offline-pet-btn{
  color:#6d5f55;
  background:linear-gradient(180deg,#fffefa,#eef9df) !important;
  border:2px solid #cfe7ad !important;
  border-radius:999px;
  box-shadow:0 5px 0 rgba(155,190,126,.12) !important;
}
.predict-dot{background:#8ecb61;box-shadow:0 0 0 4px rgba(142,203,97,.17);}
.pet-filter-btn,.pet-filter{
  border-radius:999px !important;
  border:2px solid #dce8c3 !important;
  background:linear-gradient(180deg,#fffef8,#f2f7e7) !important;
  color:#76665e !important;
}
.pet-filter-btn.active,.pet-filter.active{
  background:linear-gradient(180deg,#8edda4,#65bf85) !important;
  color:#fff !important;
  border-color:#78c88d !important;
}

.feed{gap:18px;}
.entry{
  border:2px solid rgba(216,230,190,.96);
  border-radius:28px;
  background:
    radial-gradient(circle at 98% 5%, rgba(186,231,140,.38), transparent 18%),
    linear-gradient(180deg,#fffffb 0%,#fbf8ef 100%);
  box-shadow:var(--shadow);
  overflow:hidden;
}
.entry::before{
  inset:12px;
  border:1px dashed rgba(164,203,126,.44);
  border-radius:20px;
}
.entry:hover{
  transform:translateY(-2px);
  box-shadow:0 18px 40px rgba(92,121,77,.18);
}
.image-wrap{
  background:
    radial-gradient(circle at 18% 18%,rgba(255,255,255,.75),transparent 26%),
    linear-gradient(135deg,#eef7e7,#f7f5ea);
  border-right:2px solid rgba(220,232,197,.75);
}
.image-wrap img{filter:saturate(.98) contrast(.99);}
.image-wrap::after{
  background:rgba(255,255,248,.86);
  color:#87b66a;
  border:1px solid rgba(180,213,145,.65);
  border-radius:999px;
}
.entry-info{padding:28px 30px;}
.issue,.tw-pass-state,.pet-rarity{
  border-radius:999px;
}
.issue{
  background:#8d746e;
  color:#fff;
  box-shadow:0 3px 0 rgba(106,78,72,.12);
}
.date{color:#9b9287;}
.name{
  color:#6a5b55;
  font-family:"Noto Serif TC","Noto Sans TC",serif;
  letter-spacing:-.035em;
}
.ko{color:#7ab272;}
.origin{color:#91887e;}
.tw-pass-box,.pet-variants{
  background:rgba(246,250,238,.72);
  border-radius:18px;
  padding:12px;
  border-top:0;
}
.pet-variant{
  background:#fffef8;
  border:1px solid #e0e9cf;
  border-radius:999px;
}

.viewer.open,.source-modal.open,.prediction-modal.open{backdrop-filter:blur(7px);}
.source-panel,.prediction-panel{
  border:2px solid #dce8c5;
  border-radius:28px;
  background:linear-gradient(180deg,#fffef9,#f5f7ea);
}
.source-head,.prediction-head{
  background:rgba(255,254,248,.94);
}
.prediction-item{
  border:2px solid #dbe8c6;
  border-radius:24px;
  background:linear-gradient(180deg,#fffefa,#f8f7ee);
}
.prediction-item::before{border-style:dashed;border-color:rgba(166,204,126,.45);}
.prediction-level{background:#e7f6dc;color:#5a985c;}

footer,.footer{
  color:#897f76;
  background:rgba(255,255,250,.52);
  border-top:1px solid rgba(201,222,170,.72);
}

@media(max-width:760px){
  .wrap{width:min(100% - 22px,980px);}
  .hero{width:min(100% - 20px,980px);margin-top:14px;border-width:8px;border-radius:26px;padding:22px 0;}
  .hero .wrap{width:min(100% - 24px,980px);}
  .hero-top{display:block;}
  .hero-text{padding:14px 8px 12px;}
  .hero-text::before{width:94px;height:23px;left:0;top:-4px;}
  .hero-text::after{width:100px;height:24px;right:0;bottom:-4px;}
  .eyebrow{font-size:10px;padding:7px 11px;}
  h1{font-size:clamp(30px,9vw,42px);line-height:1.18;}
  .sub{font-size:13px;line-height:1.8;}
  .source-btn{margin-top:14px;width:100%;justify-content:center;}
  .toolbar-shell{top:0;}
  .category-nav{flex-wrap:nowrap;overflow-x:auto;padding:0 2px 7px;margin:0 -2px;scrollbar-width:thin;}
  .category{white-space:nowrap;flex:0 0 auto;height:38px;font-size:12px;padding:0 13px;}
  .section-head{display:block;padding:14px;border-radius:20px;margin-bottom:14px;}
  .section-title{font-size:23px;margin-bottom:10px;}
  input[type="search"],.search-input,#searchInput{width:100%;min-height:43px;}
  .entry{border-radius:22px;}
  .entry::before{inset:9px;border-radius:16px;}
  .image-wrap{border-right:0;border-bottom:2px solid rgba(220,232,197,.75);}
  .entry-info{padding:18px 17px 19px;}
  .name{font-size:22px;}
}

@media(max-width:430px){
  .hero{border-radius:22px;}
  .category{height:36px;padding:0 11px;}
  .section-head{padding:12px;}
  .name{font-size:21px;}
  .entry-meta{gap:6px;}
  .issue{font-size:10px;}
}
'''

if marker not in text:
    if '</style>' not in text:
        raise SystemExit('Could not find </style> in index.html.')
    text = text.replace('\n</style>', css + '\n</style>', 1)

# Add a small decorative meta class to the html tag, useful for future CSS targeting and visible in source.
text = text.replace('<html lang="zh-Hant">', '<html lang="zh-Hant" class="soft-green-ui">', 1)

# Bump marker for GitHub Pages redeploy.
text = re.sub(r'\n<!-- soft green UI redesign [^>]*-->', '', text)
text = text.replace('</html>', '\n<!-- soft green UI redesign 2026-09-05 -->\n</html>')

INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Applied soft green presentation-style UI redesign.')
