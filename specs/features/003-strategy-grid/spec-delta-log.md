# Spec Delta Log

> **Feature**: 003-strategy-grid  
> **建立日期**: 2026-03-02  
> **用途**: 記錄開發過程中發現的規格差異，供 requirement-sync、pre-unify-check、unify-flow 使用

## 規格差異記錄

| ID | Stage | Phase | Type | Original (spec/plan) | Actual/Discovery | Impact | Action |
|----|-------|-------|------|---------------------|-----------------|--------|--------|
| D1 | clarify | Q1 | 需求澄清 | spec: `stock_events` 資料來源未定義 | 確認為資料庫預載唯讀資料，M03 純查詢 | Assumptions §7 | 更新 spec ✅ |
| D2 | clarify | Q2 | 需求澄清 | spec: US B-3 AC2 描述中使用「設定」字眼，隱含可調整 | 確認 pre=20/post=10 為系統固定常數，M03 不提供 UI 調整 | US B-3 AC2, Assumptions §8 | 更新 spec ✅ |
| D3 | clarify | Q3 | 需求澄清 | spec: US B-1 未定義條件格式無效的錯誤場景 | 確認採前端即時驗證，禁止提交並顯示欄位旁錯誤提示 | US B-1 AC5（新增）| 更新 spec ✅ |
| D4 | clarify | Q4 | 需求澄清 | spec: UI Unknowns 包含「QueryPanel 配置方式未定義」 | 確認採固定頂部佈局（QueryPanel 在上，Grid 在下） | UI-SCR-002 描述, UI Unknowns | 更新 spec ✅ |
| D5 | clarify | Q5 | 需求澄清 | spec: StockEvent 有 event_type 欄位，StrategyQueryParams 未明確排除 | 確認 event_type 僅供顯示，M03 不作查詢條件，明確列入 Out of Scope | Out of Scope §7, StockEvent entity 備註 | 更新 spec ✅ |
