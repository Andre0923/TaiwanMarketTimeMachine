/**
 * useChartData Composable - Unit Tests
 * 
 * 測試範疇：
 * - fetchChart 資料取得
 * - 狀態管理 (loading/success/error)
 * - refetch 重新載入
 * - reset 重置狀態
 * - useBatchChartData 批次查詢
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useChartData, useBatchChartData } from '../composables/useChartData'
import { chartAPI } from '../services/chartApi'
import { ErrorCode } from '../types/chart'
import type { ChartResponse, ErrorResponse } from '../types/chart'

// Mock chartAPI
vi.mock('../services/chartApi', () => ({
  chartAPI: {
    getDailyChart: vi.fn(),
    batchGetDailyChart: vi.fn()
  }
}))

describe('useChartData', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('初始狀態應為 idle', () => {
    const { state, isLoading, isSuccess, isError, data } = useChartData()
    
    expect(state.value).toBe('idle')
    expect(isLoading.value).toBe(false)
    expect(isSuccess.value).toBe(false)
    expect(isError.value).toBe(false)
    expect(data.value).toEqual([])
  })

  it('fetchChart 成功時應更新資料與狀態', async () => {
    const mockResponse: ChartResponse = {
      stock_code: '2330',
      chart_data: [
        {
          time: '2024-01-15',
          open: 580.0,
          high: 585.0,
          low: 578.0,
          close: 583.0,
          volume: 12345678
        }
      ],
      metadata: {
        stock_code: '2330',
        start_date: '2024-01-15',
        end_date: '2024-01-15',
        data_points: 1
      }
    }

    vi.mocked(chartAPI.getDailyChart).mockResolvedValue(mockResponse)

    const { data, metadata, state, isLoading, isSuccess, fetchChart } = useChartData()

    // 開始載入
    const promise = fetchChart({
      stock_code: '2330',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    })

    // 載入中
    expect(state.value).toBe('loading')
    expect(isLoading.value).toBe(true)

    await promise

    // 載入完成
    expect(state.value).toBe('success')
    expect(isSuccess.value).toBe(true)
    expect(isLoading.value).toBe(false)
    expect(data.value).toEqual(mockResponse.chart_data)
    expect(metadata.value).toEqual(mockResponse.metadata)
  })

  it('fetchChart 失敗時應設定錯誤狀態', async () => {
    const mockError: ErrorResponse = {
      code: ErrorCode.NETWORK_ERROR,
      message: '無法連線至伺服器'
    }

    vi.mocked(chartAPI.getDailyChart).mockRejectedValue(mockError)

    const { data, error, state, isError, fetchChart } = useChartData()

    await fetchChart({
      stock_code: '2330',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    })

    expect(state.value).toBe('error')
    expect(isError.value).toBe(true)
    expect(error.value).toEqual(mockError)
    expect(data.value).toEqual([]) // 錯誤時應清空資料
  })

  it('refetch 應使用最後一次查詢參數', async () => {
    const mockResponse: ChartResponse = {
      stock_code: '2330',
      chart_data: [],
      metadata: {
        stock_code: '2330',
        start_date: '2024-01-01',
        end_date: '2024-01-31',
        data_points: 0
      }
    }

    vi.mocked(chartAPI.getDailyChart).mockResolvedValue(mockResponse)

    const { fetchChart, refetch } = useChartData()

    const params = {
      stock_code: '2330',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    await fetchChart(params)
    
    // 清除 mock 呼叫記錄
    vi.mocked(chartAPI.getDailyChart).mockClear()

    await refetch()

    // 驗證使用相同參數
    expect(chartAPI.getDailyChart).toHaveBeenCalledWith(params)
  })

  it('refetch 無先前參數時應警告', async () => {
    const consoleSpy = vi.spyOn(console, 'warn').mockImplementation(() => {})
    
    const { refetch } = useChartData()
    
    await refetch()
    
    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringContaining('refetch: 無先前查詢參數')
    )
    
    consoleSpy.mockRestore()
  })

  it('reset 應清空所有狀態', async () => {
    const mockResponse: ChartResponse = {
      stock_code: '2330',
      chart_data: [
        {
          time: '2024-01-15',
          open: 580.0,
          high: 585.0,
          low: 578.0,
          close: 583.0,
          volume: 12345678
        }
      ],
      metadata: {
        stock_code: '2330',
        start_date: '2024-01-15',
        end_date: '2024-01-15',
        data_points: 1
      }
    }

    vi.mocked(chartAPI.getDailyChart).mockResolvedValue(mockResponse)

    const { data, metadata, state, error, fetchChart, reset } = useChartData()

    // 先載入資料
    await fetchChart({
      stock_code: '2330',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    })

    expect(data.value).toHaveLength(1)

    // 重置
    reset()

    expect(data.value).toEqual([])
    expect(metadata.value).toBeNull()
    expect(state.value).toBe('idle')
    expect(error.value).toBeNull()
  })
})

describe('useBatchChartData', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetchBatch 應批次取得多個股票資料', async () => {
    const mockResponses: ChartResponse[] = [
      {
        stock_code: '2330',
        chart_data: [],
        metadata: {
          stock_code: '2330',
          start_date: '2024-01-01',
          end_date: '2024-01-31',
          data_points: 0
        }
      },
      {
        stock_code: '2317',
        chart_data: [],
        metadata: {
          stock_code: '2317',
          start_date: '2024-01-01',
          end_date: '2024-01-31',
          data_points: 0
        }
      }
    ]

    vi.mocked(chartAPI.batchGetDailyChart).mockResolvedValue(mockResponses)

    const { results, state, fetchBatch } = useBatchChartData()

    await fetchBatch([
      { stock_code: '2330', start_date: '2024-01-01', end_date: '2024-01-31' },
      { stock_code: '2317', start_date: '2024-01-01', end_date: '2024-01-31' }
    ])

    expect(state.value).toBe('success')
    expect(results.value).toHaveLength(2)
    expect(results.value[0].stock_code).toBe('2330')
    expect(results.value[0].error).toBeNull()
    expect(results.value[1].stock_code).toBe('2317')
    expect(results.value[1].error).toBeNull()
  })

  it('fetchBatch 應處理部分失敗情況', async () => {
    const mockResponses = [
      {
        stock_code: '2330',
        chart_data: [],
        metadata: {
          stock_code: '2330',
          start_date: '2024-01-01',
          end_date: '2024-01-31',
          data_points: 0
        }
      },
      {
        code: ErrorCode.INVALID_STOCK_CODE,
        message: '股票代碼格式錯誤'
      }
    ]

    vi.mocked(chartAPI.batchGetDailyChart).mockResolvedValue(mockResponses as any)

    const { results, fetchBatch } = useBatchChartData()

    await fetchBatch([
      { stock_code: '2330', start_date: '2024-01-01', end_date: '2024-01-31' },
      { stock_code: 'INVALID', start_date: '2024-01-01', end_date: '2024-01-31' }
    ])

    expect(results.value).toHaveLength(2)
    expect(results.value[0].error).toBeNull()
    expect(results.value[1].error).not.toBeNull()
    expect(results.value[1].error?.code).toBe(ErrorCode.INVALID_STOCK_CODE)
  })

  it('reset 應清空批次結果', async () => {
    const mockResponses: ChartResponse[] = [
      {
        stock_code: '2330',
        chart_data: [],
        metadata: {
          stock_code: '2330',
          start_date: '2024-01-01',
          end_date: '2024-01-31',
          data_points: 0
        }
      }
    ]

    vi.mocked(chartAPI.batchGetDailyChart).mockResolvedValue(mockResponses)

    const { results, state, fetchBatch, reset } = useBatchChartData()

    await fetchBatch([
      { stock_code: '2330', start_date: '2024-01-01', end_date: '2024-01-31' }
    ])

    expect(results.value).toHaveLength(1)

    reset()

    expect(results.value).toEqual([])
    expect(state.value).toBe('idle')
  })
})
