# Project Constitution（簡化版）
## SpecKit Plan / Analyze 階段專用

> **版本**：v1.0.0  
> **批准日期**：2026-01-21  
> **最後修訂**：2026-01-21  
> **文件性質**：SpecKit 流程中 Plan 填寫與 Analyze 檢驗的核心準則  
> **語言規範**：關鍵字（MUST / SHOULD / MAY）維持英文，其餘使用繁體中文  

---

# Part I: SDD 核心架構

## §1.1 Specification-Driven Development 🔴 NON-NEGOTIABLE

本專案以 **Specification-Driven Development（SDD）** 為核心方法。

**MUST 要求**：
- 先定義規格再實作
- 依序完成：`spec.md` → `plan.md` → `tasks.md` → 實作
- 以可執行規格描述功能目的與驗收準則

**驗收標準**：
- [ ] 所有功能都有對應的 spec.md
- [ ] 實作前已完成 plan.md 與 tasks.md
- [ ] 規格包含明確的驗收準則

---

## §1.2 目錄結構（強制）🔴 NON-NEGOTIABLE

```
project-root/
├── .specify/                      # Spec Kit 內部資料
├── specs/                         # 🔴 SDD 中心
│   ├── system/                    # 🟥 System Level（唯一真相）
│   │   ├── spec.md                # System Spec：系統當前外部行為（WHAT）
│   │   ├── data-model.md          # Design：資料模型
│   │   ├── flows.md               # Design：流程圖 / 狀態流轉
│   │   ├── ui/                    # Design：UI/UX Authority
│   │   └── contracts/             # Design：介面契約
│   ├── features/                  # 🟡 Feature Level
│   │   └── NNN-feature-name/
│   │       ├── spec.md            # Feature Spec（Change Set）
│   │       ├── plan.md            # Feature Plan
│   │       └── tasks.md           # Feature Tasks
│   └── history/                   # 🟤 History（封存，唯讀）
├── src/                           # 程式碼
├── tests/                         # 測試
├── logs/                          # 日誌
└── docs/                          # 開發規劃文件（輸入，非真相來源）
```

### 層級權威

| 層級 | 位置 | 用途 | 狀態 |
|------|------|------|------|
| **System** | `specs/system/` | 唯一真相：整體系統行為與設計 | 🟢 Live |
| **Feature** | `specs/features/NNN-*/` | 差異規格：本次開發變更 | 🟡 開發中 |
| **History** | `specs/history/NNN-*/` | 封存：歷史開發變更(透過unify-flow封存) | 🔴 唯讀 |

### Feature 封存規範 🔴 NON-NEGOTIABLE

**MUST 要求**：
- Unify Flow 完成後，原 Feature 目錄 MUST 整個移至 `specs/history/NNN-feature-name/`
- **main 分支不得存在未整合的 Feature Spec**
- 封存後的 Feature 目錄為唯讀，AI 不得從中推導現行行為

### 測試與分析產物（Artifacts）目錄規範 🔴 NON-NEGOTIABLE

**MUST 要求**：
- 任何由工具執行時產生、可再生（reproducible）的產物 MUST 輸出到 `.artifacts/`
- `.artifacts/` MUST 被 `.gitignore` 排除

**測試產物分類與位置**：

| 產物類型 | 預設位置 | 目標位置 |
|----------|----------|----------|
| pytest 快取 | `.pytest_cache/` | `.artifacts/pytest_cache/` |
| Coverage 資料檔 | `.coverage` | `.artifacts/coverage/.coverage` |
| Coverage HTML 報告 | `htmlcov/` | `.artifacts/coverage/html/` |
| Coverage XML 報告 | `coverage.xml` | `.artifacts/coverage/coverage.xml` |
| 其他測試/分析產物 | 專案根目錄 | `.artifacts/<tool_name>/` |

**配置方式**（`pyproject.toml`）：
```toml
[tool.pytest.ini_options]
cache_dir = ".artifacts/pytest_cache"
addopts = [
    "--cov-report=html:.artifacts/coverage/html",
    "--cov-report=xml:.artifacts/coverage/coverage.xml",
]

[tool.coverage.run]
data_file = ".artifacts/coverage/.coverage"

[tool.coverage.html]
directory = ".artifacts/coverage/html"
```

---

## §1.3 System Spec（WHAT）🔴 NON-NEGOTIABLE

**文件**：`specs/system/spec.md`（唯一真相）

**MUST 要求**：
- User Stories MUST 依 BDD 格式撰寫
- 此文件 MUST 是 main 分支上的唯一行為定義來源
- AI 不得以「程式碼現況」推翻 spec
- AI 不得從 `specs/history/` 推導現行行為

---

## §1.4 System Design（HOW）🟡

**位置**：`specs/system/`（長期活檔）

| 文件 | 用途 |
|------|------|
| `data-model.md` | 系統所有實體、欄位、關聯 |
| `contracts/` | Webhook / API / Schema 介面契約 |
| `flows.md` | 系統流程圖、狀態流轉 |
| `ui/` | UI/UX Design Authority |

---

# Part II: User Story 標準

## §2.1 Acceptance Criteria 規範 🔴 NON-NEGOTIABLE

**MUST 要求**：
1. 統一使用 **BDD 格式**（Given / When / Then）
2. AC 數量依情境而定，建議 1～5 條，涵蓋正常與例外情境
3. 每條 AC 建議加入簡短語意標題

**SHOULD 要求**：
- Acceptance Criteria SHOULD 可直接轉換為驗收測試

---

# Part III: 核心原則

> 以下為 Plan 填寫 Constitution Check 與 Analyze 檢驗的核心條款。

## §3.1 Test-First & TDD/BDD 🔴 NON-NEGOTIABLE

**MUST 要求**：
- 新增或修改行為時，MUST 先從對應 AC 衍生或更新測試案例
- 在 `tests/` 內新增或更新對應測試後，才可修改 `src/`
- 重大變更不得僅修改 `src/`，不更新對應測試
- 所有測試檔案 MUST 放在 `tests/` 資料夾

**SHOULD 要求**：
- 優先以「單元測試」覆蓋核心商業邏輯
- 測試名稱 SHOULD 標註對應的 User Story / AC 編號

**例外處理**：
- 若技術限制無法先寫測試，MUST 在 `plan.md` 記錄原因與替代驗證方式

### §3.1.1 開發者體驗（IDE Coverage Gutter）相容性 🟡

由於 `.coverage` 檔案位於 `.artifacts/coverage/` 目錄，IDE 的 Coverage Gutter 功能可能需要額外設定才能正常顯示。

**MUST 要求**：
- 專案 MUST 提供「IDE 設定指引」以恢復 Coverage Gutter 顯示
- 設定指引 SHOULD 放置於 `docs/dev/ide-coverage.md`

**常見 IDE 設定**：
- **VS Code**：安裝 Coverage Gutters 擴充，設定 `coverage-gutters.coverageFileNames` 指向 `.artifacts/coverage/.coverage`
- **PyCharm**：Run Configuration → Code Coverage → 指定 coverage 資料檔案路徑

---

## §3.2 Observability & Traceability 🔴 NON-NEGOTIABLE

**MUST 要求**：
- 所有自動化流程 MUST 可觀察，具備明確的 logging 輸出
- 程式碼 MUST 使用 logging 模組，禁止使用 print 作為日誌輸出
- 新增或修改自動化流程時，MUST 在 `plan.md` 說明 logging 策略
- 所有日誌 MUST 寫入 `logs/` 目錄
- 日誌命名格式 MUST 為 `YYYYMMDD_HHMMSS.log`

**SHOULD 要求**：
- 包含錯誤碼與執行上下文（trace id、feature id）
- 關鍵業務流程 SHOULD 記錄 start / end / error 事件

**日誌等級**：`DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL`

---

## §3.3 Maintainability & Reusability 🟡

**MUST 要求**：
- 單一職責原則（Single Responsibility Principle）
- 低耦合、高內聚（Low Coupling, High Cohesion）
- 模組 MUST 自給自足、可獨立測試、具備文件

**SHOULD 要求**：
- 優先選擇可維護性與可複用性高的方案
- 功能應設計為獨立模組，具備清晰目的

**成本權衡準則**：

| 成本差異 | 選擇 | 理由 |
|----------|------|------|
| < 20% | ✅ 可維護方案 | 長期收益 > 短期成本 |
| 20-50% | 🟡 評估生命週期 | 長期維護建議可維護方案 |
| > 50% | 🔴 團隊討論 | 技術債務追蹤 |

---

## §3.4 Interface-Logic Separation 🟡

**MUST 要求**：
- 明確分離介面層（UI/API/CLI）與業務邏輯層
- 確保修改介面不影響邏輯或資料流程
- 定義穩定的互動邊界（DTO、輸入參數、事件物件）

---

## §3.5 Minimalism & Clarity 🟢

**MUST 要求**：
- 使用繁體中文撰寫說明與註解（技術名詞保留原文）

**SHOULD 要求**：
- 採用最小必要修改原則
- 避免過度工程化
- 單一檔案超過 1000 行時 SHOULD 拆分並更新架構文件

---

## §3.6 UI 行為治理 🟡

> 僅適用於 UI Impact ≠ None 的 Feature

### §3.6.1 行為治理（MUST / Analyze 可檢查）

- UI 行為 MUST 以 User Story + AC 記錄
- UI 行為變更 MUST 整合進 System Spec
- 非同步 UI 行為的 AC，MUST 定義 Loading / Empty / Error 狀態（若適用）
- 涉及不可逆操作的 AC，MUST 包含確認機制描述
- UI ID 引用 MUST 使用正確格式：`[UI-SCR-###]` / `[UI-CMP-###]` / `[UI-PAT-###]` / `[UI-STATE-###]`

### §3.6.2 UI 成熟度門檻

| 等級 | 名稱 | Gate |
|------|------|------|
| **L0** | Draft | specify 可通過（允許 `[UI-TBD]`） |
| **L1** | Buildable | implement 必須達到 |

**L1 最低要求**：
- Global States（loading/empty/error）規則可執行
- 不可逆操作 policy 明確
- 主要 Screen/Flow 已定義且可被 AC 引用

### §3.6.3 UI 文件層級權威

| 優先級 | 文件 | 說明 |
|--------|------|------|
| 1 | `spec.md` (AC) | 行為唯一真相 |
| 2 | `specs/system/ui/*` | UI 範圍權威 |
| 3 | `specs/system/contracts/*` | 介面契約 |

### §3.6.4 禁止事項

- ❌ 不得建立第二份「UI spec」取代 AC 的行為真相
- ❌ UI 文件不得複製 contracts/schema 欄位（只能連結）
- ❌ 不得實作 AC 未定義的 UI 行為

---

# Part IV: 一致性檢查與 AI 規範

## §4.1 一致性檢查（Analyze）🔴 NON-NEGOTIABLE

為確保所有層級不產生矛盾，MUST 執行 `/speckit.analyze`。

**強制規範**：
- 若存在 `data-model.md` 或 `contracts/`，MUST 將它們納入一致性檢查

**檢查範圍**：

| 來源 | 目標 | 檢查項目 |
|------|------|----------|
| spec | plan | 計畫是否涵蓋規格 |
| spec | tasks | 任務是否對應規格 |
| spec | data-model.md | 資料結構是否符合規格 |
| spec | contracts/ | 介面契約是否一致 |
| plan | design | 計畫是否與設計對齊 |
| tasks | design | 任務是否符合設計 |
| plan | observability | 是否說明 logging 策略（§3.2） |

---

## §4.2 AI Agent 使用規範 🔴 NON-NEGOTIABLE

AI MUST 遵守：

1. AI 以 `specs/system/spec.md` 作為當前行為唯一依據
2. AI 修改資料欄位、行為、介面時，MUST 同步調整：
   - `specs/system/spec.md`（行為）
   - `specs/system/data-model.md`（資料）
   - `specs/system/contracts/`（介面）
   - `specs/system/flows.md`（流程）
   - `specs/system/ui/`（UI，若 UI Impact ≠ None）
3. AI 不得以「程式碼現況」推翻 spec
4. AI 不得從 `specs/history/` 推導現行行為
5. `/speckit.analyze` MUST 通過才可合併
6. 不得修改或引用已封存文件作為現行規則
7. AI 撰寫或修改程式碼前，MUST 先檢查相關 AC，並在 `tests/` 產生或更新對應測試

---

## §4.3 AI 知識來源控制 🟡

**MUST 限制**：
- AI 只能引用已核准且已提交的正式文件作為專案規範依據
- 禁止引用未審查的草稿作為專案決策依據

| 狀態 | 來源 |
|------|------|
| ✅ 許可 | 專案文件、官方技術文件、廣泛認可的最佳實踐 |
| 🟡 需評估 | 外部參考資源（需確認適用性） |
| ❌ 禁止 | 草稿、過時技術、與專案技術棧不符的方案 |

---

# Part V: 工程標準

## §5.1 文件一致性 🔴 NON-NEGOTIABLE

**MUST 要求**：
- `spec.md`、`plan.md`、`tasks.md` 與程式碼 MUST 語意一致
- 修改資料流、架構、流程時 MUST 同步更新文件
- 文件與程式碼 MUST 於同一 PR 完成同步

**檢查清單**：
- [ ] 文件描述與程式碼實作一致
- [ ] 新增的類別/函式已更新至架構文件
- [ ] API 變更已反映於 spec.md
- [ ] 流程圖與實際執行順序相符

---

## §5.2 Python 環境標準 🔴 NON-NEGOTIABLE

> 本條僅適用於 Python 相關工作

**MUST 要求**：
- AI 處理 Python 任務時 MUST 使用 `uv` 作為唯一環境與依賴管理工具
- AI MUST 維護 `uv.lock`

**標準指令**：

| 操作 | 指令 |
|------|------|
| 安裝套件 | `uv add <package>` |
| 建立虛擬環境 | `uv venv`（MUST 使用 `./.venv/`） |
| 初始化專案 | `uv init <project-name>` |
| 執行程式 | `uv run <script.py>` |

**禁止指令**：`pip`, `python -m venv`, `pipenv`, `conda`, `poetry`, `pipx`

---

# Part VI: 治理

## §6.1 不確定性處理 🔴 MUST

AI 若對以下內容產生疑慮，MUST 先詢問人類，不得自行假設或修改：
- 需求不明確
- 資料欄位定義
- 流程邏輯
- 架構決策

---
## §6.2 Unify Flow（統合流程） 🔴 NON-NEGOTIABLE

**MUST 要求**：
- System Spec 的唯一修改通道是 Unify Flow
- MUST NOT 在 Feature 開發中直接修改 `specs/system/**` 下的任何文件
- Unify Flow：合併 Feature Spec（更新來源） → System Spec（基底）

**封存規範**：
- Unify Flow 完成後，原 Feature 目錄 MUST 整個移至 `specs/history/`
- 移動後目錄結構保持不變：`specs/history/NNN-feature-name/`
- main 分支不得存在未整合的 Feature Spec

**禁止事項**：
- ❌ 不得跨過 Unify Flow 直接合併 Feature 分支至 main
- ❌ 不得將 Feature Spec 留在 `specs/features/` 而不封存
- ❌ 不得從 `specs/history/` 推導現行行為

---

# 附錄 A：條款索引

## NON-NEGOTIABLE（🔴）條款

| 條款 | 名稱 | Plan | Analyze |
|------|------|:----:|:-------:|
| §1.1 | SDD 方法論 | ✅ | ✅ |
| §1.2 | 目錄結構 | ✅ | ✅ |
| §1.3 | System Spec 唯一真相 | — | ✅ |
| §2.1 | AC 使用 BDD 格式 | — | ✅ |
| §3.1 | TDD/BDD Flow | ✅ | ✅ |
| §3.2 | Observability | ✅ | ✅ |
| §4.1 | 一致性檢查 | — | ✅ |
| §4.2 | AI Agent 規範 | — | ✅ |
| §5.1 | 文件一致性 | ✅ | ✅ |
| §5.2 | Python 環境 | ✅ | — |
| §6.1 | 不確定性處理 | ✅ | — |
| §6.2 | Feature 合併限制 | — | ✅ |

## SHOULD（🟡）條款

| 條款   | 名稱              | Plan | Analyze |
| ---- | --------------- | :--: | :-----: |
| §1.4 | System Design 層 |  ✅   |    —    |
| §3.3 | 可維護性優先          |  ✅   |    —    |
| §3.4 | 介面-邏輯分離         |  ✅   |    —    |
| §3.5 | 最小化與清晰          |  ✅   |    —    |
| §3.6 | UI 行為治理         |  ✅   |    ✅    |
| §4.3 | AI 知識來源控制       |  —   |    ✅    |

