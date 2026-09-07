// Labels, tips, Taiwan release state, and shared external tools.
// TW_CURRENT_IDS = gold "台服當期"; TW_RELEASED_IDS = gray "台服已推出".
// Abyss/Raid cards intentionally do not render these status chips.
window.MABI=window.MABI||{};
window.MABI.LABELS={
  pass:['通行證','PASS'],lucky:['幸運箱','LUCKY BOX'],package:['全套套組','SET ITEM'],
  legend:['傳說時裝','LEGEND'],pet:['寵物','PET'],abyss:['深淵副本時裝','ABYSS'],raid:['團隊副本時裝','RAID'],tools:['小工具','TOOLS']
};
window.MABI.TIPS_CONTENT={
  pass:[
    ['怎麼看這頁','冒險家通行證外觀依韓服推出日期整理；排序切換只改顯示順序，不代表台服推出期數。'],
    ['台服參考方式','台服上架時間可能與韓服不同，建議把這頁當作「韓服未來可能輪到哪些外觀」的順序參考。']
  ],
  lucky:[
    ['韓服 # 是什麼','「韓服 #」只代表韓服實際推出順序，不是台服期數；下方日期是韓服推出日期。'],
    ['為什麼不能直接對照台服期數','台服可能一次上架多個韓服幸運箱內容，或用不同批次組合，因此本站不用「第 N 期」稱呼。']
  ],
  package:[
    ['這一頁收什麼','收錄韓服以整套形式販售的外觀套組，與幸運箱、通行證分開整理。'],
    ['日期怎麼看','以韓服首次推出日期排序；台服實際販售時間、組合與售價可能不同。']
  ],
  legend:[
    ['取得方式','使用 <span class="tip-em">2 件史詩（粉紅色）時裝</span>＋商城販售的 <span class="tip-em">傳說級縫紉剪刀</span> 合成。當期只能合出當期傳說時裝。'],
    ['輪替與代數','每一代都有自己的取得期間；本站第 1～5 代對應韓服前 5 代，第 6 代為「幻蜃卡爾德蕾雅｜미라주 칼드레아」。第 1～6 代的每件裝備效果與 3 Set 效果相同；第 6 代起只有 4 Set 額外增加「最終防禦力 +3%」。'],
    ['套裝效果','<div class="tip-table-wrap"><table class="tip-table"><thead><tr><th>世代</th><th>每件裝備</th><th>3 Set</th><th>4 Set</th></tr></thead><tbody><tr><td class="nowrap">第 1～5 代</td><td rowspan="2">該部位防禦力 +10%<br>耐久度消耗 -40%<br>魅力 +4000</td><td rowspan="2">所有能力值 +220</td><td>攻擊力 +450<br>防禦力 +450</td></tr><tr><td class="nowrap">第 6 代起</td><td>攻擊力 +450<br>防禦力 +450<br>最終防禦力 +3%</td></tr></tbody></table></div>'],
    ['傳說級長袍','<div class="tip-table-wrap"><table class="tip-table"><tbody><tr><th>台版取得</th><td>全部配戴「宇宙星之子」套裝時，將解鎖可獲得傳說稀有度「宇宙星之子」長袍的專用任務。</td></tr><tr><th>裝備效果</th><td>魅力 +6000</td></tr><tr><th>取得後 60 天</th><td>已裝備防具防禦力 +1%<br>已裝備時裝魅力 +10%</td></tr></tbody></table></div>'],
    ['一般版／長袍版','「長袍版」指角色另外裝備傳說級長袍後的外觀預覽；台版需全部配戴「宇宙星之子」套裝，解鎖可獲得傳說級長袍的專用任務。']
  ],
  pet:[
    ['常駐池','<div class="tip-table-wrap"><table class="tip-table"><thead><tr><th>票券</th><th>對應池</th></tr></thead><tbody><tr><td class="nowrap">寵物票券</td><td>一般池：菁英／稀有／高級，不含史詩</td></tr><tr><td class="nowrap">頂級寵物票券</td><td>頂級池：史詩＋菁英以下，並有累積開箱獎勵</td></tr></tbody></table></div><div style="margin-top:7px">新常駐加入時，菁英以下會累積進一般池；頂級池則同步加入新的史詩與下位寵物。</div>'],
    ['限定寵物','多為活動期間直接販售的指定寵物，通常不使用「寵物票券／頂級寵物票券」，也不會加入常駐池。'],
    ['聯動寵物','使用聯動專屬寵物票券與獨立池，常駐的兩種票券不能代用。聯動史詩只在聯動池出現，菁英以下通常沿用當期常駐池。']
  ],
  abyss:[
    ['怎麼取得','這裡收錄由特定深淵副本取得的時裝；卡片右下角直接標示掉落副本名稱。'],
    ['名稱規則','台服已推出的副本使用台服正式名稱＋韓服名稱；尚未推出的則使用中文暫譯＋韓服原名。']
  ],
  raid:[
    ['怎麼取得','這裡收錄由特定團隊副本取得的時裝；卡片右下角直接標示掉落團隊副本。'],
    ['名稱規則','台服已推出的副本使用台服正式名稱＋韓服名稱；尚未推出的則使用中文暫譯＋韓服原名。']
  ],
  tools:[
    ['用途','集中分享實用的瑪奇 Mobile 查詢頁面與玩家工具；之後可持續新增更多項目。'],
    ['外部連結','小工具可能會開啟第三方網站，內容與可用性以該網站實際狀態為準。']
  ]
};
window.MABI.TW_CURRENT_IDS=new Set(['pass-2','lucky-2','lucky-4','lucky-5','package-1','legend-1','pet-1']);
window.MABI.TW_STATUS_UPDATED='2026-09-07';
window.MABI.TW_STATUS_SOURCES=[
  {label:'台服 2026/08/19 更新公告',url:'https://tw.nexon.com/mabinogimobile/home/news/update/3527491'},
  {label:'宇宙星之子相關公告',url:'https://tw.nexon.com/mabinogimobile/home/news/notice/3504848'}
];
window.MABI.TW_RELEASED_IDS=new Set(['pass-1','pass-2','lucky-1','lucky-2','lucky-4','lucky-5','lucky-8','package-1','legend-1','pet-0','pet-1']);
window.MABI.TOOL_LINKS=[
  {
    id:'mobilay-dress-room',
    title:'瑪奇 Mobile 更衣室',
    source:'MOBILAY｜韓國作者製作',
    icon:'✦',
    description:'Mobilay 的瑪奇 Mobile 更衣室工具，由韓國作者製作，目前仍為測試版本；可用來瀏覽與搭配時裝，分享給需要找穿搭與外觀資料的玩家。',
    url:'https://mobilay.kr/tw/dress-room'
  }
];
