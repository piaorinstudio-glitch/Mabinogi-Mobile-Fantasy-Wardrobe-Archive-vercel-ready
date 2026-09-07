from pathlib import Path

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from the repository root.')

text = INDEX.read_text(encoding='utf-8')

css_marker = '/* responsive layout + pet availability filters */'
css = r'''

/* responsive layout + pet availability filters */
:root{
  --pet-filter-regular:#3f6751;
  --pet-filter-limited:#a7772f;
  --pet-filter-collab:#b86642;
  --pet-filter-collab-2:#884e38;
}
.wrap{width:min(1120px,calc(100% - 28px));}
.toolbar{flex-wrap:wrap;align-items:center;row-gap:10px;}
.category-nav{min-width:0;}
.sort{margin-left:auto;}
.section-head{
  align-items:center;
  flex-wrap:wrap;
  margin:4px 0 16px;
}
.pet-filter-bar{
  display:none;
  align-items:center;
  gap:8px;
  flex-wrap:wrap;
  margin-left:auto;
}
.pet-filter-bar.show{display:flex;}
.pet-filter{
  height:34px;
  border:1px solid #d2c4a8;
  border-radius:999px;
  padding:0 12px;
  background:linear-gradient(180deg,#fffef9,#f3ecdf);
  color:#3a3a34;
  font-size:12px;
  font-weight:950;
  cursor:pointer;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.78),0 2px 6px rgba(49,59,48,.06);
  transition:transform .15s ease, box-shadow .15s ease, border-color .15s ease, background .15s ease;
  white-space:nowrap;
}
.pet-filter:hover{transform:translateY(-1px);border-color:#b99f72;box-shadow:0 5px 13px rgba(49,59,48,.10);}
.pet-filter.active{color:#fff;border-color:#4f694f;background:linear-gradient(180deg,#4c7055,#325c4d);}
.pet-filter[data-pet="limited"].active{border-color:#a7772f;background:linear-gradient(180deg,#c99a4a,#9a6a24);}
.pet-filter[data-pet="collab"]{
  border-color:#d2a18e;
  color:#694335;
  background:linear-gradient(180deg,#fff6ef,#f6e6db);
}
.pet-filter[data-pet="collab"].active{
  border-color:var(--pet-filter-collab-2);
  color:#fff;
  background:linear-gradient(180deg,var(--pet-filter-collab),var(--pet-filter-collab-2));
  box-shadow:0 4px 14px rgba(136,78,56,.18);
}
.issue.collab{background:linear-gradient(180deg,var(--pet-filter-collab),var(--pet-filter-collab-2)) !important;box-shadow:0 3px 10px rgba(136,78,56,.18) !important;}
.feed{gap:18px;}
.entry{grid-template-columns:minmax(280px,38%) minmax(0,1fr);min-height:286px;}
.image-wrap{height:100%;min-height:260px;}
.image-wrap img{object-position:center center;}
.entry-info{padding:30px clamp(22px,3vw,36px);}
.entry-meta{gap:8px 10px;}
.name{max-width:100%;}
.ko{max-width:100%;}
.pet-variants{gap:7px;}
.pet-variant{max-width:100%;}

@media(min-width:1180px){
  .entry{grid-template-columns:390px minmax(0,1fr);}
  .image-wrap{min-height:300px;}
}
@media(max-width:900px){
  .wrap{width:min(100% - 24px,980px);}
  .hero{padding:34px 0 28px;}
  .toolbar{align-items:flex-start;}
  .category-nav{flex:1 1 100%;order:1;flex-wrap:nowrap;overflow-x:auto;overscroll-behavior-x:contain;padding-bottom:4px;scrollbar-width:thin;}
  .category{flex:0 0 auto;white-space:nowrap;}
  .predict-btn,.offline-pet-btn,.sort{order:2;}
  .sort{margin-left:0;}
  main{padding-top:18px;}
  .entry{grid-template-columns:44% minmax(0,1fr);min-height:230px;border-radius:18px;}
  .image-wrap{min-height:230px;}
  .entry-info{padding:22px 20px;}
  .name{font-size:clamp(22px,3.5vw,28px);}
}
@media(max-width:680px){
  .wrap{width:min(100% - 18px,980px);}
  .hero-top{display:block;}
  .source-btn{margin-top:16px;}
  h1{font-size:clamp(29px,8vw,40px);}
  .toolbar-shell{position:sticky;top:0;}
  .toolbar{padding:10px 0;gap:8px;}
  .category-nav{margin:0 -2px;padding:0 2px 5px;}
  .category,.sort,.predict-btn{height:38px;font-size:12px;border-radius:11px;}
  .sort{max-width:118px;}
  .section-head{display:block;margin:0 0 12px;}
  .section-title{font-size:23px;margin-bottom:10px;}
  .pet-filter-bar{margin-left:0;width:100%;flex-wrap:nowrap;overflow-x:auto;padding:1px 0 6px;scrollbar-width:thin;}
  .pet-filter{flex:0 0 auto;height:33px;padding:0 12px;}
  .feed{gap:13px;}
  .entry{display:block;border-radius:18px;min-height:0;}
  .entry::before{inset:8px;border-radius:13px;}
  .image-wrap{width:100%;aspect-ratio:408/340;min-height:0;height:auto;}
  .image-wrap::after{opacity:1;transform:none;font-size:10px;padding:5px 8px;right:10px;bottom:10px;}
  .entry-info{padding:17px 17px 18px;}
  .entry-meta{margin-bottom:9px;}
  .issue{font-size:10px;padding:5px 8px;}
  .date{font-size:11px;}
  .name{font-size:22px;line-height:1.28;}
  .ko{font-size:13px;margin-top:5px;}
  .pet-variants{margin-top:12px;padding-top:11px;display:grid;grid-template-columns:1fr;gap:6px;}
  .pet-variant{justify-content:flex-start;font-size:10px;padding:6px 7px;}
  .tw-pass-row{display:block;font-size:11px;}
  .tw-pass-state{display:inline-flex;margin-left:0;margin-top:7px;}
}
@media(max-width:380px){
  .wrap{width:min(100% - 14px,980px);}
  .category,.sort,.predict-btn{font-size:11px;padding:0 9px;}
  .entry-info{padding:15px 14px 16px;}
  .name{font-size:20px;}
}
'''
if css_marker not in text:
    text = text.replace('\n</style>', css + '\n</style>', 1)

# Add pet filter state.
text = text.replace(
    "const state={type:'pass',sort:'old'};",
    "const state={type:'pass',sort:'old',petKind:'all'};"
)

js_marker = 'function petKindKey(kind)'
js = r'''
function petKindKey(kind){
  if(kind==='限定')return 'limited';
  if(kind==='聯動')return 'collab';
  return 'regular';
}
function petKindLabel(kind){
  const key=petKindKey(kind);
  if(key==='regular')return '常駐';
  if(key==='limited')return '限定';
  if(key==='collab')return '聯動';
  return kind||'';
}
function ensurePetFilters(){
  const head=document.querySelector('.section-head');
  if(!head||document.getElementById('petFilterBar'))return;
  const bar=document.createElement('div');
  bar.className='pet-filter-bar';
  bar.id='petFilterBar';
  bar.setAttribute('aria-label','寵物取得方式篩選');
  bar.innerHTML=[
    ['all','全部'],
    ['regular','常駐'],
    ['limited','限定'],
    ['collab','聯動']
  ].map(([key,label])=>`<button class="pet-filter" type="button" data-pet="${key}">${label}</button>`).join('');
  head.appendChild(bar);
  bar.querySelectorAll('.pet-filter').forEach(btn=>btn.addEventListener('click',()=>{
    state.petKind=btn.dataset.pet;
    updatePetFilters();
    render();
  }));
}
function updatePetFilters(){
  ensurePetFilters();
  const bar=document.getElementById('petFilterBar');
  if(!bar)return;
  bar.classList.toggle('show',state.type==='pet');
  bar.querySelectorAll('.pet-filter').forEach(btn=>btn.classList.toggle('active',btn.dataset.pet===state.petKind));
}
'''
if js_marker not in text:
    text = text.replace('function render(){\n', js + '\nfunction render(){\n', 1)

# Ensure render uses the filter and the displayed pet label.
text = text.replace(
    "document.getElementById('offlinePetBtn').classList.remove('show');\n  let rows=DATA.filter(x=>x.type===state.type);",
    "document.getElementById('offlinePetBtn').classList.remove('show');\n  updatePetFilters();\n  let rows=DATA.filter(x=>x.type===state.type);\n  if(state.type==='pet'&&state.petKind!=='all')rows=rows.filter(x=>petKindKey(x.kind)===state.petKind);"
)
text = text.replace(
    "const issue=item.type==='package'?`第 ${item.number} 代`:item.type==='pet'?item.kind:(item.type==='abyss'||item.type==='raid')?`第 ${item.number} 套`:`第 ${item.number} 期`;",
    "const issue=item.type==='package'?`第 ${item.number} 代`:item.type==='pet'?petKindLabel(item.kind):(item.type==='abyss'||item.type==='raid')?`第 ${item.number} 套`:`第 ${item.number} 期`;"
)
text = text.replace(
    "const issueClass=item.type==='pet'?(item.kind==='限定'?'limited':item.kind==='聯動'?'collab':'regular'):'';",
    "const issueClass=item.type==='pet'?(petKindKey(item.kind)==='limited'?'limited':petKindKey(item.kind)==='collab'?'collab':'regular'):'';"
)

# Source list pet label normalization.
text = text.replace(
    "x.type==='package'?`第 ${x.number} 代`:x.type==='pet'?x.kind:(x.type==='abyss'||x.type==='raid')?`第 ${x.number} 套`:`第 ${x.number} 期`",
    "x.type==='package'?`第 ${x.number} 代`:x.type==='pet'?petKindLabel(x.kind):(x.type==='abyss'||x.type==='raid')?`第 ${x.number} 套`:`第 ${x.number} 期`"
)

# Remove old redeploy marker then add a fresh one.
text = text.replace('<!-- redeploy 2026-09-05 -->\n', '')
text = text.replace('</html>', '<!-- layout fix 2026-09-05 -->\n</html>')

INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Layout fix applied to index.html')
