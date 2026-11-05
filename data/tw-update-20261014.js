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

// 2026-11-05 correction: follow the original Taiwan-only numbering, pet skill format,
// and Korean/Taiwan interleaving rules. The two JJK outfits each have a TW number;
// the JJK pets are ONE Taiwan pool with two separate selectable skill details.
(() => {
  'use strict';
  const M=window.MABI;
  if(!M || !Array.isArray(M.DATA))throw new Error('Missing wardrobe catalog');
  const data=M.DATA;
  const twNotice='https://tw.nexon.com/mabinogimobile/home/news/notice/3569092';
  const krJJK='https://mabinogimobile.nexon.com/News/Notice/3571431';
  const krPass='https://mabinogimobile.nexon.com/News/Notice/3571556';
  const krGhost='https://mabinogimobile.nexon.com/News/Notice/3571557';
  const twStart='2026-11-04T00:00:00+08:00';
  const twEnd='2026-12-02T05:59:00+08:00';
  const now=Date.now();
  // Explicitly remove the four Crion cards (as requested), even if a previously
  // loaded file added them. Do NOT affect other packages, notably Cozy Day.
  const removeIds=new Set(['package-8','package-9','package-10','package-11','pet-25']);
  for(let i=data.length-1;i>=0;i--){if(removeIds.has(data[i].id))data.splice(i,1);}

  // Previous pass and fashion boxes stop being marked newest after this release.
  for(const item of data){if(item.type==='pass'||item.type==='lucky')item.latest=false;}
  const items=[
    {id:'pass-14',type:'pass',typeLabel:'冒險家通行證',number:14,
      zh:'Cozy Day 冒險家通行證（暫譯）',ko:'코지데이 모험가 패스',
      lines:['Cozy Day 冒險家通行證（暫譯）','코지데이 모험가 패스','Cozy Day 花漾耳環｜코지데이 블라썸 이어링'],
      date:'2026-10-29',endDate:'2026-12-16',year:'2026',notice:krPass,
      nameStatus:'provisional',image:'image/pass-14.png',latest:true,priceMCash:1980,
      notes:['高級通行證70階；第5階 Cozy Day 花漾耳環。']},
    {id:'package-12',type:'package',typeLabel:'全套套組',number:8,
      zh:'Cozy Day 收藏包（暫譯）',ko:'코지데이 컬렉션 백',
      lines:['Cozy Day 收藏包（暫譯）','코지데이 컬렉션 백'],
      date:'2026-10-29',endDate:'2027-01-28',year:'2026',notice:krPass,
      nameStatus:'provisional',image:'image/package-12.png',priceMCash:1000,
      notes:['高級通行證第25階後可以購買；2026/12/16前優惠1000 M Cash。']},
    {id:'pet-23',type:'pet',typeLabel:'寵物',number:23,
      zh:'幽靈獵犬（菁英，暫譯）',ko:'유령 리트리버',kind:'限定',
      lines:['幽靈獵犬（菁英，暫譯）','유령 리트리버 (엘리트)'],
      date:'2026-10-29',endDate:'2026-11-12',year:'2026',notice:krGhost,
      nameStatus:'provisional',image:'image/pet-23.png',
      variants:[{zh:'幽靈獵犬',ko:'유령 리트리버',rarity:'菁英'}],
      notes:['期間限定禮包售價4900 M Cash；技能與固定同行詞條缺可驗證面板。']},
    // Taiwan first release: keep the same '台版 #' convention as the existing
    // MapleStory collaboration, and interleave by independent TW sequence.
    {id:'lucky-41',type:'lucky',typeLabel:'幸運箱',number:2,
      displayNumber:'台版 #2',pairOrder:2,server:'TW',
      zh:'束襟制服',ko:'여민 깃 제복',
      lines:['台版 #2','束襟制服','여민 깃 제복','咒術迴戰：時裝幸運箱'],
      date:'2026-11-04',year:'2026',twDate:'2026-11-04',twEndDate:twEnd,
      krDate:'2026-11-05',krNotice:krJJK,
      notice:twNotice,twNotice,twNameStatus:'official_tw',nameStatus:'official_tw',
      image:'image/lucky-41.png',latest:true},
    {id:'lucky-42',type:'lucky',typeLabel:'幸運箱',number:3,
      displayNumber:'台版 #3',pairOrder:3,server:'TW',
      zh:'兩面宿儺服飾',ko:'양면 스쿠나 의상',
      lines:['台版 #3','兩面宿儺服飾','양면 스쿠나 의상','咒術迴戰：時裝幸運箱'],
      date:'2026-11-04',year:'2026',twDate:'2026-11-04',twEndDate:twEnd,
      krDate:'2026-11-05',krNotice:krJJK,
      notice:twNotice,twNotice,twNameStatus:'official_tw',nameStatus:'official_tw',
      image:'image/lucky-42.png',latest:true},
    {id:'pet-24',type:'pet',typeLabel:'寵物幸運箱',number:2,
      displayNumber:'台版 #2',pairOrder:2,server:'TW',
      zh:'咒術迴戰 式神：寵物幸運箱',ko:'옥견 혼 · 누에',kind:'聯動',
      lines:['台版 #2','咒術迴戰 式神：寵物幸運箱','玉犬・渾｜옥견 혼','鵺｜누에'],
      date:'2026-11-04',year:'2026',twDate:'2026-11-04',twEndDate:twEnd,
      krDate:'2026-11-05',krNotice:krJJK,
      notice:twNotice,twNotice,twNameStatus:'official_tw',nameStatus:'official_tw',
      image:'image/pet-24.png',
      imageNote:'玉犬・渾、鵺同一個聯名史詩寵物池。',
      variants:[{zh:'玉犬・渾',ko:'옥견 혼',rarity:'史詩'},
                {zh:'鵺',ko:'누에',rarity:'史詩'}],
      latest:true}
  ];

  const byId=new Map(data.map((item,i)=>[item.id,i]));
  for(const row of items){
    const idx=byId.get(row.id);
    if(idx===undefined){byId.set(row.id,data.length);data.push(row);}
    else if(data[idx].ko===row.ko){
      // Replace the full record to remove stale Korean-only numbering and variants.
      data[idx]=row;
    }else if(row.id==='pet-24'){
      // Older release stored only the first pet on this card; now the two share a pool.
      data[idx]=row;
    }else throw new Error('Catalog ID collision '+row.id);
  }
  // Idempotent removal and confirmation, including if an older helper script ran.
  for(let i=data.length-1;i>=0;i--){if(removeIds.has(data[i].id))data.splice(i,1);}
  if(data.filter(x=>x.id==='pet-24').length!==1)throw new Error('Pet pool must have one card');

  M.TW_CURRENT_IDS=new Set(M.TW_CURRENT_IDS||[]);
  M.TW_RELEASED_IDS=new Set(M.TW_RELEASED_IDS||[]);
  for(const id of ['lucky-41','lucky-42','pet-24']){
    M.TW_RELEASED_IDS.add(id);
    if(now>=Date.parse(twStart)&&now<Date.parse(twEnd)) M.TW_CURRENT_IDS.add(id);
    else M.TW_CURRENT_IDS.delete(id);
  }
  for(const id of [...removeIds]){
    M.TW_CURRENT_IDS.delete(id);M.TW_RELEASED_IDS.delete(id);
  }
  M.TW_STATUS_UPDATED='2026-11-05';
  M.TW_STATUS_SOURCES=[...(M.TW_STATUS_SOURCES||[]),
    {label:'台版 2026/11/04 咒術迴戰幸運箱與寵物',url:twNotice},
    {label:'韓服 2026/10/29 Cozy Day 與幽靈獵犬',url:krPass},
    {label:'韓服 2026/11/05 咒術迴戰合作',url:krJJK}];

  M.PET_STATS=M.PET_STATS||{};
  M.PET_FAMILY_BY_KO=M.PET_FAMILY_BY_KO||{};
  M.PET_SKILL_FAMILIES=M.PET_SKILL_FAMILIES||{};
  // The site traditionally shows ONLY core fixed companion combat attributes
  // (two badges), not the five shared +5 basics or the shared charm +3000.
  // Preserve their verified numeric values in these two visible badges.
  M.PET_STATS['옥견 혼']=['技能威力 +14','攻擊力 +8'];
  M.PET_STATS['누에']=['追擊 +14','攻擊力 +8'];
  M.PET_FIXED_BASELINE=M.PET_FIXED_BASELINE||{};
  const base={力量:5,技巧:5,智力:5,意志:5,幸運:5,魅力:3000};
  M.PET_FIXED_BASELINE['옥견 혼']={...base};
  M.PET_FIXED_BASELINE['누에']={...base};

  M.PET_FAMILY_BY_KO['옥견 혼']='jjk_gyokuken_20261105';
  M.PET_SKILL_FAMILIES.jjk_gyokuken_20261105={
    base:'資料缺失',
    epic:'破防嚎叫 S',
    legendEpic:'資料缺失',
    baseEffect:'史詩以下版本尚無可靠面板；詳細數值缺失',
    epicEffect:'[主動] 寵物主人鎖定的敵人處於破防狀態時可施放。施放時，於 7 秒期間，寵物主人的無防備傷害增加 3%。（冷卻時間：8 秒）',
    legendEpicEffect:'傳說升階的 SS 效果尚無可靠面板；詳細數值缺失',
    epicNote:'台服 2026/11/04 原生史詩 Lv.1 面板。同行能力：技能威力 +14、攻擊力 +8；基本五維各 +5、魅力 +3000。',
    legendEpicNote:'不以其他幼狼技能推算 SS 效果。'
  };
  M.PET_FAMILY_BY_KO['누에']='jjk_nue_20261105';
  M.PET_SKILL_FAMILIES.jjk_nue_20261105={
    base:'資料缺失',
    epic:'疾速的振翅 S',
    legendEpic:'資料缺失',
    baseEffect:'史詩以下版本尚無可靠面板；詳細數值缺失',
    epicEffect:'[主動] 施放時，於 5 秒期間，將寵物主人的技能使用速度、攻擊速度、施法及蓄力速度增加 12%。（冷卻時間：30 秒）',
    legendEpicEffect:'傳說升階的 SS 效果尚無可靠面板；詳細數值缺失',
    epicNote:'台服 2026/11/04 原生史詩 Lv.1 面板。同行能力：追擊 +14、攻擊力 +8；基本五維各 +5、魅力 +3000。',
    legendEpicNote:'不以其他貓頭鷹技能推算 SS 效果。'
  };
  M.PET_FAMILY_BY_KO['유령 리트리버']='ghost_retriever_20261029';
  M.PET_STATS['유령 리트리버']=[];
  M.PET_SKILL_FAMILIES.ghost_retriever_20261029={
    base:'資料缺失',epic:'資料缺失',legendEpic:'資料缺失',
    baseEffect:'固有技能面板尚缺資料；詳細數值缺失',
    epicEffect:'升階史詩 S 技能面板尚缺資料；詳細數值缺失',
    legendEpicEffect:'傳說 SS 技能面板尚缺資料；詳細數值缺失'
  };
  M.PET_DETAIL_SOURCES=M.PET_DETAIL_SOURCES||[];
  for(const entry of [
    {title:'玉犬・渾：原生史詩技能與同行能力面板',kind:'使用者提供台服遊戲截圖'},
    {title:'鵺：原生史詩技能與同行能力面板',kind:'使用者提供台服遊戲截圖'}
  ])if(!M.PET_DETAIL_SOURCES.some(x=>x.title===entry.title))M.PET_DETAIL_SOURCES.push(entry);
})();
