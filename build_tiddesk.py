"""
TidyDesk Universal Build Script
Creates cross-platform builds for Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import shutil
import platform
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
    dirs_to_clean = ['build', 'dist', '__pycache__']
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

def create_installers():
    """Create platform-specific installers"""
    print("\n📦 Creating installers...")
    
    # Create installer directories
    os.makedirs("installers", exist_ok=True)
    
    current_platform = platform.system().lower()
    
    if current_platform == "windows":
        if os.path.exists("dist/TidyDesk.exe"):
            shutil.copy("dist/TidyDesk.exe", "installers/TidyDesk-Windows.exe")
            print("📦 Windows executable ready: installers/TidyDesk-Windows.exe")
    
    elif current_platform == "darwin":
        if os.path.exists("dist/TidyDesk.app"):
            # Create DMG
            dmg_cmd = "hdiutil create -volname 'TidyDesk' -srcfolder dist/TidyDesk.app -ov -format UDZO installers/TidyDesk-macOS.dmg"
            run_command(dmg_cmd, "macOS DMG creation")
            print("📦 macOS app ready: dist/TidyDesk.app")
    
    elif current_platform == "linux":
        if os.path.exists("dist/tiddesk"):
            shutil.copy("dist/tiddesk", "installers/tiddesk-linux")
            os.chmod("installers/tiddesk-linux", 0o755)
            print("📦 Linux executable ready: installers/tiddesk-linux")

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
    docs = ["README.md", "LICENSE", "CHANGELOG.md"]
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

See LICENSE for license information.
"""
    
    with open(f"{universal_dir}/README.txt", "w") as f:
        f.write(universal_readme)
    
    print(f"✅ Universal package created: {universal_dir}/")

def main():
    """Main build function"""
    print("🚀 TidyDesk Universal Build Script")
    print("=" * 50)
    
    # Create icons from custom TidyDesk.png
    if not create_icons_from_custom():
        return False
    
    # Clean previous builds
    clean_build_dirs()
    
    # Detect platform and build accordingly
    current_platform = platform.system().lower()
    
    if current_platform == "windows":
        success = build_windows()
    elif current_platform == "darwin":
        success = build_macos()
    elif current_platform == "linux":
        success = build_linux()
    else:
        print(f"❌ Unsupported platform: {current_platform}")
        return False
    
    if not success:
        print("❌ Build failed!")
        return False
    
    # Create installers
    create_installers()
    
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
