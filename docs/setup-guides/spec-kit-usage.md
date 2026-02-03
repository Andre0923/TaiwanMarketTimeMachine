# 如何在 VS Code 中使用 GitHub 官方 Spec Kit

> **建立日期**: 2025-11-15  
> **適用對象**: 已完成基礎安裝的開發者  
> **前置作業**: 已依照「安裝Spec kit 準備-基礎版.md」完成環境設定

---

## 📋 目錄

1. [你目前的進度](#你目前的進度)
2. [工具生態系統說明](#工具生態系統說明)
3. [在 VS Code 中開始使用](#在-vs-code-中開始使用)
4. [Python 專案設定](#python-專案設定)
5. [完整工作流程](#完整工作流程)

---

## 🎯 你目前的進度

根據你提供的截圖和「安裝Spec kit 準備-基礎版.md」，你已經完成：

✅ **已安裝的工具**：
- PowerShell v7.5
- Windows Terminal
- Git
- uv (Python 套件管理器)
- Node.js
- ripgrep (搜尋工具)
- GitHub Copilot CLI 或 Claude Code
- **Spec Kit 的 Specify CLI** (`specify-cli`)

✅ **執行過的檢查**：
```bash
specify check
```

你應該看到類似這樣的結果：
- ✅ Git version control (綠燈)
- ✅ GitHub Copilot 或 Claude Code (綠燈)
- ✅ Visual Studio Code (綠燈)

---

## 🛠️ 工具生態系統說明

### 為什麼需要這些工具？

#### 1. **Spec Kit (specify-cli)** - 規格驅動開發核心
```bash
# 安裝位置
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

**作用**：
- 檢查開發環境 (`specify check`)
- 初始化專案規格文件
- 與 AI Coding 工具整合
- 管理開發流程

**為什麼重要**：這是整個規格驅動開發流程的核心工具

---

#### 2. **uv** - Python 套件管理器
```bash
# 你已經透過 scoop 安裝了
scoop install uv
```

**作用**：
- 管理 Python 虛擬環境（比 venv 快很多）
- 安裝 Python 套件（比 pip 快很多）
- 管理專案依賴

**為什麼重要**：
- 🚀 **極快的速度** - 比 pip 快 10-100 倍
- 🎯 **現代化** - Rust 編寫，穩定可靠
- 🔒 **依賴解析** - 自動處理套件衝突

**在這個專案中的用途**：
- 建立 Python 虛擬環境
- 安裝專案依賴套件
- 管理 Python 版本

---

#### 3. **Node.js 和 npm** - JavaScript 執行環境
```bash
# 你已經透過 scoop 安裝了
scoop install nodejs
```

**作用**：
- 執行 JavaScript 程式
- npm 用於安裝 JavaScript 套件

**為什麼在 Python 專案中需要它**：
- ❌ **注意**：GitHub 官方的 Spec Kit 是用 **Python** 寫的（透過 `uv tool install` 安裝）
- ✅ 但你可能需要 Node.js 來安裝：
  - GitHub Copilot CLI (`npm install -g @github/copilot`)
  - Claude Code (`npm install -g @anthropic-ai/claude-code`)
  - 其他開發工具

**在這個專案中**：
- 我們剛才開發的 `.spec-kit-tool/` 是 npm 套件（**這個可以忽略**）
- 實際使用的是 GitHub 官方的 Python 版 Spec Kit

---

#### 4. **AI Coding 工具**
```bash
# GitHub Copilot CLI
npm install -g @github/copilot

# 或 Claude Code
npm install -g @anthropic-ai/claude-code
```

**作用**：
- 在終端機中使用 AI 協助寫程式
- 與 Spec Kit 整合，幫助生成規格文件
- 協助實作程式碼

---

## 🚀 在 VS Code 中開始使用

### 步驟 1: 開啟專案資料夾

1. 啟動 VS Code
2. 開啟你的專案資料夾：
   ```
   C:\Projects\your-project-name
   ```

### 步驟 2: 開啟整合終端機

在 VS Code 中：
- 按下 `` Ctrl+` `` (控制鍵 + 反引號)
- 或從選單：`終端機` → `新增終端機`
- 確認使用的是 **PowerShell 7.5**（右上角下拉選單可切換）

### 步驟 3: 驗證環境

在終端機中執行：

```powershell
# 檢查 Spec Kit 環境
specify check

# 檢查 uv
uv --version

# 檢查 Python
python --version

# 檢查 Node.js (如果需要 AI 工具)
node --version
```

---

## 🐍 Python 專案設定

### 步驟 1: 建立 Python 虛擬環境

在 VS Code 終端機中執行：

```powershell
# 使用 uv 建立虛擬環境
uv venv

# 啟動虛擬環境 (PowerShell)
.venv\Scripts\Activate.ps1
```

你會看到提示符號前面出現 `(.venv)`，表示虛擬環境已啟動。

### 步驟 2: 設定 VS Code 使用此環境

1. 按下 `Ctrl+Shift+P` 開啟命令面板
2. 輸入 `Python: Select Interpreter`
3. 選擇 `.venv` 中的 Python 解譯器

### 步驟 3: 安裝 Python 開發依賴

```powershell
# 安裝測試框架
uv pip install pytest pytest-cov

# 安裝程式碼格式化工具
uv pip install black ruff

# 將依賴儲存到 requirements.txt（如果需要）
uv pip freeze > requirements.txt
```

---

## 📝 完整工作流程：使用 GitHub Spec Kit

### 工作流程 1: 初始化新功能的規格

```powershell
# 1. 確保在專案根目錄
cd "C:\Projects\your-project-name"

# 2. 啟動虛擬環境
.venv\Scripts\Activate.ps1

# 3. 使用 Spec Kit 開始規格定義
# (這裡需要根據 GitHub Spec Kit 的實際指令，通常是與 AI 工具整合使用)
```

### 工作流程 2: 與 AI 工具協作

#### 使用 GitHub Copilot

```powershell
# 在終端機中使用 Copilot
gh copilot suggest "如何實作任務排程功能"
gh copilot explain "解釋這段程式碼"
```

#### 使用 Claude Code

```powershell
# 啟動 Claude Code
claude-code
```

### 工作流程 3: 規格驅動開發流程

```powershell
# 1. 建立規格文件 (specs/ 資料夾)
# 使用 VS Code 編輯器 + AI 協助建立 spec.md

# 2. 建立開發計畫 (docs/ 資料夾)
# 編輯 plan.md

# 3. 分解任務
# 編輯 tasks.md

# 4. 實作功能 (src/ 資料夾)
# 在虛擬環境中開發

# 5. 執行測試
pytest

# 6. 格式化程式碼
black src/
ruff check src/
```

---

## 📁 專案結構建議

由於你已經有 Spec Kit 憲章，建議的專案結構：

```
TaskScheduler/
├── .venv/                    # Python 虛擬環境（使用 uv venv 建立）
├── specs/                    # 規格文件
│   └── spec.md
├── docs/                     # 文件
│   ├── plan.md
│   └── tasks.md
├── src/                      # 原始碼
│   ├── __init__.py
│   ├── main.py
│   └── utils/
│       └── logger.py
├── tests/                    # 測試
│   └── test_main.py
├── logs/                     # 日誌（執行時自動生成）
├── requirements.txt          # Python 依賴
├── pyproject.toml           # Python 專案設定（可選）
├── .gitignore
├── README.md
└── Spec kit 憲章_Claude.md
```

### 手動建立基本結構

```powershell
# 在 VS Code 終端機中執行

# 建立目錄
New-Item -ItemType Directory -Path specs, docs, src, tests, logs -Force

# 建立基本檔案
New-Item -ItemType File -Path "specs\spec.md", "docs\plan.md", "docs\tasks.md" -Force
New-Item -ItemType File -Path "src\__init__.py", "src\main.py" -Force
New-Item -ItemType File -Path "tests\test_main.py" -Force
New-Item -ItemType File -Path "README.md", ".gitignore" -Force
```

---

## 🎓 實際操作範例

### 範例 1: 開始一個新功能開發

```powershell
# 1. 開啟 VS Code，開啟專案資料夾
# 2. 開啟終端機 (Ctrl+`)
# 3. 啟動虛擬環境
.venv\Scripts\Activate.ps1

# 4. 檢查環境
specify check

# 5. 建立規格文件
# 使用 VS Code 編輯 specs/spec.md，可以請 Copilot 協助

# 6. 開始實作
# 編輯 src/main.py

# 7. 執行測試
pytest

# 8. 檢查程式碼品質
black src/
ruff check src/
```

### 範例 2: 使用 AI 協助寫規格

在 VS Code 中：

1. 開啟 `specs/spec.md`
2. 按下 `Ctrl+I` 或點擊 Copilot 圖示
3. 輸入提示：
   ```
   請幫我撰寫任務排程系統的功能規格，包含：
   - 功能目的
   - 輸入輸出
   - 驗收準則
   ```

---

## 🔄 與 Git 整合

```powershell
# 初始化 Git（如果還沒有）
git init

# 加入 .gitignore
echo ".venv/" >> .gitignore
echo "logs/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore

# 第一次提交
git add .
git commit -m "feat: 初始化 Spec Kit 專案結構"
```

---

## ⚙️ VS Code 推薦擴充套件

在 VS Code 中安裝這些擴充套件：

1. **Python** (Microsoft) - Python 語言支援
2. **Pylance** (Microsoft) - Python 語言伺服器
3. **GitHub Copilot** - AI 程式碼助手
4. **Markdown All in One** - Markdown 編輯
5. **Better Comments** - 更好的註解顯示

安裝方式：
- 按下 `Ctrl+Shift+X` 開啟擴充套件面板
- 搜尋並安裝上述擴充套件

---

## 🐛 常見問題

### Q1: 為什麼需要 uv 而不是 pip？

**答**：
- uv 速度快 10-100 倍
- 更好的依賴解析
- 現代化的工具鏈
- 與 Spec Kit 推薦的工作流程一致

### Q2: `.spec-kit-tool/` 資料夾是什麼？

**答**：
- 那是我們之前開發的自製工具（可以忽略或刪除）
- 實際使用的是 GitHub 官方的 Spec Kit（透過 `uv tool install` 安裝）

### Q3: 虛擬環境啟動失敗？

**答**：
```powershell
# 確認 PowerShell 執行政策
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# 重新建立虛擬環境
Remove-Item -Recurse -Force .venv
uv venv
```

### Q4: 如何在 VS Code 中切換 Python 解譯器？

**答**：
1. `Ctrl+Shift+P`
2. 輸入 `Python: Select Interpreter`
3. 選擇 `.venv\Scripts\python.exe`

---

## 📚 參考資源

- [GitHub Spec Kit 官方文件](https://github.com/github/spec-kit)
- [uv 官方文件](https://docs.astral.sh/uv/)
- [規格驅動開發實戰課程](https://sdd.gh.miniasp.com/)
- 本專案憲章：`Spec kit 憲章_Claude.md`

---

## 🎯 下一步行動

1. ✅ 確認你已在 VS Code 中開啟專案
2. ✅ 確認虛擬環境已建立並啟動
3. ✅ 執行 `specify check` 確認環境
4. 📝 開始編輯 `specs/spec.md` 定義你的功能規格
5. 📝 使用 AI 工具協助填寫規格內容
6. 💻 開始實作程式碼

---

**提示**：遇到問題時，可以隨時使用 `gh copilot suggest` 或 `claude-code` 請 AI 協助！

**建立日期**: 2025-11-15  
**作者**: Victor  
**版本**: 1.0.0
