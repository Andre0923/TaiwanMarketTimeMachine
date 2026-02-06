/**
 * Chart API Client
 * 
 * 對應 API 契約: specs/system/contracts/chart-api.md
 * Backend Endpoint: GET /api/chart/daily
 */

import axios, { AxiosError, AxiosInstance } from 'axios'
import {
  ErrorCode
} from '../types/chart'
import type {
  ChartResponse,
  ChartQueryParams,
  ErrorResponse
} from '../types/chart'

/**
 * API Client 配置
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_TIMEOUT = 30000 // 30 秒

/**
 * Axios Instance
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * 錯誤處理輔助函式
 * 
 * 將 Axios 錯誤轉換為標準 ErrorResponse 格式
 */
function handleApiError(error: unknown): ErrorResponse {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ErrorResponse>

    // Backend 回傳的標準錯誤格式（檢查 data.code 存在）
    if (axiosError.response?.data?.code) {
      return axiosError.response.data
    }

    // 請求逾時
    if (axiosError.code === 'ECONNABORTED' || axiosError.code === 'ETIMEDOUT') {
      return {
        code: ErrorCode.TIMEOUT_ERROR,
        message: '請求逾時，請稍後再試',
        details: axiosError.message
      }
    }

    // HTTP 錯誤狀態碼（有 response 但沒有標準錯誤格式）
    if (axiosError.response) {
      return {
        code: ErrorCode.INTERNAL_ERROR,
        message: `伺服器錯誤 (HTTP ${axiosError.response.status})`,
        details: axiosError.message
      }
    }

    // 無法連線至伺服器（沒有 response）
    return {
      code: ErrorCode.NETWORK_ERROR,
      message: '無法連線至伺服器',
      details: axiosError.message
    }
  }

  // 未知錯誤
  return {
    code: ErrorCode.INTERNAL_ERROR,
    message: '發生未知錯誤',
    details: error instanceof Error ? error.message : String(error)
  }
}

/**
 * 參數驗證輔助函式
 * 
 * 驗證查詢參數是否符合 API 契約
 */
function validateQueryParams(params: ChartQueryParams): ErrorResponse | null {
  // 驗證 stock_code（4-10 字元，數字與大寫英文）
  if (!params.stock_code || params.stock_code.length < 4 || params.stock_code.length > 10) {
    return {
      code: ErrorCode.INVALID_STOCK_CODE,
      message: '股票代碼格式錯誤',
      details: '股票代碼必須為 4-10 個字元'
    }
  }

  if (!/^[A-Z0-9]+$/.test(params.stock_code)) {
    return {
      code: ErrorCode.INVALID_STOCK_CODE,
      message: '股票代碼格式錯誤',
      details: '股票代碼只能包含數字與大寫英文'
    }
  }

  // 驗證日期格式（YYYY-MM-DD）
  const datePattern = /^\d{4}-\d{2}-\d{2}$/
  if (!datePattern.test(params.start_date) || !datePattern.test(params.end_date)) {
    return {
      code: ErrorCode.INVALID_DATE_FORMAT,
      message: '日期格式錯誤',
      details: '日期格式必須為 YYYY-MM-DD'
    }
  }

  // 驗證日期範圍
  const startDate = new Date(params.start_date)
  const endDate = new Date(params.end_date)
  
  if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
    return {
      code: ErrorCode.INVALID_DATE_FORMAT,
      message: '日期格式錯誤',
      details: '日期必須為有效的日期值'
    }
  }

  if (startDate > endDate) {
    return {
      code: ErrorCode.INVALID_DATE_RANGE,
      message: '日期範圍錯誤',
      details: '起始日期不能晚於結束日期'
    }
  }

  return null
}

/**
 * ChartAPI - 圖表 API 服務
 */
export class ChartAPI {
  /**
   * 取得日K線資料
   * 
   * @param params - 查詢參數
   * @returns ChartResponse 或拋出 ErrorResponse
   * 
   * @example
   * ```typescript
   * const api = new ChartAPI()
   * try {
   *   const response = await api.getDailyChart({
   *     stock_code: '2330',
   *     start_date: '2024-01-01',
   *     end_date: '2024-01-31'
   *   })
   *   console.log(response.chart_data)
   * } catch (error) {
   *   console.error(error)
   * }
   * ```
   */
  async getDailyChart(params: ChartQueryParams): Promise<ChartResponse> {
    // 前端參數驗證
    const validationError = validateQueryParams(params)
    if (validationError) {
      throw validationError
    }

    try {
      const response = await apiClient.get<ChartResponse>('/api/chart/daily', {
        params: {
          stock_code: params.stock_code,
          start_date: params.start_date,
          end_date: params.end_date
        }
      })

      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  }

  /**
   * 批次查詢多個股票的日K線資料
   * 
   * @param paramsArray - 查詢參數陣列
   * @returns ChartResponse 陣列（失敗的請求會被標記為 null）
   * 
   * @example
   * ```typescript
   * const api = new ChartAPI()
   * const results = await api.batchGetDailyChart([
   *   { stock_code: '2330', start_date: '2024-01-01', end_date: '2024-01-31' },
   *   { stock_code: '2317', start_date: '2024-01-01', end_date: '2024-01-31' }
   * ])
   * ```
   */
  async batchGetDailyChart(
    paramsArray: ChartQueryParams[]
  ): Promise<Array<ChartResponse | ErrorResponse>> {
    const promises = paramsArray.map(params =>
      this.getDailyChart(params)
        .then(response => response)
        .catch(error => error as ErrorResponse)
    )

    return Promise.all(promises)
  }
}

/**
 * 預設匯出 - 單例 API 客戶端
 */
export const chartAPI = new ChartAPI()
