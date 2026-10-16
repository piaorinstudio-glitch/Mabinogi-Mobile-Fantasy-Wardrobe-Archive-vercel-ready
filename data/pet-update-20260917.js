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
    epic: '흉포한 사랑 S',
    epicEffect: '[主動] 施放時，於 23 秒期間，寵物主人的技能威力增加 2、攻擊力增加 6%。（冷卻時間：60 秒）',
    epicNote: '來源：https://www.youtube.com/watch?v=OwBCx0a_X8E&t=161s；原生史詩婚禮貂遊戲面板。技能威力+2忠實保留原文；尚無證據確認是否隨等級改變，不推測成長規則。',
    legendEpicNote: '尚未取得貂SS的完整遊戲面板，不由S版本推算。'
  });

  Object.assign(M.PET_SKILL_FAMILIES.otter, {
    epic: '치유의 무지개 S',
    legendEpic: '치유의 무지개 SS',
    epicEffect: '[主動] 施放時，恢復寵物主人最大生命值的 4%。（冷卻時間：14 秒）',
    legendEpicEffect: '[主動] 施放時，恢復寵物主人最大生命值的 5%。\n詳細數值缺失',
    epicNote: '來源：https://www.youtube.com/watch?v=OwBCx0a_X8E&t=131s；原生史詩水手水獺面板僅有固有技能，未顯示神速等學習技能。',
    legendEpicNote: '來源：https://gall.dcinside.com/mgallery/board/view/?id=enban&no=1439057；傳說水手水獺面板確認恢復最大生命值5%。同圖有神速減冷卻被動，因此不將顯示的14秒視為已排除修正後的SS預設冷卻，也不反推。'
  });
})();
