/**
 * useChartInteraction Composable - Unit Tests
 * 
 * 測試範疇：
 * - Crosshair 互動（mousemove/mouseleave）
 * - Zoom 互動（wheel）
 * - Pan 互動（mousedown/mouseup/mousemove）
 * - resetZoom 重置縮放
 * - setInteractionEnabled 啟用/停用互動
 */

import { describe, it, expect, beforeEach } from 'vitest'
import { useChartInteraction } from '../composables/useChartInteraction'

describe('useChartInteraction', () => {
  beforeEach(() => {
    // Reset any global state if needed
  })

  describe('初始狀態', () => {
    it('應設定預設初始值', () => {
      const { crosshair, zoom, isPanning, interactionEnabled } = useChartInteraction()

      expect(crosshair.value).toEqual({
        visible: false,
        dataPoint: null,
        x: 0,
        y: 0
      })

      expect(zoom.value).toEqual({
        visibleRangeStart: null,
        visibleRangeEnd: null,
        zoomLevel: 1.0
      })

      expect(isPanning.value).toBe(false)
      expect(interactionEnabled.value).toBe(true)
    })
  })

  describe('Crosshair 互動', () => {
    it('handleMouseMove 應更新 crosshair 座標', () => {
      const { crosshair, handlers } = useChartInteraction()

      const mockEvent = new MouseEvent('mousemove', {
        clientX: 100,
        clientY: 200
      })

      handlers.handleMouseMove(mockEvent)

      expect(crosshair.value.visible).toBe(true)
      expect(crosshair.value.x).toBe(100)
      expect(crosshair.value.y).toBe(200)
    })

    it('handleMouseLeave 應隱藏 crosshair', () => {
      const { crosshair, handlers } = useChartInteraction()

      // 先顯示
      const moveEvent = new MouseEvent('mousemove', {
        clientX: 100,
        clientY: 200
      })
      handlers.handleMouseMove(moveEvent)
      expect(crosshair.value.visible).toBe(true)

      // 然後離開
      const leaveEvent = new MouseEvent('mouseleave')
      handlers.handleMouseLeave(leaveEvent)

      expect(crosshair.value.visible).toBe(false)
    })

    it('interactionEnabled = false 時不應更新 crosshair', () => {
      const { crosshair, handlers, setInteractionEnabled } = useChartInteraction()

      setInteractionEnabled(false)

      const mockEvent = new MouseEvent('mousemove', {
        clientX: 100,
        clientY: 200
      })
      handlers.handleMouseMove(mockEvent)

      expect(crosshair.value.visible).toBe(false)
      expect(crosshair.value.x).toBe(0)
    })
  })

  describe('Zoom 互動', () => {
    it('handleWheel 向上滾動應放大', () => {
      const { zoom, handlers } = useChartInteraction()

      const mockEvent = new WheelEvent('wheel', {
        deltaY: -100 // 向上滾動（放大）
      })

      // 阻止預設行為的測試
      const preventDefaultSpy = vi.spyOn(mockEvent, 'preventDefault')

      handlers.handleWheel(mockEvent)

      expect(zoom.value.zoomLevel).toBeGreaterThan(1.0)
      expect(zoom.value.zoomLevel).toBeCloseTo(1.1, 5) // 1.0 * 1.1
      expect(preventDefaultSpy).toHaveBeenCalled()
    })

    it('handleWheel 向下滾動應縮小', () => {
      const { zoom, handlers } = useChartInteraction()

      const mockEvent = new WheelEvent('wheel', {
        deltaY: 100 // 向下滾動（縮小）
      })

      handlers.handleWheel(mockEvent)

      expect(zoom.value.zoomLevel).toBeLessThan(1.0)
      expect(zoom.value.zoomLevel).toBeCloseTo(0.9, 5) // 1.0 * 0.9
    })

    it('zoom 應限制在 0.1 ~ 10 之間', () => {
      const { zoom, handlers } = useChartInteraction()

      // 嘗試縮小超過下限
      for (let i = 0; i < 50; i++) {
        const mockEvent = new WheelEvent('wheel', { deltaY: 100 })
        handlers.handleWheel(mockEvent)
      }
      expect(zoom.value.zoomLevel).toBeGreaterThanOrEqual(0.1)
      expect(zoom.value.zoomLevel).toBe(0.1)

      // 重置
      const { zoom: zoom2, handlers: handlers2 } = useChartInteraction()

      // 嘗試放大超過上限
      for (let i = 0; i < 50; i++) {
        const mockEvent = new WheelEvent('wheel', { deltaY: -100 })
        handlers2.handleWheel(mockEvent)
      }
      expect(zoom2.value.zoomLevel).toBeLessThanOrEqual(10)
      expect(zoom2.value.zoomLevel).toBe(10)
    })

    it('interactionEnabled = false 時不應 zoom', () => {
      const { zoom, handlers, setInteractionEnabled } = useChartInteraction()

      setInteractionEnabled(false)

      const mockEvent = new WheelEvent('wheel', { deltaY: -100 })
      handlers.handleWheel(mockEvent)

      expect(zoom.value.zoomLevel).toBe(1.0) // 不變
    })

    it('resetZoom 應重置縮放狀態', () => {
      const { zoom, handlers, resetZoom } = useChartInteraction()

      // 先放大
      const mockEvent = new WheelEvent('wheel', { deltaY: -100 })
      handlers.handleWheel(mockEvent)
      expect(zoom.value.zoomLevel).toBeGreaterThan(1.0)

      // 重置
      resetZoom()

      expect(zoom.value.zoomLevel).toBe(1.0)
      expect(zoom.value.visibleRangeStart).toBeNull()
      expect(zoom.value.visibleRangeEnd).toBeNull()
    })
  })

  describe('Pan 互動', () => {
    it('handleMouseDown 應開始 panning', () => {
      const { isPanning, handlers } = useChartInteraction()

      const mockEvent = new MouseEvent('mousedown', {
        clientX: 100,
        clientY: 200
      })

      handlers.handleMouseDown(mockEvent)

      expect(isPanning.value).toBe(true)
    })

    it('handleMouseUp 應停止 panning', () => {
      const { isPanning, handlers } = useChartInteraction()

      // 先開始
      const downEvent = new MouseEvent('mousedown', {
        clientX: 100,
        clientY: 200
      })
      handlers.handleMouseDown(downEvent)
      expect(isPanning.value).toBe(true)

      // 然後結束
      const upEvent = new MouseEvent('mouseup')
      handlers.handleMouseUp(upEvent)

      expect(isPanning.value).toBe(false)
    })

    it('handleMouseMove 在 panning 時應計算 delta', () => {
      const { isPanning, handlers } = useChartInteraction()

      // 開始 pan
      const downEvent = new MouseEvent('mousedown', {
        clientX: 100,
        clientY: 200
      })
      handlers.handleMouseDown(downEvent)

      // 移動
      const moveEvent = new MouseEvent('mousemove', {
        clientX: 150,
        clientY: 250
      })
      handlers.handleMouseMove(moveEvent)

      // 目前是 placeholder，只驗證狀態保持
      expect(isPanning.value).toBe(true)
    })

    it('handleMouseLeave 應停止 panning', () => {
      const { isPanning, handlers } = useChartInteraction()

      // 開始 pan
      const downEvent = new MouseEvent('mousedown', {
        clientX: 100,
        clientY: 200
      })
      handlers.handleMouseDown(downEvent)
      expect(isPanning.value).toBe(true)

      // 離開邊界
      const leaveEvent = new MouseEvent('mouseleave')
      handlers.handleMouseLeave(leaveEvent)

      expect(isPanning.value).toBe(false)
    })

    it('interactionEnabled = false 時不應開始 panning', () => {
      const { isPanning, handlers, setInteractionEnabled } = useChartInteraction()

      setInteractionEnabled(false)

      const mockEvent = new MouseEvent('mousedown', {
        clientX: 100,
        clientY: 200
      })
      handlers.handleMouseDown(mockEvent)

      expect(isPanning.value).toBe(false)
    })
  })

  describe('setInteractionEnabled', () => {
    it('停用互動應重置所有狀態', () => {
      const { crosshair, zoom, isPanning, handlers, setInteractionEnabled } = useChartInteraction()

      // 先建立一些互動狀態
      const moveEvent = new MouseEvent('mousemove', {
        clientX: 100,
        clientY: 200
      })
      handlers.handleMouseMove(moveEvent)
      expect(crosshair.value.visible).toBe(true)

      const wheelEvent = new WheelEvent('wheel', { deltaY: -100 })
      handlers.handleWheel(wheelEvent)
      expect(zoom.value.zoomLevel).toBeGreaterThan(1.0)

      const downEvent = new MouseEvent('mousedown', {
        clientX: 100,
        clientY: 200
      })
      handlers.handleMouseDown(downEvent)
      expect(isPanning.value).toBe(true)

      // 停用互動
      setInteractionEnabled(false)

      expect(crosshair.value.visible).toBe(false)
      expect(zoom.value.zoomLevel).toBe(1.0)
      expect(isPanning.value).toBe(false)
    })

    it('重新啟用互動應恢復功能', () => {
      const { crosshair, handlers, setInteractionEnabled } = useChartInteraction()

      setInteractionEnabled(false)
      setInteractionEnabled(true)

      const moveEvent = new MouseEvent('mousemove', {
        clientX: 100,
        clientY: 200
      })
      handlers.handleMouseMove(moveEvent)

      expect(crosshair.value.visible).toBe(true)
    })
  })
})
