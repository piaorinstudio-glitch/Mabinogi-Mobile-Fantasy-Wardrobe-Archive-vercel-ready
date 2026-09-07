const {
  DATA,LABELS,TIPS_CONTENT,PET_STATS,PET_FAMILY_BY_KO,PET_SKILL_FAMILIES,
  TW_CURRENT_IDS,TW_RELEASED_IDS,TW_STATUS_UPDATED,TOOL_LINKS
}=window.MABI;
function getTwStatusChip(item){
  if(item.type==='abyss'||item.type==='raid') return '';
  if(TW_CURRENT_IDS.has(item.id)) return `<span class="tw-status-chip tw-status-selling" title="台服目前當期販售／可取得；依台服官方公告整理，更新至 ${TW_STATUS_UPDATED}">台服當期</span>`;
  if(TW_RELEASED_IDS.has(item.id)) return `<span class="tw-status-chip tw-status-released" title="台服曾經推出；目前未標示為當期，更新至 ${TW_STATUS_UPDATED}">台服已推出</span>`;
  return '';
}
let state={type:'pass',sort:'old',search:'',petKind:'all',legendView:'regular'};
const $=(s,r=document)=>r.querySelector(s);
const $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
function normKind(k){return k==='常規'?'常駐':(k||'常駐')}
function kindKey(k){k=normKind(k);return k==='限定'?'limited':k==='聯動'?'collab':'regular'}
function rarityKey(r){return r==='史詩'?'rarity-epic':r==='菁英'?'rarity-elite':r==='稀有'?'rarity-rare':'rarity-advanced'}
const PET_BASE_GROUPS=[
  {key:'cat',zh:'貓',en:'CAT',match:v=>(v.ko||'').includes('고양이')},
  {key:'retriever',zh:'獵犬',en:'RETRIEVER',match:v=>(v.ko||'').includes('리트리버')},
  {key:'bear',zh:'小熊',en:'BEAR',match:v=>(v.ko||'').includes('아기 곰')},
  {key:'fox',zh:'小狐狸',en:'FOX',match:v=>(v.ko||'').includes('아기 여우')},
  {key:'pomeranian',zh:'博美犬',en:'POMERANIAN',match:v=>(v.ko||'').includes('포메라니안')},
  {key:'rabbit',zh:'兔子',en:'RABBIT',match:v=>(v.ko||'').includes('토끼')},
  {key:'raccoon',zh:'浣熊',en:'RACCOON',match:v=>(v.ko||'').includes('라쿤')}
];
function petBaseGroup(v){
  return PET_BASE_GROUPS.find(group=>group.match(v))||{key:'other',zh:'其他',en:'OTHER'};
}
function petChoiceButton(v,group=''){
  return `<button class="pet-rarity-choice" type="button" data-pet-zh="${v.zh||''}" data-pet-ko="${v.ko||''}" data-pet-rarity="${v.rarity||''}" data-pet-group="${group}" aria-label="查看 ${v.zh||v.ko||'寵物'} ${v.rarity||''} 詳細資訊"><span class="pet-rarity-name">${v.zh||v.ko||'寵物'}</span><span class="rarity-badge ${rarityKey(v.rarity)}">${v.rarity}</span></button>`;
}
function renderBasePoolGroups(variants){
  return PET_BASE_GROUPS.map(group=>{
    const pets=variants.filter(v=>typeof v!=='string'&&v.rarity&&group.match(v));
    if(!pets.length)return '';
    return `<section class="pet-pool-group"><div class="pet-pool-group-title">${group.zh}<small>${group.en}</small></div><div class="pet-pool-group-list">${pets.map(v=>petChoiceButton(v,group.key)).join('')}</div></section>`;
  }).join('');
}
function viewerPetButton(v){
  return `<button class="viewer-pet-rarity-btn" type="button" data-pet-zh="${v.zh||''}" data-pet-ko="${v.ko||''}" data-pet-rarity="${v.rarity||''}" aria-label="查看 ${v.zh||v.ko||'寵物'} ${v.rarity||''} 詳細資訊"><span>${v.zh||v.ko||'寵物'}</span><span class="rarity-badge ${rarityKey(v.rarity)}">${v.rarity}</span></button>`;
}
function renderViewerPetGroups(variants){
  const grouped=variants.some(v=>v.group);
  if(!grouped)return variants.map(viewerPetButton).join('');
  return PET_BASE_GROUPS.map(group=>{
    const pets=variants.filter(v=>v.group===group.key);
    if(!pets.length)return '';
    return `<section class="viewer-pet-group"><div class="viewer-pet-group-title">${group.zh}<small>${group.en}</small></div><div class="viewer-pet-group-list">${pets.map(viewerPetButton).join('')}</div></section>`;
  }).join('');
}

const PET_STAT_META={
  '攻擊力':{color:'#d66b5c'},
  '防禦力':{color:'#6d82b6'},
  '破防':{icon:'🗡',color:'#ff8452',bg:'#fff0e7',border:'#ffd0bb'},
  '強擊強化':{icon:'⚑',color:'#ff7b4d',bg:'#fff0e8',border:'#ffd0bf'},
  '連段強化':{icon:'⟳',color:'#f0a722',bg:'#fff5de',border:'#f2d89d'},
  '技能威力':{icon:'✦',color:'#31a7ff',bg:'#e9f6ff',border:'#b9ddf7'},
  '廣域強化':{icon:'◎',color:'#34afe9',bg:'#e8f9ff',border:'#bee4f3'},
  '恢復力':{icon:'✚',color:'#c06bff',bg:'#f7ebff',border:'#e0c0ff'},
  '要害迴避':{icon:'↗',color:'#47c472',bg:'#eafaf0',border:'#c5e9d0'},
  '追擊':{icon:'✪',color:'#4ccd9b',bg:'#e9fbf5',border:'#c1ebdf'},
  '傷害減少':{icon:'⬡',color:'#ff7a57',bg:'#fff0eb',border:'#ffd0c6'},
  '快速攻擊':{icon:'➹',color:'#f0ae25',bg:'#fff5df',border:'#f3daa5'},
  '連擊強化':{icon:'⚡',color:'#f2b63a',bg:'#fff6df',border:'#f2dda8'},
  '快速技能':{icon:'☄',color:'#36b2ff',bg:'#e8f6ff',border:'#bfdff5'},
  '追加體力':{icon:'❤',color:'#d36ff1',bg:'#faecff',border:'#ecc8ff'},
  '絕招':{icon:'〰',color:'#c05bff',bg:'#f7ebff',border:'#e1c0ff'},
  '暴擊':{icon:'✹',color:'#55d67c',bg:'#ebfbef',border:'#c7ecd0'}
};
function createPetStatPill(stat){
  const meta=PET_STAT_META[stat]||{color:'#7d6857'};
  const span=document.createElement('span');
  span.className='pet-stat-pill';
  span.style.setProperty('--stat',meta.color);
  span.textContent=stat;
  return span;
}
let petDetailTrigger=null;
function cleanPetInfoText(value){
  return String(value||'')
    .split('\n')
    .filter(line=>line.trim()&&!line.trim().startsWith('※'))
    .map(line=>line
      .split('；')
      .map(part=>part.trim())
      .filter(part=>part&&!/未知/.test(part))
      .join('；')
      .replace(/；+。/g,'。')
      .trim())
    .filter(Boolean)
    .join('\n')
    .trim();
}
function cleanPetNote(value){
  const s=String(value||'').trim();
  if(!s)return '';
  if(/尚未.*確認|未.*確認|尚無可靠資料|未能.*核對|未可靠核對|不填未確認|未確認數字/.test(s))return '';
  return s;
}
function petSkillNameText(value){
  const s=String(value||'').trim();
  if(!s || /未知|待確認|名稱待確認/.test(s))return '資料缺失';
  return s;
}
function petSkillEffectText(value){
  const raw=String(value||'').trim();
  if(!raw)return '資料缺失';

  const cleaned=cleanPetInfoText(raw);

  // 已知效果照常保留；只有百分比、倍率、傷害值、持續時間等細節缺資料時，
  // 在已知內容下方補上「詳細數值缺失」。
  const missingDetail=/未知|確切.*(?:未|尚未)|(?:未|尚未).*確切|未可靠核對|尚未可靠核對|未能.*核對|未從.*核對|未從.*確認|尚無可靠資料|目前尚無可靠資料|未確認數字|數值會隨寵物等級成長|詳細數值尚未確認/.test(raw);

  if(missingDetail){
    return cleaned ? `${cleaned}\n詳細數值缺失` : '詳細數值缺失';
  }

  return cleaned||'資料缺失';
}
function renderPetSkillEffect(el,value){
  const text=petSkillEffectText(value);
  const marker='詳細數值缺失';
  const parts=text.split(marker);
  el.replaceChildren();
  parts.forEach((part,index)=>{
    if(part)el.appendChild(document.createTextNode(part));
    if(index<parts.length-1){
      const span=document.createElement('span');
      span.className='pet-missing-detail';
      span.textContent=marker;
      el.appendChild(span);
    }
  });
}
function openPetDetail(button){
  const ko=button.dataset.petKo||'',zh=button.dataset.petZh||'',rarity=button.dataset.petRarity||'';
  const family=PET_SKILL_FAMILIES[PET_FAMILY_BY_KO[ko]]||{};
  const stats=PET_STATS[ko]||[];
  const nativeEpic=rarity==='史詩';
  petDetailTrigger=button;
  $('#petDetailTitle').textContent=zh||ko||'寵物詳細資訊';
  $('#petDetailKo').textContent=ko;
  const rarityEl=$('#petDetailRarity');
  rarityEl.textContent=rarity;
  rarityEl.className=`rarity-badge ${rarityKey(rarity)}`;

  const versionEl=$('#petSkillVersion');
  versionEl.textContent=nativeEpic?'原生史詩｜技能 S':'升階至史詩｜技能（無 S）';
  versionEl.className=`pet-skill-version-chip ${nativeEpic?'native':'promoted'}`;

  const currentSkillName=nativeEpic?(family.epic||family.base):(family.base||family.epic);
  const currentSkillEffect=nativeEpic?(family.epicEffect||family.effect):(family.baseEffect||family.effect);
  $('#petSkillName').textContent=petSkillNameText(currentSkillName);
  renderPetSkillEffect($('#petSkillEffect'),currentSkillEffect);

  // 傳說資料：不再自動推測 SS 名稱。沒有可靠名稱或詳細數值就直接顯示「資料缺失」。
  const legendSkillName=nativeEpic
    ?family.legendEpic
    :family.epic;
  const legendSkillEffect=nativeEpic
    ?family.legendEpicEffect
    :(family.epicEffect||family.effect);
  const legendWrap=$('#petLegendSkill');
  const legendVersionEl=$('#petLegendSkillVersion');
  if(legendVersionEl)legendVersionEl.textContent=nativeEpic?'升階至傳說｜技能 SS':'升階至傳說｜技能 S';
  $('#petLegendSkillName').textContent=petSkillNameText(legendSkillName);
  renderPetSkillEffect($('#petLegendSkillEffect'),legendSkillEffect);
  legendWrap.hidden=false;

  const lockNoteEl=$('#petLockNote');
  if(lockNoteEl)lockNoteEl.textContent='';

  const statWrap=$('#petStatPills');statWrap.replaceChildren();
  stats.forEach(stat=>statWrap.appendChild(createPetStatPill(stat)));
  if(!stats.length){statWrap.appendChild(createPetStatPill('資料待確認'))}
  const currentNote=nativeEpic?(family.epicNote||''):(family.baseNote||'');
  const legendNote=nativeEpic?(family.legendEpicNote||''):(family.epicNote||'');
  $('#petDataNote').textContent=[currentNote,legendNote].filter(Boolean).join('\n');
  const modal=$('#petDetailModal');modal.classList.add('show');modal.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';
  $('#petDetailClose').focus();
}
function closePetDetail(){
  const modal=$('#petDetailModal');if(!modal.classList.contains('show'))return;
  modal.classList.remove('show');modal.setAttribute('aria-hidden','true');document.body.style.overflow=$('#viewer').classList.contains('show')?'hidden':'';
  if(petDetailTrigger&&document.contains(petDetailTrigger))petDetailTrigger.focus();
}
function issueText(item){
  if(item.id==='pet-0')return '常駐池';
  if(item.type==='lucky'||item.type==='pet')return `韓服 #${item.number}`;
  if(item.type==='package'||item.type==='legend')return `第 ${item.number} 代`;
  if(item.type==='abyss'||item.type==='raid')return `第 ${item.number} 套`;
  return `第 ${item.number} 期`;
}
function formatKrDate(date){
  if(!date)return '';
  return String(date).replace(/-/g,'/');
}
function splitOrigin(origin){
  const [zh='',ko='']=String(origin||'').split('｜');
  return {zh:zh.trim(),ko:ko.trim()};
}
function issueBadge(item){
  if(item.type==='abyss'||item.type==='raid'){
    const origin=splitOrigin(item.origin);
    return `<span class="num-badge source-badge"><span class="source-badge-zh">${origin.zh||'出處待確認'}</span><span class="source-badge-ko">${origin.ko||''}</span></span>`;
  }
  const showDate=item.type==='lucky'||item.type==='pet';
  if(!showDate)return `<span class="num-badge">${issueText(item)}</span>`;
  return `<span class="num-badge has-date"><span class="num-badge-main">${issueText(item)}</span><span class="num-badge-date">${formatKrDate(item.date)}</span></span>`;
}
function itemMatches(item){
  const q=state.search.trim().toLowerCase();
  if(!q)return true;
  const variantNames=(item.variants||[]).flatMap(v=>typeof v==='string'?[v]:[v.zh,v.ko]);
  return [item.zh,item.ko,item.origin,...(item.lines||[]),...variantNames].filter(Boolean).some(v=>String(v).toLowerCase().includes(q));
}

function renderTools(){
  $('#sectionTitle').textContent='小工具'; $('#sectionTitle').dataset.en='TOOLS';
  $('#sectionTipsBtn').style.display='none';
  $('#archiveTools').style.display='none'; $('#sort').style.display='none'; $('#petFilters').classList.remove('show'); $('#legendViews').classList.remove('show'); $('#archiveCount').textContent='';
  const cards=TOOL_LINKS.map(tool=>`<article class="tool-card">
    <div class="tool-card-head">
      <div class="tool-card-icon" aria-hidden="true">${tool.icon}</div>
      <div><h3 class="tool-card-title">${tool.title}</h3><div class="tool-card-source">${tool.source}</div></div>
    </div>
    <p class="tool-card-desc">${tool.description}</p>
    <a class="tool-open" href="${tool.url}" target="_blank" rel="noopener noreferrer" aria-label="開啟 ${tool.title}（外部網站，新分頁）">開啟工具 <span aria-hidden="true">↗</span></a>
  </article>`).join('');
  $('#feed').innerHTML=`<div class="tools-hub">
    <section class="tools-intro">
      <h2 class="tools-intro-title">玩家實用小工具</h2>
      <p>這裡集中分享方便查資料的小工具與網站。之後有新的實用工具，可以繼續加在這一頁供大家選擇。</p>
    </section>
    <div class="tools-grid">${cards}<div class="tools-coming">更多小工具之後會陸續加入 ✦</div></div>
  </div>`;
}

function render(){
  const [zh,en]=LABELS[state.type]||LABELS.pass;
  $$('.category').forEach(b=>b.classList.toggle('active',b.dataset.type===state.type));
  if(state.type==='tools'){renderTools(); location.hash='type=tools'; return;}
  $('#archiveTools').style.display='flex'; $('#sort').style.display='inline-block';
  $('#sectionTitle').textContent=zh; $('#sectionTitle').dataset.en=en;
  $('#sectionTipsBtn').style.display=(state.type==='legend'||state.type==='pet')?'inline-flex':'none';
  $('#petFilters').classList.toggle('show',state.type==='pet');
  $('#legendViews').classList.toggle('show',state.type==='legend');
  $$('.legend-view-btn').forEach(b=>b.classList.toggle('active',b.dataset.view===state.legendView));
  let rows=DATA.filter(x=>x.type===state.type).filter(itemMatches);
  if(state.type==='pet' && state.petKind!=='all') rows=rows.filter(x=>kindKey(x.kind)===state.petKind);
  rows.sort((a,b)=>{const d=String(a.date||'').localeCompare(String(b.date||'')) || (Number(a.number)-Number(b.number));return state.sort==='old'?d:-d;});
  $('#archiveCount').textContent=`共 ${rows.length} 筆`;
  if(!rows.length){$('#feed').innerHTML=`<div class="empty">沒有找到符合的外觀</div>`; return;}
  const petHint=state.type==='pet'?'<div class="lucky-order-hint">※ 「韓服 #」代表<strong>韓服推出順序</strong>，下方日期為韓服推出日期。電腦：滑鼠移到寵物圖片可查看各稀有度並點選詳細資訊；手機：點圖片放大後查看。</div>':'';
  const luckyHint=state.type==='lucky'?'<div class="lucky-order-hint">※ 「韓服 #」代表<strong>韓服推出順序</strong>；下方日期為韓服推出日期。台服與韓服的上架組合、批次可能不同。</div>':'';
  const dungeonHint=(state.type==='abyss'||state.type==='raid')?'<div class="lucky-order-hint">※ 卡片右下角顯示<strong>時裝掉落副本</strong>。台服已推出的副本採用<strong>台服正式名稱＋韓服名稱</strong>；台服尚未推出的副本則使用<strong>中文暫譯＋韓服名稱</strong>。</div>':'';
  $('#feed').innerHTML=luckyHint+petHint+dungeonHint+rows.map(item=>{
    const kind=item.type==='pet'?`<div class="kind-chip ${kindKey(item.kind)}">${normKind(item.kind)}</div>`:'';
    const twStatus=getTwStatusChip(item);
    const tags=(kind||twStatus)?`<div class="entry-tags">${kind}${twStatus}</div>`:'';
    const petRarityHover=item.type==='pet'&&item.variants?(item.id==='pet-0'
      ?`<div class="pet-rarity-hover base-pool">${renderBasePoolGroups(item.variants)}</div>`
      :`<div class="pet-rarity-hover${item.variants.length>12?' many':''}">${item.variants.filter(v=>typeof v!=='string'&&v.rarity).map(v=>petChoiceButton(v)).join('')}</div>`):'';
    const displayImage=item.type==='legend'?(state.legendView==='hooded'?(item.hoodedImage||item.image):(item.regularImage||item.image)):item.image;
    const wrapClass=item.type==='legend'?'image-wrap figure-card':(item.type==='pet'?'image-wrap pet-image':'image-wrap');
    const modeChip=item.type==='legend'?`<div class="legend-mode-chip">${state.legendView==='hooded'?'長袍版':'一般版'}</div>`:'';
    const viewerVariants=item.type==='legend'?` data-regular-image="${item.regularImage||item.image}" data-hooded-image="${item.hoodedImage||item.image}" data-viewer-mode="${state.legendView}"` : '';
    return `<article class="entry">
      <div class="${wrapClass}" data-image="${displayImage}"${viewerVariants} tabindex="0" role="button" aria-label="放大查看 ${item.zh||'外觀'}"><img src="${displayImage}" alt="${item.zh} ${item.ko||''}" loading="lazy" decoding="async">${issueBadge(item)}${petRarityHover}</div>
      <div class="entry-info">${tags}<div class="name-row"><span class="color-dot"></span><h3 class="name">${item.zh||''}</h3></div><div class="ko">${item.ko||''}</div>${modeChip}</div>
    </article>`;
  }).join('');
  $$('.image-wrap').forEach(w=>{
    w.onclick=()=>openViewer(w,'.image-wrap');
    w.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openViewer(w,'.image-wrap')}};
  });
  $$('.pet-rarity-choice[data-pet-ko]').forEach(button=>{button.onclick=e=>{e.stopPropagation();openPetDetail(button)};button.onkeydown=e=>e.stopPropagation()});
  location.hash='type='+state.type;
}
let viewerItems=[],viewerIndex=0,viewerMode='regular',viewerTrigger=null,touchStartX=0,touchStartY=0;
function showViewerItem(){
  const item=viewerItems[viewerIndex];if(!item)return;
  const hasModes=Boolean(item.regular&&item.hooded);
  $('#viewerImg').src=hasModes?(item[viewerMode]||item.src):item.src;
  $('#viewerImg').alt=item.alt+(hasModes?(viewerMode==='hooded'?' 長袍版':' 一般版'):'');
  $('#viewerModes').hidden=!hasModes;
  $$('.viewer-mode-btn').forEach(button=>button.classList.toggle('active',button.dataset.mode===viewerMode));
  const petBox=$('#viewerPetRarities'),petList=$('#viewerPetRarityList');
  const petVariants=item.petVariants||[];
  petBox.hidden=!petVariants.length;
  petList.innerHTML=renderViewerPetGroups(petVariants);
  $$('.viewer-pet-rarity-btn',petList).forEach(button=>button.onclick=e=>{e.stopPropagation();openPetDetail(button)});
  $('#viewerCounter').textContent=`${viewerIndex+1} / ${viewerItems.length}`;
  const multiple=viewerItems.length>1;$('#viewerPrev').hidden=!multiple;$('#viewerNext').hidden=!multiple;$('#viewerCounter').hidden=!multiple;
}
function openViewer(trigger,selector){
  viewerTrigger=trigger;
  document.body.classList.add('viewer-open');
  if(document.activeElement===trigger) trigger.blur();
  viewerItems=$$(selector).filter(el=>el.dataset.image).map(el=>({element:el,src:el.dataset.image,regular:el.dataset.regularImage,hooded:el.dataset.hoodedImage,alt:el.querySelector('img')?.alt||'外觀圖片',petVariants:$$('.pet-rarity-choice[data-pet-ko]',el).map(button=>({zh:button.dataset.petZh||'',ko:button.dataset.petKo||'',rarity:button.dataset.petRarity||'',group:button.dataset.petGroup||''}))}));
  viewerMode=trigger.dataset.viewerMode||'regular';
  viewerIndex=Math.max(0,viewerItems.findIndex(item=>item.element===trigger));showViewerItem();
  $('#viewer').classList.add('show');$('#viewer').setAttribute('aria-hidden','false');document.body.style.overflow='hidden';$('#viewerClose').focus();
}
function moveViewer(step){if(viewerItems.length<2)return;viewerIndex=(viewerIndex+step+viewerItems.length)%viewerItems.length;showViewerItem()}
function closeViewer(){
  $('#viewer').classList.remove('show');
  $('#viewer').setAttribute('aria-hidden','true');
  document.body.style.overflow='';
  document.body.classList.remove('viewer-open');
  if(viewerTrigger){
    viewerTrigger.blur();
    viewerTrigger=null;
  }
}
let tipsTrigger=null;
function getTipCardClass(title){
  if(state.type!=='pet')return 'tip-card';
  if(title.includes('常駐'))return 'tip-card pet-tip-regular';
  if(title.includes('限定'))return 'tip-card pet-tip-limited';
  if(title.includes('聯動'))return 'tip-card pet-tip-collab';
  if(title.includes('固有技能'))return 'tip-card pet-tip-skill';
  return 'tip-card';
}
function renderTips(){
  const [zh,en]=LABELS[state.type]||LABELS.pass;
  $('#tipsTitle').textContent=`${zh}小提示`;
  $('#tipsTitleEn').textContent=`${en} TIPS`;
  const items=TIPS_CONTENT[state.type]||[];
  $('#tipsBody').innerHTML=items.map(([title,body])=>`<section class="${getTipCardClass(title)}"><h3>${title}</h3><div class="tip-body">${body}</div></section>`).join('')+
    '<p class="tips-note">※ 本站以韓服資料整理「未來視」；實際內容、輪替與台服實裝方式仍以官方公告為準。</p>';
}
function openTips(){
  tipsTrigger=document.activeElement;
  renderTips();
  $('#tipsModal').classList.add('show');
  $('#tipsModal').setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';
  $('#tipsClose').focus();
}
function closeTips(){
  const modal=$('#tipsModal');
  if(!modal.classList.contains('show'))return;
  modal.classList.remove('show');
  modal.setAttribute('aria-hidden','true');
  document.body.style.overflow='';
  if(tipsTrigger&&document.contains(tipsTrigger))tipsTrigger.focus();
}
function renderSources(){
  const types=['pass','lucky','package','legend','pet','abyss','raid'];
  $('#sourcesList').innerHTML=types.map(type=>{
    const rows=DATA.filter(item=>item.type===type&&item.notice);
    if(!rows.length)return '';
    return `<section class="source-group"><h3>${LABELS[type][0]}</h3><div class="source-links">${rows.map(item=>`<a class="source-link" href="${item.notice}" target="_blank" rel="noopener noreferrer"><span>${issueText(item)}｜${item.zh||item.ko||'官方公告'} ↗</span><span class="source-date">${item.date||''}</span></a>`).join('')}</div></section>`;
  }).join('');
}
function openSources(){renderSources();$('#sourcesModal').classList.add('show');$('#sourcesModal').setAttribute('aria-hidden','false');document.body.style.overflow='hidden';$('#sourcesClose').focus()}
function closeSources(){$('#sourcesModal').classList.remove('show');$('#sourcesModal').setAttribute('aria-hidden','true');document.body.style.overflow=''}
$$('.hero-photo').forEach(photo=>{
  photo.onclick=()=>openViewer(photo,'.hero-photo');
  photo.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openViewer(photo,'.hero-photo')}};
});
$('#viewerClose').onclick=closeViewer;
$('#viewerPrev').onclick=e=>{e.stopPropagation();moveViewer(-1)};
$('#viewerNext').onclick=e=>{e.stopPropagation();moveViewer(1)};
$$('.viewer-mode-btn').forEach(button=>button.onclick=e=>{e.stopPropagation();viewerMode=button.dataset.mode;showViewerItem()});
$('#viewer').onclick=e=>{if(e.target.id==='viewer')closeViewer()};
$('#viewer').addEventListener('touchstart',e=>{const t=e.changedTouches[0];touchStartX=t.clientX;touchStartY=t.clientY},{passive:true});
$('#viewer').addEventListener('touchend',e=>{const t=e.changedTouches[0],dx=t.clientX-touchStartX,dy=t.clientY-touchStartY;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy))moveViewer(dx<0?1:-1)},{passive:true});
$('#tipsClose').onclick=closeTips;
$('#tipsModal').onclick=e=>{if(e.target.id==='tipsModal')closeTips()};
$('#sourcesClose').onclick=closeSources;
$('#sourcesModal').onclick=e=>{if(e.target.id==='sourcesModal')closeSources()};
$('#petDetailClose').onclick=closePetDetail;
$('#petDetailModal').onclick=e=>{if(e.target.id==='petDetailModal')closePetDetail()};
document.addEventListener('keydown',e=>{if($('#petDetailModal').classList.contains('show')){if(e.key==='Escape')closePetDetail()}else if($('#viewer').classList.contains('show')){if(e.key==='Escape')closeViewer();else if(e.key==='ArrowLeft')moveViewer(-1);else if(e.key==='ArrowRight')moveViewer(1)}else if(e.key==='Escape'&&$('#tipsModal').classList.contains('show'))closeTips();else if(e.key==='Escape'&&$('#sourcesModal').classList.contains('show'))closeSources()});
$$('.category').forEach(btn=>btn.onclick=()=>{state.type=btn.dataset.type;state.search='';$('#archiveSearch').value='';render();});
$('#sort').onchange=e=>{state.sort=e.target.value;render();};
$('#archiveSearch').oninput=e=>{state.search=e.target.value;render();};
$$('.pet-filter-btn').forEach(btn=>btn.onclick=()=>{state.petKind=btn.dataset.kind;$$('.pet-filter-btn').forEach(b=>b.classList.toggle('active',b===btn));render();});
$$('.legend-view-btn').forEach(btn=>btn.onclick=()=>{state.legendView=btn.dataset.view;render();});
$('#sectionTipsBtn').onclick=openTips;
$('#openSources').onclick=openSources;
function initFromHash(){let t=(location.hash.match(/type=([^&]+)/)||[])[1]; if(t==='dye')t='tools'; if(t&&LABELS[t]) state.type=t; render();}
window.addEventListener('hashchange',initFromHash);
initFromHash();
