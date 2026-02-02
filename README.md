# SpecKit + FlowKit 專案範本

> **Specification-Driven Development (SDD) 完整開發套件**  
> SpecKit（規格驅動）+ FlowKit（流程自動化）｜預先清理，開箱即用

---

## 📋 這是什麼？

這是一個 **完整的 SDD 專案範本**，整合 **SpecKit** 與 **FlowKit** 兩大套件，適合：

- 🐍 Python 專案開發
- 🤖 AI 輔助開發專案
- 📊 數據分析與回測系統
- 🏢 需要嚴謹規格管理的企業專案

### 🎁 包含什麼？

| 項目 | 說明 |
|------|------|
| ✅ **SpecKit 工具鏈** | 規格驅動開發核心工具 |
| ✅ **FlowKit 套件** | 9 個自動化流程指令 |
| ✅ 標準目錄結構 | 符合 Constitution v4.0.3 |
| ✅ Logger 模組 | `src/logger.py` - 統一日誌管理 |
| ✅ AI 指令化 | GitHub Copilot + Cursor 完整支援 |
| ✅ 遷移工具 | 舊專案升級自動化腳本 |

> **💡 最佳實踐建議**：本範本整合了完整的 SpecKit + FlowKit 套件，建議搭配使用全部 9 個 FlowKit 指令以發揮最大效益。FlowKit 各指令之間環環相扣，從需求定義、規劃、一致性檢查、實作、追溯、驗證到統合，形成完整的品質保證鏈。

---

## 🚀 開始使用

### 📦 使用情境

#### 情境 A：建立新專案

```powershell
# 1. Clone 模板
git clone https://github.com/DrDeer119/99.my-speckit_template.git my-project
cd my-project

# 2. 重設 Git
Remove-Item -Recurse -Force .git
git init

# 3. 初始化專案
# 修改 pyproject.toml 中的專案名稱
# 執行 uv sync
```

📖 **新專案指南**: [START_HERE.md](START_HERE.md)

---

#### 情境 B：升級現有專案

如果您已有使用 SpecKit 的專案，可以升級到完整套件：

```powershell
# 1. Clone 模板到臨時目錄
git clone https://github.com/DrDeer119/99.my-speckit_template.git temp-template
cd temp-template

# 2. 執行自動化遷移
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\your-project"

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
