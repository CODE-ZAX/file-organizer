"""
Configuration management for the file organizer
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class OrganizationRule:
    """Represents a file organization rule"""
    name: str
    file_extensions: list
    target_folder: str
    enabled: bool = True


@dataclass
class SchedulerConfig:
    """Scheduler configuration"""
    enabled: bool = False
    interval_hours: int = 24
    time: str = "09:00"  # HH:MM format
    days: list = None  # List of days (0=Monday, 6=Sunday), None means daily

    def __post_init__(self):
        if self.days is None:
            self.days = list(range(7))  # All days by default


@dataclass
class UIConfig:
    """UI configuration"""
    theme: str = "light"  # "light" or "dark"
    window_width: int = 800
    window_height: int = 600
    remember_window_size: bool = True
    remember_last_directory: bool = True
    last_directory: str = ""


@dataclass
class AppConfig:
    """Main application configuration"""
    organization_rules: list
    scheduler: SchedulerConfig
    ui: UIConfig
    log_level: str = "INFO"
    backup_before_organize: bool = True
    dry_run: bool = False

    def __post_init__(self):
        if not isinstance(self.organization_rules, list):
            self.organization_rules = []
        if not isinstance(self.scheduler, SchedulerConfig):
            self.scheduler = SchedulerConfig()
        if not isinstance(self.ui, UIConfig):
            self.ui = UIConfig()


class Config:
    """Configuration manager"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config: Optional[AppConfig] = None
        self._load_config()

    def _get_default_config_path(self) -> str:
        """Get the default configuration file path"""
        if os.name == 'nt':  # Windows
            config_dir = Path.home() / "AppData" / "Local" / "FileOrganizer"
        else:  # macOS and Linux
            config_dir = Path.home() / ".config" / "file-organizer"
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "config.json")

    def _load_config(self):
        """Load configuration from file or create default"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._config = self._dict_to_config(data)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Error loading config: {e}. Using default configuration.")
                self._config = self._create_default_config()
        else:
            self._config = self._create_default_config()

    def _create_default_config(self) -> AppConfig:
        """Create default configuration"""
        default_rules = [
            OrganizationRule(
                name="Images",
                file_extensions=[".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
                target_folder="Images"
            ),
            OrganizationRule(
                name="Documents",
                file_extensions=[".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"],
                target_folder="Documents"
            ),
            OrganizationRule(
                name="Videos",
                file_extensions=[".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mkv"],
                target_folder="Videos"
            ),
            OrganizationRule(
                name="Audio",
                file_extensions=[".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
                target_folder="Audio"
            ),
            OrganizationRule(
                name="Archives",
                file_extensions=[".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
                target_folder="Archives"
            ),
            OrganizationRule(
                name="Code",
                file_extensions=[".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".php", ".rb", ".go"],
                target_folder="Code"
            )
        ]

        return AppConfig(
            organization_rules=default_rules,
            scheduler=SchedulerConfig(),
            ui=UIConfig()
        )

    def _dict_to_config(self, data: Dict[str, Any]) -> AppConfig:
        """Convert dictionary to AppConfig object"""
        # Convert organization rules
        rules = []
        for rule_data in data.get("organization_rules", []):
            rules.append(OrganizationRule(**rule_data))
        
        # Convert scheduler config
        scheduler_data = data.get("scheduler", {})
        scheduler = SchedulerConfig(**scheduler_data)
        
        # Convert UI config
        ui_data = data.get("ui", {})
        ui = UIConfig(**ui_data)
        
        return AppConfig(
            organization_rules=rules,
            scheduler=scheduler,
            ui=ui,
            log_level=data.get("log_level", "INFO"),
            backup_before_organize=data.get("backup_before_organize", True),
            dry_run=data.get("dry_run", False)
        )

    def save_config(self):
        """Save current configuration to file"""
        try:
            config_dict = asdict(self._config)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    @property
    def config(self) -> AppConfig:
        """Get current configuration"""
        return self._config

    def update_config(self, **kwargs):
        """Update configuration values"""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
        self.save_config()

    def add_organization_rule(self, rule: OrganizationRule):
        """Add a new organization rule"""
        self._config.organization_rules.append(rule)
        self.save_config()

    def remove_organization_rule(self, rule_name: str):
        """Remove an organization rule by name"""
        self._config.organization_rules = [
            rule for rule in self._config.organization_rules 
            if rule.name != rule_name
        ]
        self.save_config()

    def get_organization_rule(self, rule_name: str) -> Optional[OrganizationRule]:
        """Get organization rule by name"""
        for rule in self._config.organization_rules:
            if rule.name == rule_name:
                return rule
        return None
