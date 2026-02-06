/**
 * Chart API Client - Unit Tests
 * 
 * 測試範疇：
 * - 參數驗證
 * - API 呼叫成功
 * - 錯誤處理（網路錯誤、逾時、Backend 錯誤）
 * - 批次查詢
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import { ChartAPI } from '../services/chartApi'
import { ErrorCode } from '../types/chart'
import type { ChartResponse, ChartQueryParams } from '../types/chart'

// Mock axios module
vi.mock('axios')

describe('ChartAPI - 參數驗證', () => {
  let api: ChartAPI

  beforeEach(() => {
    vi.clearAllMocks()
    api = new ChartAPI()
  })

  it('應拒絕過短的股票代碼', async () => {
    const params: ChartQueryParams = {
      stock_code: '123',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    await expect(api.getDailyChart(params)).rejects.toMatchObject({
      code: ErrorCode.INVALID_STOCK_CODE,
      message: '股票代碼格式錯誤'
    })
  })

  it('應拒絕過長的股票代碼', async () => {
    const params: ChartQueryParams = {
      stock_code: '12345678901',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    await expect(api.getDailyChart(params)).rejects.toMatchObject({
      code: ErrorCode.INVALID_STOCK_CODE
    })
  })

  it('應拒絕包含特殊字元的股票代碼', async () => {
    const params: ChartQueryParams = {
      stock_code: '2330@',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    await expect(api.getDailyChart(params)).rejects.toMatchObject({
      code: ErrorCode.INVALID_STOCK_CODE
    })
  })

  it('應拒絕錯誤的日期格式', async () => {
    const params: ChartQueryParams = {
      stock_code: '2330',
      start_date: '2024/01/01',
      end_date: '2024-01-31'
    }

    await expect(api.getDailyChart(params)).rejects.toMatchObject({
      code: ErrorCode.INVALID_DATE_FORMAT
    })
  })

  it('應拒絕起始日期晚於結束日期', async () => {
    const params: ChartQueryParams = {
      stock_code: '2330',
      start_date: '2024-02-01',
      end_date: '2024-01-01'
    }

    await expect(api.getDailyChart(params)).rejects.toMatchObject({
      code: ErrorCode.INVALID_DATE_RANGE
    })
  })
})

describe('ChartAPI - API 呼叫', () => {
  let api: ChartAPI
  let mockAxiosInstance: any

  beforeEach(() => {
    vi.clearAllMocks()
    
    mockAxiosInstance = {
      get: vi.fn()
    }
    
    vi.mocked(axios.create).mockReturnValue(mockAxiosInstance as any)
    
    api = new ChartAPI()
  })

  it('應正確呼叫 Backend API', async () => {
    const params: ChartQueryParams = {
      stock_code: '2330',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    const mockResponse: ChartResponse = {
      stock_code: '2330',
      chart_data: [{
        time: '2024-01-15',
        open: 580.0,
        high: 585.0,
        low: 578.0,
        close: 583.0,
        volume: 12345678
      }],
      metadata: {
        stock_code: '2330',
        start_date: '2024-01-15',
        end_date: '2024-01-15',
        data_points: 1
      }
    }

    mockAxiosInstance.get.mockResolvedValue({ data: mockResponse })

    const result = await api.getDailyChart(params)

    expect(mockAxiosInstance.get).toHaveBeenCalledWith('/api/chart/daily', {
      params: {
        stock_code: '2330',
        start_date: '2024-01-01',
        end_date: '2024-01-31'
      }
    })
    expect(result).toEqual(mockResponse)
  })

  it('應正確處理查無資料情況', async () => {
    const params: ChartQueryParams = {
      stock_code: '9999',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    const mockResponse: ChartResponse = {
      stock_code: '9999',
      chart_data: [],
      metadata: {
        stock_code: '9999',
        start_date: '2024-01-01',
        end_date: '2024-01-31',
        data_points: 0
      }
    }

    mockAxiosInstance.get.mockResolvedValue({ data: mockResponse })

    const result = await api.getDailyChart(params)
    expect(result.chart_data).toHaveLength(0)
    expect(result.metadata?.data_points).toBe(0)
  })
})

describe('ChartAPI - 錯誤處理', () => {
  let api: ChartAPI
  let mockAxiosInstance: any

  beforeEach(() => {
    vi.clearAllMocks()
    
    mockAxiosInstance = {
      get: vi.fn()
    }
    
    vi.mocked(axios.create).mockReturnValue(mockAxiosInstance as any)
    vi.mocked(axios.isAxiosError).mockReturnValue(true)
    
    api = new ChartAPI()
  })

  it('應處理網路錯誤', async () => {
    const params: ChartQueryParams = {
      stock_code: '2330',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    const networkError = {
      isAxiosError: true,
      code: 'ERR_NETWORK',
      message: 'Network Error',
      response: undefined
    }

    mockAxiosInstance.get.mockRejectedValue(networkError)

    await expect(api.getDailyChart(params)).rejects.toMatchObject({
      code: ErrorCode.NETWORK_ERROR,
      message: '無法連線至伺服器'
    })
  })

  it('應處理請求逾時', async () => {
    const params: ChartQueryParams = {
      stock_code: '2330',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    const timeoutError = {
      isAxiosError: true,
      code: 'ETIMEDOUT',
      message: 'Timeout Error'
    }

    mockAxiosInstance.get.mockRejectedValue(timeoutError)

    await expect(api.getDailyChart(params)).rejects.toMatchObject({
      code: ErrorCode.TIMEOUT_ERROR,
      message: '請求逾時，請稍後再試'
    })
  })

  it('應處理 Backend 回傳的錯誤格式', async () => {
    const params: ChartQueryParams = {
      stock_code: '2330',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    const backendError = {
      isAxiosError: true,
      response: {
        status: 500,
        data: {
          code: ErrorCode.DATABASE_ERROR,
          message: '資料庫連線錯誤',
          details: 'Connection timeout'
        }
      }
    }

    mockAxiosInstance.get.mockRejectedValue(backendError)

    await expect(api.getDailyChart(params)).rejects.toMatchObject({
      code: ErrorCode.DATABASE_ERROR,
      message: '資料庫連線錯誤'
    })
  })

  it('應處理 HTTP 錯誤狀態碼', async () => {
    const params: ChartQueryParams = {
      stock_code: '2330',
      start_date: '2024-01-01',
      end_date: '2024-01-31'
    }

    const httpError = {
      isAxiosError: true,
      response: {
        status: 503,
        data: {}
      },
      message: 'Service Unavailable'
    }

    mockAxiosInstance.get.mockRejectedValue(httpError)

    await expect(api.getDailyChart(params)).rejects.toMatchObject({
      code: ErrorCode.INTERNAL_ERROR,
      message: '伺服器錯誤 (HTTP 503)'
    })
  })
})
