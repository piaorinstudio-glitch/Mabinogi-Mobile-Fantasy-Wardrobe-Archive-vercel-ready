from pathlib import Path
import sys

path = Path('index.html')
if not path.exists():
    raise SystemExit('index.html not found. Please run this from repository root.')

text = path.read_text(encoding='utf-8')

CSS_MARK = '/* pet availability filter patch v1 */'
JS_MARK = '// pet availability filter patch v1'

css = r'''

/* pet availability filter patch v1 */
.pet-filter-bar{
  display:none;
  align-items:center;
  justify-content:flex-end;
  gap:7px;
  flex-wrap:wrap;
  margin-left:auto;
}
.pet-filter-bar.show{display:flex}
.pet-filter-btn{
  height:34px;
  border:1px solid #d2c4a7;
  background:linear-gradient(180deg,#fffdf8,#f4ede0);
  color:#3a4038;
  border-radius:999px;
  padding:0 12px;
  cursor:pointer;
  font-size:12px;
  font-weight:950;
  letter-spacing:.01em;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.72),0 2px 5px rgba(55,65,56,.06);
}
.pet-filter-btn:hover{border-color:#b79f70;background:linear-gradient(180deg,#fffefb,#f7efdf)}
.pet-filter-btn.active{
  color:#fff;
  border-color:#496b50;
  background:linear-gradient(180deg,#557963,#2f5f4f);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 4px 12px rgba(47,95,79,.15);
}
.pet-filter-btn[data-pet-filter="permanent"].active{
  border-color:#496b50;
  background:linear-gradient(180deg,#557963,#2f5f4f);
}
.pet-filter-btn[data-pet-filter="limited"].active{
  border-color:#9a712b;
  background:linear-gradient(180deg,#cf9f4f,#9a6a24);
}
.pet-filter-btn[data-pet-filter="collab"].active{
  border-color:#516269;
  background:linear-gradient(180deg,#738389,#4b5b61);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 4px 12px rgba(75,91,97,.18);
}
@media(max-width:620px){
  .section-head{align-items:flex-start;flex-direction:column;gap:9px}
  .pet-filter-bar{justify-content:flex-start;margin-left:0;width:100%;overflow-x:auto;flex-wrap:nowrap;padding-bottom:2px}
  .pet-filter-btn{height:32px;font-size:11px;padding:0 10px;white-space:nowrap}
}
'''

js = r'''

// pet availability filter patch v1
const PET_FILTER_LABELS = {
  all: '全部',
  permanent: '常駐',
  limited: '限定',
  collab: '聯動'
};
function petAvailability(item){
  if(item.type !== 'pet') return 'all';
  if(item.kind === '聯動') return 'collab';
  if(item.kind === '限定') return 'limited';
  return 'permanent';
}
function ensurePetFilterBar(){
  const head = document.querySelector('.section-head');
  if(!head) return null;
  let bar = document.getElementById('petFilterBar');
  if(bar) return bar;
  bar = document.createElement('div');
  bar.id = 'petFilterBar';
  bar.className = 'pet-filter-bar';
  bar.setAttribute('aria-label','寵物取得方式篩選');
  bar.innerHTML = Object.entries(PET_FILTER_LABELS).map(([key,label]) =>
    `<button type="button" class="pet-filter-btn" data-pet-filter="${key}">${label}</button>`
  ).join('');
  head.appendChild(bar);
  bar.addEventListener('click', e => {
    const btn = e.target.closest('[data-pet-filter]');
    if(!btn) return;
    state.petFilter = btn.dataset.petFilter;
    render();
  });
  return bar;
}
function renderPetFilterBar(){
  const bar = ensurePetFilterBar();
  if(!bar) return;
  const show = state.type === 'pet';
  bar.classList.toggle('show', show);
  bar.querySelectorAll('[data-pet-filter]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.petFilter === (state.petFilter || 'all'));
  });
}
'''

# 1) CSS
if CSS_MARK not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

# 2) state object
text = text.replace("const state={type:'pass',sort:'old'};", "const state={type:'pass',sort:'old',petFilter:'all'};")

# 3) JS helper functions before render()
if JS_MARK not in text:
    marker = '\nfunction render(){'
    if marker not in text:
        raise SystemExit('Could not find function render() marker.')
    text = text.replace(marker, js + marker, 1)

# 4) call renderPetFilterBar() inside render()
old = "document.getElementById('offlinePetBtn').classList.remove('show');\n  let rows=DATA.filter(x=>x.type===state.type);"
new = "document.getElementById('offlinePetBtn').classList.remove('show');\n  renderPetFilterBar();\n  let rows=DATA.filter(x=>x.type===state.type);\n  if(state.type==='pet'&&state.petFilter&&state.petFilter!=='all') rows=rows.filter(x=>petAvailability(x)===state.petFilter);"
if old in text:
    text = text.replace(old, new, 1)
elif "renderPetFilterBar();" not in text:
    raise SystemExit('Could not patch row filtering block.')

# 5) reset pet filter when switching away? Keep last pet filter, but avoid stale display.
# No change needed.

path.write_text(text, encoding='utf-8')
print('Patched index.html with pet availability filter buttons.')
