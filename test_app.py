#!/usr/bin/env python3
"""
Test script to verify TidyDesk app functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        from file_organizer.core.config import Config
        print("✅ Config imported")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from file_organizer.core.file_organizer import FileOrganizer
        print("✅ FileOrganizer imported")
    except Exception as e:
        print(f"❌ FileOrganizer import failed: {e}")
        return False
    
    try:
        from file_organizer.core.scheduler import Scheduler
        print("✅ Scheduler imported")
    except Exception as e:
        print(f"❌ Scheduler import failed: {e}")
        return False
    
    try:
        from file_organizer.gui.main_window import MainWindow
        print("✅ MainWindow imported")
    except Exception as e:
        print(f"❌ MainWindow import failed: {e}")
        return False
    
    try:
        from file_organizer.gui.theme_manager import ThemeManager
        print("✅ ThemeManager imported")
    except Exception as e:
        print(f"❌ ThemeManager import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from file_organizer.core.config import Config
        config = Config()
        print("✅ Config created successfully")
        
        # Test scheduler config
        scheduler_config = config.config.scheduler
        print(f"✅ Scheduler config: enabled={scheduler_config.enabled}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scheduler():
    """Test scheduler creation"""
    print("\nTesting scheduler...")
    
    try:
        from file_organizer.core.config import Config
        from file_organizer.core.scheduler import Scheduler
        
        config = Config()
        
        def dummy_callback():
            pass
        
        scheduler = Scheduler(config, dummy_callback)
        print("✅ Scheduler created successfully")
        
        # Test methods
        print(f"✅ Scheduler running: {scheduler.is_running()}")
        print(f"✅ Scheduler status: {scheduler.get_status()}")
        
        return True
    except Exception as e:
        print(f"❌ Scheduler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_creation():
    """Test GUI creation (without showing)"""
    print("\nTesting GUI creation...")
    
    try:
        from file_organizer.core.config import Config
        from file_organizer.gui.main_window import MainWindow
        
        config = Config()
        
        # Create MainWindow but don't run it
        app = MainWindow(config)
        print("✅ MainWindow created successfully")
        
        # Test some basic properties
        print(f"✅ Window title: {app.root.title()}")
        print(f"✅ Theme manager: {type(app.theme_manager).__name__}")
        
        # Clean up
        app.root.destroy()
        print("✅ GUI cleaned up successfully")
        
        return True
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 TidyDesk App Test Suite")
    print("=" * 30)
    
    tests = [
        test_imports,
        test_config,
        test_scheduler,
        test_gui_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! App should work correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
