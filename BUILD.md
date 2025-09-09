# TidyDesk Build Guide

This guide explains how to build TidyDesk for all supported platforms.

## 🚀 Quick Build

### Automatic Build (Recommended)

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

### Universal Build

```bash
python3 build_tiddesk_universal.py
```

## 📋 Prerequisites

### Required Software

- **Python 3.8+** - [Download](https://python.org)
- **pip** - Usually included with Python
- **Git** - [Download](https://git-scm.com)

### Python Dependencies

```bash
pip install -r requirements.txt
```

### Platform-Specific Requirements

#### Windows

- Windows 10 or later
- Visual Studio Build Tools (for some packages)

#### macOS

- macOS 10.14 or later
- Xcode Command Line Tools: `xcode-select --install`
- iconutil (included with macOS)

#### Linux

- GTK+ development libraries
- Ubuntu/Debian: `sudo apt-get install python3-tk python3-dev`
- Fedora: `sudo dnf install python3-tkinter python3-devel`

## 🛠️ Build Process

### 1. Icon Generation

The build script automatically creates all required icons from `TidyDesk.png`:

- **Windows**: `app.ico` (multi-size ICO file)
- **macOS**: `app.icns` (multi-size ICNS file)
- **Linux**: PNG files in various sizes

### 2. Platform-Specific Builds

#### Windows Build

```bash
pyinstaller --onefile --windowed --name=TidyDesk --icon=file_organizer/icons/app.ico file_organizer/main.py
```

**Output**: `dist/TidyDesk.exe`

#### macOS Build

```bash
pyinstaller --onefile --windowed --name=TidyDesk --icon=file_organizer/icons/app.icns file_organizer/main.py
```

**Output**: `dist/TidyDesk.app`

#### Linux Build

```bash
pyinstaller --onefile --windowed --name=tiddesk --icon=file_organizer/icons/icon_256x256.png file_organizer/main.py
```

**Output**: `dist/tiddesk`

### 3. Installer Creation

#### macOS DMG

```bash
python3 create_dmg.py
```

**Output**: `installers/TidyDesk-macOS.dmg`

#### Windows Executable

- Copy `dist/TidyDesk.exe` to `installers/TidyDesk-Windows.exe`

#### Linux Executable

- Copy `dist/tiddesk` to `installers/tiddesk-linux`

## 📦 Distribution

### Universal Package

The build script creates a universal package containing all platforms:

```
TidyDesk-Universal/
├── Windows/
│   └── TidyDesk.exe
├── macOS/
│   └── TidyDesk.app
├── Linux/
│   └── tiddesk
├── README.md
├── CHANGELOG.md
├── BUILD.md
├── RULES.md
└── BACKUP.md
```

### Individual Installers

- **Windows**: `installers/TidyDesk-Windows.exe`
- **macOS**: `installers/TidyDesk-macOS.dmg`
- **Linux**: `installers/tiddesk-linux`

## 🔧 Advanced Build Options

### Custom Icon

Place your custom icon as `TidyDesk.png` in the root directory. The build script will automatically generate all required formats.

### Version Information

Windows builds include version information from `version_info.txt` (auto-generated).

### Code Signing (macOS)

For distribution outside the App Store, you may want to code sign:

```bash
codesign --force --deep --sign "Developer ID Application: Your Name" dist/TidyDesk.app
```

### Notarization (macOS)

For distribution outside the App Store, notarize the DMG:

```bash
xcrun notarytool submit installers/TidyDesk-macOS.dmg --keychain-profile "notarytool" --wait
```

## 🐛 Troubleshooting

### Common Build Issues

**Q: PyInstaller not found**

```bash
pip install pyinstaller
```

**Q: Icons not generating**

- Ensure `TidyDesk.png` exists in root directory
- Check Pillow installation: `pip install Pillow`

**Q: macOS build fails**

- Install Xcode Command Line Tools: `xcode-select --install`
- Check iconutil availability: `which iconutil`

**Q: Linux build fails**

- Install required libraries (see Prerequisites)
- Check GTK+ installation

**Q: DMG creation fails**

- Ensure TidyDesk.app exists in `dist/`
- Check disk space
- Verify hdiutil availability: `which hdiutil`

### Build Verification

After building, test the application:

```bash
# Test macOS app
open dist/TidyDesk.app

# Test Linux executable
./dist/tiddesk

# Test Windows executable (on Windows)
dist\TidyDesk.exe
```

## 📁 Build Output Structure

```
project/
├── build/                 # PyInstaller build files
├── dist/                  # Built executables
│   ├── TidyDesk.exe      # Windows executable
│   ├── TidyDesk.app/     # macOS application bundle
│   └── tiddesk           # Linux executable
├── installers/           # Installer packages
│   ├── TidyDesk-Windows.exe
│   ├── TidyDesk-macOS.dmg
│   └── tiddesk-linux
├── TidyDesk-Universal/   # Universal package
└── file_organizer/icons/ # Generated icons
```

## 🚀 Release Process

1. **Update version** in `setup.py` and `pyproject.toml`
2. **Build all platforms** using the build scripts
3. **Test all builds** on target platforms
4. **Create GitHub release** with installers
5. **Update documentation** if needed

## 📝 Notes

- All builds are portable and don't require installation
- macOS builds are unsigned (for development)
- Windows builds include version information
- Linux builds are statically linked where possible
- All builds include the custom TidyDesk icon

---

For more information, see the main [README.md](README.md).
