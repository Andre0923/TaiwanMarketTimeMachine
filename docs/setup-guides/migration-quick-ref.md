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
| 🏢 已有 SpecKit 專案要升級 | **方案 B：升級現有專案** | `migrate-to-full-kit.ps1` |

---

## ⚡ 3 步驟快速遷移（方案 C）

```powershell
# ⚠️ 重要：請使用「絕對路徑」避免路徑錯誤

# 1. Clone 範本（使用絕對路徑）
git clone https://github.com/DrDeer119/99.spec-kit-cross-platform-template.git E:\templates\spec-kit-template

# 2. 設定路徑變數並執行遷移
# ★ 腳本第一步（Step 0）會自動從範本同步遷移工具到目標專案
#   確保目標專案的 docs/setup-guides/ 將更新為最新版本
#   請始終從 $templatePath 執行腳本，不要使用目標專案的舊版本
$templatePath = "E:\templates\spec-kit-template"
$targetPath = "E:\projects\my-project"  # 修改為你的專案路徑

& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath

# 3. AI 記憶處理（條件式）
cd $targetPath
# 僅當 system-context 不存在時才需建立（遷移不會改變專案結構，已有的上下文仍然有效）
if (-not (Test-Path ".flowkit/memory/system-context.md")) {
    # 在 Copilot Chat 執行：/flowkit.system-context
    Write-Host "⚠️ 尚未建立 system-context，請在 IDE 中執行 /flowkit.system-context"
} else {
    Write-Host "✅ system-context 已存在，遷移不影響專案結構，無需重建"
}
```

> ⚠️ **路徑問題排查**：若出現「找不到路徑」錯誤，請：
> - 確認 Clone 時使用絕對路徑（不要用 `temp-template` 等相對路徑）
> - 使用 `Test-Path "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1"` 確認路徑存在

> 💡 **Dropbox / 雲端同步環境**：
> - 若遇到檔案被占用，腳本會自動重試（最多 3 次，每次 2 秒）
> - 建議將範本 Clone 到 `$env:TEMP` 等非同步目錄
> - 若仍失敗，暫停同步服務後重試

---

## 🛠️ 情境 B：升級現有專案（可直接照做）

```powershell
# ⚠️ 重要：請使用「絕對路徑」避免路徑錯誤
# 範例假設：
#   - 範本位置：E:\templates\spec-kit-template
#   - 目標專案：E:\projects\my-project

# 1. Clone 模板到臨時目錄（注意 Clone 後的絕對路徑）
git clone https://github.com/DrDeer119/99.spec-kit-cross-platform-template.git E:\templates\spec-kit-template

# 2. 確認遷移腳本路徑存在
$templatePath = "E:\templates\spec-kit-template"
$targetPath = "E:\projects\my-project"
Test-Path "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1"  # 應回傳 True

# 3. 執行自動化遷移（使用絕對路徑）
& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath

# 4. 確認遷移結果（腳本執行時已自動報告 ✅/❌）
cd $targetPath
git status  # 確認新增的檔案是否符合預期

# 5. AI 記憶處理（條件式）
# 若專案尚未有 system-context，才需要建立：
if (-not (Test-Path ".flowkit/memory/system-context.md")) {
    # 在 Copilot Chat 執行：/flowkit.system-context
    Write-Host "⚠️ 尚未建立 system-context，請在 IDE 中執行 /flowkit.system-context"
} else {
    Write-Host "✅ system-context 已存在，遷移不影響專案結構，無需重建"
}
```

> ⚠️ **路徑問題排查**：若執行遷移腳本時出現「找不到路徑」錯誤，請：
> - 確認 Clone 時使用的絕對路徑
> - 使用 `Test-Path` 確認腳本路徑存在
> - 避免使用相對路徑（如 `..\temp-template`）

> 💡 **Dropbox / 雲端同步環境注意事項**：
> - 若遇到「檔案被占用」錯誤，腳本會自動重試（最多 3 次，每次間隔 2 秒）
> - 建議將範本 Clone 到非同步目錄（如 `$env:TEMP`）
> - 若重試仍失敗，請暫時暫停雲端同步服務後重新執行

> 範例（使用本機暫存目錄）：

```powershell
$tempPath = "$env:TEMP\speckit-template-$(Get-Date -Format 'yyyyMMddHHmmss')"
git clone https://github.com/DrDeer119/99.spec-kit-cross-platform-template.git $tempPath
$templatePath = $tempPath
```

> 📁 **後續目錄調整建議**（參考 `docs/00.目錄結構.md`）：
> - 測試目錄：確保 `tests/` 存在且對應 `src/` 結構
> - 日誌目錄：確保 `logs/` 存在，日誌不應散落在專案根目錄
> - 測試產物目錄：建立 `.artifacts/` 存放所有測試產物（coverage、pytest cache、htmlcov 等），並加入 `.gitignore`

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
- `docs/setup-guides/migration-*.md` - 遷移文件（**Step 0 — 最先執行**）
- `docs/setup-guides/migrate-to-full-kit.ps1` - 遷移腳本（**Step 0 — 最先執行**）
- `.flowkit/version-manifest.md` - 指令版號追蹤清單（不存在時建立，已存在時提示比對）
- `.flowkit/memory/` - AI 記憶初始檔案（**完全無檔案時**從範本複製初始版本）

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
    "docs/01.開發人員doc/00.SDD 跨平台開發範本使用指南.md",
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

# 驗證 .flowkit/ 追蹤與記憶
if (Test-Path ".flowkit/version-manifest.md") { "✅ .flowkit/version-manifest.md 存在" } else { "❌ .flowkit/version-manifest.md 未建立" }
$memFiles = @(Get-ChildItem ".flowkit/memory" -File -ErrorAction SilentlyContinue)
if ($memFiles.Count -gt 0) { "✅ .flowkit/memory/ 有 $($memFiles.Count) 個記憶檔案" } else { "❌ .flowkit/memory/ 無檔案（請執行 /flowkit.system-context）" }

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
