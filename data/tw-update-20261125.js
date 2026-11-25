// 2026-11-25 Taiwan Season 1 wardrobe release-state synchronization.
// Loaded after data/tw-update-20261014.js and before assets/js/app.js.
// Reuses actual image files already committed to the repo; does not create duplicate KR cards.
(() => {
  'use strict';
  const M = window.MABI;
  if (!M || !Array.isArray(M.DATA)) throw new Error('Missing wardrobe catalog for TW 2026-11-25 update');
  if (!(M.TW_CURRENT_IDS instanceof Set) || !(M.TW_RELEASED_IDS instanceof Set)) {
    throw new Error('Missing TW release sets for 2026-11-25 update');
  }
  const twDate = '2026-11-25';
  const end = '2026-12-16T05:59:00+08:00';
  const laterEnd = '2027-01-13T05:59:00+08:00';
  const sales = 'https://forum.nexon.com/mabinogimobiletw/7125?threadId=3586203';
  const passNotice = 'https://forum.nexon.com/mabinogimobiletw/7125?threadId=3586204';
  const setNotice = 'https://forum.nexon.com/mabinogimobiletw/7125?threadId=3586213';
  const legendNotice = 'https://forum.nexon.com/mabinogimobiletw/7125?threadId=3586209';
  const byId = new Map(M.DATA.map(item => [item.id, item]));
  const updates = [
    {id: 'pass-5', ko: '이븐스타', zh: '暮星', twEndDate: end,
      twNotice: passNotice, notes: ['台服第 1 季 11/25 冒險家通行證：70 階，頂級票券 1,980 M 幣；第 5 階可取得「星鑄眼鏡」，第 25 階為「暮星收藏包」。']},
    {id: 'lucky-12', ko: '거룩한 신념', zh: '神聖信念', twEndDate: end, twNotice: sales,
      notes: ['台服 11/25 時裝幸運箱；主題套裝「神聖審判」。每抽消耗頂級時裝票券 1 張；每 50／100 抽分別有額外獎勵。']},
    {id: 'lucky-13', ko: '정화의 빛', zh: '淨化之光', twEndDate: end, twNotice: sales,
      notes: ['台服 11/25 時裝幸運箱；主題套裝「莊嚴光輝」。每抽消耗頂級時裝票券 1 張。']},
    {id: 'lucky-22', ko: '예언의 은둔자', zh: '預言隱遁者', twEndDate: end, twNotice: sales,
      notes: ['台服 11/25 時裝幸運箱；主題套裝「寂靜誓約」。每抽消耗頂級時裝票券 1 張。']},
    {id: 'pet-7', ko: '햄스터', zh: '倉鼠系列', twEndDate: end, twNotice: sales,
      notes: ['台服 11/25「倉鼠：寵物幸運箱」；黃金倉鼠（史詩）、棕色倉鼠（菁英）、白色倉鼠（稀有）、深灰色倉鼠（高級）。',
              '黃金倉鼠稱號「黃金倉鼠的朋友」：配戴效果智力 +50、幸運 +50；持有效果攻擊力 +20、防禦力 +20、強擊強化 +130。此為稱號效果，非固定同行能力。',
              '固有技能與升階技能沿用網站現有韓服技能資料；未確認的數值保持「資料缺失」，不猜測。']},
    {id: 'package-3', ko: '로드나이트', zh: '領主騎士', twEndDate: laterEnd, twNotice: setNotice,
      priceMCash: 3980,
      notes: ['台服 11/25 領主騎士全套套組；3,980 M 幣，包含時裝武器選擇盒、套組選擇包及貴族品種選擇箱等。']},
    {id: 'legend-3', ko: '홀리 루체테', zh: '神聖光輝', twEndDate: laterEnd, twNotice: legendNotice,
      notes: ['台服 11/25 傳說時裝「神聖光輝」；可透過史詩時裝合成取得。集滿並穿戴四件可解鎖長袍專屬任務；長袍禮品包亦可於商城點數商店購買。']}
  ];
  const now = Date.now();
  const start = Date.parse('2026-11-25T00:00:00+08:00');
  for (const update of updates) {
    const item = byId.get(update.id);
    if (!item) throw new Error('2026-11-25 TW item not found: ' + update.id);
    if (item.ko !== update.ko) throw new Error('2026-11-25 TW Korean name mismatch: ' + update.id);
    const {id, ko, ...attrs} = update;
    // Preserve the original KR date, numbering, image paths and rarity variants.
    Object.assign(item, attrs, {
      twDate,
      twNameStatus: 'official_tw',
      nameStatus: 'official_tw',
      twReleased: true
    });
    if (Array.isArray(item.lines) && item.lines.length) item.lines[0] = item.zh;
    M.TW_RELEASED_IDS.add(id);
    if (now >= start && now < Date.parse(update.twEndDate)) M.TW_CURRENT_IDS.add(id);
    else M.TW_CURRENT_IDS.delete(id);
  }
  // Older 10/14 Taiwan rotation ends at the 11/25 maintenance.
  for (const id of ['pass-4', 'lucky-7', 'lucky-10', 'lucky-11', 'pet-5']) {
    M.TW_CURRENT_IDS.delete(id);
    M.TW_RELEASED_IDS.add(id);
  }
  M.TW_STATUS_UPDATED = twDate;
  M.TW_STATUS_SOURCES = [...(M.TW_STATUS_SOURCES || []),
    {label: '台服 11/25 三款時裝幸運箱與倉鼠寵物', url: sales},
    {label: '台服 11/25 暮星冒險家通行證', url: passNotice},
    {label: '台服 11/25 領主騎士全套套組', url: setNotice},
    {label: '台服 11/25 神聖光輝傳說時裝', url: legendNotice}
  ];
})();
