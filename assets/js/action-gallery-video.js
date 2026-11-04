// Action-box gallery. Published previews are compressed MP4, never GIF.
// Videos are loaded ONLY when an action is opened and released on close.
(() => {
  'use strict';
  const M = window.MABI;
  if (!M || !Array.isArray(M.ACTION_BOXES)) throw new Error('Missing action-box data');
  const byId = new Map(M.ACTION_BOXES.map(box => [box.id, box]));
  const dialog = document.getElementById('actionDialog');
  const $ = id => document.getElementById(id);
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const date = v => v ? String(v).slice(0, 10).replaceAll('-', '/') : '尚未確認';
  const money = v => Number.isFinite(v) ? `${v.toLocaleString('en-US')} 德卡` : '資料缺失';
  const cleanName = v => String(v ?? '').replace(/（暫譯）/g, '');
  let activeBox = null, actionIndex = 0, previewIndex = 0, trigger = null;
  let oldOverflow = '', visibleBoxes = [], playbackToken = 0;
  const video = $('actionVideo');

  function twStatus(box) {
    if (box.twReleased !== true) return '';
    const t = Date.now();
    const until = Date.parse(box.twEndDate || '');
    const since = Date.parse(`${box.twDate || '2099-01-01'}T00:00:00+08:00`);
    const current = Number.isFinite(until) && t >= since && t < until;
    return `<span class="tw-status-chip ${current?'tw-status-selling':'tw-status-released'}" title="台服公告核對至 ${esc(box.checkedDate || '未知')}">${current?'台服當期':'台服已推出'}</span>`;
  }

  M.renderActionCards = rows => {
    visibleBoxes = rows.slice();
    $('feed').innerHTML = '<div class="lucky-order-hint">※ 「韓服 #」代表<strong>韓服推出順序</strong>；下方日期為韓服推出日期。台服與韓服的上架組合、批次可能不同。</div>' + rows.map(box => `
      <article class="entry action-entry" data-action-box="${esc(box.id)}">
        <button type="button" class="image-wrap action-cover action-open" data-action-id="${esc(box.id)}" aria-label="查看${esc(cleanName(box.zh))}全部 ${box.actions.length} 個動作">
          <img src="${esc(box.image)}" alt="${esc(cleanName(box.zh))}動作預覽封面" loading="lazy" decoding="async" width="640" height="640">
          <span class="action-play" aria-hidden="true">▶ 查看 ${box.actions.length} 個動作</span><span class="num-badge has-date action-issue-badge"><span class="num-badge-main">韓服 #${box.number}</span><span class="num-badge-date">${date(box.date)}</span><span class="num-badge-date">${money(box.priceDeka)}</span></span>
        </button>
        <div class="entry-info">${box.twReleased===true?`<div class="entry-tags">${twStatus(box)}</div>`:''}<div class="name-row"><span class="color-dot" aria-hidden="true"></span><h3 class="name">${esc(cleanName(box.zh))}</h3></div><div class="ko" lang="ko">${esc(box.ko)}</div></div>
      </article>`).join('');
    document.querySelectorAll('.action-open').forEach(button => button.addEventListener('click', () => open(byId.get(button.dataset.actionId), button)));
  };

  function open(box, button) {
    if (!box) return;
    activeBox = box; actionIndex = 0; previewIndex = 0; trigger = button;
    renderBox();
    oldOverflow = document.body.style.overflow;
    dialog.showModal(); document.body.style.overflow = 'hidden';
    renderSelectedAction(); $('actionDialogClose').focus();
  }
  function renderBox() {
    $('actionDialogTitle').textContent = cleanName(activeBox.zh);
    $('actionChoices').innerHTML = activeBox.actions.map((a, i) => `<button class="action-choice" type="button" data-action-index="${i}" aria-pressed="${i === 0}"><strong>${esc(cleanName(a.zh))}</strong><span lang="ko">${esc(a.ko)}</span></button>`).join('');
    $('actionChoices').querySelectorAll('button').forEach(button => button.onclick = () => {
      actionIndex = Number(button.dataset.actionIndex);
      previewIndex = 0;
      renderSelectedAction();
    });
  }
  function stopVideo() {
    playbackToken++;
    video.pause();
    video.removeAttribute('src');
    video.removeAttribute('poster');
    video.load();
  }
  function renderSelectedAction() {
    const action = activeBox.actions[actionIndex];
    $('actionChoices').querySelectorAll('button').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.actionIndex) === actionIndex)));
    $('actionVariants').innerHTML = action.previews.map((p, i) => `<button type="button" data-preview-index="${i}" aria-pressed="${i === previewIndex}">${esc(p.label)}</button>`).join('');
    $('actionVariants').querySelectorAll('button').forEach(button => button.onclick = () => {
      previewIndex = Number(button.dataset.previewIndex);
      renderSelectedAction();
    });
    const preview = action.previews[previewIndex];
    stopVideo();
    const token = playbackToken;
    const status = $('actionPlaybackStatus');
    status.textContent = '影片載入中…';
    if (!preview || !/^image\/actions\/[\w/-]+\.mp4$/.test(preview.path)) {
      status.textContent = '影片路徑無效，無法播放。';
      return;
    }
    video.setAttribute('aria-label', `${cleanName(activeBox.zh)}：${cleanName(action.zh)} ${action.ko}，${preview.label}`);
    video.poster = preview.cover;
    video.src = preview.path;
    video.load();
    video.play().then(() => {
      if (token === playbackToken) status.textContent = '';
    }).catch(() => {
      if (token === playbackToken) status.textContent = '請按影片播放鍵開始預覽。';
    });
  }
  video.addEventListener('error', () => {
    if (activeBox && video.getAttribute('src')) $('actionPlaybackStatus').textContent = '影片載入失敗，請重新選擇展示版本。';
  });
  $('actionDialogClose').onclick = () => dialog.close();
  function moveBox(step) {
    if (!activeBox || !visibleBoxes.length) return;
    const at = visibleBoxes.findIndex(box => box.id === activeBox.id);
    activeBox = visibleBoxes[(at + step + visibleBoxes.length) % visibleBoxes.length];
    actionIndex = 0; previewIndex = 0;
    renderBox(); renderSelectedAction();
  }
  $('actionPrev').onclick = () => moveBox(-1);
  $('actionNext').onclick = () => moveBox(1);
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    stopVideo();
    $('actionPlaybackStatus').textContent = '';
    document.body.style.overflow = oldOverflow;
    if (trigger?.isConnected) trigger.focus();
    activeBox = null;
  });
  dialog.addEventListener('keydown', event => {
    if (!activeBox) return;
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      moveBox(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
})();
