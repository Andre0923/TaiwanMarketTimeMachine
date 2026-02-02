# 🚀 SpecKit + FlowKit 快速入門

> **Version**: 2.1.0  
> **最後更新**: 2026-01-29  
> **用途**: 快速理解與開始使用完整的 SpecKit + FlowKit 套件

---

## 📋 這是什麼？

這是一個 **完整的 SDD (Specification-Driven Development) 開發套件**，整合：

- **SpecKit**：規格驅動開發核心工具（specify → plan → tasks → implement）
- **FlowKit**：9 個自動化流程指令（system-context, unify-flow, refine-loop 等）
- **AI 指令化**：GitHub Copilot + Cursor 完整支援

> **💡 建議**：FlowKit 的 9 個指令環環相扣，建議完整使用以達最佳開發體驗與品質保證。

### ✅ 已完成的事項（你不用做）

| 項目 | 狀態 | 說明 |
|------|------|------|
| 範例程式碼 | ✅ 已移除 | `src/example_module.py` (MovingAverage 計算) |
| 範例測試 | ✅ 已移除 | `tests/test_example_module.py` |
| 範例 templates | ✅ 已移除 | `templates/` 目錄 |
| System Spec | ✅ 已清空 | 只留結構框架，無範例內容 |
| uv.lock | ✅ 已移除 | 新專案應重新生成 |

### 📦 完整套件內容

| 項目 | 位置 | 用途 |
|------|------|------|
| **SpecKit 核心** | `.specify/` | 規格驅動開發工具鏈 |
| Feature 建立腳本 | `.specify/scripts/` | 自動化建立 Feature 分支與目錄 |
| Spec 範本 | `.specify/templates/` | spec.md / plan.md / tasks.md 範本 |
| Constitution | `.specify/memory/constitution.md` | 專案開發憲法 |
| **FlowKit 套件** | `.flowkit/` | 9 個自動化流程指令 |
| FlowKit 範本 | `.flowkit/templates/` | 各種輸出範本 |
| 專案上下文 | `.flowkit/memory/` | AI 記憶（system-context） |
| **AI 指令化** | `.github/agents/`, `.cursor/commands/` | Copilot + Cursor 指令 |
| 全域規範 | `.github/copilot-instructions.md` | AI 行為準則 |
| **基礎設施** | `src/logger.py` | 統一日誌模組 |
| 目錄結構 | 整個專案 | 符合 Constitution v4.0.3 |

---

## 🎯 新專案初始化（3 步驟）

### Step 1: 更新專案識別

```powershell
# 修改 pyproject.toml
[project]
name = "your-project-name"    # ← 改成你的專案名稱
version = "0.1.0"
description = "你的專案描述"
```

### Step 2: 重新生成 lock 檔案

```powershell
uv sync
```

### Step 3: 撰寫 System Spec

在 `specs/system/` 目錄下填寫：
- `spe核心工具與指令

### SpecKit 工作流程（在 AI Chat 中執行）

```bash
# 1. 建立 Feature Spec（從自然語言）
/speckit.specify "Add user authentication with OAuth2"

# 2. 澄清需求（若有疑問）
/speckit.clarify

# 3. 產生技術規劃
/speckit.plan

# 4. 分解任務
/speckit.tasks

# 5. 進入實作階段
/speckit.implement
```

### FlowKit 自動化指令（在 AI Chat 中執行）

```bash
# 產生專案上下文（AI 記憶）
/flowkit.system-context

# 合併 Feature 至 System Spec
/flowkit.unify-flow

# Debug / 優化循環
/flowkit.refine-loop

# 合併前檢查
/flowkit.pre-unify-check

# 一致性檢查
/flowkit.consistency-check

# User Story 追溯
/flowkit.trace
```

### PowerShell 腳本（直接執行）

```powershell
# 檢查環境
.\.specify\scripts\powershell\check-prerequisites.ps1

# 建立新 Feature（腳本方式）
.\.specify\scripts\powershell\create-new-feature.ps1 "Add payment system"

# 遷移舊專案
.\docs\setup-guides\migrate-to-full-kit.ps1 -TemplatePath "." -TargetPath "path\to\project"
```

### Logger 使用方式

```python
from src.logger import setup_logger

logger = setup_logger(__name__)
logger.info("程式開始執行")
logger.debug("除錯訊息")
logger.error("錯誤發生", exc_info=True)
```feature.ps1 -FeatureName "your-feature"
```

這會：
1. 建立 Git 分支 `N-your-feature`
2. 建立目錄 `specs/features/N-your-feature/`
3. 產生 `spec.md`, `plan.md`, `tasks.md` 模板

---

## 📁 目錄結構說明

```
專案根目錄/
├── .specify/                    # SDD 工具鏈
│   ├── scripts/powershell/      # 自動化腳本
│   └── templates/               # Spec/Plan/Tasks 模板
│
├── docs/                        # 專案文件
│   └── technical-debt.md        # 技術債追蹤（可清空或保留）
│
├── logs/                        # 日誌輸出目錄
│   └── .gitkeep
│
├── specs/                       # 規格文件（SDD 核心）
│   ├── features/                # Feature Specs（開發中的功能）
│   ├── history/                 # 歷史歸檔
│   └── system/                  # System Spec（唯一真相）
│       ├── spec.md              # ← 主規格文件
│       ├── data-model.md        # ← 資料模型
│       ├── flows.md             # ← 系統流程
│       └── contracts/           # API 合約
│
├── src/                         # 程式碼
│   ├──SpecKit 與 FlowKit 的差異？

- **SpecKit**：規格驅動開發的核心流程（specify → plan → tasks → implement）
- **FlowKit**：自動化輔助工具（system-context、unify-flow、refine-loop 等 9 個指令）

兩者搭配使用，形成完整的 SDD 開發體驗。建議使用全部 FlowKit 指令以確保從需求到實作的完整追溯與品質保證。

### Q: 我已有使用 SpecKit 的專案，如何升級？

使用自動化遷移工具：
```powershell
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\your-project"
```

詳見 [遷移指南](docs/setup-guides/migration-guide.md)

### Q: FlowKit 的 9 個指令分別做什麼？

| 指令 | 用途 |
|------|------|
| `BDD-Milestone` | Milestone 轉 BDD |
| `Milestone-context` | 產生本次 Milestone 開發上下文 |
| `system-context` | 產生專案全貌文件（AI 記憶） |
| `consistency-check` | 一致性檢查（Plan 階段） |
| `refine-loop` | Debug / 優化循環 |
| `trace` | User Story 追溯 |
| `pre-unify-check` | 合併前驗證 |
| `unify-flow` | 合併 Feature 至 System Spec |
| `requirement-sync` | 同步外部需求 |

完整說明：[docs/77.flowkit相關文件/README.md](docs/77.flowkit相關文件/README.md)

**建議使用順序**：依專案需求，完整流程為 BDD-Milestone → Milestone-context → (SpecKit 流程) → consistency-check → implement → pre-unify-check → trace → requirement-sync → unify-flow。

### Q: 我可以刪除 `src/logger.py` 嗎？
### 方式 1：從 System Spec 開始（推薦給新專案）

1. 撰寫 `specs/system/spec.md`（系統整體規格）
2. 執行 `/flowkit.system-context` 產生專案上下文
3. 執行 `/speckit.specify "First feature"` 建立第一個 Feature

### 方式 2：直接建立 Feature（推薦給快速原型）

1. 執行 `/speckit.specify "Your feature description"`
2. 跟隨 SpecKit 流程（clarify → plan → tasks → implement）
3. 完成後執行 `/flowkit.unify-flow` 合併至 System Spec

### 驗證環境

```powershell
# 確認環境正常
uv run pytest

# 檢查 SpecKit 腳本
.\.specify\scripts\powershell\check-prerequisites.ps1

# 測試建立 Feature（Dry Run）
.\.specify\scripts\powershell\create-new-feature.ps1 "Test feature" -DryRun
```

---

## 📚 延伸閱讀

- 📘 [SDD 開發流程指南](docs/01.開發人員doc/03.SDD開發流程指南.md)
- 📗 [FlowKit 功能總覽](docs/77.flowkit相關文件/README.md)
- 📁 [目錄結構規範](docs/00.目錄結構.md)
- 🚀 [遷移指南](docs/setup-guides/migration-guide.md)
- 📜 [AI 全域規範](.github/copilot-instructions.md)

---

**Happy Coding! 🎉**

**版本**: v2.1.0  
**最後更新**: 2026-01-29Milestone 轉 BDD |

完整說明：[docs/77.flowkit相關文件/README.md](docs/77.flowkit相關文件/README.md)

### Q: 我可以刪除 `src/logger.py` 嗎？

可以，但建議保留。它提供了：
- 自動建立 `logs/` 目錄
- 檔案 + 終端機雙輸出
- 符合 Constitution 的日誌格式

### Q: 這份 START_HERE.md 要一直保留嗎？

建議在專案成熟、團隊熟悉後刪除。它的目的是「快速入門」，不是「長期文件」。

### Q: AI 指令在哪裡執行？

- **GitHub Copilot**：在 VS Code 的 Copilot Chat 中執行（如 `/speckit.specify`）
- **Cursor**：在 Cursor 的 Chat 中執行（如 `@speckit.specify`）
- **PowerShell 腳本**：直接在終端機執行（如 `create-new-feature.ps1`）

**`src/example_module.py`** 包含：
- `MovingAverage` class — SMA/EMA 計算
- `PriceData` dataclass — 價格資料模型
- `validate_prices()` — 價格驗證函式
- `format_price()` — 價格格式化
- `calculate_price_change()` — 漲跌幅計算

**`tests/test_example_module.py`** 包含：
- 14 個測試案例，覆蓋上述功能

### 已移除的 System Spec 內容

**`specs/system/spec.md`** 原本包含 4 個 User Stories：
- US-SYS-1: 移動平均線計算
- US-SYS-2: 價格資料驗證  
- US-SYS-3: 價格格式化與變動計算
- US-SYS-4: 日誌記錄

> **為什麼移除？** 這些是「範例」而非「真實需求」。新專案應該從空白 Spec 開始，填入真正的業務需求。

---

## ❓ FAQ

### Q: 我可以刪除 `src/logger.py` 嗎？

可以，但建議保留。它提供了：
- 自動建立 `logs/` 目錄
- 檔案 + 終端機雙輸出
- 符合 Constitution 的日誌格式

### Q: `docs/technical-debt.md` 要留嗎？

這是 SDD 的標準文件。建議保留結構，清空內容。目前檔案中的 TD-001~TD-004 是範例的技術債，與你的專案無關。

### Q: 這份 START_HERE.md 要一直保留嗎？

建議在專案成熟、團隊熟悉後刪除。它的目的是「交接」，不是「長期文件」。

### Q: 我需要手動清理 `specs/features/` 嗎？

**不用**。目前 `specs/features/` 是空的。Feature 目錄只在開發新功能時才會建立。

---

## 🚀 開始開發！

完成上面的 3 步驟後，你可以：

1. 執行 `uv run pytest` 確認環境正常（目前應該是 0 tests）
2. 開始撰寫 `specs/system/spec.md`
3. 或直接用腳本建立第一個 Feature 開始開發

**Happy Coding! 🎉**
