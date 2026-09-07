# GitHub → Vercel 部署

## 一次性設定

1. 把本資料夾內容 push 到 GitHub repository 的 `main` 分支。
2. Vercel Dashboard → Add New → Project → Import 該 GitHub repository。
3. Framework Preset 選 `Other` / 靜態網站；Root Directory 使用 repository 根目錄。
4. 不需要 Build Command、Install Command、Output Directory。
5. Deploy。
6. 往後每次 push 到 `main`，Vercel 會自動建立新部署；分支/PR 可使用 Preview Deployment。

## 自訂網域

正式網域若改由 Vercel 接管，請在 Vercel Project → Settings → Domains 加入 `piaorinstudio.com`，再依 Vercel 畫面提供的 DNS 記錄修改 DNS。不要同時把同一個根網域指向 GitHub Pages 與 Vercel。

`CNAME` 是 GitHub Pages 用檔案；留在 repository 不影響 Vercel，若未來完全不再用 GitHub Pages也可以刪除。

## 為什麼不加前端框架

這個網站主要是資料圖鑑，純 HTML/CSS/JS 已足夠。保持無建置步驟，能讓資料修改後直接 push、直接部署，也降低日後維護成本。
