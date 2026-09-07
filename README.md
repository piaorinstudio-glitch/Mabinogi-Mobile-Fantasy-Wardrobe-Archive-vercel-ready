# 瑪奇 Mobile｜韓服外觀未來視

玩家整理的純靜態外觀資料站。支援 GitHub 保存版本、Vercel 自動部署，不需要 Node.js 或前端框架。

## 專案結構

```text
/
├─ index.html                 # 主頁骨架（不要再塞大量資料）
├─ about.html / privacy.html / contact.html
├─ data/
│  ├─ catalog.js              # 所有外觀卡片資料
│  ├─ pets.js                 # 寵物技能與同行能力
│  ├─ site-config.js          # Tips、台服狀態、小工具
│  └─ ads-config.js           # AdSense 開關
├─ assets/
│  ├─ css/main.css            # 主站樣式
│  ├─ css/page.css            # 資訊頁共用樣式
│  ├─ js/app.js               # UI 邏輯
│  ├─ js/ads.js               # AdSense 集中載入器
│  └─ normalized/             # 標準化外觀圖
├─ image/                     # 一般卡片圖片
├─ scripts/                   # 維護/驗證工具
├─ docs/                      # 維護與部署說明
├─ ads.txt / robots.txt / sitemap.xml
└─ vercel.json
```

## 本機預覽

```bash
python -m http.server 8000
```

打開 `http://localhost:8000/`。

## 更新資料

大多數更新只需要改 `data/`，不用碰 HTML 或 UI 程式。詳細步驟見 `docs/MAINTENANCE.md`。

更新後先跑：

```bash
python scripts/validate_site.py
```

## Vercel

直接把 GitHub repository 匯入 Vercel 即可，這是無建置步驟的靜態網站。詳見 `docs/DEPLOY_VERCEL.md`。

## Google AdSense

網站已保留 `ads.txt`、AdSense account meta、隱私權說明與集中式廣告載入器，但 `data/ads-config.js` 預設 `enabled:false`，測試期間不會載入 Google 廣告 script。核准後只需在一處開啟。

中文名稱為參考翻譯；正式內容以官方公告為準。
