import { contextBridge, ipcRenderer } from 'electron'

// Preload Script: Main Process 與 Renderer Process 之間的橋樑
// 使用 contextBridge 安全地暴露 API 給 Renderer Process

// 暴露的 API
const electronAPI = {
  // 版本資訊
  versions: {
    node: process.versions.node,
    chrome: process.versions.chrome,
    electron: process.versions.electron
  },

  // 檔案系統操作（未來 US E-1 Excel 匯出會用到）
  fs: {
    saveFile: async (filePath: string, data: string) => {
      return ipcRenderer.invoke('fs:saveFile', filePath, data)
    },
    openFile: async (filePath: string) => {
      return ipcRenderer.invoke('fs:openFile', filePath)
    }
  },

  // 系統資訊
  system: {
    getPlatform: () => process.platform,
    getArch: () => process.arch
  }
}

// 類型定義（供 Renderer Process 使用）
export type ElectronAPI = typeof electronAPI

// 安全地將 API 暴露給 Renderer Process
contextBridge.exposeInMainWorld('electronAPI', electronAPI)
