<template>
  <div class="chart-widget">
    <!-- Loading State -->
    <ChartLoading v-if="isLoading" :message="loadingMessage" />
    
    <!-- Error State -->
    <ChartError
      v-else-if="isError && error"
      :title="errorTitle"
      :message="error.message"
      :details="error.details"
      :show-retry="true"
      @retry="handleRetry"
    />
    
    <!-- Chart Display -->
    <div v-else-if="isSuccess" class="chart-container">
      <!-- Chart Header -->
      <div class="chart-header">
        <h3 class="stock-name">{{ metadata?.stock_code || stockCode }}</h3>
        <div class="chart-info">
          <span class="data-points">{{ metadata?.data_points || 0 }} 筆資料</span>
          <span v-if="metadata" class="date-range">
            {{ metadata.start_date }} ~ {{ metadata.end_date }}
          </span>
        </div>
      </div>
      
      <!-- TradingView Chart Canvas -->
      <div ref="chartContainerRef" class="chart-canvas"></div>
      
      <!-- Crosshair Info -->
      <div v-if="crosshair.visible" class="crosshair-info">
        <div v-if="crosshair.dataPoint" class="ohlcv-data">
          <span>日期: {{ crosshair.dataPoint.time }}</span>
          <span>開: {{ crosshair.dataPoint.open.toFixed(2) }}</span>
          <span>高: {{ crosshair.dataPoint.high.toFixed(2) }}</span>
          <span>低: {{ crosshair.dataPoint.low.toFixed(2) }}</span>
          <span>收: {{ crosshair.dataPoint.close.toFixed(2) }}</span>
          <span>量: {{ formatVolume(crosshair.dataPoint.volume) }}</span>
        </div>
      </div>
      
      <!-- Zoom Controls -->
      <div class="chart-controls">
        <button 
          class="control-button" 
          :disabled="zoom.zoomLevel >= 10"
          @click="handleZoomIn"
          title="放大 (滑鼠滾輪向上)"
        >
          🔍+
        </button>
        <button 
          class="control-button" 
          :disabled="zoom.zoomLevel <= 0.1"
          @click="handleZoomOut"
          title="縮小 (滑鼠滾輪向下)"
        >
          🔍-
        </button>
        <button 
          class="control-button" 
          @click="resetZoom"
          title="重置縮放"
        >
          ↻
        </button>
        <span class="zoom-level">{{ (zoom.zoomLevel * 100).toFixed(0) }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { createChart, type IChartApi, type ISeriesApi, type CandlestickData } from 'lightweight-charts'
import { useChartData } from '../composables/useChartData'
import { useChartInteraction } from '../composables/useChartInteraction'
import ChartLoading from './ChartLoading.vue'
import ChartError from './ChartError.vue'
import type { ChartQueryParams } from '../types/chart'

/**
 * ChartWidget Component
 * 
 * 單一股票圖表元件，整合 TradingView Lightweight Charts
 * 對應 US A-2: 圖表互動功能（Zoom/Pan/Crosshair）
 * 對應 US A-4: Loading & Error 狀態
 * 
 * @example
 * ```vue
 * <ChartWidget 
 *   stock-code="2330"
 *   start-date="2024-01-01"
 *   end-date="2024-01-31"
 * />
 * ```
 */

interface Props {
  /** 股票代碼 */
  stockCode: string
  /** 起始日期 (YYYY-MM-DD) */
  startDate: string
  /** 結束日期 (YYYY-MM-DD) */
  endDate: string
  /** 載入提示訊息 */
  loadingMessage?: string
}

const props = withDefaults(defineProps<Props>(), {
  loadingMessage: '載入圖表資料中...'
})

// Composables
const { data, metadata, isLoading, isSuccess, isError, error, fetchChart, refetch } = useChartData()
const { crosshair, zoom, isPanning, handlers, resetZoom, setInteractionEnabled } = useChartInteraction()

// Chart instance
const chartContainerRef = ref<HTMLDivElement | null>(null)
let chartInstance: IChartApi | null = null
let candlestickSeries: ISeriesApi<'Candlestick'> | null = null

// Computed
const errorTitle = computed(() => {
  if (!error.value) return '載入失敗'
  
  switch (error.value.code) {
    case 'NETWORK_ERROR':
      return '網路錯誤'
    case 'TIMEOUT_ERROR':
      return '請求逾時'
    case 'NO_DATA':
      return '查無資料'
    case 'INVALID_STOCK_CODE':
    case 'INVALID_DATE_FORMAT':
    case 'INVALID_DATE_RANGE':
      return '參數錯誤'
    default:
      return '載入失敗'
  }
})

/**
 * 格式化成交量
 */
function formatVolume(volume: number): string {
  if (volume >= 1000000) {
    return `${(volume / 1000000).toFixed(2)}M`
  } else if (volume >= 1000) {
    return `${(volume / 1000).toFixed(2)}K`
  }
  return volume.toString()
}

/**
 * 初始化圖表
 */
function initChart(): void {
  if (!chartContainerRef.value) return
  
  // 建立圖表實例
  chartInstance = createChart(chartContainerRef.value, {
    width: chartContainerRef.value.clientWidth,
    height: 400,
    layout: {
      background: { color: '#ffffff' },
      textColor: '#333'
    },
    grid: {
      vertLines: { color: '#f0f0f0' },
      horzLines: { color: '#f0f0f0' }
    },
    timeScale: {
      timeVisible: true,
      borderColor: '#cccccc'
    }
  })
  
  // 建立 K 線序列
  candlestickSeries = chartInstance.addCandlestickSeries({
    upColor: '#ef5350',
    downColor: '#26a69a',
    borderVisible: false,
    wickUpColor: '#ef5350',
    wickDownColor: '#26a69a'
  })
  
  // 註冊事件監聽
  attachEventListeners()
}

/**
 * 更新圖表資料
 */
function updateChartData(): void {
  if (!candlestickSeries || !data.value.length) return
  
  // 轉換資料格式為 TradingView 格式
  const chartData: CandlestickData[] = data.value.map(point => ({
    time: point.time,
    open: point.open,
    high: point.high,
    low: point.low,
    close: point.close
  }))
  
  candlestickSeries.setData(chartData)
  
  // 自動調整可見範圍
  if (chartInstance) {
    chartInstance.timeScale().fitContent()
  }
}

/**
 * 附加事件監聽器
 */
function attachEventListeners(): void {
  if (!chartContainerRef.value || !chartInstance) return
  
  const container = chartContainerRef.value
  
  // 滑鼠移動 - Crosshair
  container.addEventListener('mousemove', (e) => {
    handlers.handleMouseMove(e as MouseEvent)
    updateCrosshair(e as MouseEvent)
  })
  
  // 滑鼠離開
  container.addEventListener('mouseleave', () => {
    handlers.handleMouseLeave()
  })
  
  // 滑鼠滾輪 - Zoom
  container.addEventListener('wheel', (e) => {
    handlers.handleWheel(e as WheelEvent)
  }, { passive: false })
  
  // 滑鼠拖曳 - Pan
  container.addEventListener('mousedown', (e) => {
    handlers.handleMouseDown(e as MouseEvent)
  })
  
  container.addEventListener('mouseup', () => {
    handlers.handleMouseUp()
  })
  
  // TradingView Charts 內建的 Crosshair 事件
  chartInstance.subscribeCrosshairMove((param) => {
    if (!param.time || !param.seriesData.size) {
      crosshair.value.visible = false
      return
    }
    
    const seriesData = param.seriesData.get(candlestickSeries!) as CandlestickData | undefined
    if (seriesData) {
      crosshair.value.dataPoint = {
        time: seriesData.time as string,
        open: seriesData.open,
        high: seriesData.high,
        low: seriesData.low,
        close: seriesData.close,
        volume: 0 // TradingView 不提供 volume，需從原始資料查詢
      }
      
      // 從原始資料補齊 volume
      const originalData = data.value.find(d => d.time === seriesData.time)
      if (originalData) {
        crosshair.value.dataPoint!.volume = originalData.volume
      }
      
      crosshair.value.visible = true
    }
  })
}

/**
 * 更新 Crosshair 位置
 */
function updateCrosshair(event: MouseEvent): void {
  if (!chartContainerRef.value) return
  
  const rect = chartContainerRef.value.getBoundingClientRect()
  crosshair.value.x = event.clientX - rect.left
  crosshair.value.y = event.clientY - rect.top
}

/**
 * 放大
 */
function handleZoomIn(): void {
  if (!chartInstance) return
  
  const timeScale = chartInstance.timeScale()
  const visibleRange = timeScale.getVisibleRange()
  
  if (visibleRange) {
    const range = (visibleRange.to as number) - (visibleRange.from as number)
    const newRange = range * 0.8
    const center = ((visibleRange.from as number) + (visibleRange.to as number)) / 2
    
    timeScale.setVisibleRange({
      from: (center - newRange / 2) as any,
      to: (center + newRange / 2) as any
    })
    
    zoom.value.zoomLevel = Math.min(10, zoom.value.zoomLevel * 1.1)
  }
}

/**
 * 縮小
 */
function handleZoomOut(): void {
  if (!chartInstance) return
  
  const timeScale = chartInstance.timeScale()
  const visibleRange = timeScale.getVisibleRange()
  
  if (visibleRange) {
    const range = (visibleRange.to as number) - (visibleRange.from as number)
    const newRange = range * 1.2
    const center = ((visibleRange.from as number) + (visibleRange.to as number)) / 2
    
    timeScale.setVisibleRange({
      from: (center - newRange / 2) as any,
      to: (center + newRange / 2) as any
    })
    
    zoom.value.zoomLevel = Math.max(0.1, zoom.value.zoomLevel * 0.9)
  }
}

/**
 * 重試載入
 */
function handleRetry(): void {
  refetch()
}

/**
 * 調整圖表大小
 */
function handleResize(): void {
  if (!chartInstance || !chartContainerRef.value) return
  
  chartInstance.resize(chartContainerRef.value.clientWidth, 400)
}

// Lifecycle
onMounted(async () => {
  // 載入圖表資料
  const params: ChartQueryParams = {
    stock_code: props.stockCode,
    start_date: props.startDate,
    end_date: props.endDate
  }
  
  await fetchChart(params)
  
  // 初始化圖表
  if (isSuccess.value) {
    initChart()
    updateChartData()
  }
  
  // 視窗大小變更監聽
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  // 清理圖表實例
  if (chartInstance) {
    chartInstance.remove()
    chartInstance = null
    candlestickSeries = null
  }
  
  window.removeEventListener('resize', handleResize)
})

// 監聽資料變更
watch(data, () => {
  if (isSuccess.value && chartInstance) {
    updateChartData()
  }
})

// 監聽 props 變更
watch(() => [props.stockCode, props.startDate, props.endDate], async () => {
  const params: ChartQueryParams = {
    stock_code: props.stockCode,
    start_date: props.startDate,
    end_date: props.endDate
  }
  
  await fetchChart(params)
  
  if (isSuccess.value && chartInstance) {
    updateChartData()
  }
})
</script>

<style scoped>
.chart-widget {
  width: 100%;
  height: 100%;
  min-height: 400px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chart-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chart-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.stock-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #212529;
}

.chart-info {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6c757d;
}

.data-points::before {
  content: '📊 ';
}

.date-range::before {
  content: '📅 ';
}

.chart-canvas {
  flex: 1;
  position: relative;
  min-height: 400px;
}

.crosshair-info {
  position: absolute;
  top: 60px;
  left: 1rem;
  background-color: rgba(255, 255, 255, 0.95);
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.ohlcv-data {
  display: flex;
  gap: 0.75rem;
}

.ohlcv-data span {
  color: #495057;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-top: 1px solid #e9ecef;
  background-color: #f8f9fa;
}

.control-button {
  padding: 0.375rem 0.75rem;
  background-color: white;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.control-button:hover:not(:disabled) {
  background-color: #e9ecef;
  border-color: #adb5bd;
}

.control-button:active:not(:disabled) {
  transform: scale(0.95);
}

.control-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.zoom-level {
  margin-left: auto;
  font-size: 0.75rem;
  color: #6c757d;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .chart-widget {
    background-color: #1a1a1a;
  }
  
  .chart-header {
    border-bottom-color: #2a2a2a;
  }
  
  .stock-name {
    color: #f8f9fa;
  }
  
  .chart-info {
    color: #adb5bd;
  }
  
  .crosshair-info {
    background-color: rgba(26, 26, 26, 0.95);
    border-color: #2a2a2a;
  }
  
  .ohlcv-data span {
    color: #adb5bd;
  }
  
  .chart-controls {
    border-top-color: #2a2a2a;
    background-color: #0d0d0d;
  }
  
  .control-button {
    background-color: #1a1a1a;
    border-color: #2a2a2a;
    color: #f8f9fa;
  }
  
  .control-button:hover:not(:disabled) {
    background-color: #2a2a2a;
    border-color: #3a3a3a;
  }
}
</style>
