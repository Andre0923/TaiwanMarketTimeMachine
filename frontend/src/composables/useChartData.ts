/**
 * useChartData Composable
 * 
 * 用途：管理圖表資料取得與狀態
 * - 封裝 chartAPI 呼叫
 * - 管理 Loading/Success/Error 狀態
 * - 提供 Reactive 資料
 * 
 * 對應 US A-4: 圖表載入狀態與錯誤處理
 */

import { ref, computed, type Ref } from 'vue'
import { chartAPI } from '../services/chartApi'
import type {
  ChartDataPoint,
  ChartMetadata,
  ChartQueryParams,
  ErrorResponse,
  ChartLoadingState
} from '../types/chart'

/**
 * useChartData 返回值
 */
export interface UseChartDataReturn {
  /** 圖表資料點陣列 */
  data: Ref<ChartDataPoint[]>
  /** 查詢結果元資料 */
  metadata: Ref<ChartMetadata | null>
  /** 載入狀態 */
  state: Ref<ChartLoadingState>
  /** 錯誤資訊 */
  error: Ref<ErrorResponse | null>
  /** 是否正在載入 */
  isLoading: Ref<boolean>
  /** 是否載入成功 */
  isSuccess: Ref<boolean>
  /** 是否發生錯誤 */
  isError: Ref<boolean>
  /** 取得圖表資料 */
  fetchChart: (params: ChartQueryParams) => Promise<void>
  /** 重新載入 */
  refetch: () => Promise<void>
  /** 清空資料 */
  reset: () => void
}

/**
 * useChartData Composable
 * 
 * @example
 * ```vue
 * <script setup>
 * import { useChartData } from '@/composables/useChartData'
 * 
 * const { data, isLoading, isError, error, fetchChart } = useChartData()
 * 
 * // 取得圖表資料
 * await fetchChart({
 *   stock_code: '2330',
 *   start_date: '2024-01-01',
 *   end_date: '2024-01-31'
 * })
 * </script>
 * ```
 */
export function useChartData(): UseChartDataReturn {
  // State
  const data = ref<ChartDataPoint[]>([])
  const metadata = ref<ChartMetadata | null>(null)
  const state = ref<ChartLoadingState>('idle')
  const error = ref<ErrorResponse | null>(null)
  
  // 儲存最後一次查詢參數（用於 refetch）
  const lastParams = ref<ChartQueryParams | null>(null)

  // Computed
  const isLoading = computed(() => state.value === 'loading')
  const isSuccess = computed(() => state.value === 'success')
  const isError = computed(() => state.value === 'error')

  /**
   * 取得圖表資料
   * 
   * @param params - 查詢參數
   */
  async function fetchChart(params: ChartQueryParams): Promise<void> {
    // 重置狀態
    state.value = 'loading'
    error.value = null
    lastParams.value = params

    try {
      const response = await chartAPI.getDailyChart(params)
      
      // 更新資料
      data.value = response.chart_data
      metadata.value = response.metadata
      state.value = 'success'
    } catch (err) {
      // 錯誤處理
      error.value = err as ErrorResponse
      state.value = 'error'
      
      // 清空資料
      data.value = []
      metadata.value = null
      
      console.error('[useChartData] 取得圖表資料失敗:', err)
    }
  }

  /**
   * 重新載入（使用最後一次查詢參數）
   */
  async function refetch(): Promise<void> {
    if (!lastParams.value) {
      console.warn('[useChartData] refetch: 無先前查詢參數')
      return
    }
    
    await fetchChart(lastParams.value)
  }

  /**
   * 重置所有狀態
   */
  function reset(): void {
    data.value = []
    metadata.value = null
    state.value = 'idle'
    error.value = null
    lastParams.value = null
  }

  return {
    // Data
    data,
    metadata,
    state,
    error,
    
    // Computed
    isLoading,
    isSuccess,
    isError,
    
    // Methods
    fetchChart,
    refetch,
    reset
  }
}

/**
 * useBatchChartData Composable
 * 
 * 用途：批次取得多個股票的圖表資料
 * 
 * @example
 * ```vue
 * <script setup>
 * import { useBatchChartData } from '@/composables/useChartData'
 * 
 * const { results, fetchBatch } = useBatchChartData()
 * 
 * await fetchBatch([
 *   { stock_code: '2330', start_date: '2024-01-01', end_date: '2024-01-31' },
 *   { stock_code: '2317', start_date: '2024-01-01', end_date: '2024-01-31' }
 * ])
 * </script>
 * ```
 */
export interface UseBatchChartDataReturn {
  /** 批次查詢結果（成功或錯誤） */
  results: Ref<Array<{ stock_code: string; data: ChartDataPoint[]; error: ErrorResponse | null }>>
  /** 整體載入狀態 */
  state: Ref<ChartLoadingState>
  /** 是否正在載入 */
  isLoading: Ref<boolean>
  /** 批次取得圖表資料 */
  fetchBatch: (paramsArray: ChartQueryParams[]) => Promise<void>
  /** 清空結果 */
  reset: () => void
}

export function useBatchChartData(): UseBatchChartDataReturn {
  const results = ref<Array<{ stock_code: string; data: ChartDataPoint[]; error: ErrorResponse | null }>>([])
  const state = ref<ChartLoadingState>('idle')
  
  const isLoading = computed(() => state.value === 'loading')

  async function fetchBatch(paramsArray: ChartQueryParams[]): Promise<void> {
    state.value = 'loading'
    results.value = []

    try {
      const responses = await chartAPI.batchGetDailyChart(paramsArray)
      
      results.value = responses.map((response, index) => {
        // 判斷是成功回應還是錯誤回應
        if ('chart_data' in response) {
          return {
            stock_code: paramsArray[index].stock_code,
            data: response.chart_data,
            error: null
          }
        } else {
          return {
            stock_code: paramsArray[index].stock_code,
            data: [],
            error: response as ErrorResponse
          }
        }
      })
      
      state.value = 'success'
    } catch (err) {
      console.error('[useBatchChartData] 批次取得失敗:', err)
      state.value = 'error'
    }
  }

  function reset(): void {
    results.value = []
    state.value = 'idle'
  }

  return {
    results,
    state,
    isLoading,
    fetchBatch,
    reset
  }
}
