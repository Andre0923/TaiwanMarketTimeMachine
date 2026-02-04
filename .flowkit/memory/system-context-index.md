# System Context Index v1.0.0

> **精簡索引版** — 每次 AI 對話自動注入的輕量級上下文  
> **最後更新**: 2026-02-04 | **完整版**: `.flowkit/memory/system-context.md`

---

## One-liner

**TaiwanMarketTimeMachine（台股時光機）** 是一個 **視覺化事件研究與型態標記平台**，以「事件日」為錨點，透過多圖並列與統一時間視窗，即時產出事件後績效統計，加速台股策略研究與驗證。

---

## Boundaries（模組邊界，禁止跨越）

- `src/api/`: HTTP 端點定義與請求驗證 | Owns: API 契約、Request/Response 模型 | API: FastAPI Routes
- `src/services/`: 業務邏輯層（Time Window/Backtest/AI） | Owns: 業務邏輯、計算引擎 | API: Service 方法
- `src/db/`: 資料庫連線與查詢 | Owns: 連線管理、SQL 查詢 | API: Database Adapter
- `src/models/`: Pydantic 資料模型 | Owns: DTO、Entity 定義 | API: Python Classes
- `src/logger.py`: 統一日誌管理 | Owns: Logger 配置 | API: `get_logger()`

---

## Entry Points（開發從這裡開始）

- **後端主程式**: `src/main.py` - FastAPI 應用程式入口
- **API 路由**: `src/api/` - HTTP API 端點定義
- **業務邏輯**: `src/services/` - 核心功能實作
- **資料層**: `src/db/` - 資料庫連線與查詢
- **日誌模組**: `src/logger.py` - 統一日誌管理（已實作）
- **測試入口**: `tests/` - 單元測試與整合測試

---

## Shared Services（直接使用，勿重複實作）

- **Logger**: `src/logger.py` → `from src.logger import get_logger; logger = get_logger(__name__)`

---

## Golden Flows（核心流程路徑追蹤）

- **圖表資料查詢（M01）**: 前端請求 → `/api/v1/chart-data` → ChartDataService → DBAdapter → `[股價即時].[dbo].[1分K]` → 前端渲染

---

## Where-to-Look（遇到問題去哪找）

- **資料庫連線問題** → `.env` → `src/db/`
- **API 回應格式** → `specs/features/001-basic-chart-api/contracts/` → `src/models/`
- **日誌記錄問題** → `src/logger.py` → `logs/` → `.env` LOG_LEVEL
- **測試失敗** → `tests/` → `.artifacts/` → `specs/features/*/spec.md` AC
- **錯誤碼定義** → `specs/features/001-basic-chart-api/spec.md` Q2

---

## NON-NEGOTIABLE（強制規範）

- **套件管理**: MUST 使用 `uv`，NEVER 使用 pip/conda/poetry
- **錯誤處理**: MUST 使用標準化錯誤碼 + 詳細日誌（參考 Feature 001 Spec Q2）
- **日誌**: MUST 使用 `src/logger.py`，NEVER 使用 `print()`
- **測試**: MUST Test-First 原則，產物輸出至 `.artifacts/`
- **API 規範**: MUST RESTful 設計，統一 Response 格式
- **資料庫連線**: MUST 使用 `.env` 配置，NEVER 寫入程式碼
- **前端快取**: MUST 5 分鐘 TTL，避免過度請求
- **Loading UX**: MUST 300ms 最小顯示時間，避免閃爍

---

## Known Pitfalls（常見陷阱）

- ❌ 使用 pip/conda 而非 uv
- ❌ 直接修改 `specs/system/`（需透過 Unify Flow）
- ❌ 跳過測試直接實作（違反 Test-First）
- ❌ 日誌使用 `print()` 而非 Logger
- ❌ 資料表名稱錯誤（應為 `[股價即時].[dbo].[1分K]`）
- ❌ 忘記更新 spec.md frontmatter 的 `system_context`

---

## Features（功能清單）

| Feature ID | 狀態 | 核心能力 |
|------------|------|----------|
| 001-basic-chart-api | 🚧 開發中 | K線圖表、互動操作、API 格式規範 |

---

## Tech Stack（技術棧）

- **後端**: Python 3.12+ / FastAPI / pyodbc / uv
- **前端**: Vue 3 / TradingView Lightweight Charts
- **資料庫**: Microsoft SQL Server 2019+
- **測試**: pytest

---

## Full Context

完整文件：`.flowkit/memory/system-context.md` （363 行）
- {規範 3}: {MUST/NEVER} {具體規範}

## Known Pitfalls (常見陷阱)
- {陷阱 1}: {預防方式}
- {陷阱 2}: {預防方式}
- {陷阱 3}: {預防方式}

## Completed Features (已完成功能，避免重複實作)
- {Feature ID}: {名稱} - {核心能力}
- {Feature ID}: {名稱} - {核心能力}
- {Feature ID}: {名稱} - {核心能力}

## In Progress
- {Feature ID}: {名稱} - {核心能力}

## Full Context
See: `.flowkit/memory/system-context.md`
```

---

## 使用方式

### 方式 1：放入 Agent Context Manual 區塊

在 `.specify/agent-context.md` 的 Manual 區塊中放入精簡版內容：

```markdown
<!-- MANUAL ADDITIONS START -->
# Context Index v{VERSION}
...（精簡版內容）...
<!-- MANUAL ADDITIONS END -->
```

### 方式 2：作為獨立檔案

放在 `.flowkit/memory/context-index.md`，在 speckit.plan 或其他指令階段自動引用。

---

## 填寫指引

### One-liner
- 用一句話說明專案是什麼、做什麼
- 範例：`VideoNote: Video-first 知識萃取工具，將影片轉化為時間軸逐字稿`

### Boundaries
- 列出 4-7 個主要模組
- 每個模組標示：職責 + 擁有什麼 + Public API 路徑
- 這告訴 AI「這個模組負責什麼，邊界在哪」

### Entry Points
- 列出 4-6 個最常作為開發起點的檔案
- 幫助 AI 快速定位程式碼入口

### Shared Services
- 列出已經存在且應該被複用的模組
- 防止 AI 重複實作已有功能

### Golden Flows
- 列出 2-4 個最重要的流程
- 使用「→」表示資料/控制流向

### Where-to-Look
- 針對常見開發情境，指出應該去哪些檔案查找

### NON-NEGOTIABLE
- 列出 3-5 條絕對必須遵守的規範
- 使用 MUST/NEVER 關鍵字

### Known Pitfalls
- 列出 3-5 個過去踩過的坑
- 簡短說明預防方式

### Completed Features
- 列出已完成的 Feature 及其核心能力
- 幫助 AI 避免重複實作

---

## 與完整版的關係

| 層級 | 檔案 | 篇幅 | 用途 |
|------|------|------|------|
| **Layer 1** | `.flowkit/memory/system-context-index.md` | 50-150 行 | 每次 AI 對話自動注入 |
| **Layer 2** | `.flowkit/memory/system-context.md` | 300-700 行 | 需要深入了解時引用 |

Layer 1 是 Layer 2 的「摘要索引版」，當 AI 需要更多細節時，會去 Layer 2 查找。
