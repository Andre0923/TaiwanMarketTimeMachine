/**
 * useChartInteraction Composable
 * 
 * 用途：管理圖表互動邏輯
 * - Zoom（滑鼠滾輪縮放）
 * - Pan（拖曳平移）
 * - Crosshair（十字線與資料顯示）
 * 
 * 對應 US A-2: 圖表互動操作
 * 
 * 注意：本檔案為 placeholder，實際整合需在 Phase 3 搭配 TradingView Lightweight Charts
 */

import { ref, computed, type Ref } from 'vue'
import type { ChartDataPoint } from '../types/chart'

/**
 * 十字線資訊
 */
export interface CrosshairData {
  /** 是否顯示十字線 */
  visible: boolean
  /** 十字線對應的資料點 */
  dataPoint: ChartDataPoint | null
  /** 滑鼠位置 X */
  x: number
  /** 滑鼠位置 Y */
  y: number
}

/**
 * 縮放狀態
 */
export interface ZoomState {
  /** 可見時間範圍起點 */
  visibleRangeStart: string | null
  /** 可見時間範圍終點 */
  visibleRangeEnd: string | null
  /** 縮放層級（1.0 = 原始）*/
  zoomLevel: number
}

/**
 * useChartInteraction 返回值
 */
export interface UseChartInteractionReturn {
  /** 十字線資訊 */
  crosshair: Ref<CrosshairData>
  /** 縮放狀態 */
  zoom: Ref<ZoomState>
  /** 是否正在拖曳 */
  isPanning: Ref<boolean>
  /** 是否啟用互動 */
  interactionEnabled: Ref<boolean>
  /** 事件處理器集合 */
  handlers: {
    /** 處理滑鼠移動（十字線）*/
    handleMouseMove: (event: MouseEvent) => void
    /** 處理滑鼠離開 */
    handleMouseLeave: (event?: MouseEvent) => void
    /** 處理滑鼠滾輪（縮放）*/
    handleWheel: (event: WheelEvent) => void
    /** 處理滑鼠按下（開始拖曳）*/
    handleMouseDown: (event: MouseEvent) => void
    /** 處理滑鼠放開（結束拖曳）*/
    handleMouseUp: (event?: MouseEvent) => void
  }
  /** 重置縮放 */
  resetZoom: () => void
  /** 啟用/停用互動 */
  setInteractionEnabled: (enabled: boolean) => void
}

/**
 * useChartInteraction Composable
 * 
 * @example
 * ```vue
 * <script setup>
 * import { useChartInteraction } from '@/composables/useChartInteraction'
 * 
 * const {
 *   crosshair,
 *   zoom,
 *   isPanning,
 *   handleMouseMove,
 *   handleWheel,
 *   handleMouseDown,
 *   handleMouseUp
 * } = useChartInteraction()
 * </script>
 * 
 * <template>
 *   <div
 *     @mousemove="handleMouseMove"
 *     @wheel="handleWheel"
 *     @mousedown="handleMouseDown"
 *     @mouseup="handleMouseUp"
 *   >
 *     <ChartWidget />
 *     <CrosshairInfo v-if="crosshair.visible" :data="crosshair.dataPoint" />
 *   </div>
 * </template>
 * ```
 */
export function useChartInteraction(): UseChartInteractionReturn {
  // State
  const crosshair = ref<CrosshairData>({
    visible: false,
    dataPoint: null,
    x: 0,
    y: 0
  })

  const zoom = ref<ZoomState>({
    visibleRangeStart: null,
    visibleRangeEnd: null,
    zoomLevel: 1.0
  })

  const isPanning = ref(false)
  const interactionEnabled = ref(true)

  // 拖曳起始位置
  const panStartX = ref(0)
  const panStartY = ref(0)

  /**
   * 處理滑鼠移動（十字線）
   * 
   * 注意：實際實作需整合 TradingView Lightweight Charts API
   * 目前為 placeholder 實作
   */
  function handleMouseMove(event: MouseEvent): void {
    if (!interactionEnabled.value) return

    // 更新十字線位置
    crosshair.value = {
      visible: true,
      dataPoint: null, // TODO: 從 chart API 取得對應資料點
      x: event.clientX,
      y: event.clientY
    }

    // 如果正在拖曳，計算平移偏移量
    if (isPanning.value) {
      const deltaX = event.clientX - panStartX.value
      const deltaY = event.clientY - panStartY.value
      
      // TODO: 更新圖表平移位置
      console.debug('[useChartInteraction] Pan delta:', { deltaX, deltaY })
      
      // 更新起始位置
      panStartX.value = event.clientX
      panStartY.value = event.clientY
    }
  }

  /**
   * 處理滑鼠離開
   */
  function handleMouseLeave(): void {
    crosshair.value.visible = false
    isPanning.value = false
  }

  /**
   * 處理滑鼠滾輪（縮放）
   * 
   * 注意：實際實作需整合 TradingView Lightweight Charts API
   */
  function handleWheel(event: WheelEvent): void {
    if (!interactionEnabled.value) return

    event.preventDefault()

    // 計算縮放比例
    const zoomFactor = event.deltaY > 0 ? 0.9 : 1.1
    const newZoomLevel = zoom.value.zoomLevel * zoomFactor

    // 限制縮放範圍 (0.1x ~ 10x)
    zoom.value.zoomLevel = Math.max(0.1, Math.min(10, newZoomLevel))

    // TODO: 更新圖表縮放
    console.debug('[useChartInteraction] Zoom level:', zoom.value.zoomLevel)
  }

  /**
   * 處理滑鼠按下（開始拖曳）
   */
  function handleMouseDown(event: MouseEvent): void {
    if (!interactionEnabled.value) return

    isPanning.value = true
    panStartX.value = event.clientX
    panStartY.value = event.clientY
  }

  /**
   * 處理滑鼠放開（結束拖曳）
   */
  function handleMouseUp(): void {
    isPanning.value = false
  }

  /**
   * 重置縮放至原始狀態
   */
  function resetZoom(): void {
    zoom.value = {
      visibleRangeStart: null,
      visibleRangeEnd: null,
      zoomLevel: 1.0
    }
    
    // TODO: 更新圖表縮放
    console.debug('[useChartInteraction] Zoom reset')
  }

  /**
   * 啟用/停用互動
   */
  function setInteractionEnabled(enabled: boolean): void {
    interactionEnabled.value = enabled
    
    if (!enabled) {
      // 停用時重置所有狀態
      crosshair.value.visible = false
      isPanning.value = false
      zoom.value = {
        visibleRangeStart: null,
        visibleRangeEnd: null,
        zoomLevel: 1.0
      }
    }
  }

  return {
    // State
    crosshair,
    zoom,
    isPanning,
    interactionEnabled,
    
    // Event Handlers (grouped)
    handlers: {
      handleMouseMove,
      handleMouseLeave,
      handleWheel,
      handleMouseDown,
      handleMouseUp
    },
    
    // Methods
    resetZoom,
    setInteractionEnabled
  }
}
