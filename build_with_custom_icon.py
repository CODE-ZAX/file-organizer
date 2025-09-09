"""
Build script for creating universal packages with custom icon
"""

import os
import sys
import subprocess
import shutil
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

def build_current_platform():
    """Build for current platform with custom icon"""
    platform = sys.platform.lower()
    
    if platform.startswith('win'):
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
            "file_organizer/main.py"
        ]
    elif platform.startswith('darwin'):
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
            "--osx-bundle-identifier=com.tiddesk.app",
            "file_organizer/main.py"
        ]
    else:  # Linux
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
            "file_organizer/main.py"
        ]
    
    return run_command(" ".join(cmd), f"{platform} build with custom icon")

def create_installers():
    """Create platform-specific installers"""
    print("\n📦 Creating installers...")
    
    # Create installer directories
    os.makedirs("installers", exist_ok=True)
    
    platform = sys.platform.lower()
    
    if platform.startswith('win'):
        if os.path.exists("dist/TidyDesk.exe"):
            shutil.copy("dist/TidyDesk.exe", "installers/TidyDesk-Windows.exe")
            print("📦 Windows executable ready: installers/TidyDesk-Windows.exe")
    
    elif platform.startswith('darwin'):
        if os.path.exists("dist/TidyDesk.app"):
            # Create DMG
            dmg_cmd = "hdiutil create -volname 'TidyDesk' -srcfolder dist/TidyDesk.app -ov -format UDZO installers/TidyDesk-macOS.dmg"
            run_command(dmg_cmd, "macOS DMG creation")
            print("📦 macOS app ready: dist/TidyDesk.app")
    
    else:  # Linux
        if os.path.exists("dist/tiddesk"):
            shutil.copy("dist/tiddesk", "installers/tiddesk-linux")
            os.chmod("installers/tiddesk-linux", 0o755)
            print("📦 Linux executable ready: installers/tiddesk-linux")

def main():
    """Main build function"""
    print("🚀 TidyDesk Universal Build Script")
    print("=" * 50)
    
    # Create icons from custom TidyDesk.png
    if not create_icons_from_custom():
        return False
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build for current platform
    success = build_current_platform()
    
    if not success:
        print("❌ Build failed!")
        return False
    
    # Create installers
    create_installers()
    
    print("\n🎉 Build completed successfully!")
    print("\n📁 Output files:")
    print("   - dist/ (platform-specific builds)")
    print("   - installers/ (installer packages)")
    print("   - file_organizer/icons/ (custom icons)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
