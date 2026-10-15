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
  let activeBox=null,actionIndex=0,previewIndex=0,trigger=null,previousOverflow='';
  function twStatus(box){
    if(box.twReleased!==true)return '<span class="tw-status-chip action-unconfirmed">台服狀態尚未確認</span>';
    const now=Date.now();
    const current=now>=Date.parse(`${box.twDate}T00:00:00+08:00`) && now<Date.parse(box.twEndDate);
    return `<span class="tw-status-chip ${current?'tw-status-selling':'tw-status-released'}" title="台服公告核對至 ${box.checkedDate}">${current?'台服當期':'台服已推出'}</span>`;
  }
  M.renderActionCards=rows=>{
    $('feed').innerHTML='<p class="lucky-order-hint action-hint">韓服編號依已確認的首次上架日期排序。未有台服正式譯名的內容標示「暫譯」；台服狀態尚未確認不代表尚未推出。點選封面查看動作，完整 GIF 僅在開啟預覽時載入。</p>'+rows.map(box=>`
      <article class="entry action-entry" data-action-box="${escape(box.id)}">
        <button type="button" class="image-wrap action-cover action-open" data-action-id="${escape(box.id)}" aria-label="查看${escape(box.zh)}全部 ${box.actions.length} 個動作">
          <img src="${escape(box.image)}" alt="${escape(box.zh)}動作預覽封面" loading="lazy" decoding="async" width="640" height="640">
          <span class="action-play" aria-hidden="true">▶ 查看 ${box.actions.length} 個動作</span><span class="num-badge">韓服 #${box.number}</span>
        </button>
        <div class="entry-info"><div class="entry-tags">${twStatus(box)}</div><div class="name-row"><span class="color-dot" aria-hidden="true"></span><h3 class="name">${escape(box.zh)}</h3></div><div class="ko" lang="ko">${escape(box.ko)}</div>
          <dl class="action-meta"><div><dt>韓服推出</dt><dd>${date(box.date)}</dd></div><div><dt>韓服售價</dt><dd>${money(box.priceDeka)}</dd></div></dl>
          <button type="button" class="action-detail-button action-open" data-action-id="${escape(box.id)}">查看全部動作</button>
        </div>
      </article>`).join('');
    document.querySelectorAll('.action-open').forEach(button=>button.addEventListener('click',()=>open(boxByButton(button),button)));
  };
  function boxByButton(button){return byId.get(button.dataset.actionId)}
  function open(box,button){
    if(!box)return;
    activeBox=box;actionIndex=0;previewIndex=0;trigger=button;
    $('actionDialogTitle').textContent=box.zh;
    $('actionDialogKo').textContent=box.ko;
    $('actionChoices').innerHTML=box.actions.map((action,index)=>`<button class="action-choice" type="button" data-action-index="${index}" aria-pressed="${index===0}"><strong>${escape(action.zh)}${action.translationStatus==='provisional'?'（暫譯）':''}</strong><span lang="ko">${escape(action.ko)}</span></button>`).join('');
    $('actionChoices').querySelectorAll('button').forEach(choice=>choice.onclick=()=>{
      actionIndex=Number(choice.dataset.actionIndex);previewIndex=0;renderSelectedAction();
    });
    previousOverflow=document.body.style.overflow;
    dialog.showModal();document.body.style.overflow='hidden';
    renderSelectedAction();$('actionDialogClose').focus();
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
    img.onerror=()=>{$('actionPlaybackStatus').textContent='GIF 載入失敗，請點選上方官方預覽重試。';};
    img.alt=`${activeBox.zh}：${action.zh} ${action.ko}，${preview.label}`;
    img.removeAttribute('src');img.src=preview.path;
    $('actionOriginalLink').href=preview.path;
  }
  $('actionDialogClose').onclick=()=>dialog.close();
  dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
  dialog.addEventListener('close',()=>{
    $('actionGif').onload=null;$('actionGif').onerror=null;$('actionGif').removeAttribute('src');
    document.body.style.overflow=previousOverflow;
    if(trigger?.isConnected)trigger.focus();
    activeBox=null;
  });
  dialog.addEventListener('keydown',event=>{
    if(!activeBox||event.target.matches('button,a,summary'))return;
    if(event.key==='ArrowRight'||event.key==='ArrowLeft'){
      event.preventDefault();
      actionIndex=(actionIndex+(event.key==='ArrowRight'?1:-1)+activeBox.actions.length)%activeBox.actions.length;
      previewIndex=0;renderSelectedAction();
    }
  });
})();
