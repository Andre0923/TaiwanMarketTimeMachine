# Taiwan Market Time Machine（台股時光機）

> **視覺化事件研究平台 - 基礎繪圖功能（M01）**  
> FastAPI 後端 + 日K線圖表 API | Specification-Driven Development

[![Tests](https://img.shields.io/badge/tests-61%20passed-brightgreen)](https://github.com/Andre0923/TaiwanMarketTimeMachine)
[![Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen)](https://github.com/Andre0923/TaiwanMarketTimeMachine)
[![Python](https://img.shields.io/badge/python-3.14%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128%2B-009688)](https://fastapi.tiangolo.com/)

---

## 📋 專案簡介

台股時光機是一個**視覺化事件研究平台**，協助使用者：
- 📈 視覺化股票歷史價格與事件關聯
- 🔍 探索市場事件對股價的影響
- 📊 快速回測簡單策略假設
- 🎯 提供直覺的互動式圖表介面

### 🎯 M01 Milestone：基礎繪圖與 API 格式

本專案目前實作 **M01 核心功能**：
- ✅ 日K線圖表資料 API（從 1分K 聚合）
- ✅ RESTful API 契約與固定格式
- ✅ 完整的測試覆蓋（89% 覆蓋率）
- ✅ TradingView Lightweight Charts 相容格式
- 🚧 前端互動介面（延後至 M02）

### 📦 技術架構

| 層級 | 技術 | 說明 |
|------|------|------|
| **後端框架** | FastAPI 0.128+ | 高效能非同步 API 框架 |
| **資料庫** | MSSQL Server 2019+ | [股價即時].[dbo].[1分K] |
| **資料驗證** | Pydantic 2.12+ | Request/Response 驗證 |
| **測試框架** | pytest 9.0+ | 單元測試 + 整合測試 |
| **環境管理** | uv | 快速 Python 環境管理 |
| **開發規範** | SDD (SpecKit + FlowKit) | 規格驅動開發流程 |

### 🎯 已實作功能（M01）

#### US A-1: K線與成交量基礎繪圖
- ✅ 日K線資料查詢 API：`GET /api/chart/daily`
- ✅ 1分K → 日K 聚合邏輯（OHLC + Volume）
- ✅ 無資料處理（空陣列 + metadata）
- ✅ 43 個單元測試 + 整合測試

#### US G-2: API Response 格式設計
- ✅ 固定 Response 格式（stock_code, chart_data, metadata）
- ✅ 統一錯誤格式（error.code, error.message, error.details）
- ✅ 向後相容策略（可擴充 metadata）
- ✅ API 契約文件與 10 個契約測試

---

## 🚀 快速開始

### 1. 環境設定

#### 系統需求

| 項目 | 版本 | 驗證指令 |
|------|------|----------|
| Python | 3.14+ | `python --version` |
| uv | latest | `uv --version` |
| MSSQL Server | 2019+ | `sqlcmd -?` |

#### 安裝依賴

```powershell
# Clone 專案
git clone https://github.com/Andre0923/TaiwanMarketTimeMachine.git
cd TaiwanMarketTimeMachine

# 安裝 uv（若尚未安裝）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 建立虛擬環境並安裝依賴
uv sync
```

### 2. 資料庫連線設定

建立 `.env` 檔案（參考 `.env.example`）：

```bash
# Database Configuration
DB_SERVER=your-server-name
DB_PORT=16888
DB_DATABASE=股價即時
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_TRUST_CERT=yes
```

**測試連線**：
```powershell
uv run python -c "from src.db.connection import test_connection; test_connection()"
```

### 3. 啟動後端 API 服務

```powershell
# 開發模式（自動重載）
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 服務啟動後訪問：
# - API 文件：http://localhost:8000/docs
# - ReDoc：http://localhost:8000/redoc
# - 健康檢查：http://localhost:8000/health
```

### 4. 執行測試

```powershell
# 執行所有測試
uv run pytest tests/ -v

# 執行測試並生成覆蓋率報告
uv run pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html:.artifacts/coverage/html

# 開啟覆蓋率報告
start .artifacts/coverage/html/index.html
```

### 5. API 使用範例

#### curl
```bash
curl -X GET "http://localhost:8000/api/chart/daily?stock_code=2330&start_date=2024-01-01&end_date=2024-01-31"
```

#### Python
```python
import requests

response = requests.get(
    "http://localhost:8000/api/chart/daily",
    params={
        "stock_code": "2330",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31"
    }
)

data = response.json()
print(f"資料點數: {len(data['chart_data'])}")
```

詳見 [API 契約文件](specs/features/001-basic-chart-api/contracts/chart-api.md)

---

## 📂 專案結構

```
TaiwanMarketTimeMachine/
├── src/                          # 原始碼
│   ├── api/                      # API 路由
│   │   └── routes/
│   │       └── chart.py          # 圖表 API 端點
│   ├── db/                       # 資料庫層
│   │   ├── connection.py         # DB 連線管理
│   │   └── stock_repository.py   # 資料查詢 Repository
│   ├── models/                   # Pydantic 模型
│   │   └── chart.py              # Request/Response 模型
│   ├── services/                 # 業務邏輯層
│   │   └── chart_service.py      # 圖表資料服務
│   ├── logger.py                 # 日誌模組
│   └── main.py                   # FastAPI 應用入口
├── tests/                        # 測試程式碼
│   ├── unit/                     # 單元測試
│   └── integration/              # 整合測試
├── specs/                        # 規格文件（SDD）
│   ├── features/                 # Feature 規格
│   │   └── 001-basic-chart-api/
│   │       ├── spec.md           # User Story 定義
│   │       ├── data-model.md     # 資料模型
│   │       ├── plan.md           # 技術規劃
│   │       ├── tasks.md          # 實作任務清單
│   │       └── contracts/
│   │           └── chart-api.md  # API 契約文件
│   └── system/                   # 系統層規格
├── .artifacts/                   # 測試產物（.gitignore）
│   ├── coverage/                 # 覆蓋率報告
│   └── pytest_cache/             # pytest 快取
├── logs/                         # 應用程式日誌
├── docs/                         # 專案文件
└── pyproject.toml                # 專案配置
```

---

## 🧪 測試策略

### 測試層級

| 層級 | 目錄 | 覆蓋範圍 | 測試數量 |
|------|------|----------|----------|
| **單元測試** | `tests/unit/` | Models, Repository, Service, Connection | 42 |
| **整合測試** | `tests/integration/` | API 端點, 契約驗證 | 19 |
| **總計** | - | **整體覆蓋率 89%** | **61** |

### 測試執行策略

```powershell
# 快速測試（僅單元測試）
uv run pytest tests/unit/ -v

# 完整測試（單元 + 整合）
uv run pytest tests/ -v

# 監看模式（TDD 開發）
uv run pytest-watch tests/ -v
```

---

## 📖 文件索引

### 開發文件
- [Quick Start Guide](specs/features/001-basic-chart-api/quickstart.md) - 30 分鐘快速上手
- [API 契約文件](specs/features/001-basic-chart-api/contracts/chart-api.md) - 完整 API 規範
- [資料模型](specs/features/001-basic-chart-api/data-model.md) - 資料結構與聚合邏輯

### 規格文件（SDD）
- [Feature Spec](specs/features/001-basic-chart-api/spec.md) - User Story 定義
- [Technical Plan](specs/features/001-basic-chart-api/plan.md) - 技術架構規劃
- [Task Breakdown](specs/features/001-basic-chart-api/tasks.md) - 實作任務清單

### SpecKit + FlowKit
- [SDD 開發流程指南](docs/01.開發人員doc/03.SDD開發流程指南.md)
- [Constitution（開發憲法）](.specify/memory/constitution.md)
- [FlowKit 指令說明](docs/77.flowkit相關文件/)

---

## 🔧 開發指南

### 新增功能流程（SDD）

```powershell
# 1. 定義需求（SpecKit）
/speckit.clarify "功能描述"

# 2. 建立規劃
/speckit.plan

# 3. 任務分解
/speckit.tasks

# 4. 一致性檢查
/flowkit.consistency-check

# 5. 實作
/speckit.implement

# 6. 追溯驗證
/flowkit.trace

# 7. 統合至 System Spec
/flowkit.unify-flow
```

### 程式碼規範

- **Test-First**: 先寫測試再實作
- **覆蓋率目標**: > 80%（目前 89%）
- **Docstring**: 所有 public 函式需文件
- **Logging**: 關鍵流程需日誌記錄
- **類型註解**: 使用 Python Type Hints

---

## 🤝 貢獻指南

### 分支策略

```
main          ← 穩定版本
  └── feature/NNN-feature-name  ← Feature 開發分支
```

### Commit Message 格式

```
<type>: <繁體中文摘要>

feat: 新增日K線圖表 API
fix: 修復日期範圍驗證錯誤
docs: 更新 API 契約文件
test: 新增 Repository 單元測試
```

---

## 📊 專案狀態

### M01 Milestone 進度

| User Story | 狀態 | 測試 | 覆蓋率 |
|------------|------|------|--------|
| US A-1: K線與成交量 | ✅ | 43/43 | 100% |
| US G-2: API 格式設計 | ✅ | 18/18 | 100% |
| US A-2: 圖表互動 | 🚧 | - | - |
| US A-3: 小圖放大 | 🚧 | - | - |
| US A-4: Loading & Error | 🚧 | - | - |

### 下一步計畫（M02）

- [ ] 前端 Vue 3 + TradingView Charts 整合
- [ ] 圖表互動操作（Zoom/Pan/Crosshair）
- [ ] Loading 狀態與錯誤處理
- [ ] 小圖點擊放大功能

---

## 📜 授權

本專案採用 MIT License。

---

## 📞 聯絡方式

- **開發者**: Andre Hsu
- **GitHub**: [@Andre0923](https://github.com/Andre0923/TaiwanMarketTimeMachine)
- **專案**: [TaiwanMarketTimeMachine](https://github.com/Andre0923/TaiwanMarketTimeMachine)

---

**Built with ❤️ using SpecKit + FlowKit | Specification-Driven Development**

# 3. 重建 AI 記憶
cd E:\path\to\your-project
# 在 Copilot Chat 執行：/flowkit.system-context
```

📖 **遷移指南**: [docs/setup-guides/migration-guide.md](docs/setup-guides/migration-guide.md)  
⚡ **快速參考**: [docs/setup-guides/migration-quick-ref.md](docs/setup-guides/migration-quick-ref.md)

---

### 前置需求

- Python 3.12+
- uv (套件管理器)
- Git
- PowerShell 7+ (Windows)
- GitHub Copilot 或 Cursor（AI 輔助開發）

---

## 📁 目錄結構

```
├── .specify/              # SpecKit 工具鏈
│   ├── scripts/           # 自動化腳本（PowerShell）
│   ├── templates/         # Spec/Plan/Tasks 範本
│   └── memory/            # AI 記憶（Constitution）
│
├── .flowkit/              # FlowKit 套件
│   ├── templates/         # FlowKit 輸出範本
│   └── memory/            # 專案上下文（AI 記憶）
│
├── .github/               # GitHub Copilot 指令化
│   ├── agents/            # Copilot Agents（SpecKit + FlowKit）
│   ├── prompts/           # Copilot Prompts
│   └── copilot-instructions.md  # 全域 AI 規範
│
├── .cursor/               # Cursor 指令化
│   └── commands/          # Cursor Commands（SpecKit + FlowKit）
│
├── specs/                 # 規格文件（SDD 核心）
│   ├── system/            # System Spec（唯一真相）
│   ├── features/          # Feature Specs（開發中）
│   └── history/           # 歷史歸檔（unify-flow 後）
│
├── src/                   # 程式碼
│   ├── __init__.py
│   └── logger.py          # 統一日誌模組
│
├── te核心功能

### SpecKit 指令（規格驅動開發）

| 指令 | 用途 | 說明 |
|------|------|------|
| `/speckit.specify` | 建立 Feature Spec | 從自然語言生成規格 |
| `/speckit.clarify` | 澄清需求 | 互動式需求澄清 |
| `/speckit.plan` | 技術規劃 | 產生實作計畫 |
| `/speckit.tasks` | 任務分解 | 產生可驗收任務清單 |
| `/speckit.analyze` | 分析影響 | 分析變更影響範圍 |
| `/speckit.implement` | 實作階段 | 進入實作階段 |

### FlowKit 指令（流程自動化）

| 指令 | 用途 | 說明 |
|------|------|------|
| `/flowkit.BDD-Milestone` | BDD Milestone | Milestone 轉 BDD |
| `/flowkit.Milestone-Context` | Milestone Context | 產生本次開發上下文 |
| `/flowkit.system-context` | 系統上下文 | 產生專案全貌文件 |
| `/flowkit.consistency-check` | 一致性檢查 | 檢查規格一致性 |
| `/flowkit.refine-loop` | 精煉循環 | Debug / 優化循環 |
| `/flowkit.pre-unify-check` | 合併前檢查 | 驗證是否可合併 |
| `/flowkit.trace` | 追溯關係 | User Story 追溯 |
| `/flowkit.requirement-sync` | 需求同步 | 同步外部需求 |
| `/flowkit.unify-flow` | 統合流程 | 合併 Feature 至 System Spec |


### 基礎指令

```powershell
# 檢查環境
.\.specify\scripts\powershell\check-prerequisites.ps1

# 建立新 Feature（腳本方式）
.\.specify\scripts\powershell\create-new-feature.ps1 "Add user authentication"

# 執行測試
uv run pytest tests/ -v

# 遷移舊專案
.\docs\setup-guides\migrate-to-full-kit.ps1 -TemplatePath "." -TargetPath "path\to\project"
```

---

## 📚 文件導覽

### 新手入門
- 📖 [START_HERE.md](START_HERE.md) - 快速入門指南
- 📁 [docs/00.目錄結構.md](docs/00.目錄結構.md) - 目錄結構規範
- 🔧 [docs/setup-guides/complete-installation.md](docs/setup-guides/complete-installation.md) - 完整安裝指南

### 開發指南
- 📘 [docs/01.開發人員doc/03.SDD開發流程指南.md](docs/01.開發人員doc/03.SDD開發流程指南.md) - SDD 開發流程
- 📗 [docs/77.flowkit相關文件/README.md](docs/77.flowkit相關文件/README.md) - FlowKit 功能總覽

### 遷移指南
- 🚀 [docs/setup-guides/migration-guide.md](docs/setup-guides/migration-guide.md) - 完整遷移指南
- ⚡ [docs/setup-guides/migration-quick-ref.md](docs/setup-guides/migration-quick-ref.md) - 遷移快速參考

### 規範文件
- 📜 [.github/copilot-instructions.md](.github/copilot-instructions.md) - AI 全域規範
- 📋 [.specify/memory/constitution.md](.specify/memory/constitution.md) - 專案憲法

---

## 🆘 常見問題

### Q: 這個範本與純 SpecKit 有什麼不同？

A: 這是**完整套件**，包含：
- ✅ SpecKit（規格驅動開發核心）
- ✅ FlowKit（9 個自動化流程指令）
- ✅ AI 指令化（GitHub Copilot + Cursor）
- ✅ 遷移工具（舊專案升級腳本）

### Q: 我已經有使用 SpecKit 的專案，如何升級？

A: 使用自動化遷移工具：
```powershell
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "your-project-path"
```

詳見 [遷移指南](docs/setup-guides/migration-guide.md)

### Q: FlowKit 的 9 個指令分別做什麼？

A: FlowKit 提供完整的開發流程自動化支援，涵蓋需求定義、規劃驗證、實作追溯、品質檢查到最終統合。詳細說明請見 [FlowKit 功能總覽](docs/77.flowkit相關文件/README.md)。

建議依標準流程使用全部 9 個指令，以確保規格與實作的完整追溯性與一致性。

---

## 📜 License

MIT

---

**版本**: v2.0.0  
**最後更新**: 2026-01-29
## 🔧 快速指令

```powershell
# 檢查環境
.\.specify\scripts\powershell\check-prerequisites.ps1

# 建立新 Feature
.\.specify\scripts\powershell\create-new-feature.ps1 -FeatureName "your-feature"

# 執行測試
uv run pytest tests/ -v
```

---

## 📜 License

MIT
