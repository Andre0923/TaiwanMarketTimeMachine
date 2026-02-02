# 解決 Spec Kit 環境問題

> **建立日期**: 2025-11-15  
> **問題**: specify check 失敗，PowerShell 版本為 5.1

---

## 🔍 問題診斷

你遇到的問題：

1. ❌ 當前使用 PowerShell **5.1** (不是 7.5)
2. ❌ `specify` 指令找不到
3. ❌ `uv` 指令找不到
4. ❌ 可能 `pwsh` (PowerShell 7) 也找不到

**根本原因**：
- 可能 PowerShell 7.5 還沒安裝
- 或者已安裝但環境變數還沒更新
- 需要重新啟動終端機讓環境變數生效

---

## ✅ 解決步驟

### 步驟 1: 確認並安裝 PowerShell 7.5

在目前的 PowerShell 5.1 中執行：

```powershell
# 使用 Scoop 安裝 PowerShell 7.5
scoop install pwsh

# 檢查是否安裝成功
pwsh --version
```

**如果 scoop 也找不到**，先安裝 Scoop：

```powershell
# 安裝 Scoop
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

---

### 步驟 2: 重新啟動 Windows Terminal

**重要**：關閉所有 Windows Terminal 和 VS Code 視窗，然後重新開啟。

1. 關閉所有終端機視窗
2. 關閉 VS Code
3. 按 `Win+R`，輸入 `wt`，開啟新的 Windows Terminal
4. 或從開始選單啟動 Windows Terminal

---

### 步驟 3: 切換到 PowerShell 7

#### 方法 A: 在 Windows Terminal 中切換

1. 開啟 Windows Terminal
2. 點擊標籤旁的 **下拉箭頭 ▼**
3. 選擇 **PowerShell** (會顯示版本 7.x)

#### 方法 B: 直接啟動 PowerShell 7

```powershell
# 在任何終端機中輸入
pwsh
```

#### 方法 C: 設定 VS Code 預設使用 PowerShell 7

在 VS Code 中：

1. 按 `Ctrl+Shift+P` 開啟命令面板
2. 輸入 `Terminal: Select Default Profile`
3. 選擇 **PowerShell** (7.x 版本)

或手動編輯設定：

1. 按 `Ctrl+,` 開啟設定
2. 搜尋 `terminal.integrated.defaultProfile.windows`
3. 選擇 `PowerShell`

---

### 步驟 4: 驗證 PowerShell 版本

在新的終端機中執行：

```powershell
# 檢查版本
$PSVersionTable.PSVersion

# 應該看到類似這樣：
# Major  Minor  Build  Revision
# -----  -----  -----  --------
# 7      5      x      x
```

---

### 步驟 5: 重新安裝工具（如果需要）

如果 `uv` 和 `specify` 仍然找不到，重新執行安裝：

```powershell
# 1. 確認在 PowerShell 7
$PSVersionTable.PSVersion

# 2. 安裝 Scoop（如果還沒有）
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

# 3. 安裝必要工具
scoop install git uv nodejs ripgrep

# 4. 更新 uv 的 PATH 環境變數
uv tool update-shell

# 5. 安裝 Spec Kit
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 6. 重新啟動檔案總管（讓環境變數生效）
Stop-Process -Name explorer -Force; Start-Process explorer
```

**重要**：執行完後，**必須關閉並重新開啟終端機**。

---

### 步驟 6: 驗證安裝

在新的 PowerShell 7 終端機中執行：

```powershell
# 檢查 PowerShell 版本
$PSVersionTable.PSVersion

# 檢查 uv
uv --version

# 檢查 specify
uv tool list

# 執行 Spec Kit 檢查
specify check
```

你應該看到：
```
✅ Git version control (available)
✅ Visual Studio Code (available)
```

---

## 🎯 快速解決方案（最簡單）

如果上述步驟太複雜，試試這個：

```powershell
# 1. 關閉所有終端機和 VS Code

# 2. 按 Win+R，輸入以下指令開啟新的 PowerShell 7
pwsh

# 3. 如果 pwsh 找不到，先安裝：
winget install Microsoft.PowerShell

# 4. 重新啟動電腦（最保險）
```

---

## 📝 在 VS Code 中的操作步驟

### 1. 確保使用 PowerShell 7

在 VS Code 中：

1. 按 `` Ctrl+` `` 開啟終端機
2. 點擊終端機右上角的 **下拉箭頭**
3. 選擇 **Select Default Profile**
4. 選擇 **PowerShell** (應該會顯示版本)

### 2. 重新載入視窗

按 `Ctrl+Shift+P`，輸入並選擇：
```
Developer: Reload Window
```

### 3. 再次檢查

在新的終端機中：

```powershell
# 確認版本
$PSVersionTable.PSVersion

# 確認工具
uv --version
specify check
```

---

## 🔧 如果 specify 仍然找不到

### 檢查 uv tool 安裝路徑

```powershell
# 查看 uv 工具安裝位置
uv tool dir

# 列出已安裝的工具
uv tool list
```

### 手動加入 PATH

如果工具已安裝但找不到：

```powershell
# 1. 找到 uv tool 的 bin 目錄
uv tool dir

# 2. 手動將它加入 PATH（暫時）
$env:Path += ";C:\Users\你的使用者名稱\.local\bin"

# 3. 測試
specify --version
```

### 永久加入 PATH

```powershell
# 在 PowerShell 7 中執行
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$uvBinPath = Join-Path $env:USERPROFILE ".local\bin"
if ($userPath -notlike "*$uvBinPath*") {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$userPath;$uvBinPath",
        "User"
    )
    Write-Host "已將 uv tool bin 加入 PATH"
}

# 重新啟動終端機
```

---

## ❓ 常見問題

### Q: 為什麼要用 PowerShell 7 而不是 5.1？

**A**: 
- PowerShell 5.1 是 Windows 內建的舊版，有很多限制
- PowerShell 7.5 是跨平台的新版，更穩定、功能更強
- 許多現代開發工具（包括 AI Coding Agent）建議使用 7.x

### Q: 我已經安裝了但還是找不到指令？

**A**: 
1. 確認已重新啟動終端機
2. 確認使用的是 PowerShell 7（不是 5.1）
3. 執行 `uv tool update-shell` 更新 shell 設定
4. 最後手段：重新啟動電腦

### Q: uv tool list 顯示 specify-cli 但執行不了？

**A**:
```powershell
# 重新安裝
uv tool uninstall specify-cli
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 更新 PATH
uv tool update-shell

# 重啟終端機
```

---

## 🎯 檢查清單

完成以下檢查後再繼續：

- [ ] PowerShell 版本是 7.5 或以上（執行 `$PSVersionTable.PSVersion`）
- [ ] `uv --version` 可以執行
- [ ] `uv tool list` 顯示 `specify-cli`
- [ ] `specify check` 可以執行（即使有些項目是紅燈）
- [ ] VS Code 終端機使用 PowerShell 7

---

## 📞 下一步

完成上述步驟後，返回 [如何在VSCode中使用GitHub官方Spec-Kit.md](./如何在VSCode中使用GitHub官方Spec-Kit.md) 繼續進行專案設定。

---

**提示**：如果遇到權限問題，以系統管理員身分執行 PowerShell：
1. 搜尋 "PowerShell"
2. 右鍵點擊 "PowerShell 7"
3. 選擇 "以系統管理員身分執行"

**建立日期**: 2025-11-15  
**更新日期**: 2025-11-15  
**版本**: 1.0.0
