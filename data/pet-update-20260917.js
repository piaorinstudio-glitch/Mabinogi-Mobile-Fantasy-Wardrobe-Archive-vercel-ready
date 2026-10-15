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
    baseEffect: '[主動] 施放時，18 秒內寵物主人的造成傷害增加 5.5%，快速技能 +2。（冷卻時間：60 秒）',
    epicEffect: '[主動] 施放時，23 秒內寵物主人的造成傷害增加 6%，快速技能 +2。（冷卻時間：60 秒）',
    legendEpicEffect: '[主動] 施放時，提高寵物主人的造成傷害與快速技能。\n詳細數值缺失',
    baseNote: '韓服資料確認：菁英／稀有／高級個體持有「재빠른 경계」，但低於史詩時無法使用固有技能；升至史詩後可使用。',
    epicNote: '韓服資料確認：史詩「페스티벌 잉글리시 쉽독」為「재빠른 경계 S」，持續 23 秒、造成傷害 +6%、快速技能 +2、冷卻 60 秒。',
    legendEpicNote: '目前未找到可可靠核對的「재빠른 경계 SS」完整數值，因此不猜測。'
  };
})();

// 2026-10-15 new families. The sale notice does NOT document innate skill/stat values.
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
})();
