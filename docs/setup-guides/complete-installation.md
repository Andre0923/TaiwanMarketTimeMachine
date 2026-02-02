# Spec Kit 完整安裝與設定指南

## 概述

本指南彙整了在 Windows 環境中從零開始設定 GitHub Spec Kit 開發環境的完整步驟。

## 環境需求

- Windows 10/11
- PowerShell 7.5+
- Python 3.13+
- Git
- VS Code with GitHub Copilot

## 一、PowerShell 7 安裝與設定

### 1. 安裝 PowerShell 7

```powershell
# 使用 Scoop 安裝（推薦）
scoop install pwsh

# 或使用 winget
winget install Microsoft.PowerShell
```

### 2. 在 VS Code 中設定 PowerShell 7

**方法一：透過設定 JSON**

1. 按 `Ctrl+Shift+P` → 輸入 "Preferences: Open User Settings (JSON)"
2. 加入以下設定：

```json
{
  "terminal.integrated.defaultProfile.windows": "PowerShell 7",
  "terminal.integrated.profiles.windows": {
    "PowerShell 7": {
      "path": "C:\\Users\\<您的用戶名>\\scoop\\apps\\pwsh\\current\\pwsh.exe",
      "args": ["-NoLogo"]
    }
  }
}
```

**方法二：透過 UI 設定**

1. `Ctrl+Shift+P` → "Terminal: Select Default Profile"
2. 選擇 "PowerShell 7"

### 3. 驗證 PowerShell 版本

```powershell
$PSVersionTable.PSVersion
# 預期輸出: 7.5.4 或更高版本
```

## 二、安裝開發工具

### 1. 安裝 Scoop（如果尚未安裝）

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

### 2. 安裝 uv（Python 套件管理工具）

```powershell
# 使用 PowerShell 安裝腳本
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 驗證安裝
uv --version
# 預期輸出: uv 0.9.9 或更高版本
```

### 3. 安裝 Python 3.13

```powershell
# 使用 uv 安裝
uv python install 3.13

# 驗證安裝
uv python list
```

## 三、安裝 GitHub Spec Kit

### 1. 安裝 specify-cli

```powershell
# 從 GitHub 安裝最新版本
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 驗證安裝
uv tool list
specify --version
```

### 2. 驗證 Spec Kit 環境

```powershell
specify check
```

預期輸出應包含：
- ✓ Git
- ✓ Claude Code（如果使用 Claude Desktop）
- ✓ VS Code
- ✓ GitHub Copilot（如果在 VS Code 中使用）

## 四、初始化 Spec Kit 專案

### 1. 建立或進入專案目錄

```powershell
cd "您的專案路徑"
```

### 2. 初始化 Spec Kit

```powershell
# 使用 GitHub Copilot（VS Code 中）
specify init --here --ai copilot --force

# 或使用 Claude Desktop
specify init --here --ai claude --force
```

### 3. 驗證初始化結果

檢查是否已建立以下目錄：
- `.specify/` - Spec Kit 設定與記憶
- `.github/` - GitHub Agents 與提示詞

## 五、建立 Python 虛擬環境

### 1. 使用 uv 建立虛擬環境

```powershell
uv venv
```

### 2. 啟用虛擬環境

```powershell
.venv\Scripts\Activate.ps1
```

### 3. 安裝專案依賴

```powershell
uv pip install -r requirements.txt
```

## 六、設定專案憲章

### 1. 編輯 constitution.md

```powershell
code .specify/memory/constitution.md
```

### 2. 根據團隊需求調整憲章內容

參考 `docs/Spec kit 憲章_Claude.md` 或使用 `templates/constitution-template.md`

## 七、開始使用 Spec Kit

### 1. 建立第一個 Specification

在 GitHub Copilot Chat 中：

```
@github /new-specification 建立一個移動平均計算模組
```

### 2. 讓 AI 實作規格

```
請根據 specification 實作程式碼
```

### 3. 執行測試

```powershell
pytest tests/ -v
```

## 常見問題排除

### Q1: VS Code 終端機找不到 specify 命令

**解決方案：**
1. 確認已使用 PowerShell 7（不是 Windows PowerShell 5.1）
2. 重新啟動 VS Code
3. 手動重新載入環境變數：`. $PROFILE`

### Q2: uv 安裝後找不到命令

**解決方案：**
1. 確認 PATH 環境變數包含 `%USERPROFILE%\.local\bin`
2. 重新啟動終端機或 VS Code
3. 檢查安裝路徑：`$env:PATH -split ';' | Select-String local`

### Q3: specify init 失敗

**解決方案：**
1. 確認已安裝 Git
2. 確認網路連線正常（需下載模板）
3. 使用 `--force` 參數覆蓋現有檔案
4. 檢查是否有權限問題

### Q4: Python 版本錯誤

**解決方案：**
```powershell
# 檢查所有已安裝的 Python 版本
uv python list

# 安裝特定版本
uv python install 3.13

# 在專案中指定版本
uv venv --python 3.13
```

## 驗證清單

安裝完成後，確認以下項目：

- [ ] PowerShell 版本 >= 7.5
- [ ] uv 版本 >= 0.9.9
- [ ] Python 版本 >= 3.13
- [ ] specify-cli 已安裝
- [ ] `specify check` 所有項目通過
- [ ] 專案已初始化（存在 .specify/ 目錄）
- [ ] 虛擬環境已建立並啟用
- [ ] 憲章已設定完成

## 參考文件

- [GitHub Spec Kit 官方文件](https://github.com/github/spec-kit)
- [uv 官方文件](https://docs.astral.sh/uv/)
- [PowerShell 7 文件](https://learn.microsoft.com/powershell/)
- 專案內部文件：
  - `docs/setup-guides/切換到PowerShell7的步驟.md`
  - `docs/setup-guides/如何在VSCode中使用GitHub官方Spec-Kit.md`
  - `docs/setup-guides/解決Spec-Kit環境問題.md`

## 下一步

1. 閱讀 `README.md` 了解專案結構
2. 查看 `templates/` 中的範例程式碼
3. 研究 `.specify/memory/constitution.md` 了解開發原則
4. 開始使用 Spec Kit 進行 AI 驅動開發！
