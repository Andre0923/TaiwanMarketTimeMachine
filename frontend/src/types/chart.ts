/**
 * Chart Type Definitions
 * 
 * 對應 System Spec: specs/system/data-model.md
 * 對應 API 契約: specs/system/contracts/chart-api.md
 */

/**
 * ChartDataPoint - 單一時間點的 OHLCV 資料
 * 
 * @property time - 交易日期 (YYYY-MM-DD)
 * @property open - 開盤價
 * @property high - 最高價
 * @property low - 最低價
 * @property close - 收盤價
 * @property volume - 成交量
 */
export interface ChartDataPoint {
  time: string
  open: number
  high: number
  low: number
  close: number
  volume: number
}

/**
 * ChartMetadata - 查詢結果的元資料
 * 
 * @property stock_code - 股票代碼
 * @property start_date - 查詢起始日期
 * @property end_date - 查詢結束日期
 * @property data_points - 回傳的資料點數量
 */
export interface ChartMetadata {
  stock_code: string
  start_date: string
  end_date: string
  data_points: number
}

/**
 * ChartResponse - API 回應格式
 * 
 * @property stock_code - 股票代碼
 * @property chart_data - OHLCV 資料陣列
 * @property metadata - 查詢結果元資料
 */
export interface ChartResponse {
  stock_code: string
  chart_data: ChartDataPoint[]
  metadata: ChartMetadata | null
}

/**
 * ErrorCode - 標準錯誤碼列表
 */
export enum ErrorCode {
  INVALID_STOCK_CODE = 'INVALID_STOCK_CODE',
  INVALID_DATE_RANGE = 'INVALID_DATE_RANGE',
  INVALID_DATE_FORMAT = 'INVALID_DATE_FORMAT',
  NO_DATA = 'NO_DATA',
  DATABASE_ERROR = 'DATABASE_ERROR',
  INTERNAL_ERROR = 'INTERNAL_ERROR',
  NETWORK_ERROR = 'NETWORK_ERROR', // 前端專屬錯誤碼
  TIMEOUT_ERROR = 'TIMEOUT_ERROR'  // 前端專屬錯誤碼
}

/**
 * ErrorResponse - 統一錯誤回應格式
 * 
 * @property code - 錯誤碼
 * @property message - 錯誤訊息摘要
 * @property details - 詳細錯誤說明（選填）
 */
export interface ErrorResponse {
  code: ErrorCode
  message: string
  details?: string
}

/**
 * ChartQueryParams - API 查詢參數
 * 
 * @property stock_code - 股票代碼（4-10 字元）
 * @property start_date - 起始日期（YYYY-MM-DD）
 * @property end_date - 結束日期（YYYY-MM-DD）
 */
export interface ChartQueryParams {
  stock_code: string
  start_date: string
  end_date: string
}

/**
 * ChartLoadingState - 圖表載入狀態
 */
export type ChartLoadingState = 'idle' | 'loading' | 'success' | 'error'

/**
 * ChartData - 圖表元件使用的資料結構
 * 
 * @property data - OHLCV 資料
 * @property metadata - 元資料
 * @property state - 載入狀態
 * @property error - 錯誤資訊（若有）
 */
export interface ChartData {
  data: ChartDataPoint[]
  metadata: ChartMetadata | null
  state: ChartLoadingState
  error: ErrorResponse | null
}
