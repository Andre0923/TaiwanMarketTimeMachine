import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ChartLoading from '../components/ChartLoading.vue'

describe('ChartLoading', () => {
  it('應正確渲染預設載入訊息', () => {
    const wrapper = mount(ChartLoading)
    
    expect(wrapper.find('.loading-text').text()).toBe('載入中...')
    expect(wrapper.find('.spinner').exists()).toBe(true)
  })

  it('應正確渲染自訂載入訊息', () => {
    const wrapper = mount(ChartLoading, {
      props: {
        message: '載入圖表資料中...'
      }
    })
    
    expect(wrapper.find('.loading-text').text()).toBe('載入圖表資料中...')
  })
})
