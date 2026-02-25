import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import ChartGrid from './ChartGrid.vue'
import ChartWidget from './ChartWidget.vue'

// Mock ChartWidget
vi.mock('./ChartWidget.vue', () => ({
  default: {
    name: 'ChartWidget',
    template: '<div class="mock-chart-widget"></div>',
    props: ['stockCode', 'startDate', 'endDate', 'loadingMessage']
  }
}))

describe('ChartGrid', () => {
  const mockCharts = [
    { stockCode: '2330', startDate: '2024-01-01', endDate: '2024-01-31' },
    { stockCode: '2317', startDate: '2024-01-01', endDate: '2024-01-31' },
    { stockCode: '2454', startDate: '2024-01-01', endDate: '2024-01-31' }
  ]

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('應正確渲染網格標題', () => {
    const wrapper = mount(ChartGrid, {
      props: {
        charts: mockCharts
      }
    })

    expect(wrapper.find('.grid-title').text()).toBe('多股票監控面板')
  })

  it('應根據 charts 陣列渲染對應數量的圖表', () => {
    const wrapper = mount(ChartGrid, {
      props: {
        charts: mockCharts
      }
    })

    const gridItems = wrapper.findAll('.grid-item')
    expect(gridItems).toHaveLength(3)
  })

  it('應在空白時顯示 empty state', () => {
    const wrapper = mount(ChartGrid, {
      props: {
        charts: []
      }
    })

    expect(wrapper.find('.empty-state').exists()).toBe(true)
    expect(wrapper.find('.empty-state').text()).toContain('尚未新增任何股票圖表')
  })

  it('應支援調整網格列數', async () => {
    const wrapper = mount(ChartGrid, {
      props: {
        charts: mockCharts,
        defaultColumns: 3
      }
    })

    const select = wrapper.find('.grid-size-select')
    expect(select.element.value).toBe('3')

    await select.setValue('4')
    expect(select.element.value).toBe('4')
  })

  it('應在點擊圖表時展開模態視窗（US A-3 AC1）', async () => {
    const wrapper = mount(ChartGrid, {
      props: {
        charts: mockCharts
      },
      attachTo: document.body // 需要附加到 body 才能測試 Teleport
    })

    const firstGridItem = wrapper.findAll('.grid-item')[0]
    await firstGridItem.trigger('click')
    await wrapper.vm.$nextTick()

    // 檢查模態視窗是否出現在 document.body（Teleport 目標）
    const modal = document.body.querySelector('.expanded-modal')
    expect(modal).toBeTruthy()
    expect(modal?.querySelector('.expanded-header h3')?.textContent).toContain('2330')

    wrapper.unmount()
  })

  it('應在點擊關閉按鈕時關閉模態視窗（US A-3 AC3）', async () => {
    const wrapper = mount(ChartGrid, {
      props: {
        charts: mockCharts
      },
      attachTo: document.body
    })

    // 先展開
    const firstGridItem = wrapper.findAll('.grid-item')[0]
    await firstGridItem.trigger('click')
    await wrapper.vm.$nextTick()
    expect(document.body.querySelector('.expanded-modal')).toBeTruthy()

    // 點擊關閉按鈕
    const closeButton = document.body.querySelector('.close-button') as HTMLElement
    closeButton?.click()
    await wrapper.vm.$nextTick()
    
    expect(document.body.querySelector('.expanded-modal')).toBeFalsy()

    wrapper.unmount()
  })

  it('應在按 ESC 鍵時關閉模態視窗（US A-3 AC3）', async () => {
    const wrapper = mount(ChartGrid, {
      props: {
        charts: mockCharts
      },
      attachTo: document.body
    })

    // 先展開
    const firstGridItem = wrapper.findAll('.grid-item')[0]
    await firstGridItem.trigger('click')
    await wrapper.vm.$nextTick()
    expect(document.body.querySelector('.expanded-modal')).toBeTruthy()

    // 模擬按 ESC 鍵
    const escapeEvent = new KeyboardEvent('keydown', { key: 'Escape' })
    window.dispatchEvent(escapeEvent)
    await wrapper.vm.$nextTick()

    expect(document.body.querySelector('.expanded-modal')).toBeFalsy()

    wrapper.unmount()
  })

  it('應在點擊模態視窗背景時關閉（US A-3 AC3）', async () => {
    const wrapper = mount(ChartGrid, {
      props: {
        charts: mockCharts
      },
      attachTo: document.body
    })

    // 先展開
    const firstGridItem = wrapper.findAll('.grid-item')[0]
    await firstGridItem.trigger('click')
    await wrapper.vm.$nextTick()
    expect(document.body.querySelector('.expanded-modal')).toBeTruthy()

    // 點擊模態視窗背景（.expanded-modal 本身）
    const modal = document.body.querySelector('.expanded-modal') as HTMLElement
    modal?.click()
    await wrapper.vm.$nextTick()

    expect(document.body.querySelector('.expanded-modal')).toBeFalsy()

    wrapper.unmount()
  })
})
