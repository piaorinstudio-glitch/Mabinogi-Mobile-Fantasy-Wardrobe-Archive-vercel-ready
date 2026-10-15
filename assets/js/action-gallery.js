// Action-box-only UI. Existing viewers, category rendering, and data remain independent.
(() => {
  'use strict';
  const M=window.MABI;
  const byId=new Map(M.ACTION_BOXES.map(box=>[box.id,box]));
  const dialog=document.getElementById('actionDialog');
  const $=id=>document.getElementById(id);
  const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const date=value=>value?String(value).slice(0,10).replaceAll('-','/'):'尚未確認';
  const money=value=>Number.isFinite(value)?`${value.toLocaleString('en-US')} 德卡`:'資料缺失';
  const displayName=value=>String(value??'').replace(/（暫譯）/g,'');
  let activeBox=null,actionIndex=0,previewIndex=0,trigger=null,previousOverflow='',visibleBoxes=[];
  function twStatus(box){
    if(box.twReleased!==true)return '';
    const now=Date.now();
    const current=now>=Date.parse(`${box.twDate}T00:00:00+08:00`) && now<Date.parse(box.twEndDate);
    return `<span class="tw-status-chip ${current?'tw-status-selling':'tw-status-released'}" title="台服公告核對至 ${box.checkedDate}">${current?'台服當期':'台服已推出'}</span>`;
  }
  M.renderActionCards=rows=>{
    visibleBoxes=rows.slice();
    $('feed').innerHTML='<div class="lucky-order-hint">※ 「韓服 #」代表<strong>韓服推出順序</strong>；下方日期為韓服推出日期。台服與韓服的上架組合、批次可能不同。</div>'+rows.map(box=>`
      <article class="entry action-entry" data-action-box="${escape(box.id)}">
        <button type="button" class="image-wrap action-cover action-open" data-action-id="${escape(box.id)}" aria-label="查看${escape(displayName(box.zh))}全部 ${box.actions.length} 個動作">
          <img src="${escape(box.image)}" alt="${escape(displayName(box.zh))}動作預覽封面" loading="lazy" decoding="async" width="640" height="640">
          <span class="action-play" aria-hidden="true">▶ 查看 ${box.actions.length} 個動作</span><span class="num-badge has-date action-issue-badge"><span class="num-badge-main">韓服 #${box.number}</span><span class="num-badge-date">${date(box.date)}</span><span class="num-badge-date">${money(box.priceDeka)}</span></span>
        </button>
        <div class="entry-info">${box.twReleased===true?`<div class="entry-tags">${twStatus(box)}</div>`:''}<div class="name-row"><span class="color-dot" aria-hidden="true"></span><h3 class="name">${escape(displayName(box.zh))}</h3></div><div class="ko" lang="ko">${escape(box.ko)}</div>
        </div>
      </article>`).join('');
    document.querySelectorAll('.action-open').forEach(button=>button.addEventListener('click',()=>open(boxByButton(button),button)));
  };
  function boxByButton(button){return byId.get(button.dataset.actionId)}
  function open(box,button){
    if(!box)return;
    activeBox=box;actionIndex=0;previewIndex=0;trigger=button;
    renderBox();
    previousOverflow=document.body.style.overflow;
    dialog.showModal();document.body.style.overflow='hidden';
    renderSelectedAction();$('actionDialogClose').focus();
  }
  function renderBox(){
    const box=activeBox;
    $('actionDialogTitle').textContent=displayName(box.zh);
    $('actionChoices').innerHTML=box.actions.map((action,index)=>`<button class="action-choice" type="button" data-action-index="${index}" aria-pressed="${index===0}"><strong>${escape(displayName(action.zh))}</strong><span lang="ko">${escape(action.ko)}</span></button>`).join('');
    $('actionChoices').querySelectorAll('button').forEach(choice=>choice.onclick=()=>{
      actionIndex=Number(choice.dataset.actionIndex);previewIndex=0;renderSelectedAction();
    });
  }
  function renderSelectedAction(){
    const action=activeBox.actions[actionIndex];
    $('actionChoices').querySelectorAll('button').forEach(choice=>choice.setAttribute('aria-pressed',String(Number(choice.dataset.actionIndex)===actionIndex)));
    $('actionVariants').innerHTML=action.previews.map((preview,index)=>`<button type="button" data-preview-index="${index}" aria-pressed="${index===previewIndex}">${escape(preview.label)}</button>`).join('');
    $('actionVariants').querySelectorAll('button').forEach(button=>button.onclick=()=>{
      previewIndex=Number(button.dataset.previewIndex);renderSelectedAction();
    });
    const preview=action.previews[previewIndex];
    const img=$('actionGif');
    $('actionPlaybackStatus').textContent='GIF 載入中…';
    img.onload=()=>{$('actionPlaybackStatus').textContent='';};
    img.onerror=()=>{$('actionPlaybackStatus').textContent='GIF 載入失敗，請重新選擇展示版本。';};
    img.alt=`${displayName(activeBox.zh)}：${displayName(action.zh)} ${action.ko}，${preview.label}`;
    img.removeAttribute('src');img.src=preview.path;
  }
  $('actionDialogClose').onclick=()=>dialog.close();
  function moveBox(step){
    if(!activeBox)return;
    const index=visibleBoxes.findIndex(box=>box.id===activeBox.id);
    activeBox=visibleBoxes[(index+step+visibleBoxes.length)%visibleBoxes.length];
    actionIndex=0;previewIndex=0;renderBox();renderSelectedAction();
  }
  $('actionPrev').onclick=()=>moveBox(-1);
  $('actionNext').onclick=()=>moveBox(1);
  dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
  dialog.addEventListener('close',()=>{
    $('actionGif').onload=null;$('actionGif').onerror=null;$('actionGif').removeAttribute('src');
    document.body.style.overflow=previousOverflow;
    if(trigger?.isConnected)trigger.focus();
    activeBox=null;
  });
  dialog.addEventListener('keydown',event=>{
    if(!activeBox)return;
    if(event.key==='ArrowRight'||event.key==='ArrowLeft'){
      event.preventDefault();
      moveBox(event.key==='ArrowRight'?1:-1);
    }
  });
})();
