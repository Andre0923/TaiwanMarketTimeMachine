/**
 * ChartWidget Integration Tests
 * 
 * 整合測試：驗證 ChartWidget 與 composables 的協作
 * 注意：不測試真實 API 呼叫，使用 mock
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import ChartWidget from './ChartWidget.vue'
import { chartAPI } from '../services/chartApi'
import type { ChartResponse } from '../types/chart'

// Mock chartAPI
vi.mock('../services/chartApi', () => ({
  chartAPI: {
    getDailyChart: vi.fn()
  }
}))

// Mock TradingView Charts
vi.mock('lightweight-charts', () => ({
  createChart: vi.fn(() => ({
    addCandlestickSeries: vi.fn(() => ({
      setData: vi.fn()
    })),
    subscribeCrosshairMove: vi.fn(),
    timeScale: vi.fn(() => ({
      fitContent: vi.fn(),
      getVisibleRange: vi.fn(() => ({ from: 0, to: 100 })),
      setVisibleRange: vi.fn()
    })),
    resize: vi.fn(),
    remove: vi.fn()
  }))
}))

describe('ChartWidget Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('應在載入中顯示 ChartLoading 元件', async () => {
    // Mock 一個延遲的 promise
    vi.mocked(chartAPI.getDailyChart).mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({
        stock_code: '2330',
        chart_data: [],
        metadata: {
          stock_code: '2330',
          start_date: '2024-01-01',
          end_date: '2024-01-31',
          data_points: 0
        }
      }), 100))
    )

    const wrapper = mount(ChartWidget, {
      props: {
        stockCode: '2330',
        startDate: '2024-01-01',
        endDate: '2024-01-31'
      }
    })

    // 立即檢查（在載入完成前）
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.chart-loading').exists()).toBe(true)
  })

  it('應在載入成功後顯示圖表', async () => {
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
        start_date: '2024-01-01',
        end_date: '2024-01-31',
        data_points: 1
      }
    }

    vi.mocked(chartAPI.getDailyChart).mockResolvedValue(mockResponse)

    const wrapper = mount(ChartWidget, {
      props: {
        stockCode: '2330',
        startDate: '2024-01-01',
        endDate: '2024-01-31'
      }
    })

    await flushPromises()

    expect(wrapper.find('.chart-container').exists()).toBe(true)
    expect(wrapper.find('.stock-name').text()).toBe('2330')
  })

  it('應在載入失敗後顯示 ChartError 元件', async () => {
    vi.mocked(chartAPI.getDailyChart).mockRejectedValue({
      code: 'NETWORK_ERROR',
      message: '無法連線至伺服器'
    })

    const wrapper = mount(ChartWidget, {
      props: {
        stockCode: '2330',
        startDate: '2024-01-01',
        endDate: '2024-01-31'
      }
    })

    await flushPromises()

    expect(wrapper.find('.chart-error').exists()).toBe(true)
  })

  it('應支援重試功能', async () => {
    vi.mocked(chartAPI.getDailyChart)
      .mockRejectedValueOnce({
        code: 'NETWORK_ERROR',
        message: '無法連線至伺服器'
      })
      .mockResolvedValueOnce({
        stock_code: '2330',
        chart_data: [],
        metadata: {
          stock_code: '2330',
          start_date: '2024-01-01',
          end_date: '2024-01-31',
          data_points: 0
        }
      })

    const wrapper = mount(ChartWidget, {
      props: {
        stockCode: '2330',
        startDate: '2024-01-01',
        endDate: '2024-01-31'
      }
    })

    await flushPromises()

    // 應顯示錯誤
    expect(wrapper.find('.chart-error').exists()).toBe(true)

    // 點擊重試
    await wrapper.find('.retry-button').trigger('click')
    await flushPromises()

    // 應顯示圖表
    expect(wrapper.find('.chart-container').exists()).toBe(true)
  })
})
