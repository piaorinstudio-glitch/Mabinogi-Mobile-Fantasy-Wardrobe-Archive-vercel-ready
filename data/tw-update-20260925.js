// Taiwan server status sync through 2026-09-25.
// Load after data/site-config.js and after any catalog update files, before assets/js/app.js.
(() => {
  window.MABI = window.MABI || {};
  const M = window.MABI;
  const data = Array.isArray(M.DATA) ? M.DATA : [];
  const byId = new Map(data.map(item => [item && item.id, item]));

  // Official Taiwan-localized names for items that are now released on TW.
  const twNames = {
    'pass-3': '寧靜花漾',
    'lucky-3': '寂靜的審判',
    'lucky-14': '淡雅誘惑',
    'lucky-15': '盛宴的主人',
    'package-2': '皇家交響',
    'legend-2': '古樹統治者',
    'pet-3': '幼貓頭鷹系列'
  };

  for (const [id, zh] of Object.entries(twNames)) {
    const item = byId.get(id);
    if (!item) continue;
    item.zh = zh;
    if (Array.isArray(item.lines) && item.lines.length) item.lines[0] = zh;
  }

  // Keep Taiwan launch windows on the item data for future UI/use.
  const twMeta = {
    'pass-3':    {twDate:'2026-09-09', twEndDate:'2026-10-14', twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541015'},
    'lucky-3':   {twDate:'2026-09-09', twEndDate:'2026-10-14', twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541055'},
    'lucky-14':  {twDate:'2026-09-09', twEndDate:'2026-10-14', twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541055'},
    'lucky-15':  {twDate:'2026-09-09', twEndDate:'2026-10-14', twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541055'},
    'package-2': {twDate:'2026-09-09', twEndDate:'2026-11-25', twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541044'},
    'legend-2':  {twDate:'2026-09-09', twEndDate:'2026-11-25', twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541066'},
    'pet-3':     {twDate:'2026-09-09', twEndDate:'2026-10-14', twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541055'},
    'pet-6':     {twDate:'2026-09-23', twEndDate:'2026-10-14', twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3550055'}
  };
  for (const [id, meta] of Object.entries(twMeta)) {
    const item = byId.get(id);
    if (item) Object.assign(item, meta);
  }

  // Gold chip: currently on sale / obtainable in TW as of 2026-09-25.
  M.TW_CURRENT_IDS = new Set([
    'pass-3',
    'lucky-3', 'lucky-14', 'lucky-15',
    'package-2',
    'legend-2',
    'pet-3', 'pet-6'
  ]);

  // Gray chip: released at least once in TW. Preserve the previous released set and add new releases.
  const released = new Set(M.TW_RELEASED_IDS || []);
  [
    'pass-3',
    'lucky-3', 'lucky-14', 'lucky-15',
    'package-2',
    'legend-2',
    'pet-3', 'pet-6'
  ].forEach(id => released.add(id));
  M.TW_RELEASED_IDS = released;

  M.TW_STATUS_UPDATED = '2026-09-25';
  M.TW_STATUS_SOURCES = [
    {label:'台服 2026/09/09 冒險家通行證', url:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541015'},
    {label:'台服 2026/09/09 幸運箱與寵物幸運箱', url:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541055'},
    {label:'台服 皇家交響全套套組', url:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541044'},
    {label:'台服 古樹統治者', url:'https://tw.nexon.com/mabinogimobile/home/news/notice/3541066'},
    {label:'台服 2026/09/23 新套組（賞月兔）', url:'https://tw.nexon.com/mabinogimobile/home/news/notice/3550055'}
  ];
})();
