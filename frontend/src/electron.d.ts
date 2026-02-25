// TypeScript 型別定義：讓 Renderer Process 可以正確使用 electronAPI

interface ElectronAPI {
  versions: {
    node: string
    chrome: string
    electron: string
  }
  fs: {
    saveFile: (filePath: string, data: string) => Promise<void>
    openFile: (filePath: string) => Promise<string>
  }
  system: {
    getPlatform: () => NodeJS.Platform
    getArch: () => string
  }
}

declare global {
  interface Window {
    electronAPI: ElectronAPI
  }
}

export {}
