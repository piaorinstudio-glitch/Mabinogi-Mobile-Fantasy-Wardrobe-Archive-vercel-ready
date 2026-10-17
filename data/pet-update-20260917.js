// 2026-09-17 KR English Sheepdog pet detail update.
// Loaded after data/pets.js and before assets/js/app.js.
(() => {
  window.MABI = window.MABI || {};
  const M = window.MABI;
  M.PET_STATS = M.PET_STATS || {};
  M.PET_FAMILY_BY_KO = M.PET_FAMILY_BY_KO || {};
  M.PET_SKILL_FAMILIES = M.PET_SKILL_FAMILIES || {};

  // Fixed companion combat stats. Chinese terms follow this site's existing TW terminology.
  Object.assign(M.PET_STATS, {
    '페스티벌 잉글리시 쉽독': ['暴擊', '快速技能'],
    '스카프 잉글리시 쉽독': ['技能威力', '追擊'],
    '리본 잉글리시 쉽독': ['破防', '攻擊力'],
    '회색 잉글리시 쉽독': ['快速技能', '絕招']
  });

  Object.assign(M.PET_FAMILY_BY_KO, {
    '잉글리시 쉽독': 'sheepdog',
    '페스티벌 잉글리시 쉽독': 'sheepdog',
    '스카프 잉글리시 쉽독': 'sheepdog',
    '리본 잉글리시 쉽독': 'sheepdog',
    '회색 잉글리시 쉽독': 'sheepdog'
  });

  M.PET_SKILL_FAMILIES.sheepdog = {
    base: '재빠른 경계',
    epic: '재빠른 경계 S',
    legendEpic: '재빠른 경계 SS',
    baseEffect: '[主動] 施放時，於 18 秒期間，寵物主人造成的傷害增加 5.5%，並提高快速技能。（冷卻時間：60 秒）\n詳細數值缺失',
    epicEffect: '[主動] 施放時，於 23 秒期間，寵物主人造成的傷害增加 6%，並提高快速技能。（冷卻時間：60 秒）\n詳細數值缺失',
    legendEpicEffect: '[主動] 施放時，提高寵物主人的造成傷害與快速技能。\n詳細數值缺失',
    baseNote: '韓服資料確認：菁英／稀有／高級個體持有「재빠른 경계」，但低於史詩時無法使用固有技能；升至史詩後可使用。',
    epicNote: '原始面板可確認 S 版為23秒、造成傷害增加6%、冷卻60秒；快速技能在不同等級面板有不同值，不將舊Lv1的+2寫成通用常數。',
    legendEpicNote: '目前未找到可可靠核對的「재빠른 경계 SS」完整數值，因此不猜測。'
  };
})();

// 2026-10-15 new families; verified in-game detail supplement on 2026-10-16.
(() => {
  const M=window.MABI;
  const families={marten:['담비','웨딩 담비','비행사 담비','신사 담비','노랑 담비'],
    otter:['수달','세일러 수달','앞치마 수달','스카프 수달','갈색 수달']};
  for(const [key,names] of Object.entries(families)){
    for(const ko of names){M.PET_FAMILY_BY_KO[ko]=key;M.PET_STATS[ko]=[];}
    M.PET_SKILL_FAMILIES[key]={base:'資料缺失',epic:'資料缺失',legendEpic:'資料缺失',
      baseEffect:'資料缺失',epicEffect:'資料缺失',legendEpicEffect:'資料缺失',
      baseNote:'韓服官方公告已確認外觀與稀有度；公告未提供固有技能與固定同行能力，待補遊戲內資料。',
      epicNote:'韓服官方公告已確認外觀與稀有度；公告未提供固有技能與固定同行能力，待補遊戲內資料。'};
  }

  // Only these epic variants have directly verified companion-stat panels.
  // Do not infer the other appearances' stats from a shared family name.
  Object.assign(M.PET_STATS, {
    '웨딩 담비': ['暴擊', '技能威力'],
    '세일러 수달': ['暴擊', '追擊']
  });

  Object.assign(M.PET_SKILL_FAMILIES.marten, {
    baseEffect: '[主動] 施放時，提高寵物主人的技能威力與攻擊力。\n詳細數值缺失',
    epic: '흉포한 사랑 S',
    epicEffect: '[主動] 施放時，於 23 秒期間，寵物主人的技能威力增加 2、攻擊力增加 6%。（冷卻時間：60 秒）',
    legendEpicEffect: '[主動] 施放時，提高寵物主人的技能威力與攻擊力。\n詳細數值缺失',
    baseNote: '只列同族技能共同作用；基本版本的名稱、係數、持續時間與冷卻尚缺完整面板，不沿用S數字。',
    epicNote: '原生史詩婚禮貂遊戲面板。技能威力+2忠實保留原文；尚無證據確認是否隨等級改變，不推測成長規則。',
    legendEpicNote: '只列同族技能共同作用；SS版本的名稱與完整數值尚缺面板，不由S版本推算。'
  });

  Object.assign(M.PET_SKILL_FAMILIES.otter, {
    baseEffect: '[主動] 施放時，恢復寵物主人的生命值。\n詳細數值缺失',
    epic: '치유의 무지개 S',
    legendEpic: '치유의 무지개 SS',
    epicEffect: '[主動] 施放時，恢復寵物主人最大生命值的 4%。（冷卻時間：14 秒）',
    legendEpicEffect: '[主動] 施放時，恢復寵物主人最大生命值的 5%。\n詳細數值缺失',
    baseNote: '只列同族技能共同作用；基本版本的名稱、恢復量與冷卻尚缺完整面板，不沿用S數字。',
    epicNote: '原生史詩水手水獺面板僅有固有技能，未顯示神速等學習技能。',
    legendEpicNote: '傳說水手水獺面板確認恢復最大生命值5%。同圖有神速減冷卻被動，因此不將顯示的14秒視為已排除修正後的SS預設冷卻，也不反推。'
  });

  // Citations belong in the site's existing Sources dialog, never in pet footers.
  M.PET_DETAIL_SOURCES = [
    {title:'寵物培養與固有技能升階規則',url:'https://mabinogimobile.nexon.com/Info/Guide/2751130',kind:'韓服官方指南'},
    {title:'浣熊固有技能與等級上限調整',url:'https://mabinogimobile.nexon.com/News/Update/3511370',kind:'韓服官方更新'},
    {title:'貓頭鷹施法與蓄力速度效果調整',url:'https://mabinogimobile.nexon.com/News/Update/2999050',kind:'韓服官方更新'},
    {title:'寵物技能面板整理：挪威森林貓、小豬、西施犬、博美犬',url:'https://peak.nexon.com/post/2736',kind:'玩家遊戲面板'},
    {title:'牧羊犬S與西施犬各階級技能面板',url:'https://gonryu.tistory.com/54',kind:'玩家遊戲面板'},
    {title:'小狐狸S／SS技能面板',url:'https://dszw1qtcnsa5e.cloudfront.net/community/20250331/e0f3a922-907b-4c90-89c0-d31179befa3b/20250401032441856.png',kind:'遊戲內截圖'},
    {title:'台服寵物資料與用語交叉核對',url:'https://mabi.hongkongfootprint.com/2026/09/mabi-mobile-pet.html',kind:'玩家整理'},
    {title:'台服寵物技能討論',url:'https://forum.gamer.com.tw/C.php?bsn=32564&snA=2621',kind:'玩家社群'},
    {title:'婚禮貂S技能與固定同行能力｜影片02:41',url:'https://www.youtube.com/watch?v=OwBCx0a_X8E&t=161s',kind:'玩家遊戲面板'},
    {title:'水手水獺S技能與固定同行能力｜影片02:11',url:'https://www.youtube.com/watch?v=OwBCx0a_X8E&t=131s',kind:'玩家遊戲面板'},
    {title:'水手水獺SS技能與固定同行能力',url:'https://gall.dcinside.com/mgallery/board/view/?id=enban&no=1439057',kind:'玩家遊戲面板'},
    {title:'快樂粉豆貓、企鵝王與小熊S技能及同行能力',kind:'使用者提供台服截圖'}
  ];
})();
