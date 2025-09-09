# TidyDesk - File Organizer

A production-ready file organizer with modern GUI, custom scheduler, and theme support. Cross-platform compatible and ready for distribution.

![TidyDesk](https://img.shields.io/badge/TidyDesk-v1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🎨 **Modern GUI** - Clean, intuitive interface with directory selection
- 🌞 **Light Theme** - Professional light theme for comfortable usage
- ⏰ **Custom Scheduler** - Schedule automatic file organization
- 🔄 **Manual Sorting** - Organize files on-demand
- 🖥️ **Cross-Platform** - Works on Windows, macOS, and Linux
- 📁 **Smart Organization** - Organize files by type, date, size, and more
- ⚙️ **Custom Rules** - Create and manage your own organization rules
- 📊 **Progress Tracking** - Real-time progress updates and activity logging
- 💾 **Backup Management** - Automatic backups with restore functionality
- 🎯 **Rule Helper** - Guided rule creation with templates

## 🚀 Quick Start

### Download Pre-built Binaries

Download the latest release from the [Releases](https://github.com/code-zax/tiddesk/releases) page:

- **Windows**: `TidyDesk-Windows.exe`
- **macOS**: `TidyDesk-macOS.dmg`
- **Linux**: `tiddesk-linux`

### Installation

#### Windows

1. Download `TidyDesk-Windows.exe`
2. Run the executable
3. No installation required - portable application

#### macOS

1. Download `TidyDesk-macOS.dmg`
2. Open the DMG file
3. Drag TidyDesk.app to Applications folder
4. Open from Applications or Launchpad

#### Linux

1. Download `tiddesk-linux`
2. Make executable: `chmod +x tiddesk-linux`
3. Run: `./tiddesk-linux`

## 🛠️ Building from Source

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/code-zax/tiddesk.git
   cd tiddesk
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run from source**
   ```bash
   python -m file_organizer --gui
   ```

### Building Executables

#### Automatic Build (Recommended)

Run the build script for your platform:

**Windows:**

```cmd
build_windows.bat
```

**macOS:**

```bash
./build_macos.sh
```

**Linux:**

```bash
./build_linux.sh
```

#### Manual Build

1. **Create icons from TidyDesk.png**

   ```bash
   python build.py
   ```

2. **Build for your platform**

   ```bash
   # Windows
   pyinstaller --onefile --windowed --name=TidyDesk --icon=file_organizer/icons/app.ico file_organizer/main.py

   # macOS
   pyinstaller --onefile --windowed --name=TidyDesk --icon=file_organizer/icons/app.icns file_organizer/main.py

   # Linux
   pyinstaller --onefile --windowed --name=tiddesk --icon=file_organizer/icons/icon_256x256.png file_organizer/main.py
   ```

## 📖 Usage

### GUI Mode (Recommended)

Launch the application:

```bash
python -m file_organizer --gui
```

### Command Line Mode

```bash
python -m file_organizer --help
```

### Basic Workflow

1. **Select Directory** - Choose the folder you want to organize
2. **Preview Organization** - See what files will be moved where
3. **Create Custom Rules** - Set up your own organization rules
4. **Organize Files** - Run the organization process
5. **Manage Backups** - Restore or delete backups as needed

## ⚙️ Configuration

### Settings

- **Theme**: Light theme (dark mode removed for simplicity)
- **Backup**: Automatic backup before organization
- **Scheduler**: Custom scheduling for automatic organization
- **Rules**: Custom organization rules

### Custom Rules

Create custom organization rules:

1. Open **Custom Rules** from the main window
2. Click **Add Rule** to create a new rule
3. Use the **Rule Helper** for guided rule creation
4. Set file patterns, destination folders, and conditions
5. Save and apply rules

### Backup Management

- **Automatic Backups**: Created before each organization
- **Backup Location**: `~/Documents/TidyDesk/backups/`
- **Backup Format**: ZIP files with metadata
- **Management**: View, restore, and delete backups through the UI

## 🏗️ Project Structure

```
tiddesk/
├── file_organizer/          # Main application code
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration management
│   │   ├── file_organizer.py # File organization logic
│   │   ├── backup_manager.py # Backup management
│   │   └── scheduler.py    # Scheduling system
│   ├── gui/                # GUI components
│   │   ├── main_window.py  # Main application window
│   │   ├── rules_manager.py # Rules management UI
│   │   ├── rule_helper.py  # Rule creation helper
│   │   ├── backup_manager.py # Backup management UI
│   │   └── theme_manager.py # Theme management
│   └── icons/              # Application icons
├── build.py                # Universal build script
├── build_windows.bat       # Windows build script
├── build_macos.sh          # macOS build script
├── build_linux.sh          # Linux build script
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
└── README.md              # This file
```

## 🔧 Development

### Setting up Development Environment

1. **Clone and install**

   ```bash
   git clone https://github.com/code-zax/tiddesk.git
   cd tiddesk
   pip install -e .
   ```

2. **Run tests**

   ```bash
   python -m pytest tests/
   ```

3. **Run from source**
   ```bash
   python -m file_organizer --gui
   ```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📋 Requirements

### System Requirements

- **Windows**: Windows 10 or later
- **macOS**: macOS 10.14 (Mojave) or later
- **Linux**: Modern Linux distribution with GTK+ support

### Python Requirements

- Python 3.8 or higher
- tkinter (usually included with Python)
- Pillow >= 9.0.0
- schedule >= 1.2.0
- psutil >= 5.9.0
- pyinstaller >= 5.0.0 (for building)

## 🐛 Troubleshooting

### Common Issues

**Q: Application won't start**

- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`

**Q: Icons not displaying**

- Ensure TidyDesk.png is in the root directory
- Run the build script to generate icons

**Q: Backup creation fails**

- Check write permissions in Documents folder
- Ensure sufficient disk space

**Q: Rules not saving**

- Check file permissions in the application directory
- Verify the config file is writable

### Getting Help

- Check the [Issues](https://github.com/code-zax/tiddesk/issues) page
- Create a new issue with detailed information
- Include your operating system and Python version

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and tkinter
- Icons created from custom TidyDesk.png
- Cross-platform compatibility ensured
- Modern UI design principles

## 📊 Version History

### v1.0.0 (Current)

- Initial release
- Modern GUI with light theme
- Custom rules management
- Backup system
- Cross-platform builds
- Scheduler integration

---

**Made with ❤️ by [code-zax](https://github.com/code-zax)**
