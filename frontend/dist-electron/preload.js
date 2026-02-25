import { contextBridge, ipcRenderer } from "electron";
const electronAPI = {
  // 版本資訊
  versions: {
    node: process.versions.node,
    chrome: process.versions.chrome,
    electron: process.versions.electron
  },
  // 檔案系統操作（未來 US E-1 Excel 匯出會用到）
  fs: {
    saveFile: async (filePath, data) => {
      return ipcRenderer.invoke("fs:saveFile", filePath, data);
    },
    openFile: async (filePath) => {
      return ipcRenderer.invoke("fs:openFile", filePath);
    }
  },
  // 系統資訊
  system: {
    getPlatform: () => process.platform,
    getArch: () => process.arch
  }
};
contextBridge.exposeInMainWorld("electronAPI", electronAPI);
