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
