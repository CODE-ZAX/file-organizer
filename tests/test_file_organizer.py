"""
Tests for the file organizer core functionality
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

from file_organizer.core.config import Config, OrganizationRule
from file_organizer.core.file_organizer import FileOrganizer


class TestFileOrganizer:
    """Test cases for FileOrganizer class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.config = Config()
        self.organizer = FileOrganizer(self.config)
        
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup test fixtures"""
        import shutil
        if self.temp_path.exists():
            shutil.rmtree(self.temp_path)
    
    def test_organize_directory_invalid_path(self):
        """Test organizing with invalid directory path"""
        with pytest.raises(ValueError):
            self.organizer.organize_directory("/invalid/path")
    
    def test_organize_directory_empty_directory(self):
        """Test organizing empty directory"""
        stats = self.organizer.organize_directory(self.temp_dir)
        
        assert stats['files_processed'] == 0
        assert stats['files_moved'] == 0
        assert stats['files_skipped'] == 0
        assert stats['errors'] == 0
    
    def test_organize_directory_with_files(self):
        """Test organizing directory with files"""
        # Create test files
        test_files = [
            "test1.jpg",
            "test2.png", 
            "test3.txt",
            "test4.pdf"
        ]
        
        for filename in test_files:
            (self.temp_path / filename).touch()
        
        # Organize files
        stats = self.organizer.organize_directory(self.temp_dir)
        
        assert stats['files_processed'] == 4
        assert stats['files_moved'] > 0
        assert stats['errors'] == 0
    
    def test_preview_organization(self):
        """Test preview functionality"""
        # Create test files
        (self.temp_path / "test.jpg").touch()
        (self.temp_path / "test.txt").touch()
        
        preview = self.organizer.preview_organization(self.temp_dir)
        
        assert len(preview) > 0
        assert all('file_name' in item for item in preview)
        assert all('target_folder' in item for item in preview)
    
    def test_get_file_stats(self):
        """Test file statistics"""
        # Create test files
        (self.temp_path / "test1.jpg").touch()
        (self.temp_path / "test2.png").touch()
        (self.temp_path / "test3.txt").touch()
        
        stats = self.organizer.get_file_stats(self.temp_dir)
        
        assert stats['total_files'] == 3
        assert '.jpg' in stats['files_by_extension']
        assert '.png' in stats['files_by_extension']
        assert '.txt' in stats['files_by_extension']
    
    def test_dry_run_mode(self):
        """Test dry run mode"""
        # Create test files
        (self.temp_path / "test.jpg").touch()
        
        # Run in dry run mode
        stats = self.organizer.organize_directory(self.temp_dir, dry_run=True)
        
        assert stats['files_processed'] > 0
        # Files should not actually be moved in dry run mode
        assert (self.temp_path / "test.jpg").exists()
    
    def test_progress_callback(self):
        """Test progress callback functionality"""
        progress_calls = []
        
        def progress_callback(progress, message):
            progress_calls.append((progress, message))
        
        organizer = FileOrganizer(self.config, progress_callback)
        
        # Create test files
        (self.temp_path / "test.jpg").touch()
        
        # Organize with progress callback
        organizer.organize_directory(self.temp_dir)
        
        assert len(progress_calls) > 0
        assert all(isinstance(progress, (int, float)) for progress, _ in progress_calls)


class TestConfig:
    """Test cases for Config class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_config.close()
        self.config_path = self.temp_config.name
    
    def teardown_method(self):
        """Cleanup test fixtures"""
        if os.path.exists(self.config_path):
            os.unlink(self.config_path)
    
    def test_config_creation(self):
        """Test config creation with default values"""
        config = Config()
        
        assert config.config is not None
        assert len(config.config.organization_rules) > 0
        assert config.config.scheduler is not None
        assert config.config.ui is not None
    
    def test_config_save_load(self):
        """Test config save and load"""
        config = Config(self.config_path)
        
        # Modify config
        config.update_config(dry_run=True)
        
        # Save and reload
        config.save_config()
        new_config = Config(self.config_path)
        
        assert new_config.config.dry_run == True
    
    def test_add_organization_rule(self):
        """Test adding organization rule"""
        config = Config()
        
        rule = OrganizationRule(
            name="Test Rule",
            file_extensions=[".test"],
            target_folder="Test"
        )
        
        config.add_organization_rule(rule)
        
        added_rule = config.get_organization_rule("Test Rule")
        assert added_rule is not None
        assert added_rule.name == "Test Rule"
    
    def test_remove_organization_rule(self):
        """Test removing organization rule"""
        config = Config()
        
        # Add rule
        rule = OrganizationRule(
            name="Test Rule",
            file_extensions=[".test"],
            target_folder="Test"
        )
        config.add_organization_rule(rule)
        
        # Remove rule
        config.remove_organization_rule("Test Rule")
        
        removed_rule = config.get_organization_rule("Test Rule")
        assert removed_rule is None


class TestOrganizationRule:
    """Test cases for OrganizationRule class"""
    
    def test_organization_rule_creation(self):
        """Test creating organization rule"""
        rule = OrganizationRule(
            name="Test Rule",
            file_extensions=[".test", ".spec"],
            target_folder="Test",
            enabled=True
        )
        
        assert rule.name == "Test Rule"
        assert rule.file_extensions == [".test", ".spec"]
        assert rule.target_folder == "Test"
        assert rule.enabled == True
    
    def test_organization_rule_defaults(self):
        """Test organization rule with defaults"""
        rule = OrganizationRule(
            name="Test Rule",
            file_extensions=[".test"],
            target_folder="Test"
        )
        
        assert rule.enabled == True
