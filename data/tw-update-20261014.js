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

// 2026-10-15 completion of the 10/14 TW rotation. Data-only, no UI changes.
(() => {
  const M=window.MABI;
  const sale='https://tw.nexon.com/mabinogimobile/home/news/notice/3562703';
  const pass='https://tw.nexon.com/mabinogimobile/home/news/notice/3562691';
  const updates={
    'pass-4':{zh:'呱呱雨季',twNotice:pass,twNameBasis:'台服公告各件時裝的共同名稱前綴：呱呱雨季'},
    'lucky-7':{zh:'霜花的盛宴',twNotice:sale},
    'lucky-10':{zh:'怦然心動探險隊',twNotice:sale},
    'lucky-11':{zh:'清新微風',twNotice:sale},
    'pet-5':{zh:'西施犬系列',twNotice:sale}
  };
  const current=new Set(M.TW_CURRENT_IDS||[]),released=new Set(M.TW_RELEASED_IDS||[]);
  for(const [id,update] of Object.entries(updates)){
    const item=M.DATA.find(row=>row.id===id);
    if(!item)continue;
    Object.assign(item,update,{twDate:'2026-10-14',twEndDate:'2026-11-25T05:59:00+08:00',twNameStatus:'official_tw'});
    if(item.lines?.length)item.lines[0]=item.zh;
    if(id==='lucky-7'&&item.lines?.length>2)item.lines[2]='套裝｜高潔恩典';
    if(id==='pet-5'){
      const names={'연갈색 시추':'淺棕色西施犬','회색 시추':'灰色西施犬','흰 시추':'白色西施犬','갈색 시추':'棕色西施犬'};
      for(const variant of item.variants||[])if(names[variant.ko])variant.zh=names[variant.ko];
    }
    current.add(id);released.add(id);
  }
  // Recalculate known sale windows at page load, using Taiwan-local time explicitly.
  // Status refers to the featured box, not every pet remaining in the cumulative pool.
  const now=Date.now();
  for(const id of [...current]){
    const item=M.DATA.find(row=>row.id===id);
    if(!item?.twEndDate)continue;
    const end=Date.parse(item.twEndDate.length===10?item.twEndDate+'T05:59:00+08:00':item.twEndDate);
    const start=item.twDate?Date.parse(item.twDate+'T00:00:00+08:00'):-Infinity;
    if(now>=end){current.delete(id);released.add(id);}
    else if(now<start){current.delete(id);released.delete(id);}
  }
  M.TW_CURRENT_IDS=current;M.TW_RELEASED_IDS=released;M.TW_STATUS_UPDATED='2026-10-15';
  M.TW_STATUS_SOURCES=[...(M.TW_STATUS_SOURCES||[]),
    {label:'台服2026/10/14幸運箱、寵物與動作箱',url:sale},
    {label:'台服2026/10/14冒險家通行證',url:pass}];
  M.TW_STATUS_VERIFICATION={date:'2026-10-15',
    archives:['https://erinn.tw/notices/3562703','https://erinn.tw/notices/3562691'],
    note:'本次官方網頁內文未正常載入；10/14商品內容以官方公告存檔交叉核對，保留原公告網址。'};
})();
