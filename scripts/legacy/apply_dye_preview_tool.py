from pathlib import Path

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from the repository root.')

text = INDEX.read_text(encoding='utf-8')

# 1) Add category button
btn = '<button class="category" data-type="dye">染色預覽</button>'
if btn not in text:
    anchor = '<button class="category" data-type="pet">寵物</button>'
    if anchor in text:
        text = text.replace(anchor, btn + '\n      ' + anchor, 1)
    else:
        anchor = '<button class="category" data-type="package">全套套組</button>'
        text = text.replace(anchor, anchor + '\n      ' + btn, 1)

# 2) Add LABELS key
if "dye:'染色預覽'" not in text and 'dye:"染色預覽"' not in text:
    text = text.replace(
        "const LABELS={pass:'通行證',lucky:'幸運箱',package:'全套套組',pet:'寵物',abyss:'深淵副本時裝',raid:'團隊副本時裝'};",
        "const LABELS={pass:'通行證',lucky:'幸運箱',package:'全套套組',dye:'染色預覽',pet:'寵物',abyss:'深淵副本時裝',raid:'團隊副本時裝'};"
    )

# 3) CSS
css_marker = '/* dye preview tool */'
css = r'''

/* dye preview tool */
.dye-tool{
  display:grid;
  grid-template-columns:minmax(0,1.15fr) minmax(280px,.85fr);
  gap:18px;
  align-items:start;
}
.dye-panel{
  border:1px solid var(--line);
  border-radius:22px;
  background:linear-gradient(180deg,#fffdf8,#f7f2e8);
  box-shadow:var(--shadow);
  overflow:hidden;
}
.dye-panel-head{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  padding:16px 18px;
  border-bottom:1px solid rgba(201,188,160,.65);
  background:linear-gradient(180deg,rgba(255,255,255,.72),rgba(248,241,226,.78));
}
.dye-panel-title{font-family:"Noto Serif TC",Georgia,serif;font-size:18px;font-weight:950;letter-spacing:-.02em;}
.dye-hex-pill{font-size:12px;font-weight:950;color:#fff;background:linear-gradient(180deg,#4c7055,#325c4d);border-radius:999px;padding:7px 10px;font-variant-numeric:tabular-nums;}
.dye-preview-stage{
  padding:18px;
  background:
    radial-gradient(circle at 18% 14%,rgba(255,255,255,.74),transparent 22%),
    radial-gradient(circle at 80% 18%,rgba(210,185,128,.20),transparent 28%),
    linear-gradient(180deg,#f0f3ec,#e8e5d8);
}
.dye-scene-tabs{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:14px;}
.dye-scene{
  height:32px;border:1px solid #d0c3a9;border-radius:999px;padding:0 11px;background:rgba(255,253,247,.82);color:#504b42;font-size:11px;font-weight:900;cursor:pointer;
}
.dye-scene.active{color:#fff;border-color:#4e6b52;background:linear-gradient(180deg,#6f8b70,#4e6d56);}
.dye-preview-card{
  position:relative;
  border:1px solid rgba(118,106,78,.22);
  border-radius:20px;
  overflow:hidden;
  min-height:390px;
  background:linear-gradient(180deg,#f7f3ea,#e9e4d7);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 14px 34px rgba(46,57,47,.08);
}
.dye-preview-card::after{
  content:"";position:absolute;inset:0;pointer-events:none;mix-blend-mode:multiply;opacity:.75;
}
.dye-preview-card.scene-day::after{background:linear-gradient(135deg,rgba(255,244,205,.24),rgba(255,255,255,.05));mix-blend-mode:screen;}
.dye-preview-card.scene-cloudy::after{background:linear-gradient(135deg,rgba(145,162,172,.22),rgba(220,230,232,.12));}
.dye-preview-card.scene-night::after{background:linear-gradient(135deg,rgba(17,28,61,.50),rgba(45,58,90,.30));}
.dye-preview-card.scene-warm::after{background:linear-gradient(135deg,rgba(255,206,143,.28),rgba(112,74,36,.08));}
.dye-light-label{position:absolute;left:14px;top:13px;z-index:2;font-size:11px;font-weight:950;color:#4e4739;background:rgba(255,252,246,.82);border:1px solid rgba(190,174,135,.45);border-radius:999px;padding:6px 9px;}
.dye-model{
  --dye:#B6B33B;
  position:absolute;left:50%;top:52%;width:min(310px,72%);height:330px;transform:translate(-50%,-50%);
}
.dye-model .head{position:absolute;left:50%;top:6px;width:70px;height:70px;transform:translateX(-50%);border-radius:50%;background:linear-gradient(160deg,#f1d3bd,#d5a991);box-shadow:inset -8px -10px 18px rgba(101,71,51,.12);}
.dye-model .neck{position:absolute;left:50%;top:72px;width:34px;height:32px;transform:translateX(-50%);border-radius:0 0 16px 16px;background:linear-gradient(160deg,#e3bea6,#c99d85);}
.dye-model .body{position:absolute;left:50%;top:91px;width:150px;height:168px;transform:translateX(-50%);border-radius:34px 34px 42px 42px;background:
  linear-gradient(120deg,rgba(255,255,255,.50),rgba(255,255,255,0) 22%,rgba(0,0,0,.10) 74%,rgba(0,0,0,.18)),
  repeating-linear-gradient(90deg,rgba(255,255,255,.055) 0 3px,rgba(0,0,0,.025) 3px 6px),
  var(--dye);box-shadow:inset 16px 0 22px rgba(255,255,255,.18),inset -18px -10px 26px rgba(0,0,0,.16),0 10px 28px rgba(0,0,0,.14);}
.dye-model .body::before{content:"";position:absolute;left:50%;top:10px;width:58px;height:130px;transform:translateX(-50%);border-radius:22px;background:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,0));}
.dye-model .sleeve{position:absolute;top:105px;width:58px;height:126px;border-radius:28px;background:linear-gradient(125deg,rgba(255,255,255,.38),rgba(0,0,0,.12)),var(--dye);box-shadow:inset -10px -8px 18px rgba(0,0,0,.12);}
.dye-model .sleeve.left{left:30px;transform:rotate(13deg)}
.dye-model .sleeve.right{right:30px;transform:rotate(-13deg)}
.dye-model .skirt{position:absolute;left:50%;top:230px;width:210px;height:92px;transform:translateX(-50%);clip-path:polygon(19% 0,81% 0,100% 100%,0 100%);background:
  linear-gradient(115deg,rgba(255,255,255,.38),rgba(255,255,255,0) 26%,rgba(0,0,0,.16)),
  repeating-linear-gradient(90deg,rgba(0,0,0,.045) 0 10px,rgba(255,255,255,.06) 10px 17px),
  var(--dye);filter:saturate(1.02);}
.dye-material-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:14px;}
.dye-material{border:1px solid #d7ccb5;border-radius:14px;overflow:hidden;background:#fffdf8;}
.dye-material-swatch{height:54px;background:var(--dye);}
.dye-material.fabric .dye-material-swatch{background:repeating-linear-gradient(90deg,rgba(255,255,255,.10) 0 2px,rgba(0,0,0,.05) 2px 4px),var(--dye);}
.dye-material.silk .dye-material-swatch{background:linear-gradient(115deg,rgba(255,255,255,.62),rgba(255,255,255,.05) 28%,rgba(0,0,0,.20) 68%,rgba(255,255,255,.20)),var(--dye);}
.dye-material.leather .dye-material-swatch{background:radial-gradient(circle at 30% 20%,rgba(255,255,255,.25),transparent 19%),linear-gradient(135deg,rgba(0,0,0,.08),rgba(0,0,0,.24)),var(--dye);}
.dye-material.metal .dye-material-swatch{background:linear-gradient(90deg,rgba(255,255,255,.75),rgba(255,255,255,.12) 23%,rgba(0,0,0,.28) 51%,rgba(255,255,255,.50) 73%,rgba(0,0,0,.18)),var(--dye);}
.dye-material-label{padding:7px 8px;font-size:11px;font-weight:900;text-align:center;color:#5e574c;}
.dye-controls{padding:18px;}
.dye-input-row{display:grid;grid-template-columns:64px 1fr;gap:10px;margin-bottom:12px;}
.dye-color-input{width:64px;height:44px;border:1px solid #cbbd9e;border-radius:13px;background:#fff;padding:4px;cursor:pointer;}
.dye-text-input{height:44px;border:1px solid #cbbd9e;border-radius:13px;background:#fffdf8;padding:0 13px;font-weight:950;font-size:15px;font-variant-numeric:tabular-nums;color:#343a32;}
.dye-help{font-size:12px;line-height:1.65;color:var(--muted);margin:0 0 14px;}
.dye-saved-title{font-size:13px;font-weight:950;margin:14px 0 8px;color:#3e483e;}
.dye-chip-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}
.dye-chip{height:38px;border:1px solid rgba(120,106,76,.28);border-radius:999px;display:flex;align-items:center;gap:7px;padding:0 9px;background:rgba(255,253,248,.92);cursor:pointer;font-size:11px;font-weight:900;color:#4b463d;box-shadow:0 2px 7px rgba(46,57,47,.06);}
.dye-chip:hover{transform:translateY(-1px);}
.dye-dot{width:17px;height:17px;border-radius:50%;border:1px solid rgba(0,0,0,.16);background:var(--chip);flex:none;}
.dye-note{margin-top:13px;padding:11px 12px;border:1px dashed #d4c7ad;border-radius:14px;background:#fffaf0;color:#6f6658;font-size:11px;line-height:1.65;}
@media(max-width:850px){
  .dye-tool{grid-template-columns:1fr;}
  .dye-panel-head{padding:14px 15px;}
  .dye-preview-stage{padding:14px;}
  .dye-preview-card{min-height:350px;}
  .dye-model{width:min(280px,78%);height:310px;}
  .dye-material-grid{grid-template-columns:repeat(2,1fr);}
  .dye-chip-grid{grid-template-columns:repeat(2,1fr);}
}
@media(max-width:430px){
  .dye-preview-card{min-height:320px;border-radius:17px;}
  .dye-model{transform:translate(-50%,-50%) scale(.88);}
  .dye-input-row{grid-template-columns:58px 1fr;}
  .dye-color-input{width:58px;}
  .dye-chip-grid{grid-template-columns:1fr;}
}
'''
if css_marker not in text:
    text = text.replace('\n</style>', css + '\n</style>', 1)

# 4) JS tool functions
js_marker = 'function normalizeDyeHex'
js = r'''
function normalizeDyeHex(value){
  let v=String(value||'').trim().toUpperCase();
  if(!v.startsWith('#'))v='#'+v;
  if(/^#[0-9A-F]{3}$/.test(v))v='#'+v[1]+v[1]+v[2]+v[2]+v[3]+v[3];
  if(/^#[0-9A-F]{6}$/.test(v))return v;
  return null;
}
function setDyeColor(hex){
  const clean=normalizeDyeHex(hex)||'#B6B33B';
  document.documentElement.style.setProperty('--dye-preview-color',clean);
  const model=document.querySelector('.dye-model');
  if(model)model.style.setProperty('--dye',clean);
  document.querySelectorAll('.dye-material-swatch').forEach(x=>x.style.backgroundColor=clean);
  const text=document.getElementById('dyeHexInput');
  const color=document.getElementById('dyeColorInput');
  const pill=document.getElementById('dyeHexPill');
  if(text)text.value=clean;
  if(color)color.value=clean;
  if(pill)pill.textContent=clean;
}
function setDyeScene(scene){
  const card=document.getElementById('dyePreviewCard');
  const label=document.getElementById('dyeLightLabel');
  if(!card)return;
  ['scene-day','scene-cloudy','scene-night','scene-warm'].forEach(c=>card.classList.remove(c));
  card.classList.add('scene-'+scene);
  const names={day:'白天自然光',cloudy:'陰天冷光',night:'夜晚偏暗',warm:'室內暖光'};
  if(label)label.textContent=names[scene]||'白天自然光';
  document.querySelectorAll('.dye-scene').forEach(btn=>btn.classList.toggle('active',btn.dataset.scene===scene));
}
function renderDyeTool(){
  document.getElementById('sectionTitle').textContent='染色預覽';
  document.getElementById('sectionNote').textContent='輸入遊戲染色碼，快速看白天、陰天、夜晚與室內暖光下的視覺差異';
  document.getElementById('openPrediction').classList.remove('show');
  const offlineBtn=document.getElementById('offlinePetBtn'); if(offlineBtn)offlineBtn.classList.remove('show');
  const petBar=document.getElementById('petFilterBar'); if(petBar)petBar.classList.remove('show');
  const samples=['#B6B74C','#639E9E','#97979B','#56522E','#B3B3B3','#C3766C','#F5EFE2','#242B31','#7D8E69'];
  feed.innerHTML=`
    <section class="dye-tool">
      <div class="dye-panel">
        <div class="dye-panel-head"><div class="dye-panel-title">實際視覺預覽</div><div class="dye-hex-pill" id="dyeHexPill">#B6B74C</div></div>
        <div class="dye-preview-stage">
          <div class="dye-scene-tabs" aria-label="光源環境">
            <button class="dye-scene active" type="button" data-scene="day">白天</button>
            <button class="dye-scene" type="button" data-scene="cloudy">陰天</button>
            <button class="dye-scene" type="button" data-scene="night">夜晚</button>
            <button class="dye-scene" type="button" data-scene="warm">室內暖光</button>
          </div>
          <div class="dye-preview-card scene-day" id="dyePreviewCard">
            <div class="dye-light-label" id="dyeLightLabel">白天自然光</div>
            <div class="dye-model" style="--dye:#B6B74C">
              <div class="head"></div><div class="neck"></div><div class="sleeve left"></div><div class="sleeve right"></div><div class="body"></div><div class="skirt"></div>
            </div>
          </div>
          <div class="dye-material-grid">
            <div class="dye-material fabric"><div class="dye-material-swatch" style="background:#B6B74C"></div><div class="dye-material-label">布料</div></div>
            <div class="dye-material silk"><div class="dye-material-swatch" style="background:#B6B74C"></div><div class="dye-material-label">絲綢高光</div></div>
            <div class="dye-material leather"><div class="dye-material-swatch" style="background:#B6B74C"></div><div class="dye-material-label">皮革陰影</div></div>
            <div class="dye-material metal"><div class="dye-material-swatch" style="background:#B6B74C"></div><div class="dye-material-label">金屬反光</div></div>
          </div>
        </div>
      </div>
      <aside class="dye-panel">
        <div class="dye-panel-head"><div class="dye-panel-title">染色碼</div></div>
        <div class="dye-controls">
          <div class="dye-input-row">
            <input class="dye-color-input" id="dyeColorInput" type="color" value="#B6B74C" aria-label="選擇顏色">
            <input class="dye-text-input" id="dyeHexInput" value="#B6B74C" maxlength="7" spellcheck="false" aria-label="輸入 HEX 色碼">
          </div>
          <p class="dye-help">可以輸入遊戲裡看到的色碼，例如 <b>#B6B74C</b>。左邊會用衣服模型、材質塊和不同光源模擬它在畫面中的感覺。</p>
          <div class="dye-saved-title">範例色票</div>
          <div class="dye-chip-grid">
            ${samples.map(hex=>`<button class="dye-chip" type="button" data-hex="${hex}"><span class="dye-dot" style="--chip:${hex}"></span>${hex}</button>`).join('')}
          </div>
          <div class="dye-note">這不是官方遊戲渲染器，但比單看色號更接近實際觀感。之後也可以再加「角色膚色底」、「深色地圖」、「亮色地圖」、「拍照模式」等環境。</div>
        </div>
      </aside>
    </section>`;
  document.getElementById('dyeHexInput').addEventListener('input',e=>{const v=normalizeDyeHex(e.target.value);if(v)setDyeColor(v);});
  document.getElementById('dyeColorInput').addEventListener('input',e=>setDyeColor(e.target.value));
  feed.querySelectorAll('.dye-chip').forEach(btn=>btn.addEventListener('click',()=>setDyeColor(btn.dataset.hex)));
  feed.querySelectorAll('.dye-scene').forEach(btn=>btn.addEventListener('click',()=>setDyeScene(btn.dataset.scene)));
}
'''
if js_marker not in text:
    # Insert before render function. Works whether pet filter helper exists or not.
    marker = 'function render(){\n'
    if marker not in text:
        raise SystemExit('Could not find render() function.')
    text = text.replace(marker, js + '\n' + marker, 1)

# 5) Branch in render()
branch = "if(state.type==='dye'){renderDyeTool();return;}"
if branch not in text:
    target = "document.getElementById('offlinePetBtn').classList.remove('show');"
    if target in text:
        text = text.replace(target, target + "\n  " + branch, 1)
    else:
        target = "document.getElementById('openPrediction').classList.toggle('show',state.type==='lucky');"
        text = text.replace(target, target + "\n  " + branch, 1)

# 6) Sources should not include dye as DATA-backed source; no action needed.
text = text.replace('<!-- dye preview tool 2026-09-05 -->\n', '')
text = text.replace('</html>', '<!-- dye preview tool 2026-09-05 -->\n</html>')

INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Dye preview tool applied to index.html')
