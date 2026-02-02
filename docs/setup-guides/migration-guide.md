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
# 1. 準備範本專案
git clone https://github.com/DrDeer119/99.my-speckit_template.git speckit-template
cd speckit-template

# 2. 執行自動遷移（Dry Run）
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\your\old-project" `
    -DryRun

# 3. 檢查 Dry Run 輸出後，實際執行
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\your\old-project" `
    -Force

# 4. 切換到目標專案
cd E:\path\to\your\old-project

# 5. 重建 AI 記憶
# （在 Copilot Chat 或 Cursor 中執行）
/flowkit.system-context

# 6. 檢查變更並提交
git status
git diff
git add .
git commit -m "chore: 升級至完整 SpecKit + FlowKit 套件"
```

### 風險與注意事項
- ⚠️ AI 記憶檔案會被重置（需執行 `/flowkit.system-context` 重建）
- ⚠️ 客製化的 copilot-instructions.md 會被覆蓋
- ✅ 所有變更都有備份（`.migration-backup-*` 目錄）

---

## 🛠️ 方案 B：增量遷移（最安全）

### 適用情境
- 成熟專案，有大量客製化
- 需要完全掌控每個變更
- 時間充裕

### 執行步驟

#### Phase 1: 核心工具遷移

```powershell
cd speckit-template

# 1. 複製 SpecKit 腳本
Copy-Item -Path ".specify/scripts" -Destination "E:\path\to\old-project\.specify\" -Recurse -Force

# 2. 複製 SpecKit 範本
Copy-Item -Path ".specify/templates" -Destination "E:\path\to\old-project\.specify\" -Recurse -Force

# 3. 複製 FlowKit 範本
New-Item -ItemType Directory -Path "E:\path\to\old-project\.flowkit" -Force
Copy-Item -Path ".flowkit/templates" -Destination "E:\path\to\old-project\.flowkit\" -Recurse -Force
```

#### Phase 2: 指令化檔案遷移

```powershell
# 4. GitHub Copilot Agents
Copy-Item -Path ".github/agents" -Destination "E:\path\to\old-project\.github\" -Recurse -Force
Copy-Item -Path ".github/prompts" -Destination "E:\path\to\old-project\.github\" -Recurse -Force

# 5. Cursor Commands
Copy-Item -Path ".cursor/commands" -Destination "E:\path\to\old-project\.cursor\" -Recurse -Force
```

#### Phase 3: 文件遷移

```powershell
# 6. 標準化文件
Copy-Item -Path "docs/00.目錄結構.md" -Destination "E:\path\to\old-project\docs\" -Force
Copy-Item -Path "docs/77.flowkit相關文件" -Destination "E:\path\to\old-project\docs\" -Recurse -Force
Copy-Item -Path "docs/76.改版歷史" -Destination "E:\path\to\old-project\docs\" -Recurse -Force
```

#### Phase 4: 規範檔案處理

```powershell
# 7. copilot-instructions.md（需手動比對）
code --diff .github/copilot-instructions.md E:\path\to\old-project\.github\copilot-instructions.md

# 8. constitution.md（需手動比對）
code --diff .specify/memory/constitution.md E:\path\to\old-project\.specify\memory\constitution.md
```

#### Phase 5: AI 記憶重建

```powershell
cd E:\path\to\old-project

# 9. 刪除舊的 AI 記憶（備份後）
if (Test-Path ".flowkit/memory") {
    Copy-Item -Path ".flowkit/memory" -Destination ".migration-backup/flowkit-memory" -Recurse
    Remove-Item -Path ".flowkit/memory" -Recurse -Force
}

# 10. 執行重建
# 在 Copilot Chat 或 Cursor 中執行
/flowkit.system-context
```

---

## 🎨 方案 C：智能混合（推薦）

### 適用情境
- 大多數情況（平衡速度與安全）
- 有少量客製化
- 想要自動化但保留控制

### 執行步驟

```powershell
# 1. 準備範本
git clone https://github.com/DrDeer119/99.my-speckit_template.git speckit-template
cd speckit-template

# 2. Dry Run（檢查會做什麼）
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\your\old-project" `
    -DryRun

# 3. 實際執行（自動處理 Tier 1-2）
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\your\old-project"

# 4. 手動處理 copilot-instructions.md（若有客製化）
cd E:\path\to\your\old-project
code --diff .github/copilot-instructions.md .migration-backup-*/. github/copilot-instructions.md

# 5. 手動處理 constitution.md（若有客製化規則）
code --diff .specify/memory/constitution.md .migration-backup-*/.specify/memory/constitution.md

# 6. 重建 AI 記憶
/flowkit.system-context

# 7. 檢查並提交
git status
git diff
git add .
git commit -m "chore: 升級至完整 SpecKit + FlowKit 套件"
```

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

### 🟡 Tier 2：選擇性覆蓋（需檢查）

```
docs/00.目錄結構.md          ← 標準目錄結構定義
docs/77.flowkit相關文件/     ← FlowKit 功能說明
docs/76.改版歷史/            ← 套件改版歷史
.github/copilot-instructions.md  ← 全域 AI 規範（可能有客製化）
```

**檢查方式**：
```powershell
# 比對舊版與新版
code --diff old-file.md new-file.md

# 若有客製化內容，手動合併
```

---

### 🔴 Tier 3：需要重建（專案特定）

```
.flowkit/memory/system-context.md       ← 專案上下文（需重建）
.flowkit/memory/system-context-index.md ← 上下文索引（需重建）
.specify/memory/constitution.md         ← 憲法（需合併客製化規則）
```

**處理方式**：
1. 備份舊版
2. 刪除或覆蓋
3. 執行 `/flowkit.system-context` 重建 AI 記憶
4. 若 constitution.md 有客製化，手動合併

---

### ⚫ Tier 4：絕不覆蓋（專案核心）

```
specs/                  ← 專案規格（絕不覆蓋）
src/                    ← 程式碼（絕不覆蓋）
tests/                  ← 測試（絕不覆蓋）
docs/requirements/      ← 專案需求（絕不覆蓋）
docs/technical-debt.md  ← 技術債（絕不覆蓋）
pyproject.toml          ← 專案設定（絕不覆蓋）
```

---

## ✅ 遷移後檢查清單

完成遷移後，逐項檢查：

### 基礎檢查
- [ ] `.specify/scripts/` 已更新
- [ ] `.specify/templates/` 已更新
- [ ] `.flowkit/templates/` 已建立
- [ ] `.cursor/commands/` 已更新（若使用 Cursor）
- [ ] `.github/agents/` 已更新（若使用 GitHub Copilot）

### 文件檢查
- [ ] `docs/00.目錄結構.md` 已更新
- [ ] `docs/77.flowkit相關文件/` 已建立
- [ ] `docs/76.改版歷史/` 已建立

### 規範檢查
- [ ] `.github/copilot-instructions.md` 客製化已合併
- [ ] `.specify/memory/constitution.md` 客製化規則已保留

### AI 記憶檢查
- [ ] `.flowkit/memory/system-context.md` 已重建
- [ ] `.flowkit/memory/system-context-index.md` 已重建
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

**版本**：v1.0.0  
**最後更新**：2026-01-29
