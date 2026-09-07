from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from repository root.')

text = INDEX.read_text(encoding='utf-8')

# Mark the document as using the new style.
text = re.sub(r'<html lang="zh-Hant"(?: class="[^"]*")?>', '<html lang="zh-Hant" class="paper-collage-ui">', text, count=1)

# Keep search placeholder simple, if the search patch exists.
text = text.replace('placeholder="搜尋中文名 / 韓文名 / 來源 / 期數 / 分類"', 'placeholder="搜尋中文名 / 韓文名"')
text = text.replace('placeholder="搜尋中文名／韓文名／來源／期數／分類"', 'placeholder="搜尋中文名 / 韓文名"')

marker = '/* paper collage sticky-note redesign */'
css = r'''

/* paper collage sticky-note redesign */
:root{
  --bg:#f3f4e9;
  --bg-2:#fbf7e8;
  --surface:#fffdf5;
  --surface-2:#f8f1df;
  --ink:#5c5149;
  --muted:#948b81;
  --line:#eadfca;
  --line-2:#ddcda9;
  --green:#78b797;
  --green-2:#6aa889;
  --green-3:#e6f4df;
  --gold:#e4b766;
  --gold-2:#c99a47;
  --berry:#d58aa3;
  --shadow:0 14px 30px rgba(122,105,82,.12);
  --shadow-deep:0 24px 60px rgba(116,99,78,.18);
}
html.paper-collage-ui body{
  color:var(--ink);
  background:
    radial-gradient(circle at 3% 5%, rgba(224,156,178,.32) 0 8px, transparent 9px),
    radial-gradient(circle at 7% 3%, rgba(145,190,218,.30) 0 7px, transparent 8px),
    radial-gradient(circle at 11% 6%, rgba(238,199,124,.28) 0 6px, transparent 7px),
    radial-gradient(circle at 91% 4%, rgba(168,203,154,.30) 0 7px, transparent 8px),
    radial-gradient(circle at 95% 7%, rgba(206,171,216,.28) 0 7px, transparent 8px),
    radial-gradient(circle at 98% 3%, rgba(238,184,185,.28) 0 6px, transparent 7px),
    linear-gradient(180deg,#f4f6e7 0%,#fffaf0 40%,#f4f7ea 100%);
  background-attachment:fixed;
}
html.paper-collage-ui body::before{
  content:"";
  position:fixed;
  inset:0;
  z-index:-1;
  pointer-events:none;
  opacity:.38;
  background-image:
    linear-gradient(90deg, rgba(117,101,82,.035) 1px, transparent 1px),
    linear-gradient(180deg, rgba(117,101,82,.03) 1px, transparent 1px);
  background-size:28px 28px;
  mask-image:linear-gradient(180deg,rgba(0,0,0,.65),rgba(0,0,0,.1));
}

.paper-collage-ui .wrap{width:min(1120px,calc(100% - 34px));}
.paper-collage-ui .hero{
  color:#75645c;
  margin:22px auto 0;
  width:min(1120px,calc(100% - 34px));
  padding:54px 28px 46px;
  border-radius:34px;
  border:1px solid rgba(227,215,192,.88);
  background:
    radial-gradient(ellipse at 18% 0%, rgba(190,225,161,.62), transparent 34%),
    radial-gradient(ellipse at 86% 16%, rgba(159,212,182,.55), transparent 34%),
    radial-gradient(ellipse at 48% 100%, rgba(223,236,183,.58), transparent 42%),
    rgba(255,254,248,.88);
  box-shadow:0 20px 48px rgba(130,111,88,.13);
}
.paper-collage-ui .hero::before{
  width:210px;height:72px;left:24px;top:18px;border:0;border-radius:999px;
  transform:rotate(-8deg);
  background:repeating-linear-gradient(90deg,rgba(126,194,157,.35) 0 12px,rgba(255,255,255,.55) 12px 23px);
  opacity:.75;
}
.paper-collage-ui .hero::after{
  width:230px;height:88px;right:26px;bottom:20px;border:0;border-radius:999px;
  transform:rotate(7deg);
  background:radial-gradient(circle, rgba(255,255,255,.85) 0 2px, transparent 3px), rgba(197,228,147,.48);
  background-size:18px 18px;
  opacity:.7;
}
.paper-collage-ui .hero-top{align-items:center;justify-content:center;text-align:center;display:block;}
.paper-collage-ui .eyebrow{
  border:0;
  background:transparent;
  color:#99918a;
  letter-spacing:.28em;
  box-shadow:none;
  padding:0;
  justify-content:center;
}
.paper-collage-ui .eyebrow::before,.paper-collage-ui .eyebrow::after{content:"";display:inline-block;width:26px;height:1px;background:#ddcfc0;vertical-align:middle;}
.paper-collage-ui h1{
  position:relative;
  display:inline-block;
  margin:18px 0 10px;
  color:#6d5c55;
  text-shadow:none;
  font-family:"Noto Serif TC","Noto Sans TC",serif;
  letter-spacing:.03em;
}
.paper-collage-ui h1::before{
  content:"";
  position:absolute;
  left:50%;top:-12px;
  width:118px;height:32px;
  transform:translateX(-50%) rotate(-2deg);
  border-radius:8px;
  background:rgba(213,138,163,.28);
  box-shadow:0 3px 10px rgba(144,101,112,.06);
  z-index:-1;
}
.paper-collage-ui h1::after{
  content:"";
  display:block;
  width:92px;height:4px;
  margin:16px auto 0;
  border-radius:999px;
  background:linear-gradient(90deg,#e7a6bd 0 24%,#f0c77b 24% 48%,#96cfa8 48% 72%,#93b8d7 72% 100%);
  opacity:.9;
}
.paper-collage-ui .source-btn{
  position:absolute;right:0;top:0;
  background:rgba(255,255,255,.58);
  color:#746862;
  border:1px solid #e2d6c1;
  border-radius:999px;
  box-shadow:0 7px 18px rgba(111,93,72,.08);
}

.paper-collage-ui .toolbar-shell{
  margin-top:16px;
  background:rgba(255,252,242,.78);
  border-top:1px solid rgba(236,226,209,.6);
  border-bottom:1px solid rgba(228,214,190,.75);
  backdrop-filter:blur(16px);
  box-shadow:0 8px 22px rgba(128,113,88,.06);
}
.paper-collage-ui .category-nav{justify-content:center;gap:10px;}
.paper-collage-ui .category,
.paper-collage-ui .sort,
.paper-collage-ui .predict-btn,
.paper-collage-ui .offline-pet-btn,
.paper-collage-ui .pet-filter-btn,
.paper-collage-ui .search-input,
.paper-collage-ui .search-box input{
  border-radius:999px;
  border:1px solid rgba(222,204,176,.95);
  background:rgba(255,255,255,.68);
  color:#665b54;
  box-shadow:0 8px 18px rgba(117,100,76,.07), inset 0 1px 0 rgba(255,255,255,.7);
}
.paper-collage-ui .category{height:39px;padding:0 15px;position:relative;}
.paper-collage-ui .category:nth-child(1){transform:rotate(-1.2deg);}
.paper-collage-ui .category:nth-child(2){transform:rotate(.8deg);}
.paper-collage-ui .category:nth-child(3){transform:rotate(-.6deg);}
.paper-collage-ui .category:nth-child(4){transform:rotate(1deg);}
.paper-collage-ui .category.active{
  color:#fff;
  border-color:transparent;
  background:linear-gradient(180deg,#95cfaa,#65af91);
  box-shadow:0 9px 19px rgba(104,166,135,.22);
}
.paper-collage-ui .category.active::after{
  content:"";
  position:absolute;
  left:20%;right:20%;top:-7px;height:12px;
  background:rgba(248,220,154,.54);
  border-radius:3px;
  transform:rotate(-2deg);
}

.paper-collage-ui main{padding-top:28px;}
.paper-collage-ui .section-head{
  align-items:center;
  padding:0 2px 8px;
  border-bottom:1px dashed rgba(211,194,166,.72);
}
.paper-collage-ui .section-title{
  color:#66564f;
  letter-spacing:.08em;
  font-family:"Noto Serif TC","Noto Sans TC",serif;
}
.paper-collage-ui .section-title::before{
  content:"";
  width:34px;height:34px;
  border-radius:50%;
  background:rgba(166,211,187,.72);
  box-shadow:16px 6px 0 rgba(237,204,134,.44), -10px 10px 0 rgba(222,156,178,.35);
}

.paper-collage-ui .feed{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:28px 24px;
  align-items:start;
}
.paper-collage-ui .entry{
  display:block;
  min-height:0;
  border:0;
  overflow:visible;
  border-radius:10px;
  background:transparent;
  box-shadow:none;
  transform:rotate(var(--tilt,0deg));
}
.paper-collage-ui .entry:nth-child(6n+1){--tilt:-1.2deg;}
.paper-collage-ui .entry:nth-child(6n+2){--tilt:.8deg;}
.paper-collage-ui .entry:nth-child(6n+3){--tilt:1.1deg;}
.paper-collage-ui .entry:nth-child(6n+4){--tilt:-.7deg;}
.paper-collage-ui .entry:nth-child(6n+5){--tilt:.4deg;}
.paper-collage-ui .entry:nth-child(6n){--tilt:-.4deg;}
.paper-collage-ui .entry:hover{transform:rotate(var(--tilt,0deg)) translateY(-4px);box-shadow:none;}
.paper-collage-ui .entry::before{
  content:"";
  position:absolute;
  left:28px;right:28px;top:-10px;height:20px;
  border:0;border-radius:4px;
  background:rgba(244,218,154,.54);
  box-shadow:0 2px 8px rgba(121,100,72,.08);
  transform:rotate(-2deg);
  z-index:3;
}
.paper-collage-ui .entry:nth-child(3n+2)::before{background:rgba(169,206,227,.48);transform:rotate(3deg);}
.paper-collage-ui .entry:nth-child(3n)::before{background:rgba(221,169,195,.42);transform:rotate(-3deg);}
.paper-collage-ui .entry::after{display:none;}
.paper-collage-ui .image-wrap{
  width:100%;
  aspect-ratio:408/340;
  min-height:0;
  border-radius:6px 6px 0 0;
  background:#f7f0e2;
  border:10px solid rgba(255,255,255,.92);
  border-bottom-width:8px;
  box-shadow:0 16px 30px rgba(105,91,72,.14);
}
.paper-collage-ui .image-wrap img{object-fit:cover;}
.paper-collage-ui .image-wrap::after{
  content:"zoom";
  background:rgba(255,255,255,.82);
  color:#8c8077;
  border:1px solid rgba(224,210,188,.8);
}
.paper-collage-ui .entry-info{
  margin:-1px 10px 0;
  padding:20px 18px 18px;
  min-height:168px;
  display:block;
  background:rgba(255,253,247,.93);
  border:1px solid rgba(232,220,200,.92);
  border-top:0;
  border-radius:0 0 16px 16px;
  box-shadow:0 15px 26px rgba(105,91,72,.10);
  text-align:center;
}
.paper-collage-ui .entry-meta{justify-content:center;margin-bottom:12px;}
.paper-collage-ui .issue{
  border-radius:9px;
  padding:7px 10px;
  background:#a8d3bb;
  color:#fff;
  box-shadow:none;
}
.paper-collage-ui .issue.limited{background:#e5b871;}
.paper-collage-ui .issue.collab{background:#b8a6d9;}
.paper-collage-ui .issue.regular{background:#a8d3bb;}
.paper-collage-ui .date{color:#a2988f;}
.paper-collage-ui .name{
  color:#695852;
  font-family:"Noto Serif TC","Noto Sans TC",serif;
  font-size:clamp(20px,2.1vw,27px);
  letter-spacing:.06em;
}
.paper-collage-ui .ko{
  color:#8bb9a3;
  font-size:13px;
  letter-spacing:.05em;
}
.paper-collage-ui .tw-pass-row,
.paper-collage-ui .pet-variants{
  text-align:left;
  border-radius:14px;
  background:rgba(250,247,235,.7);
}
.paper-collage-ui .pet-variant{background:rgba(255,255,255,.7);border-color:#eadfcc;}

.paper-collage-ui .source-modal,
.paper-collage-ui .prediction-modal,
.paper-collage-ui .viewer{backdrop-filter:blur(8px);}
.paper-collage-ui .source-panel,
.paper-collage-ui .prediction-panel{
  border-radius:26px;
  background:linear-gradient(180deg,#fffef9,#fbf5e9);
  border:1px solid #eadcca;
}
.paper-collage-ui .prediction-item{
  border:0;
  overflow:visible;
  background:rgba(255,253,247,.92);
  box-shadow:0 16px 30px rgba(105,91,72,.13);
  transform:rotate(-.4deg);
}
.paper-collage-ui .prediction-item:nth-child(even){transform:rotate(.5deg);}
.paper-collage-ui .prediction-item::before{
  left:30px;right:30px;top:-9px;bottom:auto;height:18px;border:0;border-radius:4px;background:rgba(244,218,154,.5);
}
.paper-collage-ui footer,
.paper-collage-ui .site-footer{
  color:#8f857c;
}

@media(max-width:980px){
  .paper-collage-ui .feed{grid-template-columns:repeat(2,minmax(0,1fr));}
}
@media(max-width:680px){
  .paper-collage-ui .wrap{width:min(100% - 22px,980px);}
  .paper-collage-ui .hero{width:min(100% - 22px,980px);margin-top:12px;padding:38px 18px 34px;border-radius:26px;}
  .paper-collage-ui .source-btn{position:relative;right:auto;top:auto;margin-top:18px;}
  .paper-collage-ui h1{font-size:clamp(28px,9vw,38px);}
  .paper-collage-ui .toolbar{padding:11px 0;}
  .paper-collage-ui .category-nav{justify-content:flex-start;flex-wrap:nowrap;overflow-x:auto;padding:2px 2px 7px;}
  .paper-collage-ui .category{height:38px;flex:0 0 auto;}
  .paper-collage-ui .feed{grid-template-columns:1fr;gap:23px;}
  .paper-collage-ui .entry{transform:none;}
  .paper-collage-ui .entry:hover{transform:translateY(-3px);}
  .paper-collage-ui .entry::before{left:58px;right:58px;}
  .paper-collage-ui .entry-info{min-height:0;margin:0 8px;padding:18px 16px;}
  .paper-collage-ui .name{font-size:23px;}
}
@media(max-width:390px){
  .paper-collage-ui .hero{padding:32px 14px 28px;}
  .paper-collage-ui .entry::before{left:42px;right:42px;}
  .paper-collage-ui .image-wrap{border-width:8px;border-bottom-width:7px;}
}
'''

if marker not in text:
    text = text.replace('\n</style>', css + '\n</style>', 1)
else:
    # Replace existing block if re-run after tweaks.
    text = re.sub(r'\n/\* paper collage sticky-note redesign \*/[\s\S]*?\n(?=</style>)', css + '\n', text, count=1)

# Make sure existing generated card images are lazy-loaded if render HTML is still using img tags.
text = text.replace('<img src="${item.image}" alt="${item.zh}" onerror="this.parentElement.classList.add(\'missing\')">', '<img src="${item.image}" alt="${item.zh}" loading="lazy" decoding="async" onerror="this.parentElement.classList.add(\'missing\')">')
text = text.replace('<img src="${item.image}" alt="${item.zh}">', '<img src="${item.image}" alt="${item.zh}" loading="lazy" decoding="async">')

text = re.sub(r'\n<!-- paper collage ui [^>]*-->', '', text)
text = text.replace('</html>', '\n<!-- paper collage ui 2026-09-05 -->\n</html>')

INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Applied paper collage sticky-note UI redesign.')
