# File Organizer API Reference

## Core Classes

### FileOrganizer

The main class for file organization operations.

```python
from file_organizer import FileOrganizer, Config

config = Config()
organizer = FileOrganizer(config, progress_callback=None)
```

#### Methods

##### `__init__(config, progress_callback=None)`

Initialize the file organizer.

**Parameters:**

- `config` (Config): Configuration object
- `progress_callback` (callable, optional): Callback function for progress updates

**Callback signature:**

```python
def progress_callback(progress: float, message: str):
    # progress: 0.0 to 100.0
    # message: Status message
    pass
```

##### `organize_directory(directory_path, dry_run=False)`

Organize files in the specified directory.

**Parameters:**

- `directory_path` (str): Path to directory to organize
- `dry_run` (bool): If True, only simulate organization

**Returns:**

- `dict`: Statistics about the organization process

**Example:**

```python
stats = organizer.organize_directory("/path/to/directory")
print(f"Files moved: {stats['files_moved']}")
```

##### `preview_organization(directory_path)`

Preview what files would be organized.

**Parameters:**

- `directory_path` (str): Path to directory to preview

**Returns:**

- `list`: List of files that would be organized

**Example:**

```python
preview = organizer.preview_organization("/path/to/directory")
for item in preview:
    print(f"{item['file_name']} -> {item['target_folder']}")
```

##### `get_file_stats(directory_path)`

Get statistics about files in the directory.

**Parameters:**

- `directory_path` (str): Path to directory

**Returns:**

- `dict`: File statistics

**Example:**

```python
stats = organizer.get_file_stats("/path/to/directory")
print(f"Total files: {stats['total_files']}")
```

### Config

Configuration management class.

```python
from file_organizer import Config

config = Config()
```

#### Methods

##### `__init__(config_path=None)`

Initialize configuration.

**Parameters:**

- `config_path` (str, optional): Path to custom config file

##### `save_config()`

Save current configuration to file.

##### `update_config(**kwargs)`

Update configuration values.

**Example:**

```python
config.update_config(dry_run=True)
config.update_config(ui={"theme": "dark"})
```

##### `add_organization_rule(rule)`

Add a new organization rule.

**Parameters:**

- `rule` (OrganizationRule): Rule to add

##### `remove_organization_rule(rule_name)`

Remove an organization rule.

**Parameters:**

- `rule_name` (str): Name of rule to remove

##### `get_organization_rule(rule_name)`

Get organization rule by name.

**Parameters:**

- `rule_name` (str): Name of rule

**Returns:**

- `OrganizationRule` or `None`

### OrganizationRule

Represents a file organization rule.

```python
from file_organizer.core.config import OrganizationRule

rule = OrganizationRule(
    name="Images",
    file_extensions=[".jpg", ".png"],
    target_folder="Images",
    enabled=True
)
```

#### Attributes

- `name` (str): Rule name
- `file_extensions` (list): List of file extensions
- `target_folder` (str): Target folder name
- `enabled` (bool): Whether rule is enabled

### Scheduler

Scheduler for automatic file organization.

```python
from file_organizer import Scheduler

def organize_callback():
    # Your organization logic
    pass

scheduler = Scheduler(config, organize_callback)
```

#### Methods

##### `start()`

Start the scheduler.

##### `stop()`

Stop the scheduler.

##### `is_running()`

Check if scheduler is running.

**Returns:**

- `bool`: True if running

##### `get_next_run_time()`

Get next scheduled run time.

**Returns:**

- `datetime` or `None`

##### `get_schedule_info()`

Get detailed schedule information.

**Returns:**

- `dict`: Schedule information

##### `update_schedule(new_config)`

Update scheduler configuration.

**Parameters:**

- `new_config` (SchedulerConfig): New configuration

##### `run_now()`

Manually trigger organization.

##### `get_status()`

Get human-readable status.

**Returns:**

- `str`: Status description

## GUI Classes

### MainWindow

Main GUI application window.

```python
from file_organizer.gui import MainWindow

app = MainWindow()
app.run()
```

#### Methods

##### `__init__()`

Initialize the main window.

##### `run()`

Start the GUI application.

### ThemeManager

Theme management for the GUI.

```python
from file_organizer.gui import ThemeManager

theme_manager = ThemeManager()
```

#### Methods

##### `get_theme(theme_name=None)`

Get theme by name or current theme.

**Parameters:**

- `theme_name` (str, optional): Theme name

**Returns:**

- `dict`: Theme configuration

##### `set_theme(theme_name)`

Set the current theme.

**Parameters:**

- `theme_name` (str): Theme name

##### `get_available_themes()`

Get list of available themes.

**Returns:**

- `list`: List of theme names

##### `get_color(color_name, theme_name=None)`

Get color from theme.

**Parameters:**

- `color_name` (str): Color name
- `theme_name` (str, optional): Theme name

**Returns:**

- `str`: Color value

##### `create_tkinter_style(theme_name=None)`

Create tkinter-compatible style.

**Returns:**

- `dict`: Style dictionary

## Utility Classes

### Logging

```python
from file_organizer.utils import setup_logging, get_logger

# Setup logging
logger = setup_logging(log_level="INFO", log_file="app.log")

# Get logger
logger = get_logger("my_module")
```

### Exceptions

```python
from file_organizer.utils import (
    FileOrganizerError,
    ConfigurationError,
    OrganizationError,
    SchedulerError,
    ThemeError,
    ValidationError
)
```

## Configuration Schema

### AppConfig

```python
{
    "organization_rules": [
        {
            "name": "Images",
            "file_extensions": [".jpg", ".png"],
            "target_folder": "Images",
            "enabled": True
        }
    ],
    "scheduler": {
        "enabled": False,
        "interval_hours": 24,
        "time": "09:00",
        "days": [0, 1, 2, 3, 4, 5, 6]
    },
    "ui": {
        "theme": "light",
        "window_width": 800,
        "window_height": 600,
        "remember_window_size": True,
        "remember_last_directory": True,
        "last_directory": ""
    },
    "log_level": "INFO",
    "backup_before_organize": True,
    "dry_run": False
}
```

## Examples

### Basic Organization

```python
from file_organizer import FileOrganizer, Config

# Create configuration
config = Config()

# Create organizer
organizer = FileOrganizer(config)

# Organize directory
stats = organizer.organize_directory("/path/to/directory")
print(f"Organized {stats['files_moved']} files")
```

### Custom Rules

```python
from file_organizer import Config
from file_organizer.core.config import OrganizationRule

config = Config()

# Add custom rule
custom_rule = OrganizationRule(
    name="Custom Files",
    file_extensions=[".custom", ".special"],
    target_folder="Custom"
)
config.add_organization_rule(custom_rule)

# Save configuration
config.save_config()
```

### Scheduled Organization

```python
from file_organizer import Scheduler, Config

config = Config()

def organize_files():
    organizer = FileOrganizer(config)
    organizer.organize_directory("/path/to/directory")

# Create scheduler
scheduler = Scheduler(config, organize_files)

# Start scheduler
scheduler.start()
```

### Progress Tracking

```python
def progress_callback(progress, message):
    print(f"{message}: {progress:.1f}%")

organizer = FileOrganizer(config, progress_callback)
organizer.organize_directory("/path/to/directory")
```

### Custom Theme

```python
from file_organizer.gui import ThemeManager

theme_manager = ThemeManager()

# Get current theme
theme = theme_manager.get_theme()

# Get specific color
primary_color = theme_manager.get_color("accent_primary")

# Create tkinter style
style = theme_manager.create_tkinter_style()
```
