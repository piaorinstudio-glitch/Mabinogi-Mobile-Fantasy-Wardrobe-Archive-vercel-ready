// Taiwan MapleStory collaboration additions — 2026-09-30.
// These are separate TW cards. Existing KR MapleStory entries remain untouched.
(() => {
  window.MABI = window.MABI || {};
  const M = window.MABI;
  const data = Array.isArray(M.DATA) ? M.DATA : (M.DATA = []);

  const updates = [
    {
      id: 'tw-lucky-maple-1',
      type: 'lucky',
      typeLabel: '幸運箱',
      number: '台版 #1',
      zh: '楓葉朋友們：時裝幸運箱',
      ko: '',
      lines: ['台版 #1', '楓葉朋友們：時裝幸運箱', '《瑪奇 Mobile》×《新楓之谷》'],
      date: '2026-09-30',
      endDate: '2026-10-21',
      year: '2026',
      notice: 'https://tw.nexon.com/mabinogimobile/home/news/notice/3550868',
      image: 'image/tw-lucky-maple-1.png',
      twDate: '2026-09-30',
      twEndDate: '2026-10-21',
      twNotice: 'https://tw.nexon.com/mabinogimobile/home/news/notice/3550868',
      latest: true,
      server: 'TW'
    },
    {
      id: 'tw-pet-maple-2',
      type: 'pet',
      typeLabel: '寵物',
      number: '台版 #2',
      zh: '楓葉朋友們：寵物幸運箱',
      ko: '',
      lines: ['台版 #2', '楓葉朋友們：寵物幸運箱', '《瑪奇 Mobile》×《新楓之谷》'],
      kind: '聯動',
      date: '2026-09-30',
      endDate: '2026-10-21',
      year: '2026',
      notice: 'https://tw.nexon.com/mabinogimobile/home/news/notice/3550868',
      image: 'image/tw-pet-maple-2.png',
      variants: [
        {zh:'快樂粉豆貓', ko:'', rarity:'史詩'},
        {zh:'企鵝王與小熊', ko:'', rarity:'史詩'}
      ],
      twDate: '2026-09-30',
      twEndDate: '2026-10-21',
      twNotice: 'https://tw.nexon.com/mabinogimobile/home/news/notice/3550868',
      server: 'TW'
    }
  ];

  const byId = new Map(data.map((item,index)=>[item && item.id,index]));
  for (const item of updates) {
    const i=byId.get(item.id);
    if(i===undefined){ data.push(item); byId.set(item.id,data.length-1); }
    else data[i]={...data[i],...item};
  }

  // Do not remove/replace the original KR MapleStory entries.
  const current = new Set(M.TW_CURRENT_IDS || []);
  current.add('tw-lucky-maple-1');
  current.add('tw-pet-maple-2');
  M.TW_CURRENT_IDS = current;

  const released = new Set(M.TW_RELEASED_IDS || []);
  released.add('tw-lucky-maple-1');
  released.add('tw-pet-maple-2');
  M.TW_RELEASED_IDS = released;

  M.TW_STATUS_UPDATED = '2026-10-04';
})();
