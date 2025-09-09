#!/usr/bin/env python3
"""
Create a professional DMG installer for TidyDesk on macOS
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

def create_dmg_installer():
    """Create a professional DMG installer"""
    print("🍎 Creating professional DMG installer for TidyDesk...")
    
    # Check if TidyDesk.app exists
    if not os.path.exists("dist/TidyDesk.app"):
        print("❌ TidyDesk.app not found. Build the macOS app first.")
        return False
    
    # Create temporary directory for DMG contents
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create DMG structure
        dmg_contents = temp_path / "TidyDesk"
        dmg_contents.mkdir()
        
        # Copy the app
        shutil.copytree("dist/TidyDesk.app", dmg_contents / "TidyDesk.app")
        
        # Create Applications symlink
        applications_link = dmg_contents / "Applications"
        applications_link.symlink_to("/Applications")
        
        # Create a proper DMG layout with background and positioning
        # This will be handled by the DMG creation process
        
        # Create README
        readme_content = """# TidyDesk

Welcome to TidyDesk - Your File Organization Solution

## Installation

1. Drag TidyDesk.app to the Applications folder
2. Open TidyDesk from Applications or Launchpad
3. Start organizing your files!

## Features

- Modern, intuitive interface
- Custom organization rules
- Automatic backup system
- Cross-platform compatibility
- Light theme for comfortable usage

## Support

For support and updates, visit:
https://github.com/code-zax/tiddesk

## License

MIT License - See LICENSE file for details

Enjoy organizing your files with TidyDesk! 🎉
"""
        
        with open(dmg_contents / "README.txt", "w") as f:
            f.write(readme_content)
        
        # Create DMG
        dmg_path = "installers/TidyDesk-macOS.dmg"
        os.makedirs("installers", exist_ok=True)
        
        # Remove existing DMG if it exists
        if os.path.exists(dmg_path):
            os.remove(dmg_path)
        
        # Create DMG with proper formatting
        cmd = [
            "hdiutil", "create",
            "-volname", "TidyDesk",
            "-srcfolder", str(dmg_contents),
            "-ov",
            "-format", "UDZO",
            "-fs", "HFS+",
            dmg_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ DMG created successfully: {dmg_path}")
            
            # Get DMG size
            size = os.path.getsize(dmg_path)
            size_mb = size / (1024 * 1024)
            print(f"📦 DMG size: {size_mb:.1f} MB")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create DMG: {e}")
            return False

def create_installer_script():
    """Create an installer script for the DMG"""
    installer_script = """#!/bin/bash
# TidyDesk DMG Installer Script

echo "Installing TidyDesk..."

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This installer is for macOS only."
    exit 1
fi

# Check if TidyDesk.app exists in the DMG
if [ ! -d "TidyDesk.app" ]; then
    echo "Error: TidyDesk.app not found in this DMG."
    exit 1
fi

# Copy to Applications
echo "Copying TidyDesk.app to Applications..."
cp -R "TidyDesk.app" "/Applications/"

# Set permissions
chmod -R 755 "/Applications/TidyDesk.app"

echo "✅ TidyDesk installed successfully!"
echo "You can now open TidyDesk from Applications or Launchpad."

# Ask if user wants to open the app
read -p "Would you like to open TidyDesk now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "/Applications/TidyDesk.app"
fi
"""
    
    with open("installers/install.sh", "w") as f:
        f.write(installer_script)
    
    os.chmod("installers/install.sh", 0o755)
    print("✅ Created installer script: installers/install.sh")

def main():
    """Main function"""
    print("🚀 TidyDesk DMG Creator")
    print("=" * 30)
    
    # Create DMG
    if create_dmg_installer():
        # Create installer script
        create_installer_script()
        
        print("\n🎉 DMG installer created successfully!")
        print("\n📁 Output files:")
        print("   - installers/TidyDesk-macOS.dmg")
        print("   - installers/install.sh")
        
        print("\n📋 Installation instructions:")
        print("1. Open TidyDesk-macOS.dmg")
        print("2. Drag TidyDesk.app to Applications folder")
        print("3. Open TidyDesk from Applications or Launchpad")
        
        return True
    else:
        print("❌ Failed to create DMG installer")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
