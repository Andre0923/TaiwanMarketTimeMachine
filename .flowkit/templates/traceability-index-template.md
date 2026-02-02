# Traceability Index: {FEATURE_NAME}

> **Generated**: {TIMESTAMP}  
> **Feature**: {FEATURE_ID}  
> **Spec Reference**: [spec.md](./spec.md)

---

## Summary

| 指標 | 數值 |
|------|------|
| User Stories | <!-- 數量 --> |
| Acceptance Criteria | <!-- 數量 --> |
| 程式碼檔案 | <!-- 數量 --> |
| 測試檔案 | <!-- 數量 --> |
| US 覆蓋率 | <!-- 百分比 --> |
| AC 覆蓋率 | <!-- 百分比 --> |

---

## User Story 1: {STORY_TITLE}

**Spec Reference**: [spec.md#user-story-1](./spec.md#user-story-1)

### 程式碼對應

| 類型 | 檔案 | @spec-ac | 任務 ID |
|------|------|----------|---------|
| Model | [src/models/xxx.py](../../src/models/xxx.py) | AC1.1 | T00X |
| Service | [src/services/xxx.py](../../src/services/xxx.py) | AC1.1, AC1.2 | T00X |
| API | [src/api/xxx.py](../../src/api/xxx.py) | - | T00X |
| Test | [tests/test_xxx.py](../../tests/test_xxx.py) | AC1.1, AC1.2 | T00X |

### AC 覆蓋

| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| AC1.1 | <!-- AC 描述 --> | [tests/test_xxx.py#L20](../../tests/test_xxx.py#L20) | ✅ |
| AC1.2 | <!-- AC 描述 --> | [tests/test_xxx.py#L45](../../tests/test_xxx.py#L45) | ✅ |
| AC1.3 | <!-- AC 描述 --> | - | ❌ 無測試 |

---

## User Story 2: {STORY_TITLE}

**Spec Reference**: [spec.md#user-story-2](./spec.md#user-story-2)

### 程式碼對應

| 類型 | 檔案 | @spec-ac | 任務 ID |
|------|------|----------|---------|
| <!-- 填入 --> | <!-- 填入 --> | <!-- 填入 --> | <!-- 填入 --> |

### AC 覆蓋

| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| <!-- 填入 --> | <!-- 填入 --> | <!-- 填入 --> | <!-- 填入 --> |

---

## Issues

> 列出覆蓋率問題或需要關注的項目

| 嚴重性 | 問題 | 說明 | 建議 |
|--------|------|------|------|
| HIGH | US3 無對應檔案 | User Story 3 沒有任何實作 | 檢查 tasks.md 是否遺漏 |
| MEDIUM | AC2.3 無對應測試 | 該 AC 沒有測試覆蓋 | 建議補充測試 |
| LOW | src/utils/helper.py 無 @spec | 檔案缺少 @spec 註解 | 建議加入註解 |

---

## 維護說明

- 本檔案由 `/flowkit.trace` 自動產生
- 修改程式碼後建議重新執行以更新索引
- Unify Flow 會將此索引合併至 System 層
- 手動修改可能在下次執行時被覆蓋

---

## @spec 註解格式參考

```python
# @spec US1 (001-feature/spec.md#user-story-1)
# @spec-ac AC1.1, AC1.2
```

| 註解 | 必要性 | 說明 |
|------|--------|------|
| `@spec US{N}` | REQUIRED | User Story 對應 |
| `@spec-ac AC{N}.{M}` | RECOMMENDED | AC 對應（可多個） |
