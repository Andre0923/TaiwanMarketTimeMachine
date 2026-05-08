# SpecKit + FlowKit 完整套件遷移指南

> **目標**：將已使用 SpecKit 的舊專案升級到完整的 SpecKit + FlowKit 套件  
> **適用對象**：已有 specs/ 目錄結構的現有專案  
> **難度**：中等  
> **預計時間**：30-60 分鐘

---

## 📋 遷移前檢查清單

在開始遷移前，請確認：

- [ ] 專案已納入 Git 版本控制
- [ ] 已提交所有未保存的變更
- [ ] 已創建新的 Git 分支（建議：`upgrade-to-full-kit`）
- [ ] 備份重要的客製化設定檔案
- [ ] 了解專案目前的 SpecKit 版本與結構

---

## 🎯 遷移策略選擇

### 快速判斷：我該用哪種方案？

| 專案狀況 | 推薦方案 | 說明 |
|----------|----------|------|
| 新專案（< 3 個月） | **方案 A：完全覆蓋** | 快速升級，接受重置 AI 記憶 |
| 有客製化規範 | **方案 C：智能混合** | 保留客製化，選擇性覆蓋 |
| 成熟專案（> 6 個月） | **方案 B：增量遷移** | 最安全，逐項檢查 |
| 不確定 | **方案 C：智能混合** | 平衡速度與安全 |

---

## 🚀 方案 A：完全覆蓋（快速升級）

### 適用情境
- 願意重置 AI 記憶檔案
- 沒有客製化 copilot-instructions.md
- 專案較新，變更不多

### 執行步驟

```powershell
# ⚠️ 重要：請使用「絕對路徑」避免路徑錯誤
# 範例假設：
#   - 範本位置：E:\templates\spec-kit-template
#   - 目標專案：E:\projects\my-old-project

# 1. 準備範本專案（Clone 到絕對路徑）
git clone https://github.com/DrDeer119/99.spec-kit-cross-platform-template.git E:\templates\spec-kit-template

# 2. 設定路徑變數
$templatePath = "E:\templates\spec-kit-template"
$targetPath = "E:\projects\my-old-project"

# 3. 確認遷移腳本存在
Test-Path "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1"  # 應回傳 True

# 3.5 先行同步遷移工具（腳本 Step 0 會自動完成）
# 腳本執行的第一步會從範本同步以下檔案到目標專案，
# 確保目標專案日後升級時可使用最新版本的遷移文件與腳本：
# - docs/setup-guides/migration-guide.md
# - docs/setup-guides/migration-quick-ref.md
# - docs/setup-guides/migrate-to-full-kit.ps1

# 4. 執行自動遷移（Dry Run）
& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath `
    -DryRun

# 5. 檢查 Dry Run 輸出後，實際執行
& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath `
    -Force

# 6. 手動補充範本檔案（腳本已自動複製，但建議確認）
cd $targetPath
# 確認需求文件範本已複製
Test-Path "docs\requirements\Milestone\MNN-MilestoneName-template.md"
Test-Path "docs\requirements\user-stories\US-X-GroupName-template.md"

# 7. ⚗️ 智慧處理 Technical Debt Registry
if (-not (Test-Path "docs\technical-debt.md")) {
    Copy-Item -Path "$templatePath\docs\technical-debt.md" -Destination "docs\" -Force
    Write-Host "✅ 已建立 technical-debt.md"
}

# 8. AI 記憶處理（條件式）
# 僅當 system-context 不存在時才需建立（遷移不會改變專案結構，已有的上下文仍然有效）
# 若不存在，在 Copilot Chat 或 Cursor 中執行：
# /flowkit.system-context

# 9. 檢查變更並提交
git status
git diff

# 10. 版號清單驗證（遷移完成後 SHOULD 比對）
code --diff "$templatePath\.flowkit\version-manifest.md" ".\.flowkit\version-manifest.md"
# 若版號清單一致，代表指令化檔案同步完整

git add .
git commit -m "chore: 升級至完整 SpecKit + FlowKit 套件"
```

> ⚠️ **路徑問題排查**：若執行遷移腳本時出現「找不到路徑」錯誤，請：
> 1. 確認 Clone 時使用的是絕對路徑（不要使用 `temp-template` 等相對路徑）
> 2. 使用 `Test-Path` 確認腳本路徑存在
> 3. 使用 `& "$path\script.ps1"` 調用（而非 `cd` 後 `.\ script.ps1`）

### 風險與注意事項
- ⚠️ AI 記憶檔案會被重置（需執行 `/flowkit.system-context` 重建）
- ⚠️ 客製化的 copilot-instructions.md 會被覆蓋
- ✅ 所有變更都有備份（`.migration-backup-*` 目錄）

---

## 🛠️ 方案 B：升級現有專案（Scenario B）

### 適用情境
- 已有使用 SpecKit 的專案
- 希望直接升級到完整套件（以遷移腳本自動處理）
- 需明確避開相對路徑造成的錯誤

### 執行步驟

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

### ⚠️ 路徑問題排查

若執行遷移腳本時出現「找不到路徑」錯誤，請：

1. 確認 Clone 時使用的絕對路徑
2. 使用 `Test-Path` 確認腳本路徑存在
3. 避免使用相對路徑（如 `..\temp-template`）

### 💡 Dropbox / 雲端同步環境注意事項

- 若遇到「檔案被占用」錯誤，腳本會自動重試（最多 3 次，每次間隔 2 秒）
- 建議將範本 Clone 到非同步目錄（如 `$env:TEMP`）以避免檔案占用問題
- 若重試仍失敗，請暫時暫停雲端同步服務後重新執行

範例（使用本機暫存目錄）：

```powershell
$tempPath = "$env:TEMP\speckit-template-$(Get-Date -Format 'yyyyMMddHHmmss')"
git clone https://github.com/DrDeer119/99.spec-kit-cross-platform-template.git $tempPath
$templatePath = $tempPath
```

### 📁 後續目錄調整建議

遷移完成後，請參考 `docs/00.目錄結構.md` 調整專案目錄結構，特別是：

- 測試目錄：確保 `tests/` 存在且對應 `src/` 結構
- 日誌目錄：確保 `logs/` 存在，日誌不應散落在專案根目錄
- 測試產物目錄：建立 `.artifacts/` 存放所有測試產物（coverage、pytest cache、htmlcov 等），並加入 `.gitignore`

### 參考文件

- 遷移指南：`docs/setup-guides/migration-guide.md`
- 快速參考：`docs/setup-guides/migration-quick-ref.md`

---

## 🎨 方案 C：智能混合（推薦）

### 適用情境
- 大多數情況（平衡速度與安全）
- 有少量客製化
- 想要自動化但保留控制

> ⚠️ **重要警告 - AI 常見誤判**：
> 1. **constitution.md 簡化版陷阱**：範本中的 `constitution.md` 是**刻意製造的精簡優化版**。AI 看到舊專案的版本較長，常誤以為自己的是「完整版」而拒絕更新。**請務必使用範本版本**。(除非你確定舊版有必要的客製化規則，或者使用者明確表示不更新，否則請全部覆蓋)
> 2. **FlowKit 指令化容易被忽略**：AI 有時只願意更新 SpecKit，忽略 FlowKit。請明確要求更新 `.cursor/commands/flowkit.*` 和 `.github/agents/flowkit.*`。

### 執行步驟

```powershell
# ⚠️ 重要：請使用「絕對路徑」避免路徑錯誤

# 1. 準備範本（Clone 到絕對路徑）
git clone https://github.com/DrDeer119/99.spec-kit-cross-platform-template.git E:\templates\spec-kit-template

# 2. 設定路徑變數
$templatePath = "E:\templates\spec-kit-template"
$targetPath = "E:\projects\my-old-project"

# 2.5 要點：腳本第一步（Step 0）會自動同步遷移工具
# 執行後目標專案的 docs/setup-guides/ 將更新為最新版本，
# 包含：migration-guide.md、migration-quick-ref.md、migrate-to-full-kit.ps1

# 3. Dry Run（檢查會做什麼）
& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath `
    -DryRun

# 4. 實際執行（自動處理 Tier 1-2）
& "$templatePath\docs\setup-guides\migrate-to-full-kit.ps1" `
    -TemplatePath $templatePath `
    -TargetPath $targetPath

# 5. 手動處理 copilot-instructions.md（若有客製化）
cd $targetPath
code --diff .github/copilot-instructions.md .migration-backup-*/.github/copilot-instructions.md

# 6. 🔴 強制更新 constitution.md（範本版是優化簡化版）
# ⚠️ 範本中的 constitution.md 是「刻意製造的簡化版」
# 舊版本較長不代表較完整，請使用範本版本並手動補回客製化規則
Copy-Item -Path "$templatePath\.specify\memory\constitution.md" -Destination ".specify\memory\" -Force
# 然後手動補回客製化規則（若有）

# 7. ⚗️ 手動比對目錄結構文件（每個專案結構不同）
code --diff "$templatePath\docs\00.目錄結構.md" "docs\00.目錄結構.md"

# 8. ⚗️ 智慧處理 Technical Debt Registry
if (-not (Test-Path "docs\technical-debt.md")) {
    Copy-Item -Path "$templatePath\docs\technical-debt.md" -Destination "docs\" -Force
    Write-Host "✅ 已建立 technical-debt.md"
} else {
    Write-Host "ℹ️ technical-debt.md 已存在，建議手動比對範本是否有新欄位或規則"
    code --diff "$templatePath\docs\technical-debt.md" "docs\technical-debt.md"
}

# 9. 確認範本檔案已複製
@(
    "docs/requirements/Milestone/MNN-MilestoneName-template.md",
    "docs/requirements/user-stories/US-X-GroupName-template.md",
    "docs/01.開發人員doc/00.SDD 跨平台開發範本使用指南.md"
) | ForEach-Object {
    if (Test-Path $_) { Write-Host "✅ $_" } else { Write-Host "❌ $_ 未複製" }
}

# 10. AI 記憶處理（條件式）
# 僅當 system-context 不存在時才需建立（遷移不會改變專案結構）
if (-not (Test-Path ".flowkit/memory/system-context.md")) {
    # 在 Copilot Chat 或 Cursor 中執行：/flowkit.system-context
    Write-Host "⚠️ 尚未建立 system-context，請在 IDE 中執行 /flowkit.system-context"
} else {
    Write-Host "✅ system-context 已存在，無需重建"
}

# 11. 驗證 FlowKit 指令化已更新
@(".cursor/commands/flowkit.system-context.md", ".github/agents/flowkit.system-context.agent.md") | ForEach-Object {
    if (Test-Path $_) { Write-Host "✅ $_" } else { Write-Host "❌ $_ 未更新" }
}

# 12. 檢查並提交
git status
git diff
git add .
git commit -m "chore: 升級至完整 SpecKit + FlowKit 套件"
```

> ⚠️ **路徑問題排查**：若執行遷移腳本時出現「找不到路徑」錯誤，請：
> 1. 確認 Clone 時使用的是絕對路徑（不要使用 `temp-template` 等相對路徑）
> 2. 使用 `Test-Path` 確認腳本路徑存在
> 3. 使用 `& "$path\script.ps1"` 調用（而非 `cd` 後 `.\ script.ps1`）

---

## 📁 檔案分類參考

### 🟢 Tier 1：直接覆蓋（無風險，標準化）

```
.specify/scripts/            ← SpecKit 自動化腳本
.specify/templates/          ← Spec/Plan/Tasks 範本
.flowkit/templates/          ← FlowKit 輸出範本
.cursor/commands/            ← Cursor 指令
.github/agents/              ← GitHub Copilot Agents
.github/prompts/             ← GitHub Copilot Prompts
```

**特性**：
- 標準化內容，無需客製化
- 直接覆蓋即可
- 備份後可放心更新

---

### � Tier 1.5：範本檔案與開發文件（自動複製）

```
docs/requirements/PRD-Template.md                           ← PRD 範本
docs/requirements/Milestone/MNN-MilestoneName-template.md   ← Milestone 範本
docs/requirements/user-stories/README-template.md           ← User Stories README 範本
docs/requirements/user-stories/US-X-GroupName-template.md   ← User Stories 範本
docs/01.開發人員doc/*                                        ← 開發人員文件
docs/setup-guides/migration-guide.md                        ← 完整遷移指南
docs/setup-guides/migration-quick-ref.md                    ← 遷移快速參考
docs/setup-guides/migrate-to-full-kit.ps1                   ← 遷移腳本
```

**特性**：
- 範本檔案，協助新功能開發
- 不會覆蓋專案已有的需求文件
- 開發人員指南文件
- 遷移文件，作為未來升級參考

---

### �🟡 Tier 2：選擇性覆蓋（需檢查）

```
docs/00.目錄結構.md          ← ⚗️ 智慧比對（每個專案結構不同，手動合併）
docs/77.flowkit相關文件/     ← FlowKit 功能說明（直接覆蓋）
docs/76.改版歷史/            ← 套件改版歷史（直接覆蓋）
docs/technical-debt.md       ← ⚗️ 智慧判斷（不存在→建立；已存在→比對合併）
.github/copilot-instructions.md  ← 全域 AI 規範（可能有客製化）
```

**檢查方式**：
```powershell
# 比對舊版與新版
code --diff old-file.md new-file.md

# 若有客製化內容，手動合併
```

**`docs/00.目錄結構.md` 特殊處理**：
- 每個專案的目錄結構可能不同（自訂資料夾、特殊模組等）
- MUST 手動比對，確認範本中的標準目錄規範已涵蓋
- 保留專案特有的目錄說明

**`docs/technical-debt.md` 特殊處理**：
- 不存在 → 直接複製範本版本
- 已存在 → 手動比對範本是否有新欄位（如 Dedup-Key、老化規則等），合併新規則但保留既有 TD 項目

---

### 🔴 Tier 3：條件式處理（專案特定）

```
.flowkit/memory/system-context.md       ← 僅當不存在時建立（遷移不改變專案結構）
.flowkit/memory/system-context-index.md ← 隨 system-context 一起建立
.specify/memory/constitution.md         ← 憲法（🔴 MUST 使用範本版本）
```

> ⚠️ **constitution.md 重要說明**：
> - 範本中的版本是**刻意製造的精簡優化版**，經過多次迭代去除冗餘內容
> - 舊專案的版本可能較長，但**較長不代表較完整**
> - AI 常因舊版本較長而誤判，拒絕更新。請**強制使用範本版本**
> - 更新後再手動補回專案特定的客製化規則（如有）

**處理方式**：
1. 備份舊版
2. **強制使用範本版本**（不要因為舊版較長就保留）
3. 手動補回客製化規則（若有）
4. 若 `system-context.md` 不存在，執行 `/flowkit.system-context` 建立（已存在則無需重建）

---

### ⚫ Tier 4：絕不覆蓋（專案核心）

```
specs/                  ← 專案規格（絕不覆蓋）
src/                    ← 程式碼（絕不覆蓋）
tests/                  ← 測試（絕不覆蓋）
docs/requirements/      ← 專案需求（絕不覆蓋）
pyproject.toml          ← 專案設定（絕不覆蓋）
```

> ⚠️ `docs/technical-debt.md` 已移至 Tier 2 智慧處理：不存在時建立，已存在時比對合併。

---

## ✅ 遷移後檢查清單

完成遷移後，逐項檢查：

### 基礎檢查
- [ ] `.specify/scripts/` 已更新
- [ ] `.specify/templates/` 已更新
- [ ] `.flowkit/templates/` 已建立
- [ ] `.flowkit/version-manifest.md` 已建立（或已確認比對版號）
- [ ] `.flowkit/memory/` 已確認（無檔案時已從範本複製初始記憶）
- [ ] `.cursor/commands/` 已更新（若使用 Cursor）
- [ ] `.github/agents/` 已更新（若使用 GitHub Copilot）

### 文件檢查
- [ ] `docs/00.目錄結構.md` 已更新
- [ ] `docs/77.flowkit相關文件/` 已建立
- [ ] `docs/76.改版歷史/` 已建立
- [ ] `docs/01.開發人員doc/` 已複製

### 範本檔案檢查
- [ ] `docs/requirements/PRD-Template.md` 已複製
- [ ] `docs/requirements/Milestone/MNN-MilestoneName-template.md` 已複製
- [ ] `docs/requirements/user-stories/README-template.md` 已複製
- [ ] `docs/requirements/user-stories/US-X-GroupName-template.md` 已複製
- [ ] `docs/setup-guides/migration-guide.md` 已複製（未來升級參考）
- [ ] `docs/setup-guides/migration-quick-ref.md` 已複製（未來升級參考）
- [ ] `docs/setup-guides/migrate-to-full-kit.ps1` 已複製（未來升級參考）

### 規範檢查
- [ ] `.github/copilot-instructions.md` 客製化已合併
- [ ] `.specify/memory/constitution.md` 客製化規則已保留

### AI 記憶檢查
- [ ] 若 `system-context.md` 原本不存在，已執行 `/flowkit.system-context` 建立
- [ ] 若 `system-context.md` 已存在，確認未被意外刪除
- [ ] 測試 `/flowkit.system-context` 指令正常運作

### 功能驗證
- [ ] 執行 `/speckit.specify "Test feature"` 測試建立 Feature
- [ ] 執行 `/speckit.plan` 測試規劃功能
- [ ] 執行 `/flowkit.system-context` 測試上下文生成
- [ ] 測試其他常用 FlowKit 指令

### Git 檢查
- [ ] `git status` 確認所有變更已暫存
- [ ] `git diff` 檢查變更內容合理
- [ ] 提交變更並推送

### 📁 目錄結構調整建議（參考 `docs/00.目錄結構.md`）
- [ ] **測試目錄**：確保 `tests/` 存在且對應 `src/` 結構
- [ ] **日誌目錄**：確保 `logs/` 存在，日誌不應散落在專案根目錄
- [ ] **產物目錄**：建立 `.artifacts/` 存放 coverage、build 等可再生產物
- [ ] **Git 忽略**：將 `.artifacts/` 加入 `.gitignore`

---

## 🔧 常見問題

### Q1: 遷移後 `/speckit.specify` 無法執行？

**可能原因**：
- `.specify/scripts/` 未正確複製
- PowerShell 執行政策限制

**解決方式**：
```powershell
# 檢查腳本是否存在
Test-Path .specify/scripts/powershell/create-new-feature.ps1

# 設定執行政策
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Q2: `/flowkit.system-context` 生成的內容不正確？

**可能原因**：
- `specs/system/` 內容不完整
- Feature history 未整理

**解決方式**：
1. 確認 `specs/system/spec.md` 存在且完整
2. 檢查 `specs/history/` 是否有遺留的舊 Feature
3. 手動編輯 `.flowkit/memory/system-context.md`

---

### Q3: 遷移後發現遺漏了客製化內容？

**解決方式**：
```powershell
# 檢查備份
ls .migration-backup-*

# 比對備份與現有檔案
code --diff .migration-backup-*/path/to/file current/path/to/file

# 手動恢復需要的部分
```

---

### Q4: 如何回滾遷移？

**方式 1：使用 Git**
```powershell
git reset --hard HEAD
git clean -fd
```

**方式 2：使用備份**
```powershell
# 找到備份目錄
$backup = Get-ChildItem -Directory ".migration-backup-*" | Select-Object -First 1

# 恢復特定檔案
Copy-Item -Path "$backup\.github\copilot-instructions.md" -Destination ".github\" -Force
```

---

### Q5: 遷移後如何驗證完整性？

**執行完整性檢查**：
```powershell
# 檢查關鍵目錄
@(
    ".specify/scripts",
    ".specify/templates",
    ".flowkit/templates",
    ".github/agents",
    ".cursor/commands"
) | ForEach-Object {
    if (Test-Path $_) {
        Write-Host "✅ $_"
    } else {
        Write-Host "❌ $_ 不存在"
    }
}

# 檢查關鍵檔案
@(
    ".github/copilot-instructions.md",
    ".specify/memory/constitution.md",
    "docs/00.目錄結構.md"
) | ForEach-Object {
    if (Test-Path $_) {
        Write-Host "✅ $_"
    } else {
        Write-Host "❌ $_ 不存在"
    }
}
```

---

## 📚 延伸閱讀

- [SpecKit 開發流程指南](../01.開發人員doc/03.SDD開發流程指南.md)
- [FlowKit 功能說明總覽](../77.flowkit相關文件/README.md)
- [目錄結構規範](../00.目錄結構.md)
- [Copilot Instructions 說明](.github/copilot-instructions.md)

---

## 🆘 需要協助？

如果遇到問題：

1. **檢查日誌**：查看終端機輸出的錯誤訊息
2. **查看備份**：所有被覆蓋的檔案都有備份
3. **Git 回滾**：可以隨時 `git reset --hard` 回到遷移前
4. **提 Issue**：到 GitHub repo 提出問題

---

**版本**：v1.2.0  
**最後更新**：2026-02-26
