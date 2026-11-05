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

// 2026-11-04 official Taiwan Jujutsu Kaisen collaboration.
// Deliberately embedded in this already-loaded script, so index.html DOES NOT need modification.
// These 4 records are backed by real PNG images attached by the user; see UPDATE_NOTES.txt.
(() => {
  const M = window.MABI;
  if (!M || !Array.isArray(M.DATA)) throw new Error('The 2026-11-04 update requires data/catalog.js');
  const krNotice='https://mabinogimobile.nexon.com/News/Notice/3571431';
  const twNotice='https://tw.nexon.com/mabinogimobile/home/news/notice/3569092';
  const twEnd='2026-12-02T05:59:00+08:00';
  const shared = {date:'2026-11-05',endDate:'2026-12-03',year:'2026',notice:krNotice,
    twDate:'2026-11-04',twEndDate:twEnd,twNotice,twNameStatus:'official_tw',nameStatus:'official_tw'};
  const rows=[
    {id:'lucky-41',type:'lucky',typeLabel:'幸運箱',number:41,zh:'束襟制服',ko:'여민 깃 제복',
      lines:['束襟制服','여민 깃 제복','咒術迴戰聯名時裝票券','台服2026/11/04'],
      image:'image/lucky-41.png',latest:true, ...shared},
    {id:'lucky-42',type:'lucky',typeLabel:'幸運箱',number:42,zh:'兩面宿儺服飾',ko:'양면 스쿠나 의상',
      lines:['兩面宿儺服飾','양면 스쿠나 의상','咒術迴戰聯名時裝票券','台服2026/11/04'],
      image:'image/lucky-42.png',latest:true, ...shared},
    {id:'pet-24',type:'pet',typeLabel:'寵物',number:24,zh:'玉犬・渾',ko:'옥견 혼',kind:'聯動',
      lines:['玉犬・渾','옥견 혼','咒術迴戰 式神：寵物幸運箱（史詩）'],
      image:'image/pet-24.png',imageNote:'使用官方台服寵物幸運箱合照（玉犬・渾與鵺）',
      variants:[{zh:'玉犬・渾',ko:'옥견 혼',rarity:'史詩'}], ...shared},
    {id:'pet-25',type:'pet',typeLabel:'寵物',number:25,zh:'鵺',ko:'누에',kind:'聯動',
      lines:['鵺','누에','咒術迴戰 式神：寵物幸運箱（史詩）'],
      image:'image/pet-25.png',imageNote:'使用官方台服寵物幸運箱合照（玉犬・渾與鵺）',
      variants:[{zh:'鵺',ko:'누에',rarity:'史詩'}], ...shared}
  ];
  const byId=new Map(M.DATA.map((row,i)=>[row.id,i]));
  for(const row of rows){
    const idx=byId.get(row.id);
    if(idx===undefined){byId.set(row.id,M.DATA.length);M.DATA.push(row);}
    else if(M.DATA[idx].ko===row.ko){Object.assign(M.DATA[idx],row);}
    else throw new Error('Record ID collision: '+row.id);
  }
  M.TW_CURRENT_IDS=new Set(M.TW_CURRENT_IDS||[]);
  M.TW_RELEASED_IDS=new Set(M.TW_RELEASED_IDS||[]);
  const now=Date.now(), begin=Date.parse('2026-11-04T00:00:00+08:00'), end=Date.parse(twEnd);
  for(const row of rows){
    M.TW_RELEASED_IDS.add(row.id);
    if(now>=begin&&now<end)M.TW_CURRENT_IDS.add(row.id);
    else M.TW_CURRENT_IDS.delete(row.id);
  }
  M.TW_STATUS_UPDATED='2026-11-04';
  M.TW_STATUS_SOURCES=[...(M.TW_STATUS_SOURCES||[]),
    {label:'台服 2026/11/04 咒術迴戰聯名幸運箱',url:twNotice},
    {label:'韓服 2026/11/05 咒術迴戰聯名商品（預告）',url:krNotice}];
  // These are NOT demonstrated to share base skills with the standard wolf/owl.
  M.PET_STATS=M.PET_STATS||{};
  M.PET_FAMILY_BY_KO=M.PET_FAMILY_BY_KO||{};
  M.PET_SKILL_FAMILIES=M.PET_SKILL_FAMILIES||{};
  for(const [ko,id] of [['옥견 혼','jjk_gyokuken_20261105'],['누에','jjk_nue_20261105']]){
    M.PET_STATS[ko]=[];
    M.PET_FAMILY_BY_KO[ko]=id;
    M.PET_SKILL_FAMILIES[id]={
      base:'資料缺失',epic:'資料缺失',legendEpic:'資料缺失',
      baseEffect:'固有技能效果未取得可核對的面板。詳細數值缺失',
      epicEffect:'固有技能及技能效果尚待遊戲內面板。詳細數值缺失',
      legendEpicEffect:'升階至傳說後的固有技能及效果未確認。詳細數值缺失',
      baseNote:'官方確認為史詩寵物，但未在公告提供固有技能或固定同行能力的數值。',
      epicNote:'官方確認對應一般系列的標籤機率／傳說寵物裝備套裝規則；不等於確認固有技能。',
      legendEpicNote:'官方確認升階失敗可得傳說寵物選擇箱碎片，SS效果未見可靠面板。'};
  }
})();

// 2026-10-01 Crion packages: already present in the repo but not loaded by its index.html.
// Included here after the 2026-10-14 rotation, before the 2026-11-04 additions.
(() => {
  const M = window.MABI = window.MABI || {};
  const data = Array.isArray(M.DATA) ? M.DATA : (M.DATA = []);
  const items = [
    {id:'package-8',type:'package',typeLabel:'全套套組',number:8,zh:'Crion Striker（暫譯）',ko:'크리온 스트라이커',lines:['Crion Striker（暫譯）','크리온 스트라이커'],date:'2026-10-01',endDate:'2026-10-29',year:'2026',notice:'https://mabinogimobile.nexon.com/News/Notice/3554491',image:'image/package-8.png'},
    {id:'package-9',type:'package',typeLabel:'全套套組',number:9,zh:'Crion Dog Tag（暫譯）',ko:'크리온 독 택',lines:['Crion Dog Tag（暫譯）','크리온 독 택'],date:'2026-10-01',endDate:'2026-10-29',year:'2026',notice:'https://mabinogimobile.nexon.com/News/Notice/3554491',image:'image/package-9.png'},
    {id:'package-10',type:'package',typeLabel:'全套套組',number:10,zh:'Crion Pop Patch（暫譯）',ko:'크리온 팝 패치',lines:['Crion Pop Patch（暫譯）','크리온 팝 패치'],date:'2026-10-01',endDate:'2026-10-29',year:'2026',notice:'https://mabinogimobile.nexon.com/News/Notice/3554491',image:'image/package-10.png'},
    {id:'package-11',type:'package',typeLabel:'全套套組',number:11,zh:'Crion Wire（暫譯）',ko:'크리온 와이어',lines:['Crion Wire（暫譯）','크리온 와이어'],date:'2026-10-01',endDate:'2026-10-29',year:'2026',notice:'https://mabinogimobile.nexon.com/News/Notice/3554491',image:'image/package-11.png'}
  ];
  const byId = new Map(data.map((item,index)=>[item.id,index]));
  for(const item of items){
    const index=byId.get(item.id);
    if(index===undefined){byId.set(item.id,data.length);data.push(item);}
    else if(data[index].ko===item.ko){data[index]={...data[index],...item};}
    else throw new Error('Crion package ID collision: '+item.id);
  }
})();

// Mark previously featured Korean pass and lucky boxes as no longer the newest.
(() => {
  const data = window.MABI?.DATA || [];
  for (const item of data) {
    if ((item.type==='pass' || item.type==='lucky') && item.server!=='TW') item.latest=false;
  }
})();

// KR/TW official notice research as of 2026-11-04 (Asia/Taipei).
// New photographs must be real, locally stored PNG before this script is deployed.
// Loaded after existing data/tw-update-20261014.js and before assets/js/app.js.
(() => {
  const M = window.MABI = window.MABI || {};
  const data = Array.isArray(M.DATA) ? M.DATA : (M.DATA = []);
  const krPass = 'https://mabinogimobile.nexon.com/News/Notice/3571556';
  const krGhost = 'https://mabinogimobile.nexon.com/News/Notice/3571557';
  const krJJK = 'https://mabinogimobile.nexon.com/News/Notice/3571431';
  const twJJK = 'https://tw.nexon.com/mabinogimobile/home/news/notice/3569092';
  const newEntries = [
    { id:'pass-14',type:'pass',typeLabel:'冒險家通行證',number:14,
      zh:'Cozy Day 冒險家通行證（暫譯）',ko:'코지데이 모험가 패스',
      nameStatus:'provisional',lines:['Cozy Day 冒險家通行證（暫譯）','코지데이 모험가 패스','Cozy Day 花漾耳環｜코지데이 블라썸 이어링'],
      date:'2026-10-29',endDate:'2026-12-16',year:'2026',notice:krPass,
      image:'image/pass-14.png',latest:true,priceMCash:1980,
      notes:['高級通行證70階；第5階獎勵 Cozy Day 花漾耳環；第25階可取得 Cozy Day 收藏包。'] },
    { id:'package-12',type:'package',typeLabel:'全套套組',number:12,
      zh:'Cozy Day 收藏包（暫譯）',ko:'코지데이 컬렉션 백',nameStatus:'provisional',
      lines:['Cozy Day 收藏包（暫譯）','코지데이 컬렉션 백','含貝雷帽、針織上衣、護腕、鞋子；性別款不同'],
      date:'2026-10-29',endDate:'2027-01-28',year:'2026',notice:krPass,
      image:'image/package-12.png',priceMCash:1000,
      notes:['先完成當期高級通行證25階後可購買；至2026/12/16 23:59優惠1000 M Cash，其後2000 M Cash。'] },
    { id:'pet-23',type:'pet',typeLabel:'寵物',number:23,
      zh:'幽靈黃金獵犬（菁英，暫譯）',ko:'유령 리트리버',nameStatus:'provisional',
      kind:'限定',lines:['幽靈黃金獵犬（菁英，暫譯）','유령 리트리버 (엘리트)'],
      date:'2026-10-29',endDate:'2026-11-12',year:'2026',notice:krGhost,
      image:'image/pet-23.png',variants:[{zh:'幽靈黃金獵犬',ko:'유령 리트리버',rarity:'菁英'}],
      notes:['期間限定禮包，售價4900 M Cash。固有技能、升階效果、固定同行能力尚缺可驗證面板，不推測。'] },
    { id:'lucky-41',type:'lucky',typeLabel:'幸運箱',number:41,
      zh:'束襟制服',ko:'여민 깃 제복',nameStatus:'official_tw',
      lines:['束襟制服','여민 깃 제복','套裝｜束襟制服','여민 깃 제복'],
      date:'2026-11-05',endDate:'2026-12-03',year:'2026',notice:krJJK,
      twDate:'2026-11-04',twEndDate:'2026-12-02T05:59:00+08:00',twNotice:twJJK,
      image:'image/lucky-41.png',latest:true,
      notes:['韓服預定11/05維護後；台服已11/04推出。使用咒術迴戰聯名時裝票券。'] },
    { id:'lucky-42',type:'lucky',typeLabel:'幸運箱',number:42,
      zh:'兩面宿儺服飾',ko:'양면 스쿠나 의상',nameStatus:'official_tw',
      lines:['兩面宿儺服飾','양면 스쿠나 의상','套裝｜兩面宿儺服飾','양면 스쿠나 의상'],
      date:'2026-11-05',endDate:'2026-12-03',year:'2026',notice:krJJK,
      twDate:'2026-11-04',twEndDate:'2026-12-02T05:59:00+08:00',twNotice:twJJK,
      image:'image/lucky-42.png',latest:true,
      notes:['韓服預定11/05維護後；台服已11/04推出。使用咒術迴戰聯名時裝票券。'] },
    { id:'pet-24',type:'pet',typeLabel:'寵物',number:24,
      zh:'玉犬・渾',ko:'옥견 혼',nameStatus:'official_tw',kind:'聯動',
      lines:['玉犬・渾','옥견 혼','史詩｜咒術迴戰 式神：寵物幸運箱'],
      date:'2026-11-05',endDate:'2026-12-03',year:'2026',notice:krJJK,
      twDate:'2026-11-04',twEndDate:'2026-12-02T05:59:00+08:00',twNotice:twJJK,
      image:'image/pet-24.png',variants:[{zh:'玉犬・渾',ko:'옥견 혼',rarity:'史詩'}],
      notes:['幼狼系列標籤與傳說裝備套裝規則相同，但不能據此推斷固有技能數值。'] },
    { id:'pet-25',type:'pet',typeLabel:'寵物',number:25,
      zh:'鵺',ko:'누에',nameStatus:'official_tw',kind:'聯動',
      lines:['鵺','누에','史詩｜咒術迴戰 式神：寵物幸運箱'],
      date:'2026-11-05',endDate:'2026-12-03',year:'2026',notice:krJJK,
      twDate:'2026-11-04',twEndDate:'2026-12-02T05:59:00+08:00',twNotice:twJJK,
      image:'image/pet-25.png',variants:[{zh:'鵺',ko:'누에',rarity:'史詩'}],
      notes:['貓頭鷹系列標籤與傳說裝備套裝規則相同，但不能據此推斷固有技能數值。'] }
  ];
  const byId = new Map(data.map((row,i)=>[row.id,i]));
  for (const row of newEntries) {
    const idx = byId.get(row.id);
    if (idx == null) { byId.set(row.id,data.length);data.push(row); }
    else if (data[idx].ko === row.ko) Object.assign(data[idx],row);
    else throw new Error('New update ID collides with an unrelated record: '+row.id);
  }
  // Keep previously released items; only these four outfits/pets are TW on-sale as of 11/04.
  M.TW_CURRENT_IDS = new Set(M.TW_CURRENT_IDS || []);
  M.TW_RELEASED_IDS = new Set(M.TW_RELEASED_IDS || []);
  const now = Date.now();
  for (const id of ['lucky-41','lucky-42','pet-24','pet-25']) {
    const row = data.find(x=>x.id===id);
    M.TW_RELEASED_IDS.add(id);
    if (now >= Date.parse('2026-11-04T00:00:00+08:00') && now < Date.parse(row.twEndDate)) M.TW_CURRENT_IDS.add(id);
    else M.TW_CURRENT_IDS.delete(id);
  }
  M.TW_STATUS_UPDATED='2026-11-04';
  M.TW_STATUS_SOURCES=[...(M.TW_STATUS_SOURCES||[]),
    {label:'2026/11/04台服咒術迴戰聯名幸運箱',url:twJJK},
    {label:'2026/11/05韓服咒術迴戰聯名商品公告',url:krJJK},
    {label:'2026/10/29韓服Cozy Day通行證與收藏包',url:krPass},
    {label:'2026/10/29韓服萬聖節幽靈獵犬禮包',url:krGhost}];
  M.PET_STATS=M.PET_STATS||{};
  M.PET_FAMILY_BY_KO=M.PET_FAMILY_BY_KO||{};
  M.PET_SKILL_FAMILIES=M.PET_SKILL_FAMILIES||{};
  for(const [ko,family] of [['유령 리트리버','ghost_retriever_20261029'],['옥견 혼','jjk_gyokuken_20261105'],['누에','jjk_nue_20261105']]){
    M.PET_FAMILY_BY_KO[ko]=family;
    M.PET_STATS[ko]=[];
    M.PET_SKILL_FAMILIES[family]={
      base:'資料缺失',epic:'資料缺失',legendEpic:'資料缺失',
      baseEffect:'詳細數值缺失',epicEffect:'詳細數值缺失',legendEpicEffect:'詳細數值缺失',
      baseNote:'官方僅確認販售／稀有度；固有技能未取得可核實的遊戲內面板。',
      epicNote:'無法確認升階技能及效果，不依同類寵物的技能推估。',
      legendEpicNote:'傳說升階技能及效果待核實。'
    };
  }
})();


// 2026-11-04 correction: two TW fashion boxes and ONE TW collaboration pet pool.
// Official TW in-game screenshots (user supplied) confirm the two epic S skills and companion attributes.
// Keep all Crion package-8 through package-11 and all Korean pass / special-pet entries untouched.
(() => {
  'use strict';
  const M=window.MABI;
  if (!M || !Array.isArray(M.DATA)) throw new Error('TW JJK correction requires existing MABI.DATA');
  const data=M.DATA;
  const notice='https://tw.nexon.com/mabinogimobile/home/news/notice/3569092';
  const krNotice='https://mabinogimobile.nexon.com/News/Notice/3571431';
  const twEnd='2026-12-02T05:59:00+08:00';
  const now=Date.now();
  const start=Date.parse('2026-11-04T00:00:00+08:00');
  const end=Date.parse(twEnd);
  const common={server:'TW',displayNumber:'台服聯名',date:'2026-11-04',
    twDate:'2026-11-04',twEndDate:twEnd,twNotice:notice,notice,
    twReleased:true,twNameStatus:'official_tw',nameStatus:'official_tw',year:'2026',
    krDate:'2026-11-05',krNotice,latest:true};
  const outfits=[
    {id:'lucky-41',zh:'束襟制服',ko:'여민 깃 제복',type:'lucky',typeLabel:'幸運箱',number:41,
      lines:['束襟制服','여민 깃 제복','咒術迴戰聯名｜時裝幸運箱','台服2026/11/04'],
      image:'image/lucky-41.png',notes:['台服正式名稱：束襟制服；台服11/04維護後販售至12/02 05:59。韓服11/05公告上架。'],...common},
    {id:'lucky-42',zh:'兩面宿儺服飾',ko:'양면 스쿠나 의상',type:'lucky',typeLabel:'幸運箱',number:42,
      lines:['兩面宿儺服飾','양면 스쿠나 의상','咒術迴戰聯名｜時裝幸運箱','台服2026/11/04'],
      image:'image/lucky-42.png',notes:['台服正式名稱：兩面宿儺服飾；台服11/04維護後販售至12/02 05:59。韓服11/05公告上架。'],...common}
  ];
  for(const record of outfits){
    let row=data.find(x=>x.id===record.id);
    if(row)Object.assign(row,record);
    else data.push(record);
  }

  // One lucky-box item contains two selectable epic pets; no duplicate cards.
  const pooled={
    ...common,
    id:'pet-24',type:'pet',typeLabel:'寵物幸運箱',number:24,
    zh:'咒術迴戰 式神：寵物幸運箱',ko:'옥견 혼 · 누에',
    kind:'聯動',latest:true,image:'image/pet-24.png',
    imageNote:'同一張台服官方幸運箱主圖包含玉犬・渾與鵺；兩者為同池史詩寵物。',
    lines:['咒術迴戰 式神：寵物幸運箱','玉犬・渾｜옥견 혼','鵺｜누에',
           '同一個寵物幸運箱，兩款皆為史詩寵物'],
    variants:[
      {zh:'玉犬・渾',ko:'옥견 혼',rarity:'史詩'},
      {zh:'鵺',ko:'누에',rarity:'史詩'}
    ],
    notes:['請在此卡片點選玉犬・渾或鵺，查看各自固有技能與固定同行能力。',
           '台服2026/11/04維護後推出，2026/12/02 05:59結束販售。']
  };
  const target=data.find(x=>x.id==='pet-24');
  if(target)Object.assign(target,pooled);
  else data.push(pooled);
  // Ensure one pet box even if earlier scripts populated pet-25 separately.
  for(let i=data.length-1;i>=0;i--){
    if(data[i].id==='pet-25')data.splice(i,1);
  }

  M.TW_RELEASED_IDS=new Set(M.TW_RELEASED_IDS||[]);
  M.TW_CURRENT_IDS=new Set(M.TW_CURRENT_IDS||[]);
  for(const id of ['lucky-41','lucky-42','pet-24']){
    M.TW_RELEASED_IDS.add(id);
    if(now>=start && now<end)M.TW_CURRENT_IDS.add(id);
    else M.TW_CURRENT_IDS.delete(id);
  }
  M.TW_RELEASED_IDS.delete('pet-25');
  M.TW_CURRENT_IDS.delete('pet-25');
  M.TW_STATUS_UPDATED='2026-11-04';

  M.PET_STATS=M.PET_STATS||{};
  M.PET_FAMILY_BY_KO=M.PET_FAMILY_BY_KO||{};
  M.PET_SKILL_FAMILIES=M.PET_SKILL_FAMILIES||{};
  const standardAttributes=['力量 +5','技巧 +5','智力 +5','意志 +5','幸運 +5'];
  M.PET_STATS['옥견 혼']=[...standardAttributes,'攻擊力 +8','技能威力 +14','魅力 +3000'];
  M.PET_STATS['누에']=[...standardAttributes,'追擊 +14','攻擊力 +8','魅力 +3000'];
  const dogFamily='jjk_gyokuken_20261105';
  M.PET_FAMILY_BY_KO['옥견 혼']=dogFamily;
  M.PET_SKILL_FAMILIES[dogFamily]={
    base:'資料缺失',epic:'破防嚎叫 S',legendEpic:'資料缺失',
    baseEffect:'基本版本未提供可確認面板；詳細數值缺失',
    epicEffect:'[主動] 寵物主人鎖定的敵人處於破防狀態時可施放。施放時，於7秒期間，寵物主人的無防備傷害增加3%。（冷卻時間：8秒）',
    legendEpicEffect:'升階至傳說後的技能 SS 效果尚無可靠面板；詳細數值缺失',
    epicNote:'台服2026/11/04玩家提供的「玉犬・渾」原生史詩等級1面板。',
    legendEpicNote:'沒有使用其他幼狼寵物的數值推估。'
  };
  const nueFamily='jjk_nue_20261105';
  M.PET_FAMILY_BY_KO['누에']=nueFamily;
  M.PET_SKILL_FAMILIES[nueFamily]={
    base:'資料缺失',epic:'疾速的振翅 S',legendEpic:'資料缺失',
    baseEffect:'基本版本未提供可確認面板；詳細數值缺失',
    epicEffect:'[主動] 施放時，於5秒期間，將寵物主人的技能使用速度、攻擊速度、施法及蓄力速度增加12%。（冷卻時間：30秒）',
    legendEpicEffect:'升階至傳說後的技能 SS 效果尚無可靠面板；詳細數值缺失',
    epicNote:'台服2026/11/04玩家提供的「鵺」原生史詩等級1面板。',
    legendEpicNote:'不由既有貓頭鷹系列推估傳說版本數值。'
  };
  // Preserve supplementary official TW references for the two real pet panels.
  M.PET_DETAIL_SOURCES=M.PET_DETAIL_SOURCES||[];
  for(const record of [
    {title:'台服2026/11/04 玉犬・渾 S 技能及固定同行能力',kind:'使用者提供台服遊戲面板'},
    {title:'台服2026/11/04 鵺 S 技能及固定同行能力',kind:'使用者提供台服遊戲面板'}
  ]){
    if(!M.PET_DETAIL_SOURCES.some(x=>x.title===record.title))M.PET_DETAIL_SOURCES.push(record);
  }
  // Do not remove Crion packages; earlier data source still provides all four.
  for(const id of ['package-8','package-9','package-10','package-11']){
    if(!data.some(x=>x.id===id))throw new Error('Expected Crion package absent: '+id);
  }
})();
