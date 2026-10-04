// 2026-10-01 KR wardrobe update.
(() => {
  window.MABI = window.MABI || {};
  const data = Array.isArray(window.MABI.DATA) ? window.MABI.DATA : (window.MABI.DATA = []);
  const updates = [
    {id:'package-8',type:'package',typeLabel:'全套套組',number:8,zh:'Crion Striker（暫譯）',ko:'크리온 스트라이커',lines:['Crion Striker（暫譯）','크리온 스트라이커'],date:'2026-10-01',endDate:'2026-10-29',year:'2026',notice:'https://mabinogimobile.nexon.com/News/Notice/3554491',image:'image/package-8.png'},
    {id:'package-9',type:'package',typeLabel:'全套套組',number:9,zh:'Crion Dog Tag（暫譯）',ko:'크리온 독 택',lines:['Crion Dog Tag（暫譯）','크리온 독 택'],date:'2026-10-01',endDate:'2026-10-29',year:'2026',notice:'https://mabinogimobile.nexon.com/News/Notice/3554491',image:'image/package-9.png'},
    {id:'package-10',type:'package',typeLabel:'全套套組',number:10,zh:'Crion Pop Patch（暫譯）',ko:'크리온 팝 패치',lines:['Crion Pop Patch（暫譯）','크리온 팝 패치'],date:'2026-10-01',endDate:'2026-10-29',year:'2026',notice:'https://mabinogimobile.nexon.com/News/Notice/3554491',image:'image/package-10.png'},
    {id:'package-11',type:'package',typeLabel:'全套套組',number:11,zh:'Crion Wire（暫譯）',ko:'크리온 와이어',lines:['Crion Wire（暫譯）','크리온 와이어'],date:'2026-10-01',endDate:'2026-10-29',year:'2026',notice:'https://mabinogimobile.nexon.com/News/Notice/3554491',image:'image/package-11.png'}
  ];
  const byId = new Map(data.map((item,index)=>[item.id,index]));
  for (const item of updates) {
    const i=byId.get(item.id);
    if(i===undefined){data.push(item);byId.set(item.id,data.length-1);}
    else data[i]={...data[i],...item};
  }
})();
