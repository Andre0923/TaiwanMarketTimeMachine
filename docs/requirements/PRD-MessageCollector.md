# 產品需求文件 (PRD) v3.1（以 v3.0 為基準補齊完整版）
專案名稱：LINE 自動備份精靈 (LINE Auto Backup Genie - Text, Image & Video)
文件日期：2025/12/19
技術核心：Python RPA + Clipboard Strategy + Windows Dialog Handler + MSSQL

> 說明：本文件以 v3.0 為主體，補齊「原始需求單」與「LINE 本地端自動化備份精靈」中較完整但 v3.0 較簡略的規格（例如：閒置/中斷機制、目標對象管理、去重、輪詢、事件通知、開機自啟、視窗開關、擬人化操作、監控心跳）。

---

## 1. 專案背景與目標 (Overview)
### 1.1 背景
使用者依賴電腦版 LINE 進行與家人及重要資訊溝通，但 LINE 原生備份機制不足且訊息有過期風險，需建立可靠且可長期運行的備份系統。

同時，為了對於個別家人及重要聯絡人也能夠善加備分，必須符合：
- **隱形**：常駐背景/系統列，盡量不影響使用者操作。
- **不驚動對方（家人/朋友/重要夥伴）**：不在群組加入任何第三方機器人、不主動對外發送訊息、不改變群組成員結構。
- **可備份**：可持續、可追溯、可去重、可落地保存（文字＋圖片＋影片）。

### 1.2 產品目標
建立一套本地端自動化系統，在電腦閒置時運作，將指定 LINE 群組/聯絡人的訊息結構化存入 MSSQL，並保存圖片/影片檔案。

- **優先順序**：文字（穩定） > 圖片（快、低風險） > 影片（可做但高風險）
- **策略彈性**：針對媒體檔案，支援「快速備份 (Clipboard)」與「完整備份 (Save As Dialog)」兩條技術路徑

### 1.3 範圍 (Scope)
**In Scope**
- Windows 10/11 桌面環境，以 RPA 方式操作 LINE 電腦版
- 針對可設定的聊天室清單進行訊息擷取與備份
- 訊息去重、結構化寫入 MSSQL
- 圖片/影片檔案保存至本機資料夾，並在資料庫建立關聯
- 事件驅動的監控與通知（可能改版、心跳停止、訊息量異常等）

**Out of Scope（本期不做）**
- 雲端同步/多機協作
- 直接串 LINE 非公開 API 做抓取（以「方案一：本機 RPA」為主）
- 即時監聽（本系統以輪詢＋閒置觸發為主）

### 1.4 主要風險與假設
- 假設：LINE 視窗 UI 元件可被穩定定位；若改版需快速調整 selector/流程
- 風險：RPA 可能受到解析度、縮放、視窗層級、通知彈窗等影響
- 風險：開啟聊天室可能造成「已讀」狀態變更（需與使用者確認是否可接受）

---

## 2. 系統模組架構 (System Architecture)
### 2.1 核心模組概覽
- **IdleMonitor**：偵測滑鼠/鍵盤閒置時間；支援備份中斷與讓出控制權
- **Scheduler**：輪詢與節奏控制（例如每 N 分鐘檢查一次是否需要執行）
- **TargetManager**：管理需備份的群組/聯絡人清單、優先序與規則
- **RPAExecutor**：主控流程；負責開啟 LINE、搜尋/進入聊天室、滾動載入、擷取 UI 文本
- **DataParser**：解析訊息（聊天室、發言者、內容、時間、訊息類型）與相對時間正規化
- **Deduplicator**：為每則訊息產生唯一雜湊，寫入前去重
- **DbWriter (MSSQL)**：批次寫入、斷線重試、唯一鍵衝突處理
- **MediaHandler**：圖片/影片下載與落地保存（Clipboard / Save As Dialog）
- **Watchdog & Notifier**：事件偵測（UI 異常/改版、心跳停止、訊息量異常）與通知（Email/LINE 等）

### 2.2 媒體下載策略（延續 v3.0 雙軌機制）
本模組需支援兩種下載策略，可透過 YAML 設定檔切換：

|策略名稱|Strategy A: Clipboard (快取法)|Strategy B: Save As Dialog (對話框法)|
|---|---|---|
|適用對象|圖片 (Images)|影片 (Videos) & 圖片（替代方案）|
|優點|速度極快、背景運作、不干擾 UI|可下載影片、可取得原始解析度檔案|
|缺點|無法下載影片、圖片可能被壓縮|速度慢、需處理 Windows 視窗、易受干擾|
|技術庫|`Pillow`, `pyperclip`|`pywinauto`（處理另存新檔視窗）|

---

## 3. 詳細功能規格 (Functional Requirements)

### 3.1 觸發機制：閒置偵測與中斷 (Idle Detection & Abort)
- **常駐方式**：程式常駐於背景（建議 System Tray）
- **閒置規則**：`System Idle Time` > `閒置門檻分鐘`（預設 10 分鐘）時，才可開始執行備份
- **全螢幕保護**：若目前為全螢幕應用（簡報/影片），可選擇延後執行（可設定）
- **中斷規則**：備份流程中若偵測到使用者有滑鼠/鍵盤活動，需立即停止 RPA 動作並讓出控制權（例如最小化視窗或暫停）

### 3.2 輪詢規則：多久檢查一次 (Polling)
- 系統需可設定 `輪詢間隔秒`（例如 60 秒）
- 每次輪詢檢查：
  1) 是否閒置達標
  2) 是否在允許的時間窗（選配）
  3) 是否達到冷卻時間（避免頻繁打擾）
  4) 若符合條件才執行一次備份循環（遍歷目標清單）

### 3.2.1 執行節奏與降頻原則（接近人類速度）
由於本系統為自用，且不希望因為過於頻繁擷取造成 LINE 判定為機械化操作或造成不必要負擔，系統需具備「接近人類操作」的節奏控制：
- **最低執行間隔**：兩次完整掃描（遍歷目標清單）之間需有最低間隔（例如 30–60 分鐘，可設定）
- **每個目標冷卻時間**：同一個聊天室在短時間內避免重覆進入/重覆滾動（例如每目標至少 10–30 分鐘，可設定）
- **單次處理上限**：每輪最多處理 N 個目標（例如 5–20，可設定），其餘延後到下一輪
- **動作抖動（Jitter）**：所有等待時間採亂數區間，避免固定節奏
- **失敗退避（Backoff）**：若連續抓不到 UI 元素或下載失敗，需增加等待時間再重試，避免短時間內大量重覆操作

### 3.3 目標對象管理：群組/聯絡人清單 (Target Management)
系統需可設定要擷取的對象（群組或聯絡人）：
- **設定來源**：YAML 設定檔（或未來可移到資料庫設定表）
- **欄位建議**：
  - `target_id`：**固定 5 碼流水編號**（例如 `00001`），做為資料夾命名與資料庫對應的穩定識別碼（建議由系統自動產生，見 3.3.1）
  - `display_name`：聊天室名稱（用於搜尋/比對）
  - `aliases`：（選配）聊天室別名清單，用於改名後仍能對應到同一個 `TargetId`
  - `type`：`group` / `contact`
  - `enabled`：是否啟用
  - `priority`：優先序（數字越小越優先）
- **自動導航能力**：RPA 可在 LINE 搜尋欄輸入關鍵字並點擊正確對象以開啟聊天室

### 3.3.1 TargetId 配置策略（自動產生/自動遞增）
為降低人工維護成本，並避免「群組/聯絡人改名」導致資料夾與資料庫對應混亂，`TargetId` 建議採用**自動產生且永久不變**的策略。

**目標**
- 使用者只需在 YAML 填寫「要備份哪些對象」與必要屬性，不需手填 `target_id`
- 系統首次執行時自動建立 `TargetId` 對照表，後續沿用同一個 `TargetId`
- 對象顯示名稱變更時，只更新顯示名稱（或新增 alias），不更換 `TargetId`

**資料來源與落地（YAML + DB 對照表）**
- YAML：保存「目標清單」與啟用/優先序等策略設定
- DB：保存 `TargetId` 與顯示名稱/類型/別名的對照表，作為最終權威來源（Source of Truth）

**首次執行自動建檔流程（Bootstrap）**
1. 程式讀取 YAML 的 `目標清單.項目`（每個項目至少含 `顯示名稱`、`類型`）
2. 逐一比對資料庫 `[LINE_目標對象]`：
   - 若已存在同一筆目標（以 `display_name`/alias 正規化比對），取回既有 `TargetId`
  - 若不存在，向資料庫取得下一個流水號 → 產生 5 碼 `TargetId` → 建立一筆 `[LINE_目標對象]`
3. 後續所有訊息寫入與資料夾命名一律使用該 `TargetId`

**TargetId 格式**
- 固定 5 碼、左補 0：`00001`、`00002`…
- 遞增來源建議使用 MSSQL `SEQUENCE`（避免同時啟動造成衝突）

### 3.4 視窗控制：開啟/關閉聊天室 (Open/Close Chat)
- 系統需具備：
  - 開啟 LINE 主視窗並 bring-to-front
  - 透過搜尋切換至指定聊天室
  - 備份完成後可選擇「維持在聊天室」或「切回列表/關閉聊天室視窗」（依 LINE UI 能力與設定決定）

### 3.5 訊息擷取：文字、圖片、影片 (Capture)
#### 3.5.1 文字擷取
- 開啟聊天室後，向上滾動指定次數或直到無新歷史訊息載入
- 擷取目前可見訊息區塊的 raw text 與必要的 UI 屬性

#### 3.5.2 圖片擷取（Phase 2）
- 預設使用 Clipboard strategy：在圖片上觸發「複製」→ 從剪貼簿讀取 → 落地保存

#### 3.5.3 影片擷取（Phase 3）
- 影片無法複製到剪貼簿，需使用 Save As Dialog strategy（見 3.9）

### 3.6 資料解析：結構化欄位 (Parsing)
系統需將 raw message 解析為至少以下欄位：
- `TargetId`：目標對象 5 碼流水編號（由系統配置；來源為資料庫 `[LINE_目標對象]`，用於資料夾/資料庫對應）
- `ChatRoomName`：群組/聯絡人名稱
- `SenderName`：發言者
- `MessageContent`：內容（文字；若為媒體可為描述/空）
- `SentTime`：發送時間（需處理「昨天」「上午/下午」等相對時間轉絕對時間）
- `MessageType`：`Text` / `Image` / `Video`
- （媒體時）`LocalFilePath`、`FileHash`、`FileSizeKB`、`DownloadMethod`、`IsDownloadSuccess`

### 3.7 去重：只保留單一份 (Deduplication)
由於 RPA 每次掃描可能重覆讀到相同訊息，系統需在寫入前去重。

- **唯一鍵設計**：`UniqueHash = SHA256(TargetId + SenderName + MessageContent + SentTime + MessageType + FileHash?)`
  - 目的：同一則訊息/同一個媒體檔只保留一份
  - 註：顯示名稱（群組/聯絡人）可能變動，因此去重建議以穩定的 `TargetId` 為主。媒體檔建議以 `FileHash` 補強，避免同時段同內容但不同檔案的誤判。
- **寫入策略**：DB 端以 `UNIQUE` 約束保護；應用端先查詢可選配（減少衝突 log），但最終以 DB 唯一鍵為準

### 3.8 儲存：MSSQL (Database)
採用 MSSQL 作為主儲存，需具備：
- 連線設定（主機/資料庫/帳密/加密選項）
- 批次寫入與重試
- 唯一鍵衝突視為正常去重（Skip，不算錯誤）

### 3.8.1 本機資料夾與暫存路徑規則 (Data/Staging Layout)
系統需可在 YAML 設定檔指定「資料落地」與「程式暫存」路徑，並以一致規則生成資料夾結構，主要目標：
- 媒體檔（圖片/影片）可追溯到哪個聊天室、哪個月份
- 資料夾名稱穩定（以 5 碼 `TargetId` 為主），即使 LINE 顯示名稱變更也不會影響既有資料
- 暫存資料可集中管理（例如下載中檔案、UI raw dump、剪貼簿快取），便於清理與除錯

**路徑類型**
- `storage.data_root`：正式保存的資料根目錄（備份成果）
- `storage.staging_root`：程式暫存根目錄（可定期清理）

**暫存使用原則**
- 媒體下載建議先落在 `staging_root`（例如 `in_progress/`），下載完成後再搬移到 `data_root` 的正式目錄，以降低「半成品檔案」混入正式備份的風險。

**建議資料夾結構（正式保存）**
- 先依年月：`YYYY-MM` 建子資料夾
- 再依對象：`{TargetId}-{TargetDisplayName}`（其中 TargetId 為 5 碼；DisplayName 需做檔名安全化）
- 再依內容類型：
  - `media/images/`
  - `media/videos/`
  - （選配）`text/raw/`：保存原始擷取文字快照（便於除錯；主要文字仍以 MSSQL 為準）

**範例**
- `D:\Line_Backup\2025-12\00001-家人群組\media\images\...`
- `D:\Line_Backup\2025-12\00002-重要聯絡人-王先生\media\videos\...`

**命名規則**
- `TargetId` 必須為 5 碼數字字串（左補 0）
- `TargetDisplayName` 用於展示與資料夾命名；需進行檔名安全化（移除 `\\ / : * ? \" < > |` 等非法字元，並限制長度）
- 資料庫需同時保存 `TargetId` 與當下顯示名稱，確保查詢與檔案對得上

### 3.9 媒體下載：Save As Dialog（Phase 3）
由於影片無法複製到剪貼簿，必須執行以下標準動作：
1. **識別**：RPA 掃描到訊息類型為 `Video`（或圖片在降級策略中）
2. **開啟**：點擊縮圖開啟檢視/播放視窗
3. **觸發下載**：尋找並點擊介面上的「下載/保存」圖示
4. **處理對話框**：
  - 偵測 Windows「存檔/另存新檔」視窗彈出
  - 自動填入絕對路徑與檔名（依 3.8.1 規則，例如 `D:\Line_Backup\2025-12\00001-家人群組\media\videos\Video_01.mp4`）
  - 點擊「存檔」
5. **等待下載完成**：
   - 監控目標檔案大小；若在 5 秒內無變化且 > 0KB，判定完成
   - 設定 `timeout_seconds`（例如 300 秒），逾時記錄 Error 並放棄
6. **關閉檢視器**：發送 `Esc` 關閉播放/檢視視窗

### 3.10 擬人化操作：亂數延遲與動作節奏 (Human Simulation)
系統需可設定模擬人類操作行為，包含：
- **隨機延遲區間**（例如：開啟視窗後等待、滾動後等待、切換聊天室前等待）
- **亂數功能**：每次執行在區間內取隨機值，以降低固定節奏
- （選配）滑鼠移動軌跡平滑化

### 3.11 異常監控與主動通知：事件驅動 (Watchdog & Notifications)
當以下事件觸發時，需能執行對應的動作（Email/LINE 訊息/其他指令）。

**事件模型需求**
- 一個事件可對應多個 action
- action 以「指令/通道」抽象（例如：寄信、呼叫 webhook、發 LINE 通知）

**事件類型（至少）**
1. **UI 元素抓不到（疑似改版）**：連續 N 次找不到搜尋欄/訊息區塊
2. **長時間無新資料（Heartbeat Lost）**：超過 X 小時資料庫沒有任何新寫入
3. **使用情境異常（訊息量過低/過高）**：特定家人/朋友/重要夥伴群組每日訊息數異常（例如 < N）

### 3.12 自動化運維：開機自啟 (Autostart)
- 系統需可設定開機後自動啟動
- 建議方式：Windows Task Scheduler（可確保權限/延遲啟動）或 Startup Folder

---

## 4. 資料庫設計 (Database Schema)
### 4.1 建議表結構（支援文字＋圖片＋影片）
SQL
```
-- 目標對象對照表（目標編號來源）
CREATE SEQUENCE [目標編號流水序列]
AS INT
START WITH 1
INCREMENT BY 1;

CREATE TABLE [LINE_目標對象] (
  [目標編號] CHAR(5) NOT NULL PRIMARY KEY,      -- 5 碼流水編號
  [對象類型] NVARCHAR(20) NOT NULL,             -- 'group' / 'contact'
  [顯示名稱] NVARCHAR(200) NOT NULL,            -- 當下顯示名稱（可更新）
  [別名] NVARCHAR(MAX) NULL,                    -- 選配：用於比對改名/別名
  [建立時間] DATETIME NOT NULL DEFAULT GETDATE(),
  [更新時間] DATETIME NOT NULL DEFAULT GETDATE()
);

-- 建議：程式在新增目標時
-- 1) 先取 seq = NEXT VALUE FOR [目標編號流水序列]
-- 2) 再把 目標編號 = RIGHT('00000' + CAST(seq AS VARCHAR(5)), 5)
-- 3) Insert into [LINE_目標對象]

CREATE TABLE [LINE_訊息紀錄] (
  [紀錄ID] BIGINT IDENTITY(1,1) PRIMARY KEY,

  -- 基本欄位
  [目標編號] CHAR(5) NOT NULL,                  -- 5 碼流水編號（與資料夾命名一致）
  [聊天室名稱] NVARCHAR(200) NOT NULL,          -- 當下顯示名稱（可能變動）
  [對象類型] NVARCHAR(20) NULL,                 -- 'group' / 'contact'（可選）
  [發言者] NVARCHAR(100) NOT NULL,
  [訊息內容] NVARCHAR(MAX) NULL,
  [訊息類型] NVARCHAR(20) NOT NULL,             -- 'Text', 'Image', 'Video'
  [發送時間] DATETIME NOT NULL,
  [擷取時間] DATETIME NOT NULL DEFAULT GETDATE(),

  -- 去重
  [唯一雜湊] CHAR(64) NOT NULL UNIQUE,           -- 建議 SHA-256

  -- 檔案相關（媒體用）
  [本機檔案路徑] NVARCHAR(1000) NULL,
  [檔案雜湊] CHAR(64) NULL,                      -- 建議 SHA-256（對檔案內容）
  [檔案大小KB] INT NULL,
  [下載成功] BIT NOT NULL DEFAULT 1,
  [下載方式] NVARCHAR(20) NULL                  -- 'Clipboard' or 'SaveAsDialog'
);

CREATE INDEX [IX_LINE訊息_聊天室_發送時間]
ON [LINE_訊息紀錄]([聊天室名稱], [發送時間]);

CREATE INDEX [IX_LINE訊息_目標編號_發送時間]
ON [LINE_訊息紀錄]([目標編號], [發送時間]);

CREATE INDEX [IX_LINE訊息_唯一雜湊]
ON [LINE_訊息紀錄]([唯一雜湊]);
```

---

## 5. 核心流程 (Logic Flow)
1. **Start（開機/啟動）**
2. **Scheduler Tick（輪詢）**：每 `輪詢間隔秒` 檢查一次
3. **Check Idle**：若閒置達標且允許執行 → 進入備份流程
4. **For Each Target**：
   - Bring LINE to front
   - Search & Enter ChatRoom
   - Random Delay
   - Scroll Up & Load History
   - Extract Messages
   - Parse → Build UniqueHash
   - Insert MSSQL (Ignore duplicates)
   - Media backup if enabled
   - 若偵測到使用者活動 → Abort & Minimize
5. **Watchdog Update**：更新心跳、統計當日訊息數
6. **Return**：等待下一次輪詢

---

## 6. 設定檔範例（YAML）
YAML
```
系統:
  閒置門檻分鐘: 10
  輪詢間隔秒: 60
  偵測到操作即中斷: true
  系統列模式: true

節奏控制:
  # 目標：接近人類速度，避免頻繁擷取
  最低完整掃描間隔分鐘: 45
  每目標冷卻分鐘: 15
  單次最多處理目標數: 10
  失敗退避基礎秒: 60

目標清單:
  # 目標編號預設由系統自動產生並落地到資料庫的 [LINE_目標對象]（對應 3.3.1）
  編號策略:
    模式: "自動"            # "自動"（預設）或 "手動"
    寬度: 5                  # 固定 5 碼
  項目:
    - 顯示名稱: "家人群組"
      別名: ["家人群(舊名)"]
      類型: "group"
      啟用: true
      優先序: 10
    - 顯示名稱: "重要夥伴-王先生"
      # 手動模式下可指定：目標編號: "00002"
      類型: "contact"
      啟用: true
      優先序: 20

擬人化:
  啟用: true
  開啟聊天室延遲秒: [1.5, 3.0]
  滾動後等待秒: [0.5, 1.2]
  切換下一目標前等待秒: [2.0, 5.0]

儲存:
  # 正式保存（備份成果）根目錄
  正式資料根目錄: "D:\\Line_Backup"
  # 程式暫存根目錄（下載中檔案、raw dump、剪貼簿快取等；可定期清理）
  暫存根目錄: "D:\\Line_Backup_Staging"
  # 資料夾布局規則（對應 3.8.1）
  資料夾規則:
    月份資料夾格式: "%Y-%m"                # e.g. 2025-12
    對象資料夾格式: "{target_id}-{display_name}"  # e.g. 00001-家人群組
    圖片子資料夾: "media\\images"
    影片子資料夾: "media\\videos"
    文字原始子資料夾: "text\\raw"          # 選配
  影片最大大小MB: 500

資料庫:
  MSSQL:
    伺服器: "localhost"
    資料庫名稱: "LineArchive"
    使用者: "sa"
    密碼: "***"
    加密: false

備份策略:
  文字: true
  圖片:
    啟用: true
    方法: "clipboard"     # "clipboard"（快）或 "save_as"（慢，原始檔）
    剪貼簿失敗改用另存新檔: true
    連續失敗門檻: 3
  影片:
    啟用: true
    方法: "save_as"       # 影片只能用此模式
    逾時秒: 300

通知:
  管道:
    自己的LINE: "你的LINE通知API或Webhook"
    自己的Email: "your_email@example.com"
  事件:
    抓不到UI元素_疑似改版:
      連續門檻: 3
      動作: ["自己的LINE", "自己的Email"]
      訊息: "提醒：LINE 備份程式無法讀取視窗，可能已改版或 UI 異常。"
    長時間無寫入:
      小時: 12
      動作: ["自己的Email"]
      訊息: "提醒：備份程式已超過 12 小時未寫入任何資料。"
    訊息量過低:
      目標群組: "重要家人群"
      每日最少訊息數: 5
      動作: ["自己的LINE"]
      訊息: "提醒：重要群組今日訊息量低於門檻，請確認群組狀態。"

開機自啟:
  啟用: true
  方式: "task_scheduler"  # "task_scheduler" or "startup_folder"
```

---

## 7. 開發階段規劃 (Development Phases)
**請依序開發，嚴格控制風險。**

### Phase 1：基礎建設與文字備份（核心）
- 閒置偵測/中斷機制、輪詢排程
- 目標對象管理（群組/聯絡人清單）
- 視窗控制（開啟 LINE、搜尋切換聊天室）
- 文字擷取、解析、去重
- MSSQL 寫入
- Watchdog 基礎事件（UI 抓不到元素、無寫入心跳）
- 開機自啟

### Phase 2：圖片備份（剪貼簿模式）- 推薦
- 加入圖片擷取（Clipboard）
- 圖片落地保存與 DB 關聯
- 失敗降級：Clipboard 連續失敗時切換 Save As（可選）

### Phase 3：影片與進階圖片備份（另存新檔模式）- 後續迭代
- 加入影片下載（Save As Dialog）
- 下載完成判斷與逾時處理
- 強化對話框處理穩定性

---

## 8. 需求對照表（原始需求單 1–13）
|#|原始需求|PRD 對應章節|
|---:|---|---|
|1|隱形、可備份|1.1、1.2、1.3|
|2|閒置 10 分鐘開始|3.1、6.系統.閒置門檻分鐘|
|3|可設定群組/聯絡人|3.3、6.目標清單.項目|
|4|去重只留一份|3.7、4|
|5|記錄群組/聯絡人、使用者、內容、時間|3.6、4|
|6|MSSQL 儲存|3.8、4、6.database|
|7|可設定多久檢查一次|3.2、6.系統.輪詢間隔秒|
|8|擬人化動作/延遲/亂數|3.10、6.擬人化|
|9|疑似改版/存取異常主動通知|3.11、6.notification.events.ui_element_not_found|
|10|多久無正常運行/訊息量異常→事件觸發多指令|3.11、6.notification.events|
|11|可開啟/關閉特定聊天室視窗|3.4|
|12|開機後自動啟動|3.12、6.autostart|
|13|圖片或影片保存|3.5、3.9、6.備份策略|
