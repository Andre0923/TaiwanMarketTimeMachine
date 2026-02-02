# 🚀 SpecKit + FlowKit 遷移快速參考

> **5 分鐘快速決策指南**

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
# 1. Clone 範本
git clone https://github.com/DrDeer119/99.my-speckit_template.git temp-template

# 2. 執行遷移
cd temp-template
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\your-project"

# 3. 重建 AI 記憶
cd E:\path\to\your-project
# 在 Copilot Chat 執行：
/flowkit.system-context
```

---

## 📦 遷移涵蓋內容

### ✅ 會自動處理
- `.specify/scripts/` - SpecKit 腳本
- `.specify/templates/` - Spec/Plan/Tasks 範本
- `.flowkit/templates/` - FlowKit 範本
- `.cursor/commands/` - Cursor 指令
- `.github/agents/` - GitHub Copilot Agents
- `.github/prompts/` - GitHub Copilot Prompts
- `docs/00.目錄結構.md` - 目錄規範
- `docs/77.flowkit相關文件/` - FlowKit 文件
- `docs/76.改版歷史/` - 改版歷史

### ⚠️ 需手動檢查
- `.github/copilot-instructions.md` - 若有客製化
- `.specify/memory/constitution.md` - 若有客製化規則

### 🔄 需要重建
- `.flowkit/memory/system-context.md` - 執行 `/flowkit.system-context`

### 🚫 絕不覆蓋
- `specs/` - 專案規格
- `src/` - 程式碼
- `tests/` - 測試
- `docs/requirements/` - 需求文件

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
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\project" `
    -DryRun
```

### 完全覆蓋（包含 copilot-instructions.md）
```powershell
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\project" `
    -Force
```

### 不備份（不建議）
```powershell
.\docs\setup-guides\migrate-to-full-kit.ps1 `
    -TemplatePath "." `
    -TargetPath "E:\path\to\project" `
    -SkipBackup
```

---

## 📋 遷移後檢查

```powershell
# 驗證關鍵目錄
@(".specify/scripts", ".flowkit/templates", ".github/agents") | 
    ForEach-Object { 
        if (Test-Path $_) { "✅ $_" } else { "❌ $_ 不存在" } 
    }

# 測試功能
/speckit.specify "Test feature"
/flowkit.system-context
```

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

**快速開始**：`.\docs\setup-guides\migrate-to-full-kit.ps1 -DryRun`
