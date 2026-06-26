# Winget GUI - Windows 软件更新管理器

**其他语言版本：** [English](README_en.md) | [繁體中文](README_zh_TW.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Русский](README_ru.md)

一个基于 Python tkinter 的图形界面应用程序，用于管理 Windows 软件的更新。

## 功能特性

✅ **图形用户界面** - 直观易用的界面
✅ **软件列表显示** - 显示所有可更新的软件及其版本信息
✅ **刷新功能** - 一键获取最新的可更新软件列表
✅ **全选/单选** - 灵活选择要更新的软件
✅ **批量更新** - 一次更新多个选中的软件
✅ **进度反馈** - 实时显示更新进度和状态

## 系统要求

- Windows 10 或更高版本
- Python 3.7 或更高版本
- Windows Package Manager (winget)

## 安装

1. 克隆或下载此项目
```bash
git clone <repository-url>
cd winget_gui
```

2. 确保已安装 Python 3.7+

3. 无需安装额外依赖，tkinter 已包含在 Python 标准库中

## 使用方法

### 启动应用程序

```bash
python main.py
```

### 操作步骤

1. **自动检查** - 应用启动时会自动检查 winget 可用性
2. **自动刷新** - 自动获取可更新的软件列表
3. **选择软件** - 点击软件名称勾选要更新的软件，或使用"全选"按钮
4. **更新** - 点击"更新所选"按钮开始更新

## 功能说明

### 刷新按钮
- 重新扫描系统并获取最新的可更新软件列表
- 显示当前可更新的软件总数

### 全选复选框
- 勾选：选中列表中的所有软件
- 取消：取消所有选择

### 软件列表
显示以下信息：
- 软件名称
- 软件ID（唯一标识符）
- 当前版本
- 可用版本（最新版本）
- 来源（winget, msstore 等）

### 更新所选
- 仅更新被选中的软件
- 更新前需要确认
- 显示每个软件的更新进度和结果

## 项目结构

```
winget_gui/
├── main.py              # 主程序入口
├── gui.py               # 图形界面模块
├── winget_handler.py    # Winget 命令处理模块
├── models.py            # 数据模型
├── requirements.txt     # 依赖列表（空）
└── README.md            # 使用说明
```

## 注意事项

1. **管理员权限** - 某些软件更新可能需要管理员权限
2. **网络连接** - 更新软件需要网络连接
3. **Winget 安装** - 确保系统已安装 Windows Package Manager
4. **超时设置** - 单个软件更新超时时间为 5 分钟

## 故障排除

### Winget 未找到
- 错误信息：`未找到 winget 命令`
- 解决方案：从 Microsoft Store 安装 "App Installer"

### 权限问题
- 某些软件更新可能需要管理员权限
- 尝试以管理员身份运行应用程序

### 更新失败
- 检查网络连接
- 查看错误信息中的详细说明
- 尝试手动运行 `winget upgrade <package-id>`

## 技术栈

- **Python 3.7+** - 编程语言
- **tkinter** - GUI 框架（Python 标准库）
- **subprocess** - 命令行调用（Python 标准库）

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！