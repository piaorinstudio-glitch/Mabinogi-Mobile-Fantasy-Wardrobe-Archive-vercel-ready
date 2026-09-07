# 維護指南

這版網站刻意維持「純靜態」：沒有 Node.js、沒有資料庫、沒有建置步驟。GitHub push 後 Vercel 可直接部署。

## 平常最常改的檔案

- `data/catalog.js`：通行證、幸運箱、套組、傳說、寵物、深淵、團隊副本卡片資料。
- `data/pets.js`：寵物固定同行能力、技能家族、無 S / S / SS 效果。
- `data/site-config.js`：分類文字、Tips、台服狀態、外部小工具。
- `assets/css/main.css`：首頁與卡片樣式。
- `assets/js/app.js`：顯示、搜尋、排序、彈窗等程式邏輯。通常不需要為新增資料修改它。
- `data/ads-config.js`：Google AdSense 開關。

## 新增外觀

1. 把 WebP 圖片放進 `image/`（傳說標準化圖則放 `assets/normalized/legend/`）。若原圖是 PNG/JPG，可先執行 `python scripts/convert_to_webp.py 原圖.png image/新檔名.webp`。
2. 在 `data/catalog.js` 複製同類型的一筆資料，修改 `id`、中文名、韓文名、日期、公告網址、圖片路徑。
3. `id` 不可重複。
4. 執行：`python scripts/validate_site.py`。

## 台服狀態

`data/site-config.js` 有兩組 ID：

- `TW_CURRENT_IDS`：金色「台服當期」。
- `TW_RELEASED_IDS`：灰色「台服已推出」。

深淵與團隊副本的卡片程式固定不顯示這兩個標籤。

當一個項目結束販售時，只要從 `TW_CURRENT_IDS` 移除；如果台服確實推出過，保留在 `TW_RELEASED_IDS`。

## 新增小工具

在 `data/site-config.js` 的 `TOOL_LINKS` 增加一個物件即可。不要改 `assets/js/app.js`。

## 寵物技能

在 `data/pets.js` 的 `PET_SKILL_FAMILIES` 修改。找不到係數時保留已知效果，並明確標示尚未確認；不要自行推測。

## 廣告

預設 `data/ads-config.js` 的 `enabled:false`，所以網站不會載入 Google 廣告網路程式。AdSense 核准、準備正式開啟後：

1. 確認 `client` 是正確的 `ca-pub-...`。
2. 將 `enabled` 改為 `true`。
3. `ads.txt` 必須留在網站根目錄。
4. `privacy.html` 已預留 AdSense / Cookie 說明；若廣告或分析服務改變，要同步更新。

目前使用的是 Auto Ads 型態的載入方式；未來若要手動廣告版位，再於版面加入獨立 ad slot，不需要把廣告碼散落在每個 HTML。

## 上線前檢查

```bash
python scripts/validate_site.py
python -m http.server 8000
```

再用瀏覽器打開 `http://localhost:8000/`，檢查桌機與手機版。
