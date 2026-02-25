import { app, BrowserWindow } from 'electron'
import path from 'path'
import { fileURLToPath } from 'url'

// ESM 模式下需要手動定義 __dirname
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Electron 主程序入口
// 負責：視窗管理、應用程式生命週期、原生 API 整合

let mainWindow: BrowserWindow | null = null

const isDev = process.env.NODE_ENV === 'development'

function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    },
    title: '台灣股市時光機 (Taiwan Market Time Machine)',
    backgroundColor: '#1e1e1e',
    show: false // 先隱藏，等 ready-to-show 事件後再顯示
  })

  // 視窗準備好後才顯示，避免閃爍
  mainWindow.once('ready-to-show', () => {
    mainWindow?.show()
  })

  // 開發模式：載入 Vite dev server
  // 生產模式：載入打包後的 index.html
  if (isDev) {
    const url = process.env.VITE_DEV_SERVER_URL || 'http://localhost:5173'
    mainWindow.loadURL(url)
    mainWindow.webContents.openDevTools() // 開發模式自動開啟 DevTools
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  // 視窗關閉時清理資源
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

// Electron 初始化完成，建立視窗
app.whenReady().then(() => {
  createMainWindow()

  // macOS 特性：點擊 Dock 圖示時重新建立視窗
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow()
    }
  })
})

// 所有視窗關閉時退出應用程式（macOS 除外）
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// 應用程式即將退出
app.on('will-quit', () => {
  // 清理資源
})

// 安全性：禁止導航到外部網站
app.on('web-contents-created', (_, contents) => {
  contents.on('will-navigate', (event, navigationUrl) => {
    const parsedUrl = new URL(navigationUrl)
    
    // 僅允許開發伺服器與本地檔案
    if (isDev) {
      if (!parsedUrl.origin.includes('localhost')) {
        event.preventDefault()
        console.warn('Navigation blocked:', navigationUrl)
      }
    } else {
      event.preventDefault()
      console.warn('Navigation blocked:', navigationUrl)
    }
  })
})
