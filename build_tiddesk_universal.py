#!/usr/bin/env python3
"""
TidyDesk Universal Build Script
Creates cross-platform builds for Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import shutil
import platform
import zipfile
from pathlib import Path
from PIL import Image

def create_icons_from_custom():
    """Create all icon formats from custom TidyDesk.png"""
    custom_icon = "TidyDesk.png"
    if not os.path.exists(custom_icon):
        print("❌ TidyDesk.png not found in root directory")
        return False
    
    print("🎨 Creating icons from TidyDesk.png...")
    
    # Create icons directory
    icons_dir = "file_organizer/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Load the custom icon
    img = Image.open(custom_icon)
    
    # Create different sizes
    sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
    
    for size in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f"{icons_dir}/icon_{size}x{size}.png")
        print(f"✅ Created {size}x{size} icon")
    
    # Create Windows ICO
    img.save(f"{icons_dir}/app.ico", format="ICO")
    print("✅ Created Windows ICO")
    
    # Create macOS ICNS (requires iconutil)
    try:
        # Create iconset directory
        iconset_dir = "app.iconset"
        os.makedirs(iconset_dir, exist_ok=True)
        
        # Copy required sizes for ICNS
        required_sizes = [16, 32, 128, 256, 512, 1024]
        for size in required_sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(f"{iconset_dir}/icon_{size}x{size}.png")
        
        # Create ICNS
        subprocess.run(["iconutil", "-c", "icns", iconset_dir], check=True)
        shutil.move("app.icns", f"{icons_dir}/app.icns")
        shutil.rmtree(iconset_dir)
        print("✅ Created macOS ICNS")
    except Exception as e:
        print(f"⚠️  Could not create ICNS: {e}")
    
    return True

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__', 'installers', 'TidyDesk-Universal']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}")

def build_windows():
    """Build Windows executable"""
    print("\n🪟 Building TidyDesk for Windows...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=TidyDesk",
        "--icon=file_organizer/icons/app.ico",
        "--add-data=file_organizer/themes;themes",
        "--add-data=file_organizer/icons;icons",
        "--hidden-import=tkinter",
        "--hidden-import=PIL",
        "--hidden-import=schedule",
        "--hidden-import=psutil",
        "--hidden-import=file_organizer.core",
        "--hidden-import=file_organizer.gui",
        "--hidden-import=file_organizer.utils",
        "--version-file=version_info.txt",
        "file_organizer/main.py"
    ]
    
    return run_command(" ".join(cmd), "Windows build")

def build_macos():
    """Build macOS application bundle"""
    print("\n🍎 Building TidyDesk for macOS...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=TidyDesk",
        "--icon=file_organizer/icons/app.icns",
        "--add-data=file_organizer/themes:themes",
        "--add-data=file_organizer/icons:icons",
        "--hidden-import=tkinter",
        "--hidden-import=PIL",
        "--hidden-import=schedule",
        "--hidden-import=psutil",
        "--hidden-import=file_organizer.core",
        "--hidden-import=file_organizer.gui",
        "--hidden-import=file_organizer.utils",
        "--osx-bundle-identifier=com.tiddesk.app",
        "file_organizer/main.py"
    ]
    
    return run_command(" ".join(cmd), "macOS build")

def build_linux():
    """Build Linux executable"""
    print("\n🐧 Building TidyDesk for Linux...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=tiddesk",
        "--icon=file_organizer/icons/icon_256x256.png",
        "--add-data=file_organizer/themes:themes",
        "--add-data=file_organizer/icons:icons",
        "--hidden-import=tkinter",
        "--hidden-import=PIL",
        "--hidden-import=schedule",
        "--hidden-import=psutil",
        "--hidden-import=file_organizer.core",
        "--hidden-import=file_organizer.gui",
        "--hidden-import=file_organizer.utils",
        "file_organizer/main.py"
    ]
    
    return run_command(" ".join(cmd), "Linux build")

def create_dmg_installer():
    """Create DMG installer for macOS"""
    print("\n📦 Creating DMG installer for macOS...")
    
    if not os.path.exists("dist/TidyDesk.app"):
        print("❌ TidyDesk.app not found. Build macOS app first.")
        return False
    
    # Use the professional DMG creator
    try:
        import subprocess
        result = subprocess.run(["python3", "create_professional_dmg.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Professional DMG created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create professional DMG: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_windows_installer():
    """Create Windows installer"""
    print("\n📦 Creating Windows installer...")
    
    if not os.path.exists("dist/TidyDesk.exe"):
        print("❌ TidyDesk.exe not found. Build Windows app first.")
        return False
    
    # Create installer directory
    os.makedirs("installers", exist_ok=True)
    
    # Copy executable
    shutil.copy("dist/TidyDesk.exe", "installers/TidyDesk-Windows.exe")
    print("✅ Windows executable ready: installers/TidyDesk-Windows.exe")
    return True

def create_linux_installer():
    """Create Linux installer"""
    print("\n📦 Creating Linux installer...")
    
    if not os.path.exists("dist/tiddesk"):
        print("❌ tiddesk executable not found. Build Linux app first.")
        return False
    
    # Create installer directory
    os.makedirs("installers", exist_ok=True)
    
    # Copy executable
    shutil.copy("dist/tiddesk", "installers/tiddesk-linux")
    os.chmod("installers/tiddesk-linux", 0o755)
    print("✅ Linux executable ready: installers/tiddesk-linux")
    return True

def create_universal_package():
    """Create a universal package with all platforms"""
    print("\n🌍 Creating universal package...")
    
    # Create universal package directory
    universal_dir = "TidyDesk-Universal"
    if os.path.exists(universal_dir):
        shutil.rmtree(universal_dir)
    os.makedirs(universal_dir)
    
    # Copy platform-specific builds
    if os.path.exists("dist/TidyDesk.exe"):
        os.makedirs(f"{universal_dir}/Windows", exist_ok=True)
        shutil.copy("dist/TidyDesk.exe", f"{universal_dir}/Windows/TidyDesk.exe")
    
    if os.path.exists("dist/TidyDesk.app"):
        shutil.copytree("dist/TidyDesk.app", f"{universal_dir}/macOS/TidyDesk.app")
    
    if os.path.exists("dist/tiddesk"):
        os.makedirs(f"{universal_dir}/Linux", exist_ok=True)
        shutil.copy("dist/tiddesk", f"{universal_dir}/Linux/tiddesk")
        os.chmod(f"{universal_dir}/Linux/tiddesk", 0o755)
    
    # Copy documentation
    docs = ["README.md", "CHANGELOG.md", "BUILD.md", "RULES.md", "BACKUP.md"]
    for doc in docs:
        if os.path.exists(doc):
            shutil.copy(doc, universal_dir)
    
    # Create universal README
    universal_readme = f"""# TidyDesk - Universal Package

This package contains TidyDesk for all supported platforms.

## Installation

### Windows
1. Navigate to the `Windows` folder
2. Run `TidyDesk.exe`

### macOS
1. Navigate to the `macOS` folder
2. Open `TidyDesk.app`

### Linux
1. Navigate to the `Linux` folder
2. Run `./tiddesk`

## Requirements

- Windows 10 or later
- macOS 10.14 or later
- Linux with GTK+ (most modern distributions)

## Documentation

See README.md for detailed usage instructions.

## License

MIT License - see LICENSE file for details.
"""
    
    with open(f"{universal_dir}/README.txt", "w") as f:
        f.write(universal_readme)
    
    print(f"✅ Universal package created: {universal_dir}/")
    return True

def create_version_info():
    """Create version info file for Windows"""
    version_info = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'TidyDesk'),
        StringStruct(u'FileDescription', u'TidyDesk File Organizer'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'TidyDesk'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024 TidyDesk'),
        StringStruct(u'OriginalFilename', u'TidyDesk.exe'),
        StringStruct(u'ProductName', u'TidyDesk'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    with open("version_info.txt", "w") as f:
        f.write(version_info)
    print("✅ Created version_info.txt for Windows")

def main():
    """Main build function"""
    print("🚀 TidyDesk Universal Build Script")
    print("=" * 50)
    
    # Create icons from custom TidyDesk.png
    if not create_icons_from_custom():
        return False
    
    # Create version info for Windows
    create_version_info()
    
    # Clean previous builds
    clean_build_dirs()
    
    # Detect platform and build accordingly
    current_platform = platform.system().lower()
    
    if current_platform == "windows":
        success = build_windows()
        if success:
            create_windows_installer()
    elif current_platform == "darwin":
        success = build_macos()
        if success:
            create_dmg_installer()
    elif current_platform == "linux":
        success = build_linux()
        if success:
            create_linux_installer()
    else:
        print(f"❌ Unsupported platform: {current_platform}")
        return False
    
    if not success:
        print("❌ Build failed!")
        return False
    
    # Create universal package
    create_universal_package()
    
    print("\n🎉 Build completed successfully!")
    print("\n📁 Output files:")
    print("   - dist/ (platform-specific builds)")
    print("   - installers/ (installer packages)")
    print("   - TidyDesk-Universal/ (universal package)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
