#!/usr/bin/env python3
"""
Backup Manager Demo for TidyDesk
"""

import sys
import os
import tempfile
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_organizer.core.backup_manager import BackupManager

def create_test_files():
    """Create some test files for backup demo"""
    test_dir = Path(tempfile.mkdtemp(prefix="tiddesk_test_"))
    
    # Create test files
    (test_dir / "test1.txt").write_text("This is test file 1")
    (test_dir / "test2.txt").write_text("This is test file 2")
    (test_dir / "subdir").mkdir()
    (test_dir / "subdir" / "test3.txt").write_text("This is test file 3 in subdirectory")
    
    return test_dir

def main():
    """Backup manager demo"""
    print("💾 TidyDesk Backup Manager Demo")
    print("=" * 40)
    
    # Create backup manager
    backup_manager = BackupManager()
    print(f"✅ Backup manager initialized")
    print(f"📁 Backup directory: {backup_manager.backup_dir}")
    
    # Create test files
    print("\n📝 Creating test files...")
    test_dir = create_test_files()
    print(f"✅ Test directory created: {test_dir}")
    
    # Create backup
    print("\n💾 Creating backup...")
    try:
        backup_path = backup_manager.create_backup(str(test_dir), "demo_backup")
        print(f"✅ Backup created: {backup_path}")
    except Exception as e:
        print(f"❌ Backup creation failed: {e}")
        return
    
    # List backups
    print("\n📋 Listing backups...")
    backups = backup_manager.list_backups()
    print(f"✅ Found {len(backups)} backups:")
    
    for backup in backups:
        print(f"  - {backup['backup_name']}")
        print(f"    Created: {backup['created_at']}")
        print(f"    Source: {backup['source_path']}")
        print(f"    Size: {backup['size_mb']:.1f} MB")
        print(f"    Files: {backup['file_count']}")
        print()
    
    # Get storage info
    print("📊 Storage information:")
    storage_info = backup_manager.get_backup_size()
    print(f"  Total backups: {storage_info['backup_count']}")
    print(f"  Total size: {storage_info['total_size_mb']:.1f} MB")
    print(f"  Total size: {storage_info['total_size_gb']:.2f} GB")
    
    # Test restore
    print("\n🔄 Testing restore...")
    restore_dir = Path(tempfile.mkdtemp(prefix="tiddesk_restore_"))
    try:
        restored_path = backup_manager.restore_backup(backup_path, str(restore_dir))
        print(f"✅ Backup restored to: {restored_path}")
        
        # Verify restored files
        restored_files = list(Path(restored_path).rglob("*"))
        print(f"✅ Restored {len(restored_files)} files/directories")
        
    except Exception as e:
        print(f"❌ Restore failed: {e}")
    
    # Cleanup test files
    print("\n🧹 Cleaning up test files...")
    import shutil
    shutil.rmtree(test_dir, ignore_errors=True)
    shutil.rmtree(restore_dir, ignore_errors=True)
    print("✅ Test files cleaned up")
    
    # Cleanup old backups (keep only 5)
    print("\n🗑️  Cleaning up old backups...")
    try:
        deleted_count = backup_manager.cleanup_old_backups(5)
        print(f"✅ Deleted {deleted_count} old backups")
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
    
    print("\n🎉 Backup manager demo completed!")
    print("\n💡 To use the GUI:")
    print("   python3 -m file_organizer --gui")
    print("   Then click 'Backups' to manage backups")

if __name__ == "__main__":
    main()
