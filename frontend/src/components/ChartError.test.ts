import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ChartError from '../components/ChartError.vue'

describe('ChartError', () => {
  it('應正確渲染預設錯誤標題', () => {
    const wrapper = mount(ChartError, {
      props: {
        message: '無法連線至伺服器'
      }
    })
    
    expect(wrapper.find('.error-title').text()).toBe('載入失敗')
    expect(wrapper.find('.error-message').text()).toBe('無法連線至伺服器')
  })

  it('應正確渲染自訂錯誤標題與訊息', () => {
    const wrapper = mount(ChartError, {
      props: {
        title: '網路錯誤',
        message: '請檢查網路連線',
        details: 'Error code: NETWORK_ERROR'
      }
    })
    
    expect(wrapper.find('.error-title').text()).toBe('網路錯誤')
    expect(wrapper.find('.error-message').text()).toBe('請檢查網路連線')
    expect(wrapper.find('.error-details').text()).toBe('Error code: NETWORK_ERROR')
  })

  it('應顯示重試按鈕並觸發 retry 事件', async () => {
    const wrapper = mount(ChartError, {
      props: {
        message: '載入失敗',
        showRetry: true
      }
    })
    
    const button = wrapper.find('.retry-button')
    expect(button.exists()).toBe(true)
    
    await button.trigger('click')
    expect(wrapper.emitted('retry')).toHaveLength(1)
  })

  it('應可隱藏重試按鈕', () => {
    const wrapper = mount(ChartError, {
      props: {
        message: '載入失敗',
        showRetry: false
      }
    })
    
    expect(wrapper.find('.retry-button').exists()).toBe(false)
  })
})
