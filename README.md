# 🤖 Smart Crawler Full-Stack Portfolio

全端網頁爬蟲與數據儀表板專案，涵蓋靜態爬蟲、動態瀏覽器自動化、資料庫增量更新、FastAPI 後端 API、React 互動前端以及 GitHub Actions CI/CD 自動化測試。

---

## 🛠️ 技術棧 (Tech Stack)

* **網路爬蟲 (Crawlers)**: `Requests`, `BeautifulSoup4`, `Playwright (Chromium)`
* **資料庫與ORM (Database & ORM)**: `SQLModel`, `SQLite`
* **後端 API (Backend)**: `FastAPI`, `Uvicorn`
* **前端儀表板 (Frontend)**: `React`, `Vite`
* **自動化與測試 (CI/CD & Testing)**: `GitHub Actions`, `Pytest`

---

## ✨ 核心亮點與功能 (Key Features)

1. **雙模態爬蟲架構**：
   - **靜態爬蟲**：針對結構化網站（如 Books to Scrape）進行高效能多頁抓取。
   - **動態爬蟲**：利用 Playwright 模擬真實瀏覽器行為，處理依賴 JavaScript 渲染的動態網頁。
2. **智慧增量更新與去重**：
   - 透過 SQLModel 進行資料庫對應，結合唯一鍵與絕對路徑比對，自動識別重複資料並執行資料更新（Update）或略過，避免重複冗餘。
3. **全端資料視覺化**：
   - 後端提供 RESTful API 供前端呼叫，React 儀表板即時呈現爬取數據的統計分析與清單。
4. **自動化 CI/CD 測試**：
   - 配置 GitHub Actions 工作流程，每次 Push 程式碼時自動執行環境建置與 Pytest 離線單元測試，確保程式碼穩定性。
