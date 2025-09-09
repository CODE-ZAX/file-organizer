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

def create_professional_dmg():
    """Create a professional DMG installer with proper layout"""
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
        
        # Create DMG with proper formatting
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
            
            # Now create a proper installer DMG with AppleScript
            create_installer_dmg(dmg_path)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create DMG: {e}")
            return False

def create_installer_dmg(dmg_path):
    """Create a proper installer DMG with AppleScript"""
    print("🔧 Creating installer DMG with proper layout...")
    
    # Create AppleScript to set up the DMG layout
    applescript = '''
    tell application "Finder"
        set theDMG to POSIX file "''' + os.path.abspath(dmg_path) + '''" as alias
        open theDMG
        delay 2
        
        set theWindow to window "TidyDesk"
        set theView to current view of theWindow
        
        -- Set view options
        set current view of theWindow to list view
        set toolbar visible of theWindow to false
        set statusbar visible of theWindow to false
        set bounds of theWindow to {100, 100, 600, 400}
        
        -- Set icon positions
        set position of item "TidyDesk.app" of theWindow to {100, 100}
        set position of item "Applications" of theWindow to {300, 100}
        
        -- Set background
        set background picture of theWindow to none
        
        -- Close the window
        close theWindow
    end tell
    '''
    
    # Write AppleScript to temporary file
    script_path = "setup_dmg.applescript"
    with open(script_path, "w") as f:
        f.write(applescript)
    
    try:
        # Run AppleScript
        subprocess.run(["osascript", script_path], check=True)
        print("✅ DMG layout configured successfully")
        
        # Clean up
        os.remove(script_path)
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Could not configure DMG layout: {e}")
        # Clean up anyway
        if os.path.exists(script_path):
            os.remove(script_path)

def test_app():
    """Test the app to see if it crashes"""
    print("🧪 Testing TidyDesk app...")
    
    if not os.path.exists("dist/TidyDesk.app"):
        print("❌ TidyDesk.app not found")
        return False
    
    try:
        # Try to run the app and capture output
        result = subprocess.run([
            "open", "-W", "dist/TidyDesk.app"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ App launched successfully")
            return True
        else:
            print(f"❌ App failed to launch: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  App launch timed out (may be normal)")
        return True
    except Exception as e:
        print(f"❌ Error testing app: {e}")
        return False

def check_app_logs():
    """Check system logs for app crashes"""
    print("🔍 Checking system logs for TidyDesk...")
    
    try:
        # Check Console logs for TidyDesk
        result = subprocess.run([
            "log", "show", "--predicate", "process == 'TidyDesk'", "--last", "1m"
        ], capture_output=True, text=True)
        
        if result.stdout:
            print("📋 Recent TidyDesk logs:")
            print(result.stdout)
        else:
            print("ℹ️  No recent TidyDesk logs found")
            
    except Exception as e:
        print(f"⚠️  Could not check logs: {e}")

def main():
    """Main function"""
    print("🚀 TidyDesk Professional DMG Creator")
    print("=" * 40)
    
    # Test the app first
    print("\n1. Testing app...")
    test_app()
    
    # Check logs
    print("\n2. Checking logs...")
    check_app_logs()
    
    # Create DMG
    print("\n3. Creating DMG...")
    if create_professional_dmg():
        print("\n🎉 Professional DMG installer created successfully!")
        print("\n📁 Output files:")
        print("   - installers/TidyDesk-macOS.dmg")
        
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
