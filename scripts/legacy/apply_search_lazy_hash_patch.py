from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Run this from repository root.')

text = INDEX.read_text(encoding='utf-8')

# Clean old versions of this patch if re-run
text = re.sub(r'\n\s*<!-- search lazy hash patch [^>]*-->', '', text)

# 1) Add search input + result count near section header, only once
if 'id="archiveSearch"' not in text:
    # Insert inside section-head after the title/note block when possible
    pattern = re.compile(
        r'(<div class="section-head">\s*<div><div class="section-title" id="sectionTitle">[\s\S]*?<div class="section-note" id="sectionNote">[\s\S]*?</div></div>)',
        re.M
    )
    replacement = r'''\1
    <div class="archive-tools" id="archiveTools">
      <label class="archive-search-wrap" for="archiveSearch">
        <span>搜尋</span>
        <input id="archiveSearch" class="archive-search" type="search" placeholder="中文名 / 韓文名 / 來源 / 期數" autocomplete="off">
      </label>
      <div class="archive-count" id="archiveCount" aria-live="polite"></div>
    </div>'''
    text, count = pattern.subn(replacement, text, count=1)
    if count == 0:
        # Fallback: insert before feed
        text = text.replace('<section class="feed" id="feed"></section>', '''<div class="archive-tools" id="archiveTools">
      <label class="archive-search-wrap" for="archiveSearch">
        <span>搜尋</span>
        <input id="archiveSearch" class="archive-search" type="search" placeholder="中文名 / 韓文名 / 來源 / 期數" autocomplete="off">
      </label>
      <div class="archive-count" id="archiveCount" aria-live="polite"></div>
    </div>
  <section class="feed" id="feed"></section>''', 1)

# 2) Add CSS overrides
css_marker = '/* search lazy hash optimization patch */'
css = r'''

/* search lazy hash optimization patch */
.archive-tools{
  display:flex;
  align-items:center;
  justify-content:flex-end;
  gap:10px;
  margin-left:auto;
  flex-wrap:wrap;
}
.archive-search-wrap{
  display:flex;
  align-items:center;
  gap:8px;
  height:40px;
  padding:0 12px;
  border:1px solid rgba(199,184,150,.62);
  border-radius:14px;
  background:linear-gradient(180deg,#fffdf8,#f4ede0);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.65);
  color:#5b654f;
  font-size:12px;
  font-weight:950;
  white-space:nowrap;
}
.archive-search{
  width:min(290px,42vw);
  min-width:190px;
  border:0;
  outline:0;
  background:transparent;
  color:var(--ink);
  font-size:13px;
  font-weight:800;
}
.archive-search::placeholder{color:#9b967f;font-weight:700}
.archive-count{
  color:var(--muted);
  font-size:12px;
  font-weight:900;
  white-space:nowrap;
}
.empty-state{
  padding:34px 22px;
  border:1px dashed var(--line-2);
  border-radius:18px;
  background:rgba(255,253,248,.62);
  color:var(--muted);
  text-align:center;
  font-weight:900;
  line-height:1.8;
}
.category:focus-visible,.sort:focus-visible,.archive-search:focus-visible,.predict-btn:focus-visible,.source-btn:focus-visible{
  outline:3px solid rgba(184,144,69,.28);
  outline-offset:2px;
}
@media(max-width:680px){
  .archive-tools{
    width:100%;
    justify-content:space-between;
    margin:8px 0 0;
  }
  .archive-search-wrap{
    flex:1 1 100%;
    width:100%;
  }
  .archive-search{
    width:100%;
    min-width:0;
  }
  .archive-count{font-size:11px}
}
'''
if css_marker not in text:
    text = text.replace('\n</style>', css + '\n</style>', 1)

# 3) Patch state to include query if possible
text = re.sub(
    r"const\s+state\s*=\s*\{\s*type\s*:\s*'([^']+)'\s*,\s*sort\s*:\s*'([^']+)'\s*\}\s*;",
    r"const state={type:'\1',sort:'\2',query:''};",
    text,
    count=1
)
if 'const state=' in text and 'query:' not in text.split('const state=',1)[1].split(';',1)[0]:
    text = text.replace("const state={type:'pass',sort:'old'};", "const state={type:'pass',sort:'old',query:''};")

# 4) Add helper functions before render()
helper_marker = 'function normalizeSearchText('
helpers = r'''
function normalizeSearchText(value){
  return String(value ?? '').toLowerCase().replace(/\s+/g,' ').trim();
}
function itemSearchText(item){
  return normalizeSearchText([
    item.id,item.type,LABELS[item.type],item.zh,item.ko,item.origin,item.kind,item.date,item.number,
    Array.isArray(item.variants)?item.variants.map(v=>[v.name,v.rarity,v.note].join(' ')).join(' '):''
  ].join(' '));
}
function currentHash(){
  const params=new URLSearchParams(location.hash.replace(/^#/,''));
  return params;
}
function applyHashToState(){
  const params=currentHash();
  const type=params.get('type') || location.hash.replace(/^#/, '').split('&')[0];
  if(type && LABELS[type]) state.type=type;
  const sort=params.get('sort');
  if(sort==='old'||sort==='new') state.sort=sort;
  const q=params.get('q');
  if(q!==null) state.query=q;
  const sortEl=document.getElementById('sort');
  if(sortEl) sortEl.value=state.sort;
  const searchEl=document.getElementById('archiveSearch');
  if(searchEl) searchEl.value=state.query;
}
function updateHash(replace=false){
  const params=new URLSearchParams();
  params.set('type',state.type);
  if(state.sort!=='old') params.set('sort',state.sort);
  if(state.query) params.set('q',state.query);
  const next='#'+params.toString();
  if(location.hash!==next){
    if(replace) history.replaceState(null,'',next); else history.pushState(null,'',next);
  }
}
function updateActiveCategory(){
  document.querySelectorAll('.category').forEach(btn=>{
    btn.classList.toggle('active',btn.dataset.type===state.type);
  });
}
'''
if helper_marker not in text:
    text = text.replace('function render(){', helpers + '\nfunction render(){', 1)

# 5) Patch render filtering/count/lazy img. This is intentionally conservative.
# Replace rows filter line with query-aware version.
text = re.sub(
    r"let\s+rows\s*=\s*DATA\.filter\(x=>x\.type===state\.type\);",
    "let rows=DATA.filter(x=>x.type===state.type);\n  const query=normalizeSearchText(state.query||'');\n  if(query) rows=rows.filter(item=>itemSearchText(item).includes(query));",
    text,
    count=1
)
# Add active category call at render start
if "updateActiveCategory();" not in text:
    text = text.replace("function render(){\n", "function render(){\n  updateActiveCategory();\n", 1)
# Update count after sort line
if "archiveCount" not in text.split('function render(){',1)[1].split('const feed',1)[0]:
    text = text.replace(
        "rows.sort((a,b)=>{const d=a.date.localeCompare(b.date)||Number(a.number)-Number(b.number);return state.sort==='old'?d:-d;});",
        "rows.sort((a,b)=>{const d=a.date.localeCompare(b.date)||Number(a.number)-Number(b.number);return state.sort==='old'?d:-d;});\n  const countEl=document.getElementById('archiveCount');\n  if(countEl) countEl.textContent=query?`找到 ${rows.length} 筆`:`共 ${rows.length} 筆`;",
        1
    )
# Ensure image tags in template add lazy/async. Do not affect viewer image too much; ok but mostly card templates.
text = text.replace('<img src="${item.image}" alt="${item.zh}" onerror="this.style.display=\'none\'">', '<img src="${item.image}" alt="${item.zh}" loading="lazy" decoding="async" onerror="this.style.display=\'none\'">')
text = text.replace('<img src="${item.image}" alt="${item.zh}">', '<img src="${item.image}" alt="${item.zh}" loading="lazy" decoding="async">')
text = text.replace('<img src="${p.image}" alt="${p.zh}">', '<img src="${p.image}" alt="${p.zh}" loading="lazy" decoding="async">')
# Add empty state after feed render if known pattern present
if 'class="empty-state"' not in text:
    # after feed.innerHTML assignment close ; add empty fallback
    text = re.sub(
        r"(feed\.innerHTML\s*=\s*rows\.map\([\s\S]*?\)\.join\(''\);)",
        r"\1\n  if(!rows.length){feed.innerHTML=`<div class=\"empty-state\">沒有找到符合「${state.query||''}」的資料</div>`;}",
        text,
        count=1
    )

# 6) Patch category/sort event handlers to sync hash
# Common category handler patterns: replace state.type=...; render();
text = re.sub(
    r"state\.type\s*=\s*btn\.dataset\.type\s*;\s*render\(\)\s*;",
    "state.type=btn.dataset.type;\n    state.query='';\n    const searchEl=document.getElementById('archiveSearch'); if(searchEl) searchEl.value='';\n    updateHash();\n    render();",
    text
)
text = re.sub(
    r"state\.sort\s*=\s*this\.value\s*;\s*render\(\)\s*;",
    "state.sort=this.value;\n  updateHash();\n  render();",
    text
)
text = re.sub(
    r"state\.sort\s*=\s*e\.target\.value\s*;\s*render\(\)\s*;",
    "state.sort=e.target.value;\n  updateHash();\n  render();",
    text
)

# 7) Add search and hash event init near DOMContentLoaded or before final render call
init_marker = 'archiveSearch.addEventListener'
init_js = r'''
const archiveSearch=document.getElementById('archiveSearch');
if(archiveSearch){
  let searchTimer=null;
  archiveSearch.addEventListener('input',e=>{
    state.query=e.target.value.trim();
    clearTimeout(searchTimer);
    searchTimer=setTimeout(()=>updateHash(),180);
    render();
  });
}
window.addEventListener('hashchange',()=>{applyHashToState();render();});
applyHashToState();
updateHash(true);
'''
if init_marker not in text:
    # Insert before the last standalone render(); if present
    matches = list(re.finditer(r'\brender\(\);', text))
    if matches:
        m = matches[-1]
        text = text[:m.start()] + init_js + '\n' + text[m.start():]
    else:
        text = text.replace('</script>', init_js + '\nrender();\n</script>', 1)

# 8) Make category button clicks update active state even if original handler only toggled classes.
# No further changes needed if render calls updateActiveCategory.

# 9) Bump deploy marker
text = text.replace('</html>', '\n<!-- search lazy hash patch 2026-09-05 -->\n</html>')

INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Applied search + lazy loading + hash URL patch.')
