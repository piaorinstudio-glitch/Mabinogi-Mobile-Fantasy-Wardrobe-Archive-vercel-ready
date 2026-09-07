from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from the repository root.')

text = INDEX.read_text(encoding='utf-8')

# Ensure the final scrapbook UI class is present without duplicating unrelated classes.
text = re.sub(r'<html lang="zh-Hant"[^>]*>', '<html lang="zh-Hant" class="mabi-scrapbook-final">', text, count=1)

# Clean accidental visible undefined values in the search box.
text = text.replace('value="undefined"', 'value=""')
text = text.replace('placeholder="undefined"', 'placeholder="搜尋中文名 / 韓文名"')
text = text.replace('placeholder="搜尋中文名 / 韓文名"', 'placeholder="搜尋中文名 / 韓文名"')

marker = '/* scrapbook tight layout fix v2 */'
css = r'''

/* scrapbook tight layout fix v2 */
html.mabi-scrapbook-final body{
  min-width:0;
  overflow-x:hidden;
}

html.mabi-scrapbook-final main.wrap{
  width:min(1120px,calc(100% - 34px)) !important;
  padding-top:30px !important;
}

html.mabi-scrapbook-final .section-head{
  display:grid !important;
  grid-template-columns:minmax(0,1fr) auto !important;
  grid-template-areas:"title actions" !important;
  align-items:center !important;
  column-gap:28px !important;
  row-gap:12px !important;
  width:100% !important;
  min-height:0 !important;
  margin:0 0 20px !important;
  padding:0 !important;
  border:0 !important;
  border-radius:0 !important;
  background:transparent !important;
  box-shadow:none !important;
}

html.mabi-scrapbook-final .section-heading-block{
  grid-area:title !important;
  display:flex !important;
  align-items:center !important;
  gap:24px !important;
  min-width:0 !important;
}

html.mabi-scrapbook-final .section-title{
  display:inline-flex !important;
  align-items:center !important;
  justify-content:center !important;
  gap:16px !important;
  flex:0 0 auto !important;
  min-width:260px !important;
  min-height:70px !important;
  padding:15px 32px 16px !important;
  color:#4f4742 !important;
  font-size:clamp(34px,4.3vw,48px) !important;
  line-height:1 !important;
  letter-spacing:.08em !important;
  font-weight:950 !important;
  background:rgba(255,253,246,.82) !important;
  border:1px solid rgba(221,204,175,.95) !important;
  box-shadow:0 12px 30px rgba(117,99,77,.08) !important;
  transform:rotate(-.8deg) !important;
  white-space:nowrap !important;
}

html.mabi-scrapbook-final .section-title::before{
  display:none !important;
}

html.mabi-scrapbook-final .section-title::after{
  content:"PASS";
  margin-left:4px;
  color:#75665d;
  font-family:Georgia,"Times New Roman",serif;
  font-size:.46em;
  letter-spacing:.32em;
  font-weight:800;
}

html.mabi-scrapbook-final .section-note{
  display:block !important;
  margin:0 !important;
  max-width:360px !important;
  color:#91877d !important;
  font-size:18px !important;
  line-height:1.9 !important;
  letter-spacing:.12em !important;
  white-space:pre-line !important;
}

html.mabi-scrapbook-final .section-actions{
  grid-area:actions !important;
  display:flex !important;
  align-items:center !important;
  justify-content:flex-end !important;
  gap:12px !important;
  margin:0 !important;
  width:auto !important;
  min-width:0 !important;
  flex-wrap:nowrap !important;
}

html.mabi-scrapbook-final .section-actions .sort,
html.mabi-scrapbook-final .section-actions .predict-btn,
html.mabi-scrapbook-final .section-actions .offline-pet-btn{
  height:52px !important;
  border-radius:999px !important;
  padding:0 22px !important;
  border:0 !important;
  background:rgba(255,255,255,.78) !important;
  color:#655b53 !important;
  box-shadow:0 10px 25px rgba(111,94,72,.10), inset 0 1px 0 rgba(255,255,255,.86) !important;
  font-size:14px !important;
  font-weight:900 !important;
  white-space:nowrap !important;
}

html.mabi-scrapbook-final .section-actions .sort{
  min-width:120px !important;
  max-width:none !important;
  margin-left:0 !important;
  appearance:auto !important;
}

html.mabi-scrapbook-final .section-actions .predict-btn.show{
  display:inline-flex !important;
  background:linear-gradient(180deg,#83bd93,#609f77) !important;
  color:#fff !important;
}

html.mabi-scrapbook-final .archive-tools{
  display:grid !important;
  grid-template-columns:minmax(300px,660px) minmax(12px,1fr) auto !important;
  align-items:center !important;
  gap:16px !important;
  width:100% !important;
  margin:0 0 26px !important;
  padding:0 !important;
  border:0 !important;
  background:transparent !important;
  box-shadow:none !important;
  transform:none !important;
  clear:both !important;
}

html.mabi-scrapbook-final .archive-search-wrap{
  grid-column:1 !important;
  position:relative !important;
  display:block !important;
  width:100% !important;
  height:58px !important;
  margin:0 !important;
  padding:0 !important;
  border:0 !important;
  background:transparent !important;
  box-shadow:none !important;
}

html.mabi-scrapbook-final .archive-search-wrap > span{
  display:none !important;
}

html.mabi-scrapbook-final .archive-search-wrap::before{
  content:"⌕";
  position:absolute;
  left:0;
  top:0;
  z-index:2;
  width:70px;
  height:58px;
  display:flex;
  align-items:center;
  justify-content:center;
  color:#5d7066;
  font-size:34px;
  border-radius:999px 0 0 999px;
  background:rgba(221,239,226,.82);
  pointer-events:none;
}

html.mabi-scrapbook-final #archiveSearch,
html.mabi-scrapbook-final .archive-search{
  display:block !important;
  width:100% !important;
  height:58px !important;
  min-height:58px !important;
  margin:0 !important;
  padding:0 26px 0 92px !important;
  border:3px solid rgba(196,224,207,.95) !important;
  border-radius:999px !important;
  background:rgba(255,255,255,.82) !important;
  color:#5f554e !important;
  box-shadow:0 12px 28px rgba(122,105,82,.08), inset 0 1px 0 rgba(255,255,255,.92) !important;
  font-size:17px !important;
  font-weight:850 !important;
  outline:none !important;
}

html.mabi-scrapbook-final #archiveSearch::placeholder,
html.mabi-scrapbook-final .archive-search::placeholder{
  color:#968e86 !important;
  opacity:1 !important;
}

html.mabi-scrapbook-final .archive-count{
  grid-column:3 !important;
  display:flex !important;
  align-items:center !important;
  justify-content:flex-end !important;
  min-width:92px !important;
  margin:0 !important;
  padding:0 !important;
  color:#6d625a !important;
  font-size:15px !important;
  font-weight:900 !important;
  white-space:nowrap !important;
  align-self:center !important;
}

html.mabi-scrapbook-final .archive-count::before{
  content:"›";
  margin-right:10px;
  color:#d4c6ad;
  font-size:18px;
}

html.mabi-scrapbook-final .feed{
  display:grid !important;
  grid-template-columns:repeat(4,minmax(0,1fr)) !important;
  gap:28px 24px !important;
  align-items:start !important;
}

html.mabi-scrapbook-final .entry{
  width:100% !important;
  min-width:0 !important;
}

@media(max-width:1180px){
  html.mabi-scrapbook-final main.wrap{width:min(100% - 28px,1040px) !important;}
  html.mabi-scrapbook-final .feed{grid-template-columns:repeat(3,minmax(0,1fr)) !important;}
  html.mabi-scrapbook-final .section-title{min-width:230px !important;font-size:clamp(31px,4vw,42px) !important;}
}

@media(max-width:900px){
  html.mabi-scrapbook-final .section-head{
    grid-template-columns:1fr !important;
    grid-template-areas:"title" "actions" !important;
    gap:14px !important;
  }
  html.mabi-scrapbook-final .section-heading-block{
    flex-wrap:wrap !important;
    gap:12px 18px !important;
  }
  html.mabi-scrapbook-final .section-actions{
    justify-content:flex-start !important;
    width:100% !important;
  }
  html.mabi-scrapbook-final .archive-tools{
    grid-template-columns:minmax(0,1fr) auto !important;
    gap:12px !important;
  }
  html.mabi-scrapbook-final .archive-search-wrap{grid-column:1 !important;}
  html.mabi-scrapbook-final .archive-count{grid-column:2 !important;min-width:auto !important;}
  html.mabi-scrapbook-final .feed{grid-template-columns:repeat(2,minmax(0,1fr)) !important;}
}

@media(max-width:640px){
  html.mabi-scrapbook-final main.wrap{width:min(100% - 20px,980px) !important;padding-top:22px !important;}
  html.mabi-scrapbook-final .section-heading-block{display:block !important;}
  html.mabi-scrapbook-final .section-title{
    width:100% !important;
    min-width:0 !important;
    min-height:58px !important;
    padding:12px 18px !important;
    font-size:34px !important;
    transform:none !important;
  }
  html.mabi-scrapbook-final .section-note{
    margin-top:12px !important;
    font-size:14px !important;
    line-height:1.7 !important;
    letter-spacing:.08em !important;
  }
  html.mabi-scrapbook-final .section-actions{
    display:grid !important;
    grid-template-columns:1fr auto !important;
    gap:10px !important;
  }
  html.mabi-scrapbook-final .section-actions .sort{grid-column:2 !important;height:44px !important;padding:0 16px !important;}
  html.mabi-scrapbook-final .section-actions .predict-btn.show{grid-column:1 !important;height:44px !important;justify-content:center !important;}
  html.mabi-scrapbook-final .archive-tools{
    grid-template-columns:1fr !important;
    gap:9px !important;
    margin-bottom:20px !important;
  }
  html.mabi-scrapbook-final .archive-search-wrap{grid-column:1 !important;height:52px !important;}
  html.mabi-scrapbook-final .archive-search-wrap::before{width:58px;height:52px;font-size:28px;}
  html.mabi-scrapbook-final #archiveSearch,
  html.mabi-scrapbook-final .archive-search{
    height:52px !important;
    min-height:52px !important;
    padding-left:74px !important;
    font-size:15px !important;
  }
  html.mabi-scrapbook-final .archive-count{
    grid-column:1 !important;
    justify-content:flex-start !important;
    font-size:13px !important;
  }
  html.mabi-scrapbook-final .feed{grid-template-columns:1fr !important;gap:22px !important;}
}
'''

if marker in text:
    text = re.sub(r'\n/\* scrapbook tight layout fix v2 \*/[\s\S]*?(?=\n</style>)', css, text, count=1)
else:
    text = text.replace('\n</style>', css + '\n</style>', 1)

# Runtime guard: some older hash/search patch versions can accidentally write undefined into input.
js_marker = '/* scrapbook search undefined guard */'
js = r'''

/* scrapbook search undefined guard */
(function(){
  function cleanSearch(){
    const input=document.getElementById('archiveSearch');
    if(!input) return;
    if(input.value==='undefined'||input.value==='null') input.value='';
    if(!input.getAttribute('placeholder') || input.getAttribute('placeholder')==='undefined'){
      input.setAttribute('placeholder','搜尋中文名 / 韓文名');
    }
  }
  cleanSearch();
  document.addEventListener('DOMContentLoaded', cleanSearch);
  window.addEventListener('hashchange', function(){ setTimeout(cleanSearch,0); });
  const observer=new MutationObserver(cleanSearch);
  observer.observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['value','placeholder']});
})();
'''
if js_marker not in text:
    text = text.replace('\n</script>', js + '\n</script>', 1)

text = re.sub(r'\n<!-- scrapbook tight layout fix [^>]*-->', '', text)
text = text.replace('</html>', '\n<!-- scrapbook tight layout fix 2026-09-06 -->\n</html>')

INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Applied scrapbook tight layout fix: compact title/actions/search/count/card grid, and search undefined guard.')
