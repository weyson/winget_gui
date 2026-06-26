# Winget GUI - Windows 軟體更新管理員

**其他語言版本：** [简体中文](README.md) | [English](README_en.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Русский](README_ru.md)

一個基於 Python tkinter 的圖形界面應用程式，用於管理 Windows 軟體的更新。

## 功能特性

✅ **圖形使用者介面** - 直觀易用的介面
✅ **軟體清單顯示** - 顯示所有可更新的軟體及其版本資訊
✅ **刷新功能** - 一鍵獲取最新的可更新軟體清單
✅ **全選/單選** - 靈活選擇要更新的軟體
✅ **批次更新** - 一次更新多個選中的軟體
✅ **進度回饋** - 即時顯示更新進度和狀態

## 系統要求

- Windows 10 或更高版本
- Python 3.7 或更高版本
- Windows Package Manager (winget)

## 安裝

1. 複製或下載此專案
```bash
git clone <repository-url>
cd winget_gui
```

2. 確保已安裝 Python 3.7+

3. 無需安裝額外依賴，tkinter 已包含在 Python 標準庫中

## 使用方法

### 啟動應用程式

```bash
python main.py
```

### 操作步驟

1. **自動檢查** - 應用啟動時會自動檢查 winget 可用性
2. **自動刷新** - 自動獲取可更新的軟體清單
3. **選擇軟體** - 點擊軟體名稱勾選要更新的軟體，或使用「全選」按鈕
4. **更新** - 點擊「更新所選」按鈕開始更新

## 功能說明

### 刷新按鈕
- 重新掃描系統並獲取最新的可更新軟體清單
- 顯示當前可更新的軟體總數

### 全選複選框
- 勾選：選中清單中的所有軟體
- 取消：取消所有選擇

### 軟體清單
顯示以下資訊：
- 軟體名稱
- 軟體ID（唯一識別符）
- 當前版本
- 可用版本（最新版本）
- 來源（winget, msstore 等）

### 更新所選
- 僅更新被選中的軟體
- 更新前需要確認
- 顯示每個軟體的更新進度和結果

## 專案結構

```
winget_gui/
├── main.py              # 主程式入口
├── gui.py               # 圖形介面模組
├── winget_handler.py    # Winget 命令處理模組
├── models.py            # 資料模型
├── i18n.py              # 國際化模組
├── locales/             # 翻譯檔案目錄
│   ├── zh_CN.json       # 簡體中文
│   ├── zh_TW.json       # 繁體中文
│   ├── en.json          # 英語
│   ├── ru.json          # 俄語
│   ├── ja.json          # 日語
│   └── ko.json          # 韓語
├── requirements.txt     # 依賴列表（空）
└── README.md            # 使用說明
```

## 注意事項

1. **管理員權限** - 某些軟體更新可能需要管理員權限
2. **網路連線** - 更新軟體需要網路連線
3. **Winget 安裝** - 確保系統已安裝 Windows Package Manager
4. **超時設定** - 單個軟體更新超時時間為 5 分鐘

## 故障排除

### Winget 未找到
- 錯誤資訊：`未找到 winget 命令`
- 解決方案：從 Microsoft Store 安裝 "App Installer"

### 權限問題
- 某些軟體更新可能需要管理員權限
- 嘗試以管理員身份執行應用程式

### 更新失敗
- 檢查網路連線
- 查看錯誤資訊中的詳細說明
- 嘗試手動執行 `winget upgrade <package-id>`

## 技術堆疊

- **Python 3.7+** - 程式語言
- **tkinter** - GUI 框架（Python 標準庫）
- **subprocess** - 命令列調用（Python 標準庫）

## 許可證

MIT License

## 貢獻

歡迎提交 Issue 和 Pull Request！