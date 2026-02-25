# Spec Delta Log

> **Feature**: {NNN}-{feature-name}  
> **建立日期**: {YYYY-MM-DD}  
> **用途**: 記錄開發過程中發現的規格差異，供 requirement-sync、pre-unify-check、unify-flow 使用

## 規格差異記錄

| ID | Stage | Phase | Type | Original (spec/plan) | Actual/Discovery | Impact | Action |
|----|-------|-------|------|---------------------|-----------------|--------|--------|
| D1 | {stage} | {phase} | {type} | {原始描述} | {實際發現} | {US/AC} | {處理方式} |

## 欄位說明

| 欄位 | 說明 | 範例值 |
|------|------|--------|
| ID | 流水編號 | D1, D2, D3... |
| Stage | 產生差異的階段 | clarify / analyze / implement / refine-loop / code-check |
| Phase | 該階段中的步驟 | Phase 2, Step 5, §8 |
| Type | 差異類型 | 技術限制 / 需求變更 / 可行性 / 架構調整 / 需求澄清 |
| Original | 原始 spec/plan 描述 | spec: 即時同步 |
| Actual/Discovery | 實際發現或調整後內容 | API 僅支援輪詢 |
| Impact | 影響的 US/AC 編號 | US-A-2 AC1 |
| Action | 處理方式 | 已更新 spec ✅ / 待 refine-loop / 建議調整 |
