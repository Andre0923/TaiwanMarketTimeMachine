<template>
  <div class="chart-error">
    <div class="error-container">
      <div class="error-icon">⚠️</div>
      <h3 class="error-title">{{ title }}</h3>
      <p class="error-message">{{ message }}</p>
      <p v-if="details" class="error-details">{{ details }}</p>
      <button 
        v-if="showRetry" 
        class="retry-button" 
        @click="handleRetry"
      >
        重試
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * ChartError Component
 * 
 * 圖表錯誤狀態元件，顯示錯誤訊息與重試按鈕
 * 對應 US A-4 AC2: 顯示錯誤訊息並提供重試功能
 * 
 * @example
 * ```vue
 * <ChartError 
 *   title="載入失敗"
 *   message="無法連線至伺服器"
 *   :show-retry="true"
 *   @retry="handleRetry"
 * />
 * ```
 */

interface Props {
  /** 錯誤標題 */
  title?: string
  /** 錯誤訊息 */
  message: string
  /** 錯誤詳細資訊 */
  details?: string
  /** 是否顯示重試按鈕 */
  showRetry?: boolean
}

interface Emits {
  (e: 'retry'): void
}

withDefaults(defineProps<Props>(), {
  title: '載入失敗',
  showRetry: true
})

const emit = defineEmits<Emits>()

function handleRetry(): void {
  emit('retry')
}
</script>

<style scoped>
.chart-error {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  min-height: 300px;
  background-color: var(--color-background-soft);
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  max-width: 400px;
  padding: 2rem;
  text-align: center;
}

.error-icon {
  font-size: 3rem;
  line-height: 1;
}

.error-title {
  margin: 0;
  color: var(--color-error);
  font-size: 1.25rem;
  font-weight: 600;
}

.error-message {
  margin: 0;
  color: var(--color-text);
  font-size: 0.875rem;
  line-height: 1.5;
}

.error-details {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 0.75rem;
  font-family: monospace;
  padding: 0.5rem;
  background-color: var(--color-background-mute);
  border-radius: 4px;
  max-width: 100%;
  overflow-x: auto;
}

.retry-button {
  margin-top: 0.5rem;
  padding: 0.5rem 1.5rem;
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: var(--color-primary-hover);
}

.retry-button:active {
  transform: scale(0.98);
}

/* CSS Variables - 可在 App.vue 或全域樣式中定義 */
:root {
  --color-background-soft: #f8f9fa;
  --color-background-mute: #e9ecef;
  --color-text: #212529;
  --color-text-secondary: #6c757d;
  --color-error: #dc3545;
  --color-primary: #0d6efd;
  --color-primary-hover: #0b5ed7;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .chart-error {
    background-color: #1a1a1a;
  }
  
  :root {
    --color-background-soft: #1a1a1a;
    --color-background-mute: #2a2a2a;
    --color-text: #f8f9fa;
    --color-text-secondary: #adb5bd;
  }
}
</style>
