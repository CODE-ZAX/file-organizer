"""
Core file organization functionality
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Callable
from datetime import datetime
import hashlib
import json

from .config import Config, OrganizationRule
from .backup_manager import BackupManager


class FileOrganizer:
    """Main file organizer class"""
    
    def __init__(self, config: Config, progress_callback: Optional[Callable] = None):
        self.config = config
        self.progress_callback = progress_callback
        self.logger = logging.getLogger(__name__)
        self.backup_manager = BackupManager()
        self.stats = {
            'files_processed': 0,
            'files_moved': 0,
            'files_skipped': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }

    def organize_directory(self, directory_path: str, dry_run: bool = False) -> Dict:
        """
        Organize files in the specified directory
        
        Args:
            directory_path: Path to the directory to organize
            dry_run: If True, only simulate the organization without moving files
            
        Returns:
            Dictionary with organization statistics
        """
        self.stats = {
            'files_processed': 0,
            'files_moved': 0,
            'files_skipped': 0,
            'errors': 0,
            'start_time': datetime.now(),
            'end_time': None
        }
        
        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            raise ValueError(f"Directory does not exist or is not a directory: {directory_path}")
        
        self.logger.info(f"Starting organization of directory: {directory_path}")
        self.logger.info(f"Dry run mode: {dry_run}")
        
        # Create backup if enabled and not dry run
        if self.config.config.backup_before_organize and not dry_run:
            self._create_backup(directory)
        
        # Process files
        self._process_directory(directory, dry_run)
        
        self.stats['end_time'] = datetime.now()
        self.logger.info(f"Organization completed. Stats: {self.stats}")
        
        return self.stats

    def _create_backup(self, directory: Path):
        """Create a backup of the directory before organization using BackupManager"""
        try:
            backup_path = self.backup_manager.create_backup(str(directory))
            self.logger.info(f"Backup created at: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            raise

    def _process_directory(self, directory: Path, dry_run: bool):
        """Process all files in the directory"""
        files = [f for f in directory.iterdir() if f.is_file()]
        total_files = len(files)
        
        for i, file_path in enumerate(files):
            try:
                self.stats['files_processed'] += 1
                
                # Update progress
                if self.progress_callback:
                    self.progress_callback(i + 1, total_files, file_path.name)
                
                # Find matching rule
                rule = self._find_matching_rule(file_path)
                if not rule or not rule.enabled:
                    self.stats['files_skipped'] += 1
                    self.logger.debug(f"No rule found for file: {file_path.name}")
                    continue
                
                # Move file
                if self._move_file(file_path, directory, rule, dry_run):
                    self.stats['files_moved'] += 1
                    self.logger.info(f"Moved {file_path.name} to {rule.target_folder}")
                else:
                    self.stats['files_skipped'] += 1
                    
            except Exception as e:
                self.stats['errors'] += 1
                self.logger.error(f"Error processing {file_path.name}: {e}")

    def _find_matching_rule(self, file_path: Path) -> Optional[OrganizationRule]:
        """Find the first matching organization rule for a file"""
        file_extension = file_path.suffix.lower()
        
        for rule in self.config.config.organization_rules:
            if file_extension in [ext.lower() for ext in rule.file_extensions]:
                return rule
        
        return None

    def _move_file(self, file_path: Path, source_dir: Path, rule: OrganizationRule, dry_run: bool) -> bool:
        """Move file to the appropriate folder"""
        try:
            # Create target directory
            target_dir = source_dir / rule.target_folder
            if not dry_run:
                target_dir.mkdir(exist_ok=True)
            
            # Handle duplicate files
            target_path = target_dir / file_path.name
            if target_path.exists():
                target_path = self._get_unique_filename(target_path)
            
            # Move file
            if not dry_run:
                shutil.move(str(file_path), str(target_path))
            else:
                self.logger.info(f"[DRY RUN] Would move {file_path} to {target_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to move file {file_path.name}: {e}")
            return False

    def _get_unique_filename(self, file_path: Path) -> Path:
        """Get a unique filename if the target already exists"""
        if not file_path.exists():
            return file_path
        
        counter = 1
        while True:
            stem = file_path.stem
            suffix = file_path.suffix
            new_name = f"{stem}_{counter}{suffix}"
            new_path = file_path.parent / new_name
            
            if not new_path.exists():
                return new_path
            counter += 1

    def get_file_stats(self, directory_path: str) -> Dict:
        """Get statistics about files in the directory"""
        directory = Path(directory_path)
        if not directory.exists():
            return {}
        
        stats = {
            'total_files': 0,
            'files_by_extension': {},
            'files_by_rule': {},
            'total_size': 0
        }
        
        for file_path in directory.iterdir():
            if file_path.is_file():
                stats['total_files'] += 1
                stats['total_size'] += file_path.stat().st_size
                
                # Count by extension
                ext = file_path.suffix.lower()
                stats['files_by_extension'][ext] = stats['files_by_extension'].get(ext, 0) + 1
                
                # Count by rule
                rule = self._find_matching_rule(file_path)
                if rule:
                    rule_name = rule.name
                    stats['files_by_rule'][rule_name] = stats['files_by_rule'].get(rule_name, 0) + 1
                else:
                    stats['files_by_rule']['Uncategorized'] = stats['files_by_rule'].get('Uncategorized', 0) + 1
        
        return stats

    def preview_organization(self, directory_path: str) -> List[Dict]:
        """Preview what files would be moved where"""
        directory = Path(directory_path)
        if not directory.exists():
            return []
        
        preview = []
        for file_path in directory.iterdir():
            if file_path.is_file():
                rule = self._find_matching_rule(file_path)
                if rule and rule.enabled:
                    preview.append({
                        'file_name': file_path.name,
                        'current_path': str(file_path),
                        'target_folder': rule.target_folder,
                        'rule_name': rule.name,
                        'file_size': file_path.stat().st_size
                    })
        
        return preview

    def create_organization_report(self, directory_path: str) -> str:
        """Create a detailed organization report"""
        stats = self.get_file_stats(directory_path)
        preview = self.preview_organization(directory_path)
        
        report = f"""
File Organization Report
=======================
Directory: {directory_path}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary:
--------
Total files: {stats.get('total_files', 0)}
Total size: {self._format_size(stats.get('total_size', 0))}

Files by category:
-----------------
"""
        
        for rule_name, count in stats.get('files_by_rule', {}).items():
            report += f"{rule_name}: {count} files\n"
        
        report += "\nFiles to be organized:\n"
        report += "-" * 50 + "\n"
        
        for item in preview:
            report += f"{item['file_name']} -> {item['target_folder']} ({self._format_size(item['file_size'])})\n"
        
        return report

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
