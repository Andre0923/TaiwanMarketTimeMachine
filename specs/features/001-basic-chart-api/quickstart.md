# Quick Start Guide: 基礎繪圖與 API 格式

> **Feature ID**: 001-basic-chart-api  
> **Target Audience**: 開發者、QA、DevOps  
> **Estimated Time**: 30 分鐘

---

## 1. Overview

本指南協助您快速建立 M01 Feature 的開發環境，包括前後端專案初始化、資料庫連線設定、執行測試。

**完成後您將能夠**：
- ✅ 執行後端 API 伺服器（FastAPI）
- ✅ 執行前端開發伺服器（Vue 3 + Vite）
- ✅ 測試圖表資料 API
- ✅ 執行單元測試與整合測試

---

## 2. Prerequisites

### 2.1 系統需求

| 項目 | 版本 | 安裝驗證指令 |
|------|------|--------------|
| **Python** | 3.11+ | `python --version` |
| **uv** | latest | `uv --version` |
| **Node.js** | 18+ | `node --version` |
| **npm** | 9+ | `npm --version` |
| **Microsoft SQL Server** | 2019+ | `sqlcmd -?` (可選) |
| **Git** | 2.0+ | `git --version` |

### 2.2 安裝必要工具

#### Windows

```powershell
# 安裝 uv（Python 環境管理）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 安裝 Node.js（前端開發）
# 下載：https://nodejs.org/

# 驗證安裝
uv --version
node --version
npm --version
```

#### macOS / Linux

```bash
# 安裝 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安裝 Node.js（使用 nvm）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
nvm install 18
nvm use 18

# 驗證安裝
uv --version
node --version
npm --version
```

---

## 3. 專案結構初始化

### 3.1 Clone 專案

```bash
cd c:\程式開發\TaiwanMarketTimeMachine
git checkout 1-basic-chart-api
git pull origin 1-basic-chart-api
```

### 3.2 預期目錄結構

執行後端前端初始化後，專案結構如下：

```
TaiwanMarketTimeMachine/
├── backend/                  # FastAPI 後端
│   ├── main.py              # 應用進入點
│   ├── api/
│   │   └── v1/
│   │       └── chart.py     # 圖表 API Endpoint
│   ├── models/
│   │   └── chart.py         # 資料模型
│   ├── services/
│   │   └── chart_service.py # 業務邏輯
│   ├── database.py          # MSSQL 連線
│   ├── pyproject.toml       # Python 依賴
│   └── uv.lock              # 鎖定檔
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chart.vue
│   │   │   └── ChartGrid.vue
│   │   ├── services/
│   │   │   └── chartApi.ts
│   │   └── types/
│   │       └── chart.ts
│   ├── package.json
│   └── vite.config.ts
├── tests/                   # 測試
│   ├── test_chart_api.py    # 後端測試
│   └── test_chart_component.spec.ts
├── specs/
│   └── features/
│       └── 001-basic-chart-api/
│           ├── spec.md
│           ├── plan.md
│           ├── data-model.md
│           └── contracts/
└── logs/                    # 日誌（自動建立）
```

---

## 4. 後端設定（FastAPI）

### 4.1 建立後端專案

```bash
# 建立後端目錄
cd c:\程式開發\TaiwanMarketTimeMachine
mkdir backend
cd backend

# 使用 uv 初始化專案
uv init .
uv add fastapi uvicorn[standard] pyodbc sqlalchemy python-dotenv

# 安裝開發依賴
uv add --dev pytest pytest-cov pytest-asyncio httpx
```

### 4.2 設定資料庫連線

建立 `.env` 檔案（**請勿提交至 Git**）：

```bash
# backend/.env
DB_SERVER=localhost
DB_PORT=1433
DB_DATABASE=taiwan_stock
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 17 for SQL Server
```

**安全提示**：
- 確認 `.env` 已加入 `.gitignore`
- 生產環境使用環境變數或密鑰管理服務

### 4.3 驗證資料庫連線

建立測試腳本 `backend/test_connection.py`：

```python
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    conn_str = (
        f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
        f"SERVER={os.getenv('DB_SERVER')},{os.getenv('DB_PORT')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"UID={os.getenv('DB_USERNAME')};"
        f"PWD={os.getenv('DB_PASSWORD')}"
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        print("✅ 資料庫連線成功！")
        print(f"SQL Server 版本：{row[0][:50]}...")
        conn.close()
    except Exception as e:
        print(f"❌ 資料庫連線失敗：{e}")

if __name__ == "__main__":
    test_connection()
```

執行測試：

```bash
cd backend
uv run python test_connection.py
```

### 4.4 執行後端伺服器

```bash
cd backend
uv run uvicorn main:app --reload --port 8000
```

**驗證**：
- 開啟瀏覽器：http://localhost:8000/docs
- 應看到 FastAPI 自動生成的 API 文件（Swagger UI）

---

## 5. 前端設定（Vue 3）

### 5.1 建立前端專案

```bash
cd c:\程式開發\TaiwanMarketTimeMachine
npm create vite@latest frontend -- --template vue-ts
cd frontend
npm install

# 安裝依賴
npm install tradingview-lightweight-charts@^4.1.0
npm install axios
npm install pinia

# 安裝開發依賴
npm install --save-dev @vitejs/plugin-vue vitest @vue/test-utils
```

### 5.2 設定 API Base URL

建立 `frontend/.env.development`：

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 5.3 執行前端開發伺服器

```bash
cd frontend
npm run dev
```

**驗證**：
- 開啟瀏覽器：http://localhost:5173
- 應看到 Vue 3 預設首頁

---

## 6. 測試設定

### 6.1 後端測試設定

建立 `backend/pyproject.toml` 中的測試配置：

```toml
[tool.pytest.ini_options]
testpaths = ["../tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--cov=backend",
    "--cov-report=html:.artifacts/coverage/html",
    "--cov-report=xml:.artifacts/coverage/coverage.xml",
]
cache_dir = ".artifacts/pytest_cache"

[tool.coverage.run]
data_file = ".artifacts/coverage/.coverage"
source = ["backend"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
]

[tool.coverage.html]
directory = ".artifacts/coverage/html"
```

### 6.2 執行後端測試

```bash
cd backend
uv run pytest
```

**查看 Coverage 報告**：
- 開啟 `.artifacts/coverage/html/index.html`

### 6.3 執行前端測試

```bash
cd frontend
npm run test
```

---

## 7. 資料準備

### 7.1 確認 stock_daily 表存在

⚠️ **重要**：確認 `stock_daily` 表已建立並包含測試資料。

**檢查方式**（使用 SSMS 或 sqlcmd）：

```sql
-- 檢查表是否存在
SELECT * FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_NAME = 'stock_daily';

-- 檢查資料筆數
SELECT COUNT(*) FROM stock_daily;

-- 查看範例資料（2330 台積電）
SELECT TOP 10 * 
FROM stock_daily 
WHERE stock_code = '2330' 
ORDER BY trade_date DESC;
```

### 7.2 匯入測試資料（如需要）

若資料表為空，可使用以下腳本匯入測試資料：

```sql
-- 範例：插入 2330 台積電 2024-01-01 的資料
INSERT INTO stock_daily (stock_code, trade_date, open_price, high_price, low_price, close_price, volume)
VALUES ('2330', '2024-01-01', 580.00, 585.00, 578.00, 583.00, 12345678);
```

**生產資料來源**（M02/M03 規劃）：
- 證交所開放資料 API
- CSV 檔案匯入
- 第三方資料提供商

---

## 8. API 測試

### 8.1 使用 cURL 測試

```bash
# 測試正常查詢
curl "http://localhost:8000/api/v1/chart-data?stock_code=2330&start_date=2024-01-01&end_date=2024-01-31"

# 測試錯誤處理（無效股票代碼）
curl "http://localhost:8000/api/v1/chart-data?stock_code=XXXX&start_date=2024-01-01&end_date=2024-01-31"

# 測試錯誤處理（日期範圍錯誤）
curl "http://localhost:8000/api/v1/chart-data?stock_code=2330&start_date=2024-02-01&end_date=2024-01-01"
```

### 8.2 使用 Swagger UI 測試

1. 開啟 http://localhost:8000/docs
2. 展開 `GET /api/v1/chart-data`
3. 點擊「Try it out」
4. 輸入參數：
   - stock_code: `2330`
   - start_date: `2024-01-01`
   - end_date: `2024-01-31`
5. 點擊「Execute」
6. 檢查 Response

---

## 9. 常見問題

### Q1: 資料庫連線失敗

**錯誤訊息**：`pyodbc.OperationalError: ('08001', ...)`

**解決方式**：
1. 確認 SQL Server 正在執行
2. 確認 `.env` 中的連線參數正確
3. 確認 SQL Server 允許遠端連線
4. 確認防火牆已開放 1433 埠

### Q2: uv 指令找不到

**錯誤訊息**：`'uv' is not recognized as an internal or external command`

**解決方式**：
1. 確認 uv 已安裝：重新執行安裝腳本
2. 重新啟動終端機（讓 PATH 生效）
3. 手動加入 PATH：
   ```powershell
   $env:Path += ";$env:USERPROFILE\.local\bin"
   ```

### Q3: 前端無法連線至後端 API

**錯誤訊息**：`CORS policy: No 'Access-Control-Allow-Origin' header`

**解決方式**：
1. 確認後端已啟用 CORS Middleware（參考 `contracts/chart-api.md` Section 7.3）
2. 確認 `.env.development` 中的 `VITE_API_BASE_URL` 正確

### Q4: TradingView Charts 無法載入

**錯誤訊息**：`Cannot find module 'tradingview-lightweight-charts'`

**解決方式**：
```bash
cd frontend
npm install tradingview-lightweight-charts@^4.1.0
```

---

## 10. 下一步

完成環境設定後，建議依序進行：

1. **閱讀規格文件**：
   - [spec.md](./spec.md) — Feature 完整規格
   - [data-model.md](./data-model.md) — 資料模型
   - [contracts/chart-api.md](./contracts/chart-api.md) — API 契約

2. **開發任務**：
   - 參考 `tasks.md`（Phase 2 生成）
   - 遵循 TDD 流程（先測試後實作）

3. **提交變更**：
   - 使用 Git Feature Branch 工作流程
   - Commit Message 遵循規範（參考 `copilot-instructions.md` Section 12）

---

## 11. 技術支援

**遇到問題？**
- 📖 查閱 [troubleshooting.md](../../docs/setup-guides/troubleshooting.md)
- 💬 詢問 Tech Lead 或專案負責人
- 🐛 建立 GitHub Issue（標籤：`help wanted`, `question`）

---

**文件版本**：v1.0.0  
**維護者**：AI Development Team  
**最後更新**：2026-02-03
