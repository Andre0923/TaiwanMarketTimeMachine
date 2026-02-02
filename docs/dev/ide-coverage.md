# IDE Coverage 設定指引

> **Purpose**: 由於本專案將測試產物輸出到 `.artifacts/`（非預設位置），IDE 的 Coverage Gutter 需要額外設定才能正常顯示。

---

## 1. 測試產物目錄結構

```
.artifacts/
├── pytest_cache/          # pytest 快取
└── coverage/
    ├── .coverage          # coverage 資料檔
    ├── coverage.xml       # XML 報告
    └── html/              # HTML 報告
        └── index.html
```

---

## 1. VS Code

### 1.1 安裝擴充套件

1. 安裝 **Coverage Gutters** 擴充套件（市集搜尋：`ryanluker.vscode-coverage-gutters`）

### 1.2 設定 coverage 檔案路徑

在 `.vscode/settings.json` 中加入：

```json
{
  "coverage-gutters.coverageFileNames": [
    ".artifacts/coverage/coverage.xml",
    ".artifacts/coverage/.coverage"
  ],
  "coverage-gutters.showLineCoverage": true,
  "coverage-gutters.showRulerCoverage": true
}
```

### 1.3 使用方式

1. 執行測試（產生 coverage 報告）：
   ```bash
   uv run pytest
   ```
2. 在 VS Code 狀態列點擊 **Watch** 按鈕，或使用命令面板執行 `Coverage Gutters: Display Coverage`
3. 編輯器左側會顯示綠色（已覆蓋）/ 紅色（未覆蓋）標記

---

## 2. PyCharm

### 2.1 Run Configuration 設定

1. 開啟 **Run/Debug Configurations**（右上角下拉選單 → Edit Configurations）
2. 選擇或建立 pytest 設定
3. 勾選 **Run with coverage**
4. 在 **Coverage** 標籤中：
   - 選擇 **Use coverage.py**
   - 設定 **Coverage data file** 為：`.artifacts/coverage/.coverage`

### 2.2 手動載入 Coverage 報告

若已有 coverage 資料檔案：

1. 選單：**Run** → **Show Coverage Data**
2. 點擊 **+** 按鈕，選擇 `.artifacts/coverage/.coverage` 檔案
3. Coverage 結果會顯示在專案視圖與編輯器左側

---

## 3. 測試指令參考

```bash
# 執行測試（自動產生 coverage 到 .artifacts/coverage/）
uv run pytest

# 只執行測試，不產生 coverage
uv run pytest --no-cov

# 查看 HTML 報告
# Windows
start .artifacts/coverage/html/index.html
# macOS
open .artifacts/coverage/html/index.html
# Linux
xdg-open .artifacts/coverage/html/index.html
```

---

## 4. 注意事項

1. **首次執行**：需先執行 `uv run pytest` 產生 coverage 資料，IDE 才能顯示
2. **檔案路徑**：所有路徑皆為相對於專案根目錄
3. **版本控制**：`.artifacts/` 已被 `.gitignore` 排除，不會被提交到版本控制

---

## 5. 故障排除

### Coverage Gutter 不顯示

1. 確認已執行 `uv run pytest` 產生 coverage 檔案
2. 確認 `.artifacts/coverage/.coverage` 或 `.artifacts/coverage/coverage.xml` 存在
3. VS Code：確認擴充套件已啟用，嘗試重新載入視窗
4. PyCharm：確認 coverage data file 路徑正確

### 報告過舊

執行 `uv run pytest` 重新產生最新的 coverage 報告。

---

**參考文件**：
- [Coverage Gutters 官方文件](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters)
- [PyCharm Code Coverage 官方文件](https://www.jetbrains.com/help/pycharm/code-coverage.html)
- Constitution §1.2「測試與分析產物目錄規範」
- Constitution §3.1.1「開發者體驗（IDE Coverage Gutter）相容性」
