# Winget GUI - Windows Software Update Manager

**Other languages:** [简体中文](README.md) | [繁體中文](README_zh_TW.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Русский](README_ru.md)

A Python tkinter-based graphical interface application for managing Windows software updates.

## Features

✅ **Graphical User Interface** - Intuitive and easy-to-use interface
✅ **Software List Display** - Shows all updatable software and their version information
✅ **Refresh Function** - One-click to get the latest list of updatable software
✅ **Select All/Single Select** - Flexibly select software to update
✅ **Batch Update** - Update multiple selected software at once
✅ **Progress Feedback** - Real-time update progress and status display

## System Requirements

- Windows 10 or later
- Python 3.7 or later
- Windows Package Manager (winget)

## Installation

1. Clone or download this project
```bash
git clone <repository-url>
cd winget_gui
```

2. Ensure Python 3.7+ is installed

3. No additional dependencies needed, tkinter is included in Python standard library

## Usage

### Launch Application

```bash
python main.py
```

### Operation Steps

1. **Auto Check** - Application automatically checks winget availability on startup
2. **Auto Refresh** - Automatically fetches the list of updatable software
3. **Select Software** - Click software name to check the software to update, or use the "Select All" button
4. **Update** - Click "Upgrade Selected" button to start updating

## Function Description

### Refresh Button
- Rescan the system and get the latest list of updatable software
- Shows the total number of currently updatable software

### Select All Checkbox
- Check: Select all software in the list
- Uncheck: Deselect all

### Software List
Displays the following information:
- Software Name
- Software ID (unique identifier)
- Current Version
- Available Version (latest version)
- Source (winget, msstore, etc.)

### Upgrade Selected
- Only updates selected software
- Confirmation required before updating
- Shows update progress and results for each software

## Project Structure

```
winget_gui/
├── main.py              # Main program entry
├── gui.py               # Graphical interface module
├── winget_handler.py    # Winget command handling module
├── models.py            # Data models
├── i18n.py              # Internationalization module
├── locales/             # Translation files directory
│   ├── zh_CN.json       # Simplified Chinese
│   ├── zh_TW.json       # Traditional Chinese
│   ├── en.json          # English
│   ├── ru.json          # Russian
│   ├── ja.json          # Japanese
│   └── ko.json          # Korean
├── requirements.txt     # Dependency list (empty)
└── README.md            # Usage instructions
```

## Notes

1. **Admin Privileges** - Some software updates may require administrator privileges
2. **Network Connection** - Internet connection required for software updates
3. **Winget Installation** - Ensure Windows Package Manager is installed
4. **Timeout Setting** - Single software update timeout is 5 minutes

## Troubleshooting

### Winget Not Found
- Error message: `winget command not found`
- Solution: Install "App Installer" from Microsoft Store

### Permission Issues
- Some software updates may require administrator privileges
- Try running the application as administrator

### Update Failed
- Check network connection
- Check detailed description in error message
- Try running `winget upgrade <package-id>` manually

## Technology Stack

- **Python 3.7+** - Programming language
- **tkinter** - GUI framework (Python standard library)
- **subprocess** - Command line invocation (Python standard library)

## License

MIT License

## Contributing

Welcome to submit Issues and Pull Requests!