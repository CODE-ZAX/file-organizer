# TidyDesk - Build Guide

This guide explains how to build TidyDesk for all supported platforms.

## 🎯 Supported Platforms

- **Windows** (Windows 10+)
- **macOS** (macOS 10.14+)
- **Linux** (Most modern distributions)

## 🚀 Quick Build

### Universal Build (All Platforms)

```bash
python3 build_tiddesk.py
```

### Platform-Specific Builds

```bash
# Windows
build_windows.bat

# macOS
./build_macos.sh

# Linux
./build_linux.sh
```

## 📦 Build Output

After building, you'll find:

```
dist/                          # Platform-specific builds
├── TidyDesk.exe              # Windows executable
├── TidyDesk.app              # macOS application bundle
└── tiddesk                   # Linux executable

installers/                    # Installer packages
├── TidyDesk-Windows.exe      # Windows installer
├── TidyDesk-macOS.dmg        # macOS disk image
└── tiddesk-linux             # Linux executable

TidyDesk-Universal/            # Universal package
├── Windows/TidyDesk.exe
├── macOS/TidyDesk.app
├── Linux/tiddesk
└── README.txt
```

## 🛠️ Build Requirements

### All Platforms

- Python 3.8+
- PyInstaller 5.0+
- Pillow (PIL)
- All dependencies from `requirements.txt`

### Windows

- Windows 10 or later
- Visual Studio Build Tools (for some dependencies)

### macOS

- macOS 10.14 or later
- Xcode Command Line Tools
- `hdiutil` (for DMG creation)

### Linux

- GTK+ development libraries
- Most modern distributions supported

## 🔧 Build Process

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Icons

The build script automatically creates icons from `TidyDesk.png`:

- Multiple PNG sizes (16x16 to 1024x1024)
- Windows ICO format
- macOS ICNS format

### 3. Build Application

```bash
python3 build_tiddesk.py
```

## 📱 Platform-Specific Details

### Windows (.exe)

- **Format**: Single executable file
- **Size**: ~18-20 MB
- **Dependencies**: Bundled with PyInstaller
- **Icon**: Custom TidyDesk.ico
- **Features**:
  - No installation required
  - Windows Defender compatible
  - Taskbar integration

### macOS (.app)

- **Format**: Application bundle
- **Size**: ~18-20 MB
- **Dependencies**: Bundled with PyInstaller
- **Icon**: Custom TidyDesk.icns
- **Features**:
  - Native macOS integration
  - Dock icon support
  - Spotlight searchable
  - Code signing ready

### Linux (executable)

- **Format**: Single executable file
- **Size**: ~18-20 MB
- **Dependencies**: Requires system GTK+
- **Icon**: PNG format
- **Features**:
  - No installation required
  - Desktop integration
  - AppImage compatible

## 🎨 Custom Icon Integration

TidyDesk automatically uses your custom `TidyDesk.png` icon:

- Converts to all required formats
- Generates all necessary sizes
- Integrates into all platform builds

## 🔒 Code Signing (Optional)

### macOS

```bash
# Sign the app bundle
codesign --force --deep --sign "Developer ID Application: Your Name" dist/TidyDesk.app

# Verify signature
codesign --verify --verbose dist/TidyDesk.app
```

### Windows

```bash
# Sign the executable (requires certificate)
signtool sign /f certificate.p12 /p password dist/TidyDesk.exe
```

## 📋 Distribution Checklist

### Before Release

- [ ] Test on target platform
- [ ] Verify all features work
- [ ] Check file sizes are reasonable
- [ ] Test on clean system (no Python installed)
- [ ] Verify icons display correctly
- [ ] Test theme switching
- [ ] Verify file organization works
- [ ] Check error handling

### Release Package

- [ ] Create release notes
- [ ] Include installation instructions
- [ ] Add system requirements
- [ ] Include troubleshooting guide
- [ ] Test installer packages

## 🐛 Troubleshooting

### Common Issues

#### Build Fails

- **Solution**: Check all dependencies are installed
- **Check**: Python version compatibility
- **Verify**: PyInstaller installation

#### App Won't Start

- **Solution**: Check system requirements
- **Windows**: Install Visual C++ Redistributable
- **macOS**: Check Gatekeeper settings
- **Linux**: Install GTK+ libraries

#### Icons Not Showing

- **Solution**: Verify TidyDesk.png exists in root
- **Check**: Icon format compatibility
- **Verify**: File paths in build script

#### Large File Size

- **Solution**: Use `--exclude-module` for unused modules
- **Check**: Remove debug symbols
- **Verify**: Optimize dependencies

### Debug Mode

```bash
# Build with debug information
pyinstaller --debug=all file_organizer/main.py

# Run with verbose output
python3 -m file_organizer --log-level DEBUG
```

## 🔄 Continuous Integration

The project includes GitHub Actions workflows for automated building:

- **CI Pipeline**: Tests on multiple platforms
- **Release Pipeline**: Builds and publishes packages
- **Cross-Platform**: Windows, macOS, Linux builds

## 📊 Build Statistics

Typical build sizes:

- **Source Code**: ~2 MB
- **Dependencies**: ~16-18 MB
- **Final Package**: ~18-20 MB
- **Build Time**: 3-5 minutes

## 🎯 Optimization Tips

### Reduce Size

- Use `--exclude-module` for unused modules
- Enable UPX compression
- Remove debug information
- Optimize icon sizes

### Improve Performance

- Use `--onefile` for single executable
- Bundle only required dependencies
- Optimize startup time
- Use native libraries when possible

## 📚 Additional Resources

- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [macOS Code Signing](https://developer.apple.com/documentation/security/notarizing_your_app_before_distribution)
- [Windows Code Signing](https://docs.microsoft.com/en-us/windows-hardware/drivers/dashboard/code-signing)
- [Linux AppImage](https://appimage.org/)

## 🤝 Contributing

To contribute to the build process:

1. Test builds on your platform
2. Report issues with specific steps
3. Suggest improvements
4. Submit pull requests

## 📄 License

The build scripts are part of the TidyDesk project and are licensed under the MIT License.
