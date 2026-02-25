# 如何在 VS Code 中切換到 PowerShell 7.5

## 🎯 你的狀況

✅ PowerShell 7.5.4 已安裝在：`C:\Program Files\PowerShell\7\pwsh.exe`  
❌ VS Code 終端機仍使用 Windows PowerShell 5.1

---

## 🔧 解決方案（請依序執行）

### 步驟 1: 完全重新啟動 VS Code

**重要**：這是最常見的解決方法！

1. **完全關閉 VS Code**（不是只關閉視窗，要真的退出）
   - 在工作列右下角找到 VS Code 圖示
   - 右鍵 → 結束
   
2. **重新開啟 VS Code**

3. **開啟專案資料夾**：
   ```
   C:\Projects\your-project-name
   ```

---

### 步驟 2: 設定預設終端機設定檔

重新啟動 VS Code 後：

1. **按下 `Ctrl+Shift+P`** 開啟命令面板

2. **輸入**：`Terminal: Select Default Profile`

3. **你應該會看到這些選項**：
   ```
   PowerShell                    ← 選這個（PowerShell 7.5）
   Windows PowerShell           ← 不要選這個（舊版 5.1）
   Command Prompt
   Git Bash
   ```

4. **選擇 `PowerShell`**（注意：不是 Windows PowerShell）

---

### 步驟 3: 關閉所有舊的終端機

在 VS Code 中：

1. 找到終端機面板右上角的垃圾桶圖示
2. 點擊刪除所有舊的終端機實例
3. **按 `` Ctrl+` ``** 開啟新的終端機

---

### 步驟 4: 驗證 PowerShell 版本

在新終端機中執行：

```powershell
$PSVersionTable.PSVersion
```

你應該看到：
```
Major  Minor  Build  Revision
-----  -----  -----  --------
7      5      4      0
```

**如果還是看到 5.1**，請繼續下一步。

---

## 🛠️ 方案 2：手動編輯 VS Code 設定檔

如果上述方法無效，手動設定：

### 選項 A: 透過 UI 設定（推薦）

1. **按 `Ctrl+,`** 開啟設定
2. **搜尋**：`terminal.integrated.defaultProfile.windows`
3. **選擇下拉選單**：選擇 `PowerShell`

### 選項 B: 直接編輯 settings.json

1. **按 `Ctrl+Shift+P`**
2. **輸入**：`Preferences: Open User Settings (JSON)`
3. **加入以下設定**：

```json
{
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.profiles.windows": {
    "PowerShell": {
      "source": "PowerShell",
      "icon": "terminal-powershell"
    }
  }
}
```

4. **儲存檔案** (`Ctrl+S`)
5. **重新啟動 VS Code**

---

## 🚀 方案 3：臨時使用 PowerShell 7（不需要重啟）

如果你急著要用，可以在目前的終端機中：

```powershell
# 直接啟動 PowerShell 7
& "C:\Program Files\PowerShell\7\pwsh.exe"
```

執行後，你會看到 PowerShell 7 的提示符號。

驗證版本：
```powershell
$PSVersionTable.PSVersion
```

---

## ✅ 驗證成功

切換成功後，執行以下指令確認環境：

```powershell
# 1. 檢查 PowerShell 版本
$PSVersionTable.PSVersion

# 2. 檢查 uv 是否可用
uv --version

# 3. 檢查 Spec Kit
specify check
```

全部成功後，你就可以開始使用了！

---

## 🔍 為什麼需要 PowerShell 7？

| 功能 | Windows PowerShell 5.1 | PowerShell 7.5 |
|------|------------------------|----------------|
| 跨平台 | ❌ 僅 Windows | ✅ Windows/Mac/Linux |
| 效能 | 普通 | ⚡ 更快 |
| 新功能 | ❌ 停止更新 | ✅ 持續更新 |
| 相容性 | 舊工具 | ✅ 新舊工具都支援 |
| uv/specify 支援 | ⚠️ 可能有問題 | ✅ 完整支援 |

---

## 🐛 常見問題

### Q: 為什麼 VS Code 沒有自動識別 PowerShell 7？

**答**：VS Code 在啟動時掃描終端機設定檔。如果 PowerShell 7 是在 VS Code 啟動後才安裝的，需要重新啟動 VS Code。

### Q: 我選了 PowerShell，但還是 5.1？

**答**：
1. 確認你選的是 `PowerShell`（不是 `Windows PowerShell`）
2. 刪除所有舊的終端機實例
3. 完全關閉並重新啟動 VS Code
4. 檢查 PATH 環境變數是否包含 PowerShell 7

### Q: 如何檢查 PATH 環境變數？

在 PowerShell 5.1 中執行：
```powershell
$env:Path -split ';' | Select-String "PowerShell"
```

應該會看到類似：
```
C:\Program Files\PowerShell\7
```

---

## 📝 下一步

切換成功後：

1. ✅ 執行 `specify check` 確認環境
2. ✅ 建立 Python 虛擬環境：`uv venv`
3. ✅ 開始使用 Spec Kit 開發

參考文件：
- `如何在VSCode中使用GitHub官方Spec-Kit.md`
- `Spec kit 憲章_Claude.md`

---

**建立日期**: 2025-11-15  
**版本**: 1.0
