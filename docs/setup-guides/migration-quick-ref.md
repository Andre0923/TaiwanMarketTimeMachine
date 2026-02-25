# 🚀 SpecKit + FlowKit 遷移快速參考

> **5 分鐘快速決策指南**

---

## ⚠️ 重要警告：AI 常見誤判

> **🔴 constitution.md 陷阱**：範本中的 `constitution.md` 是**刻意製造的精簡優化版**。
> AI 看到舊專案的版本較長，常誤以為自己的是「完整版」而拒絕更新。
> **較長不代表較完整**，請務必使用範本版本！

> **🟡 FlowKit 指令化被忽略**：AI 有時只願意更新 SpecKit，忽略 FlowKit。
> 請明確要求更新 `.cursor/commands/flowkit.*` 和 `.github/agents/flowkit.*`。

---

## 🎯 我該用哪種方案？

| 你的情況 | 方案 | 指令 |
|----------|------|------|
| 🆕 新專案，沒客製化 | **方案 A：完全覆蓋** | `migrate-to-full-kit.ps1 -Force` |
| 🛠️ 有少量客製化 | **方案 C：智能混合** | `migrate-to-full-kit.ps1` |
| 🏢 成熟專案，多客製化 | **方案 B：增量遷移** | 手動執行各 Phase |

---

## ⚡ 3 步驟快速遷移（方案 C）

```powershell
# ⚠️ 重要：請使用「絕對路徑」避免路徑錯誤

# 1. Clone 範本（使用絕對路徑）
git clone https://github.com/DrDeer119/99.spec-kit-cross-platform-template.git E:\templates\spec-kit-template

# 2. 設定路徑變數並執行遷移
$templatePath = "E:\templates\spec-kit-template"
$targetPath = "E:\projects\my-project"  # 修改為你的專案路徑

& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath

# 3. AI 記憶處理（條件式）
cd $targetPath
# 僅當 system-context 不存在時才需建立（遷移不會改變專案結構，已有的上下文仍然有效）
# 若不存在，在 Copilot Chat 執行：
/flowkit.system-context
```

> ⚠️ **路徑問題排查**：若出現「找不到路徑」錯誤，請：
> - 確認 Clone 時使用絕對路徑（不要用 `temp-template` 等相對路徑）
> - 使用 `Test-Path "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1"` 確認路徑存在

---

## 📦 遷移涵蓋內容

### ✅ 會自動處理
- `.specify/scripts/` - SpecKit 腳本
- `.specify/templates/` - Spec/Plan/Tasks 範本
- `.flowkit/templates/` - FlowKit 範本
- `.cursor/commands/` - Cursor 指令
- `.github/agents/` - GitHub Copilot Agents
- `.github/prompts/` - GitHub Copilot Prompts
- `docs/77.flowkit相關文件/` - FlowKit 文件
- `docs/76.改版歷史/` - 改版歷史
- `docs/01.開發人員doc/` - 開發人員文件
- `docs/requirements/Milestone/MNN-*.md` - Milestone 範本
- `docs/requirements/user-stories/US-X-*.md` - User Stories 範本
- `docs/setup-guides/migration-*.md` - 遷移文件（未來升級參考）
- `docs/setup-guides/migrate-to-full-kit.ps1` - 遷移腳本

### ⚗️ 智慧比對（腳本會提示，需手動判斷）
- `docs/00.目錄結構.md` - 每個專案結構不同，不存在時建立，已存在時手動合併
- `docs/technical-debt.md` - TD Registry，不存在時建立，已存在時比對範本新規則
- `tests/conftest.py` - 測試基礎設施（marker 註冊、慢測試自動偵測），不存在時建立，已存在時比對範本最新版

### ⚠️ 需手動檢查
- `.github/copilot-instructions.md` - 若有客製化
- `.specify/memory/constitution.md` - **🔴 MUST 使用範本版本**（範本是精簡優化版，舊版較長不代表較完整）

### 🔄 條件式建立
- `.flowkit/memory/system-context.md` - 僅當不存在時執行 `/flowkit.system-context`（遷移不改變專案結構，已有的上下文仍有效）

### 🚫 絕不覆蓋
- `specs/` - 專案規格
- `src/` - 程式碼
- `tests/` - 測試
- `docs/requirements/` - 需求文件

---

## 🔴 constitution.md 強制更新步驟

> 範本中的 constitution.md 是刻意製造的精簡版，請勿因舊版較長而保留！

```powershell
# 強制使用範本版本
Copy-Item -Path "speckit-template\.specify\memory\constitution.md" -Destination ".specify\memory\" -Force

# 然後手動補回客製化規則（若有）
```

---

## 🛡️ 安全機制

所有遷移都會：
1. ✅ 建立 `.migration-backup-YYYYMMDD-HHMMSS/` 備份
2. ✅ 支援 `-DryRun` 預覽
3. ✅ 保留專案核心檔案
4. ✅ Git 可隨時回滾

---

## 🔧 常用指令

### Dry Run（預覽）
```powershell
$templatePath = "E:\templates\spec-kit-template"
$targetPath = "E:\projects\my-project"

& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath `
    -DryRun
```

### 完全覆蓋（包含 copilot-instructions.md）
```powershell
& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath `
    -Force
```

### 不備份（不建議）
```powershell
& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath `
    -SkipBackup
```

---

## 📋 遷移後檢查

```powershell
# 驗證關鍵目錄
@(".specify/scripts", ".flowkit/templates", ".github/agents", ".cursor/commands") | 
    ForEach-Object { 
        if (Test-Path $_) { "✅ $_" } else { "❌ $_ 不存在" } 
    }

# 驗證範本檔案已複製
@(
    "docs/requirements/Milestone/MNN-MilestoneName-template.md",
    "docs/requirements/user-stories/US-X-GroupName-template.md",
    "docs/01.開發人員doc/00.Spec Kit 跨平台開發範本使用指南.md",
    "docs/setup-guides/migration-guide.md",
    "docs/setup-guides/migration-quick-ref.md",
    "docs/setup-guides/migrate-to-full-kit.ps1"
) | ForEach-Object { 
    if (Test-Path $_) { "✅ 範本: $_" } else { "❌ 範本未複製: $_" } 
}

# 🔴 驗證 FlowKit 指令化已更新（不要只更新 SpecKit）
@(".cursor/commands/flowkit.system-context.md", ".github/agents/flowkit.system-context.agent.md") | 
    ForEach-Object { 
        if (Test-Path $_) { "✅ FlowKit: $_" } else { "❌ FlowKit 未更新: $_" } 
    }

# 測試功能
/speckit.specify "Test feature"
/flowkit.system-context
```

### ⚗️ 智慧比對檔案確認

```powershell
# 確認目錄結構文件已處理（每個專案不同，需手動比對合併）
if (Test-Path "docs\00.目錄結構.md") { "✅ docs/00.目錄結構.md 存在" } else { "❌ 需建立" }

# 確認 Technical Debt Registry 已處理
if (Test-Path "docs\technical-debt.md") { "✅ docs/technical-debt.md 存在" } else { "❌ 需建立" }

# 確認測試基礎設施已處理
if (Test-Path "tests\conftest.py") { "✅ tests/conftest.py 存在" } else { "❌ 需建立（marker 註冊 + 慢測試自動偵測）" }
```

### 🧪 測試依賴確認

```powershell
# 確認 pytest-xdist 已安裝（並行測試必備）
$pyproject = Get-Content "pyproject.toml" -Raw -ErrorAction SilentlyContinue
if ($pyproject -match "pytest-xdist") { "✅ pytest-xdist 依賴已設定" } else { "⚠️ 缺少 pytest-xdist，執行：uv add pytest-xdist" }
```

### 📁 目錄結構調整建議（參考 `docs/00.目錄結構.md`）

| 目錄 | 說明 | 建議動作 |
|------|------|----------|
| `tests/` | 測試目錄 | 確保存在且對應 `src/` 結構 |
| `logs/` | 日誌目錄 | 確保存在，日誌不應散落在根目錄 |
| `.artifacts/` | 產物目錄 | 建立並存放 coverage、build 等可再生產物 |
| `.gitignore` | Git 忽略 | 將 `.artifacts/` 加入忽略清單 |

---

## 🆘 出問題了？

### 回滾方案

**方式 1：Git**
```powershell
git reset --hard HEAD
```

**方式 2：使用備份**
```powershell
# 找到備份
ls .migration-backup-*

# 恢復特定檔案
Copy-Item ".migration-backup-*/.github/copilot-instructions.md" ".github/" -Force
```

---

## 📚 詳細文件

完整指南：[migration-guide.md](migration-guide.md)

---

**快速開始**：先執行 `Test-Path "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1"` 確認路徑存在，再執行遷移腳本
