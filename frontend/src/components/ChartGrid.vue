<template>
  <div class="chart-grid">
    <!-- Grid Header -->
    <div class="grid-header">
      <h2 class="grid-title">多股票監控面板</h2>
      <div class="grid-controls">
        <label class="grid-size-label">
          網格大小：
          <select v-model="gridColumns" class="grid-size-select">
            <option :value="2">2 列</option>
            <option :value="3">3 列</option>
            <option :value="4">4 列</option>
          </select>
        </label>
      </div>
    </div>

    <!-- Expanded Chart Modal -->
    <Teleport to="body">
      <div 
        v-if="expandedChart" 
        class="expanded-modal"
        @click.self="closeExpanded"
      >
        <div class="expanded-container">
          <div class="expanded-header">
            <h3>{{ expandedChart.stockCode }} - 詳細圖表</h3>
            <button 
              class="close-button" 
              @click="closeExpanded"
              title="關閉 (ESC)"
            >
              ✕
            </button>
          </div>
          <div class="expanded-content">
            <ChartWidget
              :key="`expanded-${expandedChart.stockCode}`"
              :stock-code="expandedChart.stockCode"
              :start-date="expandedChart.startDate"
              :end-date="expandedChart.endDate"
            />
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Grid Layout -->
    <div 
      class="grid-container" 
      :style="{ gridTemplateColumns: `repeat(${gridColumns}, 1fr)` }"
    >
      <div
        v-for="chart in charts"
        :key="`${chart.stockCode}-${chart.startDate}-${chart.endDate}`"
        class="grid-item"
        @click="handleChartClick(chart)"
      >
        <div class="grid-item-overlay">
          <span class="expand-hint">點擊展開</span>
        </div>
        <ChartWidget
          :stock-code="chart.stockCode"
          :start-date="chart.startDate"
          :end-date="chart.endDate"
          :loading-message="`載入 ${chart.stockCode}...`"
        />
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="charts.length === 0" class="empty-state">
      <p>尚未新增任何股票圖表</p>
      <p class="empty-hint">請使用上方控制面板新增股票</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import ChartWidget from './ChartWidget.vue'

/**
 * ChartGrid Component
 * 
 * 多圖表網格顯示元件，支援點擊展開功能
 * 對應 US A-3: 小圖展開功能
 * 
 * @example
 * ```vue
 * <ChartGrid :charts="chartConfigs" />
 * ```
 */

interface ChartConfig {
  stockCode: string
  startDate: string
  endDate: string
}

interface Props {
  /** 圖表配置陣列 */
  charts: ChartConfig[]
  /** 預設網格列數 */
  defaultColumns?: number
}

const props = withDefaults(defineProps<Props>(), {
  defaultColumns: 3
})

// State
const gridColumns = ref(props.defaultColumns)
const expandedChart = ref<ChartConfig | null>(null)

/**
 * 處理圖表點擊 - 展開為大圖
 * 對應 US A-3 AC1
 */
function handleChartClick(chart: ChartConfig): void {
  expandedChart.value = chart
  // 禁止背景滾動
  document.body.style.overflow = 'hidden'
}

/**
 * 關閉展開的圖表
 * 對應 US A-3 AC3
 */
function closeExpanded(): void {
  expandedChart.value = null
  // 恢復背景滾動
  document.body.style.overflow = ''
}

/**
 * ESC 鍵關閉展開圖表
 * 對應 US A-3 AC3
 */
function handleKeydown(event: KeyboardEvent): void {
  if (event.key === 'Escape' && expandedChart.value) {
    closeExpanded()
  }
}

// Lifecycle
onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  // 清理
  document.body.style.overflow = ''
})
</script>

<style scoped>
.chart-grid {
  width: 100%;
  padding: 1.5rem;
}

.grid-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--color-border);
}

.grid-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text);
}

.grid-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.grid-size-label {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.grid-size-select {
  margin-left: 0.5rem;
  padding: 0.375rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.grid-size-select:focus {
  outline: none;
  border-color: var(--color-primary);
}

.grid-container {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.grid-item {
  position: relative;
  min-height: 300px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.grid-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.grid-item:hover .grid-item-overlay {
  opacity: 1;
}

.grid-item-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
  z-index: 10;
  pointer-events: none;
}

.expand-hint {
  padding: 0.75rem 1.5rem;
  background-color: white;
  color: var(--color-text);
  border-radius: 4px;
  font-weight: 500;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--color-text-secondary);
}

.empty-state p {
  margin: 0.5rem 0;
}

.empty-hint {
  font-size: 0.875rem;
}

/* Expanded Modal */
.expanded-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  animation: fadeIn 0.2s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.expanded-container {
  width: 100%;
  max-width: 1400px;
  height: 90vh;
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s;
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.expanded-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--color-border);
  background-color: var(--color-background-soft);
}

.expanded-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text);
}

.close-button {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  border: none;
  font-size: 1.5rem;
  color: var(--color-text-secondary);
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s, color 0.2s;
}

.close-button:hover {
  background-color: var(--color-background-mute);
  color: var(--color-text);
}

.expanded-content {
  flex: 1;
  overflow: auto;
  padding: 1rem;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .grid-size-select {
    background-color: #1a1a1a;
    color: #f8f9fa;
  }
  
  .expand-hint {
    background-color: #1a1a1a;
    color: #f8f9fa;
  }
  
  .expanded-container {
    background-color: #1a1a1a;
  }
  
  .expanded-header {
    background-color: #0d0d0d;
  }
}

/* Responsive */
@media (max-width: 1024px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 640px) {
  .grid-container {
    grid-template-columns: 1fr !important;
  }
  
  .expanded-modal {
    padding: 0;
  }
  
  .expanded-container {
    height: 100vh;
    border-radius: 0;
  }
}
</style>
