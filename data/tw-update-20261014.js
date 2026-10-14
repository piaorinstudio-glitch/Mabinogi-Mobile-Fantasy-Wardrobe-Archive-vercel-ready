// 2026-10-14 Taiwan server sale-status synchronization.
// Load after data/tw-update-20260930.js, before assets/js/app.js.
// No new appearance records or images: only existing TW status transitions.
(() => {
  window.MABI = window.MABI || {};
  const M = window.MABI;

  // Official Taiwan maintenance notice: the 2026-10-14 05:59 sale cutoff.
  // Other tracked entries have twEndDate 2026-10-14 in tw-update-20260925.js.
  const ended = [
    'pass-3',      // 寧靜花漾：當期通行證票券
    'lucky-3',     // 寂靜的審判：時裝幸運箱
    'lucky-14',    // 淡雅誘惑：時裝幸運箱
    'lucky-15',    // 盛宴的主人：時裝幸運箱
    'pet-3',       // 幼貓頭鷹：寵物幸運箱
    'pet-6'        // 中秋節期間寵物商品，依已收錄的台服結束日期
  ];

  const current = new Set(M.TW_CURRENT_IDS || []);
  const released = new Set(M.TW_RELEASED_IDS || []);
  for (const id of ended) {
    current.delete(id);
    released.add(id);
  }

  // Preserve still-on-sale entries:
  // 皇家交響／古樹統治者 (until 11/25), and both MapleStory boxes (until 10/21).
  M.TW_CURRENT_IDS = current;
  M.TW_RELEASED_IDS = released;
  M.TW_STATUS_UPDATED = '2026-10-14';
  M.TW_STATUS_SOURCES = [
    ...(M.TW_STATUS_SOURCES || []),
    {
      label: '台服 2026/10/14 例行維護與結束販售商品',
      url: 'https://tw.nexon.com/mabinogimobile/home/news/notice/3562593'
    },
    {
      label: '台服 2026/09/30 楓葉朋友們幸運箱販售期間',
      url: 'https://tw.nexon.com/mabinogimobile/home/news/notice/3550860'
    }
  ];
})();
