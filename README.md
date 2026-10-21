# Hungry Map · 附近有咩食

用地圖搵附近**食環署持牌食肆**。資料真實、載入快、唔使 API key。

## 資料來源

- **食物環境衞生署** 持牌食肆名單（DATA.GOV.HK 開放數據）
- 約 1.7 萬間，含座標
- 使用時請標註：`資料來源：食物環境衞生署 / DATA.GOV.HK`

## 功能

- 📍 自動定位 + 距離／步行時間
- ❤️ 收藏 · 📝 備註 · 🎲 隨機 · 📤 分享
- 🧭 Google Maps 導航
- 🌙 深色 · 中英 · 衛星圖 · 自訂範圍
- 📲 PWA

## 本機運行

```bash
cd hungry-map
python3 -m http.server 8080
```

開 http://localhost:8080

## 部署 GitHub + Vercel

1. 將本資料夾 push 去 GitHub repo
2. Vercel Import 該 repo
3. Framework：Other（靜態），Root 即本目錄
4. Deploy 後會有 `*.vercel.app` 網址

每日更新（可選）：`.github/workflows/daily-update.yml` 會跑 `scripts/fetch-fehd.py`。

手動更新：

```bash
python3 scripts/fetch-fehd.py
```

## 目錄

```
hungry-map/
├── index.html
├── sw.js
├── manifest.webmanifest
├── vercel.json
├── data/restaurants.min.json
├── scripts/fetch-fehd.py
└── .github/workflows/daily-update.yml
```
