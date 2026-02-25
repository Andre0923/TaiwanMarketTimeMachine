<template>
  <div class="chart-loading">
    <div class="spinner-container">
      <div class="spinner"></div>
      <p class="loading-text">{{ message }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * ChartLoading Component
 * 
 * 圖表載入中的 Loading 狀態元件
 * 對應 US A-4 AC1: 顯示載入中狀態
 * 
 * @example
 * ```vue
 * <ChartLoading message="載入圖表資料中..." />
 * ```
 */

interface Props {
  /** 載入提示訊息 */
  message?: string
}

withDefaults(defineProps<Props>(), {
  message: '載入中...'
})
</script>

<style scoped>
.chart-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  min-height: 300px;
  background-color: var(--color-background-soft);
}

.spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .chart-loading {
    background-color: #1a1a1a;
  }
}
</style>
