# 🧠 專案上下文文件 (Project Context for AI)

> **Purpose**: 提供 AI 在 Feature 開發階段所需的專案全貌理解  
> **Version**: 1.0.0  
> **Last Updated**: 2026-02-04  
> **維護頻率**: 每完成一個 Feature 並執行 Unify Flow 後更新  
> **產生指令**: `.flowkit.system-context`

---

## 1. 專案定位 (Project Identity)

### 1.1 一句話描述 (One-liner)

**TaiwanMarketTimeMachine（台股時光機）** 是一個 **視覺化事件研究與型態標記平台**，以「事件日」為錨點，透過多圖並列與統一時間視窗，即時產出事件後績效統計，加速台股策略研究與驗證。

### 1.2 核心價值主張

| 面向 | 價值 |
|------|------|
| **策略研究員** | 快速驗證「事件驅動策略」，透過視覺化多圖並列發現型態規律 |
| **開發者** | 嚴謹的 Specification-Driven Development (SDD) 流程，確保品質與可維護性 |
| **資料層** | 整合 MSSQL 台股歷史資料，支援事件後績效快速回測 |

### 1.3 目標使用者

- **策略研究員**：需要快速掃描條件符合的股票，並透過多圖檢視驗證策略假設
- **量化分析師**：需要事件後績效統計（如事件後 5/10/20 日報酬率）
- **AI 協作開發**：透過 Text-to-SQL 快速產生查詢條件，降低 SQL 撰寫門檻

---

## 2. 系統架構概覽 (Architecture Overview)

### 2.1 高階架構圖

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Vue 3)                            │
├─────────────────────────────────────────────────────────────────────┤
│  TradingView Lightweight Charts  │  Grid Layout Component           │
│  - K線圖表渲染                   │  - 多圖並列                      │
│  - 互動操作（Zoom/Pan）          │  - 事件日置中對齊                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ HTTP API
┌─────────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                              │
├─────────────────────────────────────────────────────────────────────┤
│  API Layer (src/api/)                                               │
│  - 圖表資料端點                                                      │
│  - 策略掃描端點                                                      │
│  - 事件後績效統計端點                                                │
│                                                                     │
│  Business Logic (src/services/)                                     │
│  - Time Window Engine（時間視窗引擎）                               │
│  - Micro Backtest Engine（微回測引擎）                              │
│  - AI Text-to-SQL Service（LangChain）                             │
│                                                                     │
│  Data Layer (src/db/)                                               │
│  - MSSQL 連線管理                                                   │
│  - 查詢最佳化                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATABASE (MSSQL)                                 │
├─────────────────────────────────────────────────────────────────────┤
│  [股價即時].[dbo].[1分K]                                            │
│  - 1 分鐘 K 線資料（聚合為日 K）                                     │
│  - 股票代碼、時間、OHLCV                                             │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 模組邊界與職責 (Boundaries)

> ⚠️ **禁止跨越邊界**：除非有明確理由，否則不得讓模組 A 直接存取模組 B 的內部實作。

| 模組 | 職責（一句話） | 擁有的資料/契約 | Public API 路徑 |
|------|----------------|-----------------|-----------------|
| `src/api/` | HTTP 端點定義與請求驗證 | API 契約、Request/Response 模型 | FastAPI Routes |
| `src/services/` | 業務邏輯層（Time Window/Backtest/AI） | 業務邏輯、計算引擎 | Service 方法 |
| `src/db/` | 資料庫連線與查詢 | 連線管理、SQL 查詢 | Database Adapter |
| `src/models/` | Pydantic 資料模型 | DTO、Entity 定義 | Python Classes |
| `src/logger.py` | 統一日誌管理 | Logger 配置 | `get_logger()` |

### 2.3 入口點 (Entry Points)

> 🎯 **開發時從這裡開始找**

| 類型 | 路徑 | 說明 |
|------|------|------|
| **後端主程式** | `src/main.py` | FastAPI 應用程式入口 |
| **API 路由** | `src/api/` | HTTP API 端點定義 |
| **業務邏輯** | `src/services/` | 核心功能實作 |
| **資料層** | `src/db/` | 資料庫連線與查詢 |
| **日誌模組** | `src/logger.py` | 統一日誌管理（已實作） |
| **測試入口** | `tests/` | 單元測試與整合測試 |

### 2.4 資料流向

```
前端請求 → FastAPI API Layer → Service Layer → DB Layer → MSSQL
                                     ↓                  ↓
                               業務邏輯處理        日K聚合 + 查詢
                                     ↓                  ↓
                            Response DTO ←────────── 原始資料
                                     ↓
                              前端渲染圖表
```

---

## 3. 已完成 Feature 清單 (Feature Registry)

> 🔑 **重要**：新 Feature 開發時，務必確認是否與既有 Feature 有交集，避免重複實作或破壞既有行為。

### 3.1 Feature 時間軸

| Feature ID | 名稱 | 狀態 | 核心能力 |
|------------|------|------|----------|
| 001-basic-chart-api | 基礎繪圖與 API 格式 | 🚧 In Progress | K線圖表、互動操作、小圖放大、API 格式規範 |

<!-- 
狀態圖示：
✅ Completed - 已完成
🚧 In Progress - 開發中
📋 Planned - 已規劃
❌ Cancelled - 已取消
-->

### 3.2 已實作的功能群組

| 群組 | 涵蓋範圍 | 相關檔案 |
|------|----------|----------|
| **基礎建設** | Logger 模組 | `src/logger.py` |
| **圖表基礎** | （開發中）K線渲染、互動操作 | `specs/features/001-basic-chart-api/` |

### 3.3 共享模組清單 (Shared Services)

> 🔧 **這些模組已經存在，請直接使用，不要重新實作**

| 模組 | 路徑 | 用途 | 如何使用 |
|------|------|------|----------|
| Logger | `src/logger.py` | 統一日誌管理 | `from src.logger import get_logger; logger = get_logger(__name__)` |

---

## 4. 關鍵資料模型 (Core Data Models)

> 📍 完整定義請見 `specs/system/data-model.md`（目前為範本，Feature 001 完成後更新）

### 4.1 核心實體關係

```
[股價即時].[dbo].[1分K] (MSSQL 資料表)
       │
       │ 聚合為
       ▼
日 K 線 (ChartData DTO)
       │
       │ 用於
       ▼
TradingView Lightweight Charts (前端渲染)
```

### 4.2 關鍵欄位摘要

**1分K 資料表**（台股歷史 1 分鐘 K 線）：
- 股票代碼、時間戳記、Open/High/Low/Close、Volume
- **聚合邏輯**：以交易日為單位，計算日 K 線 OHLCV

**ChartData DTO**（API Response 格式）：
- `stock_code`: str - 股票代碼
- `chart_data`: object - 包含 dates、ohlc、volume
- **擴充性**：未來可新增 `metrics` 欄位（Sharpe Ratio、事件後報酬率等）

### 4.3 契約與 Schema 索引 (Key Contracts)

| 類型 | 路徑 | 說明 |
|------|------|------|
| API 契約 | `specs/features/001-basic-chart-api/contracts/` | 圖表 API Response 格式 |
| 錯誤格式 | `specs/features/001-basic-chart-api/spec.md` | 標準化錯誤碼定義 |
| 資料模型 | `specs/features/001-basic-chart-api/data-model.md` | Feature 層級資料定義 |

### 4.4 目錄結構規範

```
c:\Development\TaiwanMarketTimeMachine/
├── src/                           # 程式碼主目錄
│   ├── api/                       # FastAPI 路由與端點
│   ├── services/                  # 業務邏輯層
│   ├── db/                        # 資料庫連線與查詢
│   ├── models/                    # Pydantic 資料模型
│   ├── logger.py                  # 統一日誌管理
│   └── main.py                    # FastAPI 應用程式入口
│
├── tests/                         # 測試目錄
│   ├── unit/                      # 單元測試
│   └── integration/               # 整合測試
│
├── specs/                         # 規格文件
│   ├── system/                    # 系統層級規格
│   └── features/                  # Feature 規格
│       └── 001-basic-chart-api/   # Feature 001 規格
│
├── docs/                          # 專案文件
│   ├── requirements/              # 需求文件（PRD、User Stories）
│   └── dev/                       # 開發者文件
│
├── logs/                          # 日誌輸出目錄
└── .artifacts/                    # 測試產物（coverage、pytest cache）
```

---

## 5. 核心流程 (Golden Flows)

> 📍 完整流程圖請見 `specs/system/flows.md`（目前為範本，Feature 001 完成後更新）

### 5.1 主要流程：圖表資料查詢與渲染（M01 階段）

```
前端請求 → API 驗證 → Service 聚合日K → DB 查詢 1分K → 返回 ChartData
   │           │              │               │              │
   ▼           ▼              ▼               ▼              ▼
  參數      Request DTO    OHLCV 計算     MSSQL Query    前端渲染
```

**路徑追蹤**：
```
Frontend Chart Component → /api/v1/chart-data → ChartDataService → DBAdapter → [股價即時].[dbo].[1分K]
```

### 5.2 未來流程（M02-M04）

- **Strategy Grid Mode**：多圖並列、事件日置中對齊
- **Time Window Engine**：統一時間視窗管理
- **Micro Backtest**：事件後績效統計
- **AI Text-to-SQL**：LangChain 驅動的查詢產生

---

## 6. 技術棧與約定 (Tech Stack & Conventions)

### 6.1 技術棧

| 層級 | 技術 | 版本 |
|------|------|------|
| **語言** | Python | 3.12+ |
| **套件管理** | uv | latest |
| **後端框架** | FastAPI | ^0.110.0 |
| **前端框架** | Vue 3 | ^3.4.0 |
| **圖表庫** | TradingView Lightweight Charts | ^4.1.0 |
| **資料庫** | Microsoft SQL Server | 2019+ |
| **DB Driver** | pyodbc | ^5.0.0 |
| **測試框架** | pytest | ^8.0.0 |
| **AI Framework** | LangChain | （M04 階段） |

### 6.2 整合約定 (Integration Rules) 🔴 NON-NEGOTIABLE

| 類別 | 規範 |
|------|------|
| **套件管理** | 僅使用 `uv`，禁止 pip/conda/poetry |
| **錯誤處理** | 標準化錯誤碼 + 詳細日誌（參考 Feature 001 Spec Q2） |
| **日誌** | 使用 `src/logger.py`，輸出至 `logs/`，禁止使用 `print()` |
| **測試** | Test-First 原則，測試檔案放 `tests/`，產物輸出至 `.artifacts/` |
| **API 規範** | RESTful 設計，統一 Response 格式（`{ data, error }` 結構） |
| **資料庫連線** | 使用 `.env` 配置，連線資訊不得寫入程式碼 |
| **前端快取** | 5 分鐘 TTL，避免過度請求 API |
| **Loading UX** | 300ms 最小顯示時間，避免閃爍效應 |

### 6.3 程式碼風格

- **Docstring**：模組級 MUST，類別級 SHOULD，函式級依複雜度
- **單一職責**：每個模組有明確責任範疇
- **最小變更**：禁止 drive-by refactor
- **檔案長度**：一般模組 400-800 行，超過 1000 行 MUST 拆分
- 註解規範：`# TODO:`, `# FIXME:`, `# HACK:`

---

## 7. Where-to-Look Playbook

> 🎯 **遇到問題時，去哪裡找答案**

### 7.1 依情境查找

| 遇到... | 第一步 | 第二步 | 第三步 |
|---------|--------|--------|--------|
| **資料庫連線問題** | `.env` 檢查連線資訊 | `src/db/` 連線管理 | `specs/features/001-basic-chart-api/quickstart.md` 環境設定 |
| **API 回應格式** | `specs/features/001-basic-chart-api/contracts/` | `src/models/` Pydantic 模型 | — |
| **日誌記錄問題** | `src/logger.py` 配置 | `logs/` 日誌檔案 | `.env` LOG_LEVEL 設定 |
| **測試失敗** | `tests/` 對應測試檔案 | `.artifacts/` Coverage 報告 | `specs/features/*/spec.md` AC 定義 |
| **前端圖表渲染** | TradingView Lightweight Charts 文件 | Feature 001 `research.md` 技術驗證 | — |
| **錯誤碼定義** | `specs/features/001-basic-chart-api/spec.md` Q2 | — | — |

### 7.2 如果你要...

| 需求 | 涉及模組 | 注意事項 |
|------|----------|----------|
| **新增 API 端點** | `src/api/` + `src/services/` | 遵循 RESTful 設計，統一 Response 格式 |
| **查詢資料庫** | `src/db/` | 使用 `.env` 配置，日K 需從 1分K 聚合 |
| **新增業務邏輯** | `src/services/` | 避免直接在 API Layer 實作邏輯 |
| **記錄日誌** | `src/logger.py` | 使用 `get_logger(__name__)`，輸出至 `logs/` |
| **定義資料模型** | `src/models/` | 使用 Pydantic，保持向下相容性 |
| **撰寫測試** | `tests/` | Test-First，對應 AC 編號，產物輸出至 `.artifacts/` |

---

## 8. 深入探索指引 (Documentation Index)

| 想了解... | 去哪裡看 |
|-----------|----------|
| **專案需求與 Roadmap** | `docs/requirements/PRD-ASSRP.md` |
| **Milestone 規劃** | `docs/requirements/Milestone/M01-basic-chart-and-api.md` |
| **User Stories（業務需求）** | `docs/requirements/user-stories/` |
| **系統完整 User Stories** | `specs/system/spec.md`（目前為範本） |
| **資料模型完整定義** | `specs/system/data-model.md`（目前為範本） |
| **系統流程圖** | `specs/system/flows.md`（目前為範本） |
| **API/CLI 合約** | `specs/system/contracts/`（待建立） |
| **Feature 001 規格** | `specs/features/001-basic-chart-api/spec.md` |
| **Feature 001 快速上手** | `specs/features/001-basic-chart-api/quickstart.md` |
| **Feature 001 技術研究** | `specs/features/001-basic-chart-api/research.md` |
| **Feature 001 資料模型** | `specs/features/001-basic-chart-api/data-model.md` |
| **測試案例** | `tests/`（待建立） |
| **技術債清單** | `docs/technical-debt.md` |
| **SpecKit 開發流程** | `docs/01.開發人員doc/03.SDD開發流程指南.md` |
| **FlowKit 指令說明** | `docs/77.flowkit相關文件/` |

---

## 9. AI 開發提示 (AI Development Hints)

### 9.1 新 Feature 開發 Checklist

1. ✅ 閱讀本文件，了解專案全貌
2. ✅ 確認與既有 Feature 的交集（參考第 3 節）
3. ✅ 確認是否有可複用的共享模組（參考第 3.3 節）
4. ✅ 確認涉及的資料模型（參考第 4 節）
5. ✅ 確認涉及的流程（參考第 5 節）
6. ✅ 確認整合約定（參考第 6.2 節 NON-NEGOTIABLE）
7. ✅ 使用 Where-to-Look 定位程式碼（參考第 7 節）
8. ✅ 深入閱讀相關 spec 文件（參考第 8 節）
9. ✅ **Test-First**：先寫測試，再實作
10. ✅ **Observability**：所有自動化流程 MUST 記錄日誌

### 9.2 常見陷阱 (Known Pitfalls)

| 陷阱 | 說明 | 預防方式 |
|------|------|----------|
| **使用錯誤的套件管理工具** | 誤用 pip/conda 導致環境不一致 | 只使用 `uv`，參考 Constitution §13 |
| **直接修改 System Spec** | 在 Feature 開發中修改 `specs/system/` | 禁止直接修改，需透過 Unify Flow |
| **跳過測試直接實作** | 違反 Test-First 原則 | 先寫測試，參考 Constitution §5 |
| **日誌使用 print()** | 無法追蹤與分析 | 使用 `src/logger.py`，參考 Constitution §9 |
| **API 格式不一致** | 破壞向下相容性 | 遵循 Feature 001 Spec Q2 錯誤格式 |
| **忘記更新 frontmatter** | spec.md 的 `system_context` 未更新 | 執行 system-context 後自動更新 |
| **資料表名稱錯誤** | 使用 `stock_daily` 而非 `[股價即時].[dbo].[1分K]` | 參考 `.env` 與 Feature 001 Clarifications |

### 9.3 快速參考

```bash
# 環境初始化
uv sync

# 執行測試
uv run pytest tests/

# 執行 API 伺服器（開發模式）
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 檢查程式碼品質
uv run ruff check src/
uv run mypy src/

# FlowKit 指令（AI Agent 模式）
/flowkit.system-context      # 產生/更新系統上下文
/flowkit.plan                 # Feature 任務分解
/flowkit.refine-loop          # Debug/優化循環
/flowkit.unify-flow           # 統合至 System Spec
```

---

## 10. 版本歷史 (Version History)

| 版本 | 日期 | 變更說明 | 執行者 |
|------|------|----------|--------|
| 1.0.0 | 2026-02-04 | 初始版本，基於 Feature 001 開發前的專案狀態 | AI (FlowKit System Context) |

---

## 附錄 A：精簡索引版 (System Context Index)

> 💡 **用途**：每次 AI 對話自動注入的輕量級上下文（50-150 行）

詳見：`.flowkit/memory/system-context-index.md`

# {常用指令 3 說明}
{指令}
```

---

## 10. 版本歷史 (Version History)

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| {版本號} | {日期} | {變更說明} |

---

> 📌 **維護提醒**：每完成一個 Feature 並執行 Unify Flow 後，執行 `.flowkit.system-context` 更新本文件。
