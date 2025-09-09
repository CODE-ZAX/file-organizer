"""
Backup management for TidyDesk
Handles backup creation, restoration, and cleanup
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import json


class BackupManager:
    """Manages file backups and restoration"""
    
    def __init__(self, backup_dir: Optional[str] = None):
        self.backup_dir = Path(backup_dir) if backup_dir else self._get_default_backup_dir()
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_default_backup_dir(self) -> Path:
        """Get default backup directory"""
        if os.name == 'nt':  # Windows
            base_dir = Path.home() / "AppData" / "Local" / "TidyDesk"
        else:  # macOS/Linux
            # Use Documents folder for better accessibility
            base_dir = Path.home() / "Documents" / "TidyDesk"
        
        return base_dir / "backups"
    
    def create_backup(self, source_path: str, backup_name: Optional[str] = None) -> str:
        """Create a backup of a file or directory"""
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Source path does not exist: {source_path}")
        
        if backup_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
        
        backup_path = self.backup_dir / f"{backup_name}.zip"
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if source.is_file():
                    zipf.write(source, source.name)
                else:
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(source)
                            zipf.write(file_path, arcname)
            
            # Create backup metadata
            metadata = {
                "backup_name": backup_name,
                "source_path": str(source.absolute()),
                "created_at": datetime.now().isoformat(),
                "backup_type": "file" if source.is_file() else "directory",
                "file_count": self._count_files(source),
                "total_size": self._get_size(source)
            }
            
            metadata_path = self.backup_dir / f"{backup_name}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return str(backup_path)
            
        except Exception as e:
            # Clean up failed backup
            if backup_path.exists():
                backup_path.unlink()
            raise Exception(f"Failed to create backup: {e}")
    
    def restore_backup(self, backup_path: str, target_path: Optional[str] = None) -> str:
        """Restore a backup to a target location"""
        backup_file = Path(backup_path)
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file does not exist: {backup_path}")
        
        # Load metadata
        metadata_path = backup_file.with_suffix('.zip_metadata.json')
        if not metadata_path.exists():
            metadata_path = backup_file.parent / f"{backup_file.stem}_metadata.json"
        
        metadata = {}
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        # Determine target path
        if target_path is None:
            target_path = metadata.get("source_path", str(backup_file.parent / "restored"))
        
        target = Path(target_path)
        target.mkdir(parents=True, exist_ok=True)
        
        try:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(target)
            
            return str(target)
            
        except Exception as e:
            raise Exception(f"Failed to restore backup: {e}")
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups"""
        backups = []
        
        for backup_file in self.backup_dir.glob("*.zip"):
            metadata_path = backup_file.with_suffix('.zip_metadata.json')
            if not metadata_path.exists():
                metadata_path = backup_file.parent / f"{backup_file.stem}_metadata.json"
            
            metadata = {}
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                except:
                    pass
            
            backup_info = {
                "backup_name": backup_file.stem,
                "backup_path": str(backup_file),
                "created_at": metadata.get("created_at", "Unknown"),
                "source_path": metadata.get("source_path", "Unknown"),
                "backup_type": metadata.get("backup_type", "Unknown"),
                "file_count": metadata.get("file_count", 0),
                "total_size": metadata.get("total_size", 0),
                "size_mb": round(backup_file.stat().st_size / (1024 * 1024), 2)
            }
            backups.append(backup_info)
        
        # Sort by creation date (newest first)
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        return backups
    
    def delete_backup(self, backup_name: str) -> bool:
        """Delete a backup and its metadata"""
        try:
            backup_file = self.backup_dir / f"{backup_name}.zip"
            metadata_file = self.backup_dir / f"{backup_name}_metadata.json"
            
            if backup_file.exists():
                backup_file.unlink()
            if metadata_file.exists():
                metadata_file.unlink()
            
            return True
        except Exception as e:
            print(f"Error deleting backup {backup_name}: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """Delete old backups, keeping only the specified number"""
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            return 0
        
        deleted_count = 0
        for backup in backups[keep_count:]:
            if self.delete_backup(backup["backup_name"]):
                deleted_count += 1
        
        return deleted_count
    
    def get_backup_size(self) -> Dict[str, Any]:
        """Get total backup storage usage"""
        total_size = 0
        backup_count = 0
        
        for backup_file in self.backup_dir.glob("*.zip"):
            total_size += backup_file.stat().st_size
            backup_count += 1
        
        return {
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "total_size_gb": round(total_size / (1024 * 1024 * 1024), 2),
            "backup_count": backup_count
        }
    
    def _count_files(self, path: Path) -> int:
        """Count files in a directory"""
        if path.is_file():
            return 1
        
        count = 0
        for root, dirs, files in os.walk(path):
            count += len(files)
        return count
    
    def _get_size(self, path: Path) -> int:
        """Get total size of a file or directory"""
        if path.is_file():
            return path.stat().st_size
        
        total_size = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = Path(root) / file
                try:
                    total_size += file_path.stat().st_size
                except:
                    pass
        return total_size
