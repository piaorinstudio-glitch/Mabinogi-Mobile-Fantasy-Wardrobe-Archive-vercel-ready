// Taiwan MapleStory collaboration additions — final 2026-09-30 update.
(() => {
  window.MABI = window.MABI || {};
  const M = window.MABI;
  const data = Array.isArray(M.DATA) ? M.DATA : (M.DATA = []);

  const updates = [
    {
      id:'tw-lucky-maple-1', type:'lucky', typeLabel:'幸運箱',
      number:1, displayNumber:'台版 #1', server:'TW',
      pairOrder:1,
      zh:'楓葉朋友們：時裝幸運箱', ko:'',
      lines:['台版 #1','楓葉朋友們：時裝幸運箱','《瑪奇 Mobile》×《新楓之谷》'],
      date:'2026-09-30', endDate:'2026-10-21', year:'2026',
      notice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3550868',
      image:'image/tw-lucky-maple-1.png',
      twDate:'2026-09-30', twEndDate:'2026-10-21',
      twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3550868',
      latest:true
    },
    {
      id:'tw-pet-maple-2', type:'pet', typeLabel:'寵物',
      number:1, displayNumber:'台版 #1', server:'TW',
      pairOrder:1,
      zh:'楓葉朋友們：寵物幸運箱', ko:'',
      lines:['台版 #1','楓葉朋友們：寵物幸運箱','《瑪奇 Mobile》×《新楓之谷》'],
      kind:'聯動',
      date:'2026-09-30', endDate:'2026-10-21', year:'2026',
      notice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3550868',
      image:'image/tw-pet-maple-2.png',
      variants:[
        {zh:'快樂粉豆貓', ko:'tw-maple-happy-pinkbean-cat', rarity:'史詩'},
        {zh:'企鵝王與小熊', ko:'tw-maple-pepe-bear', rarity:'史詩'}
      ],
      twDate:'2026-09-30', twEndDate:'2026-10-21',
      twNotice:'https://tw.nexon.com/mabinogimobile/home/news/notice/3550868'
    }
  ];

  const byId=new Map(data.map((item,index)=>[item&&item.id,index]));
  for(const item of updates){
    const i=byId.get(item.id);
    if(i===undefined){data.push(item);byId.set(item.id,data.length-1);}
    else data[i]={...data[i],...item};
  }

  M.PET_STATS=M.PET_STATS||{};
  M.PET_FAMILY_BY_KO=M.PET_FAMILY_BY_KO||{};
  M.PET_SKILL_FAMILIES=M.PET_SKILL_FAMILIES||{};

  M.PET_STATS['tw-maple-happy-pinkbean-cat']=['破防','攻擊力'];
  M.PET_STATS['tw-maple-pepe-bear']=['連段強化','暴擊'];
  M.PET_FAMILY_BY_KO['tw-maple-happy-pinkbean-cat']='twMaplePinkbeanCat';
  M.PET_FAMILY_BY_KO['tw-maple-pepe-bear']='twMaplePepeBear';

  M.PET_SKILL_FAMILIES.twMaplePinkbeanCat={
    epic:'不許動 S',
    epicEffect:'[主動] 施放時，於 4 秒期間，使寵物主人鎖定的 1 名敵人的移動速度減少 20%。（冷卻時間：10 秒）',
    legendEpic:'資料缺失',
    legendEpicEffect:'資料缺失',
    epicNote:'台版實機確認：力量 +5、技巧 +5、智力 +5、意志 +5、幸運 +5、破防 +14、攻擊力 +8、魅力 +3000。'
  };
  M.PET_SKILL_FAMILIES.twMaplePepeBear={
    epic:'鬥志爆發 S',
    epicEffect:'[主動] 寵物主人被破防時可施放。施放時，於 6 秒期間，同行寵物的攻擊力增加 20%。（冷卻時間：8 秒）',
    legendEpic:'資料缺失',
    legendEpicEffect:'資料缺失',
    epicNote:'台版實機確認：力量 +5、技巧 +5、智力 +5、意志 +5、幸運 +5、連段強化 +14、暴擊 +14、魅力 +3000。'
  };

  const current=new Set(M.TW_CURRENT_IDS||[]);
  current.add('tw-lucky-maple-1'); current.add('tw-pet-maple-2');
  M.TW_CURRENT_IDS=current;
  const released=new Set(M.TW_RELEASED_IDS||[]);
  released.add('tw-lucky-maple-1'); released.add('tw-pet-maple-2');
  M.TW_RELEASED_IDS=released;
  M.TW_STATUS_UPDATED='2026-10-04';
})();
