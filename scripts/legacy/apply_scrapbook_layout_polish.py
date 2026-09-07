from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from repository root.')

text = INDEX.read_text(encoding='utf-8')
text = re.sub(r'<html lang="zh-Hant" class="[^"]*">', '<html lang="zh-Hant" class="mabi-scrapbook-final">', text, count=1)
text = text.replace('<html lang="zh-Hant">', '<html lang="zh-Hant" class="mabi-scrapbook-final">')
text = re.sub(r'placeholder="[^"]*" autocomplete="off"', 'placeholder="搜尋中文名 / 韓文名" autocomplete="off"', text, count=1)
text = re.sub(r'\n/\* scrapbook layout polish v\d+ \*/[\s\S]*?(?=\n</style>)', '', text)

css = """

/* scrapbook layout polish v3 */
html.mabi-scrapbook-final{
  --paper-bg:#f6f2e8;--paper:#fffdf6;--paper-2:#fbf4e6;--ink:#514943;--muted:#8b8178;
  --sage:#78ad89;--sage-dark:#5f9b79;--pink:#efc9d1;--cream:#f4dfb2;--lav:#dbcaf1;--blue:#c8e3ec;--mint:#d5ece3;
}
html.mabi-scrapbook-final body{
  overflow-x:hidden;color:var(--ink);
  background:
    radial-gradient(circle at 7% 4%,rgba(140,185,160,.18) 0 7px,transparent 8px),
    radial-gradient(circle at 91% 5%,rgba(239,190,199,.16) 0 8px,transparent 9px),
    radial-gradient(circle at 96% 12%,rgba(153,189,211,.13) 0 6px,transparent 7px),
    linear-gradient(180deg,#f5f2e8 0%,#fbf7ee 42%,#f5f1e6 100%);
}
html.mabi-scrapbook-final body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.45;background-image:linear-gradient(90deg,rgba(108,92,74,.035) 1px,transparent 1px),linear-gradient(180deg,rgba(108,92,74,.03) 1px,transparent 1px);background-size:30px 30px;}
html.mabi-scrapbook-final .wrap{width:min(1280px,calc(100% - 64px));}
html.mabi-scrapbook-final .hero{width:100%;margin:0 auto;padding:34px 0 26px;min-height:0;border:0;border-radius:0;overflow:hidden;color:var(--ink);background:linear-gradient(90deg,rgba(197,224,213,.82) 0%,rgba(255,253,246,.92) 18%,rgba(255,253,246,.96) 78%,rgba(214,230,219,.78) 100%);box-shadow:none;}
html.mabi-scrapbook-final .hero .wrap{position:relative;width:min(1280px,calc(100% - 64px));}
html.mabi-scrapbook-final .hero::before,html.mabi-scrapbook-final .hero::after{display:none!important;}
html.mabi-scrapbook-final .hero-top{display:block;min-height:205px;position:relative;text-align:center;padding:10px 280px 8px;}
html.mabi-scrapbook-final .hero-top::before{content:"Stories\\A in Erinn";white-space:pre;position:absolute;left:0;top:8px;width:190px;height:118px;padding:24px 18px;text-align:left;font-size:20px;line-height:1.1;font-family:Georgia,serif;font-style:italic;color:#6f7f73;background:linear-gradient(135deg,#d9ede4,#b9d9cc);border:9px solid rgba(255,255,255,.9);border-radius:16px;box-shadow:0 13px 30px rgba(115,100,80,.13);transform:rotate(-5deg);}
html.mabi-scrapbook-final .hero-top::after{content:"在艾琳，\\A遇見更喜歡的自己。";white-space:pre;position:absolute;right:0;top:18px;width:245px;height:125px;padding:34px 28px 24px;text-align:left;font-size:17px;line-height:1.65;letter-spacing:.08em;color:#736961;background:rgba(255,252,241,.9);border:1px solid #e6d8be;border-radius:8px;box-shadow:0 12px 28px rgba(115,100,80,.12);transform:rotate(4deg);}
html.mabi-scrapbook-final .eyebrow{display:block;background:transparent!important;border:0!important;box-shadow:none!important;color:#81756d!important;padding:0!important;letter-spacing:.12em;font-size:20px;font-weight:700;opacity:.86;}
html.mabi-scrapbook-final .eyebrow::before{display:none!important;}
html.mabi-scrapbook-final h1{margin:8px auto 6px;max-width:720px;color:#36302e;font-size:clamp(48px,4.8vw,72px);line-height:1.05;text-align:center;letter-spacing:-.045em;text-shadow:none;}
html.mabi-scrapbook-final .subtitle{display:block!important;margin:12px auto 0!important;color:#867b73!important;font-size:16px!important;letter-spacing:.42em;max-width:520px;}
html.mabi-scrapbook-final .source-btn{position:absolute;right:0;top:0;height:52px;padding:0 24px;border-radius:999px;background:rgba(255,253,247,.86)!important;border:1px solid #dfd2ba!important;color:#675d56!important;box-shadow:0 10px 24px rgba(115,100,80,.10)!important;z-index:6;}
html.mabi-scrapbook-final .toolbar-shell{position:sticky;top:0;z-index:20;margin:0;background:rgba(255,252,244,.82);border-top:1px solid #eee4d5;border-bottom:1px solid #e5d8c5;backdrop-filter:blur(14px);}
html.mabi-scrapbook-final .toolbar{display:block;padding:14px 0;}
html.mabi-scrapbook-final .category-nav{display:grid;grid-template-columns:repeat(7,minmax(120px,1fr));gap:12px;justify-content:center;align-items:center;width:100%;}
html.mabi-scrapbook-final .category{height:58px;padding:0 12px;border:0!important;border-radius:8px!important;background:#fff;box-shadow:0 8px 18px rgba(111,95,72,.09);font-weight:900;color:#5b524c;letter-spacing:.12em;line-height:1.15;display:flex;align-items:center;justify-content:center;gap:8px;flex-direction:column;transform:none!important;}
html.mabi-scrapbook-final .category::before{font-size:24px;line-height:1;display:block;letter-spacing:0;}
html.mabi-scrapbook-final .category[data-type="pass"]{background:#87bc99;color:#fff;} html.mabi-scrapbook-final .category[data-type="pass"]::before{content:"🎫";}
html.mabi-scrapbook-final .category[data-type="lucky"]{background:#f3c9d3;} html.mabi-scrapbook-final .category[data-type="lucky"]::before{content:"🎁";}
html.mabi-scrapbook-final .category[data-type="package"]{background:#f2ddb0;} html.mabi-scrapbook-final .category[data-type="package"]::before{content:"👗";}
html.mabi-scrapbook-final .category[data-type="dye"]{background:#d9c8ed;} html.mabi-scrapbook-final .category[data-type="dye"]::before{content:"🎨";}
html.mabi-scrapbook-final .category[data-type="pet"]{background:#c8e3ec;} html.mabi-scrapbook-final .category[data-type="pet"]::before{content:"🐾";}
html.mabi-scrapbook-final .category[data-type="abyss"]{background:#d4e8e0;} html.mabi-scrapbook-final .category[data-type="abyss"]::before{content:"⛰";}
html.mabi-scrapbook-final .category[data-type="raid"]{background:#ead1d0;} html.mabi-scrapbook-final .category[data-type="raid"]::before{content:"🛡";}
html.mabi-scrapbook-final .category.active{outline:3px solid rgba(255,255,255,.78);box-shadow:0 7px 0 rgba(93,134,107,.20),0 11px 26px rgba(111,95,72,.13)!important;filter:saturate(1.05);}
html.mabi-scrapbook-final .category.active::after{display:none!important;}
html.mabi-scrapbook-final main.wrap{padding-top:34px;}
html.mabi-scrapbook-final .section-head{display:grid;grid-template-columns:auto 1fr;align-items:center;column-gap:34px;margin:0 0 26px;padding:0;border:0!important;background:transparent!important;box-shadow:none!important;}
html.mabi-scrapbook-final .section-heading-block{display:flex;align-items:center;gap:24px;min-width:0;}
html.mabi-scrapbook-final .section-heading-block::after{content:"踏上旅程，\\A收集途中閃耀的風景。";white-space:pre;color:#7e756e;font-size:17px;line-height:1.85;letter-spacing:.18em;border-left:1px solid #d8cbb8;padding-left:28px;}
html.mabi-scrapbook-final .section-title{position:relative;padding:18px 28px 16px 30px;background:rgba(255,252,244,.88);border:1px solid #e4d6bf;box-shadow:0 10px 22px rgba(111,95,72,.08);font-size:42px;line-height:1;font-weight:950;color:#302b29;letter-spacing:.08em;white-space:nowrap;}
html.mabi-scrapbook-final .section-title::before{content:""!important;position:absolute;left:-30px;top:-18px;width:78px;height:78px;background:rgba(139,188,158,.70);border-radius:4px;clip-path:polygon(0 14%,100% 0,86% 100%,0 86%);z-index:-1;box-shadow:none;}
html.mabi-scrapbook-final .section-title::after{content:"PASS";font-size:18px;letter-spacing:.38em;margin-left:14px;color:#756960;vertical-align:middle;}
html.mabi-scrapbook-final .section-actions{display:flex!important;justify-content:flex-end;align-items:center;gap:14px;grid-column:2;grid-row:2;margin:0;}
html.mabi-scrapbook-final .archive-tools{display:contents!important;}
html.mabi-scrapbook-final .archive-search-wrap{grid-column:1 / 2;grid-row:2;position:relative;display:flex;align-items:center;height:60px;max-width:700px;width:100%;margin:0;background:#fff;border:3px solid #cce1d0;border-radius:999px;box-shadow:inset 0 1px 0 rgba(255,255,255,.8),0 8px 18px rgba(111,95,72,.07);overflow:hidden;}
html.mabi-scrapbook-final .archive-search-wrap span{font-size:0;width:76px;height:100%;flex:0 0 76px;background:#e4f1e7;display:flex;align-items:center;justify-content:center;}
html.mabi-scrapbook-final .archive-search-wrap span::before{content:"⌕";font-size:34px;line-height:1;color:#5d635d;}
html.mabi-scrapbook-final #archiveSearch,html.mabi-scrapbook-final .archive-search{border:0!important;background:#fff!important;box-shadow:none!important;outline:none!important;width:100%;height:100%;padding:0 24px!important;font-size:17px;color:#58504a;font-weight:800;}
html.mabi-scrapbook-final #archiveSearch::placeholder{color:#9a948f;font-weight:800;}
html.mabi-scrapbook-final .archive-count{grid-column:2;grid-row:2;display:flex;align-items:center;margin:0;color:#625951;font-size:17px;font-weight:900;white-space:nowrap;}
html.mabi-scrapbook-final .archive-count::before{content:"›";margin-right:12px;color:#d9cdbb;}
html.mabi-scrapbook-final .sort,html.mabi-scrapbook-final .predict-btn,html.mabi-scrapbook-final .offline-pet-btn{height:58px;border:0!important;border-radius:999px!important;background:rgba(255,255,255,.82)!important;color:#5c534d!important;box-shadow:0 9px 20px rgba(111,95,72,.09), inset 0 1px 0 rgba(255,255,255,.8)!important;font-size:16px;font-weight:900;padding:0 24px!important;}
html.mabi-scrapbook-final .predict-btn.show{display:inline-flex!important;background:#7fb58f!important;color:#fff!important;min-width:190px;justify-content:center;}
html.mabi-scrapbook-final .predict-dot{display:none;}
html.mabi-scrapbook-final .feed{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr));gap:26px 24px;align-items:start;}
html.mabi-scrapbook-final .entry{display:block!important;min-height:0!important;overflow:visible!important;border:0!important;background:transparent!important;box-shadow:none!important;border-radius:8px!important;transform:none!important;}
html.mabi-scrapbook-final .entry:hover{transform:translateY(-3px)!important;box-shadow:none!important;}
html.mabi-scrapbook-final .entry::before{content:""!important;display:block!important;position:absolute;left:34%;right:34%;top:-12px;height:22px;border:0!important;border-radius:4px;background:rgba(177,208,227,.62);box-shadow:0 2px 5px rgba(94,79,60,.09);z-index:3;transform:rotate(-2deg);}
html.mabi-scrapbook-final .entry:nth-child(3n+2)::before{background:rgba(237,183,196,.55);transform:rotate(2deg);} html.mabi-scrapbook-final .entry:nth-child(3n)::before{background:rgba(188,216,190,.65);transform:rotate(-1deg);}
html.mabi-scrapbook-final .entry::after{display:none!important;}
html.mabi-scrapbook-final .image-wrap{width:100%!important;aspect-ratio:1.62/1!important;min-height:0!important;height:auto!important;border:12px solid rgba(255,255,255,.95)!important;border-bottom:0!important;border-radius:8px 8px 0 0!important;background:#f3eadb!important;box-shadow:0 14px 26px rgba(111,95,72,.12)!important;}
html.mabi-scrapbook-final .image-wrap img{width:100%;height:100%;object-fit:cover!important;display:block;}
html.mabi-scrapbook-final .entry-info{margin:0!important;padding:16px 18px 18px!important;min-height:122px!important;display:block!important;text-align:left!important;background:rgba(255,253,247,.96)!important;border:1px solid rgba(235,225,207,.92)!important;border-top:0!important;border-radius:0 0 8px 8px!important;box-shadow:0 15px 25px rgba(111,95,72,.10)!important;}
html.mabi-scrapbook-final .entry-meta{justify-content:space-between!important;margin:0 0 8px!important;}
html.mabi-scrapbook-final .issue{position:absolute!important;right:16px;top:calc(100% - 154px);z-index:5;background:#f4ead9!important;color:#6f625a!important;border-radius:4px!important;box-shadow:0 4px 10px rgba(111,95,72,.11)!important;font-size:14px!important;padding:8px 14px!important;}
html.mabi-scrapbook-final .date{display:none!important;}
html.mabi-scrapbook-final .name{font-size:23px!important;line-height:1.25!important;color:#3e3936!important;font-weight:950!important;letter-spacing:.04em!important;}
html.mabi-scrapbook-final .name::before{content:"";display:inline-block;width:15px;height:15px;border-radius:50%;background:#87bdc3;margin-right:10px;vertical-align:middle;}
html.mabi-scrapbook-final .ko{font-size:15px!important;color:#77716b!important;margin:4px 0 0 26px!important;font-weight:700!important;letter-spacing:.06em;}
@media(max-width:1180px){html.mabi-scrapbook-final .wrap,html.mabi-scrapbook-final .hero .wrap{width:min(100% - 36px,1080px);}html.mabi-scrapbook-final .hero-top{padding-left:220px;padding-right:220px;}html.mabi-scrapbook-final .hero-top::before{width:160px;height:100px;}html.mabi-scrapbook-final .hero-top::after{width:190px;height:108px;}html.mabi-scrapbook-final .category-nav{grid-template-columns:repeat(7,minmax(98px,1fr));gap:8px;}html.mabi-scrapbook-final .category{font-size:12px;padding:0 8px;}html.mabi-scrapbook-final .feed{grid-template-columns:repeat(3,minmax(0,1fr));}}
@media(max-width:820px){html.mabi-scrapbook-final .wrap,html.mabi-scrapbook-final .hero .wrap{width:min(100% - 24px,980px);}html.mabi-scrapbook-final .hero{padding:24px 0 20px;}html.mabi-scrapbook-final .hero-top{padding:0 0 4px;min-height:0;}html.mabi-scrapbook-final .hero-top::before,html.mabi-scrapbook-final .hero-top::after{display:none;}html.mabi-scrapbook-final .source-btn{position:static;margin-top:16px;height:44px;width:100%;}html.mabi-scrapbook-final .eyebrow{font-size:14px;}html.mabi-scrapbook-final h1{font-size:clamp(34px,9vw,48px);}html.mabi-scrapbook-final .subtitle{letter-spacing:.2em;font-size:13px!important;}html.mabi-scrapbook-final .category-nav{display:flex;overflow-x:auto;justify-content:flex-start;padding:2px 2px 9px;}html.mabi-scrapbook-final .category{flex:0 0 122px;height:52px;}html.mabi-scrapbook-final .section-head{display:block;margin-bottom:18px;}html.mabi-scrapbook-final .section-heading-block{display:block;}html.mabi-scrapbook-final .section-heading-block::after{display:block;border-left:0;padding-left:0;margin:12px 0 18px;font-size:14px;}html.mabi-scrapbook-final .section-title{font-size:34px;padding:16px 22px;}html.mabi-scrapbook-final .archive-tools{display:flex!important;flex-direction:column;gap:12px;margin-bottom:16px;}html.mabi-scrapbook-final .archive-search-wrap{max-width:none;height:54px;}html.mabi-scrapbook-final .section-actions{justify-content:space-between;flex-wrap:wrap;margin-bottom:12px;}html.mabi-scrapbook-final .sort,html.mabi-scrapbook-final .predict-btn{height:48px;font-size:14px;padding:0 18px!important;}html.mabi-scrapbook-final .archive-count{display:block;text-align:right;font-size:14px;}html.mabi-scrapbook-final .feed{grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 18px;}}
@media(max-width:540px){html.mabi-scrapbook-final .feed{grid-template-columns:1fr;}html.mabi-scrapbook-final .entry-info{min-height:0!important;}html.mabi-scrapbook-final .issue{top:calc(100% - 138px);}}
"""
text = text.replace('\n</style>', css + '\n</style>', 1)

fix = """
<script>/* scrapbook undefined search fix */
(function(){
  function cleanArchiveSearch(){
    const input=document.getElementById('archiveSearch');
    if(!input) return;
    input.placeholder='搜尋中文名 / 韓文名';
    if(input.value === 'undefined' || input.value === 'null'){
      input.value='';
      input.dispatchEvent(new Event('input', {bubbles:true}));
    }
  }
  document.addEventListener('DOMContentLoaded', cleanArchiveSearch);
  window.addEventListener('hashchange', function(){ setTimeout(cleanArchiveSearch, 0); });
  setTimeout(cleanArchiveSearch, 0);
})();
</script>
"""
if 'scrapbook undefined search fix' not in text:
    text = text.replace('\n</body>', fix + '\n</body>', 1)
text = re.sub(r'\n<!-- scrapbook final polish [^>]*-->', '', text)
text = text.replace('</html>', '\n<!-- scrapbook final polish 2026-09-06 -->\n</html>')
INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Applied scrapbook layout polish v3: header, category row, controls row, cards, and search undefined fix.')
