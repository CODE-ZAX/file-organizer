# File Organizer Documentation

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [User Guide](#user-guide)
4. [Configuration](#configuration)
5. [Command Line Interface](#command-line-interface)
6. [API Reference](#api-reference)
7. [Development](#development)
8. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.8 or higher
- tkinter (usually included with Python)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Install from PyPI (when published)

```bash
pip install file-organizer
```

## Quick Start

### GUI Mode (Recommended)

```bash
# Start the GUI application
python -m file_organizer

# Or
file-organizer
```

### Command Line Mode

```bash
# Preview organization
python -m file_organizer --preview /path/to/directory

# Organize files
python -m file_organizer --organize /path/to/directory

# Dry run (preview without moving files)
python -m file_organizer --organize /path/to/directory --dry-run
```

## User Guide

### GUI Application

The GUI provides an intuitive interface for file organization:

1. **Directory Selection**: Click "Browse" to select the directory you want to organize
2. **Options**:
   - Enable "Dry run" to preview changes without moving files
   - Enable "Create backup" to backup files before organizing
3. **Actions**:
   - "Preview" shows what files will be organized
   - "Organize Files" performs the actual organization
   - "Settings" opens configuration options
4. **Progress**: Monitor the organization progress in real-time
5. **Log**: View detailed logs of the organization process

### Themes

Switch between light and dark themes using the theme button in the status bar:

- 🌙 Light theme
- ☀️ Dark theme

### Settings

Access settings through the "Settings" button to configure:

- Theme selection
- Scheduler settings
- Organization rules

## Configuration

### Configuration File

The application stores configuration in:

- **Windows**: `%APPDATA%\Local\FileOrganizer\config.json`
- **macOS/Linux**: `~/.config/file-organizer/config.json`

### Default Organization Rules

The application comes with predefined rules for common file types:

- **Images**: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .svg
- **Documents**: .pdf, .doc, .docx, .txt, .rtf, .odt, .pages
- **Videos**: .mp4, .avi, .mov, .wmv, .flv, .webm, .mkv
- **Audio**: .mp3, .wav, .flac, .aac, .ogg, .m4a
- **Archives**: .zip, .rar, .7z, .tar, .gz, .bz2
- **Code**: .py, .js, .html, .css, .java, .cpp, .c, .h, .php, .rb, .go

### Customizing Rules

You can customize organization rules through the settings or by editing the configuration file directly.

## Command Line Interface

### Basic Usage

```bash
python -m file_organizer [OPTIONS]
```

### Options

- `--gui`: Start GUI application (default)
- `--organize DIRECTORY`: Organize files in directory
- `--preview DIRECTORY`: Preview organization
- `--dry-run`: Preview mode (don't move files)
- `--no-backup`: Don't create backup
- `--config FILE`: Use custom config file
- `--log-level LEVEL`: Set logging level
- `--log-file FILE`: Log to file
- `--scheduler COMMAND`: Manage scheduler
- `--version`: Show version
- `--help`: Show help

### Examples

```bash
# Preview organization
python -m file_organizer --preview ~/Downloads

# Organize with dry run
python -m file_organizer --organize ~/Downloads --dry-run

# Organize without backup
python -m file_organizer --organize ~/Downloads --no-backup

# Use custom config
python -m file_organizer --config ~/my_config.json --organize ~/Downloads

# Set log level
python -m file_organizer --log-level DEBUG --organize ~/Downloads
```

### Scheduler Commands

```bash
# Start scheduler
python -m file_organizer --scheduler start

# Stop scheduler
python -m file_organizer --scheduler stop

# Check status
python -m file_organizer --scheduler status
```

## API Reference

### Core Classes

#### FileOrganizer

Main class for file organization.

```python
from file_organizer import FileOrganizer, Config

config = Config()
organizer = FileOrganizer(config)

# Organize directory
stats = organizer.organize_directory("/path/to/directory")

# Preview organization
preview = organizer.preview_organization("/path/to/directory")
```

#### Config

Configuration management.

```python
from file_organizer import Config

config = Config()

# Update configuration
config.update_config(dry_run=True)

# Add custom rule
from file_organizer.core.config import OrganizationRule

rule = OrganizationRule(
    name="Custom Files",
    file_extensions=[".custom"],
    target_folder="Custom"
)
config.add_organization_rule(rule)
```

#### Scheduler

Automatic scheduling.

```python
from file_organizer import Scheduler

def organize_callback():
    # Your organization logic here
    pass

scheduler = Scheduler(config, organize_callback)
scheduler.start()
```

### GUI Classes

#### MainWindow

Main GUI application.

```python
from file_organizer.gui import MainWindow

app = MainWindow()
app.run()
```

## Development

### Project Structure

```
file-organizer/
├── file_organizer/
│   ├── core/           # Core functionality
│   ├── gui/            # GUI components
│   ├── utils/          # Utilities
│   └── main.py         # Main entry point
├── docs/               # Documentation
├── tests/              # Test files
├── setup.py            # Package setup
├── requirements.txt    # Dependencies
└── README.md           # Project README
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=file_organizer
```

### Building

```bash
# Build package
python setup.py sdist bdist_wheel

# Install locally
pip install dist/file_organizer-1.0.0-py3-none-any.whl
```

## Troubleshooting

### Common Issues

#### GUI Not Starting

- Ensure tkinter is installed: `python -m tkinter`
- Check Python version (3.8+ required)
- Verify all dependencies are installed

#### Permission Errors

- Run with appropriate permissions
- Check file/directory permissions
- Ensure target directories are writable

#### Configuration Issues

- Delete config file to reset to defaults
- Check JSON syntax in config file
- Verify file paths are correct

#### Scheduler Not Working

- Check if scheduler is enabled in settings
- Verify time format (HH:MM)
- Check system permissions for background tasks

### Log Files

Log files are stored in:

- **Windows**: `%APPDATA%\Local\FileOrganizer\logs\`
- **macOS/Linux**: `~/.config/file-organizer/logs/`

### Getting Help

1. Check the log files for error details
2. Run with `--log-level DEBUG` for verbose output
3. Create an issue on GitHub with:
   - Error message
   - Log file contents
   - System information
   - Steps to reproduce

### System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows 10+, macOS 10.14+, or Linux
- **Memory**: 100MB minimum
- **Disk**: 50MB for installation
