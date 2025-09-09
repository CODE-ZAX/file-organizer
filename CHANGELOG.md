# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added

- Initial release of TidyDesk
- GUI application with modern interface
- Dark and light theme support
- Cross-platform compatibility (Windows, macOS, Linux)
- Command-line interface
- Custom scheduler for automatic organization
- Configurable organization rules
- Preview mode for safe organization
- Backup functionality before organizing
- Comprehensive logging system
- Progress tracking and real-time updates
- Settings management
- Support for common file types:
  - Images (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .svg)
  - Documents (.pdf, .doc, .docx, .txt, .rtf, .odt, .pages)
  - Videos (.mp4, .avi, .mov, .wmv, .flv, .webm, .mkv)
  - Audio (.mp3, .wav, .flac, .aac, .ogg, .m4a)
  - Archives (.zip, .rar, .7z, .tar, .gz, .bz2)
  - Code files (.py, .js, .html, .css, .java, .cpp, .c, .h, .php, .rb, .go)

### Features

- **GUI Mode**: Intuitive graphical interface with directory selection
- **CLI Mode**: Command-line interface for automation and scripting
- **Scheduler**: Automatic file organization with customizable schedules
- **Themes**: Beautiful dark and light themes
- **Preview**: Safe preview mode to see changes before applying
- **Backup**: Automatic backup creation before organization
- **Custom Rules**: Create and manage custom organization rules
- **Progress Tracking**: Real-time progress updates and detailed logging
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Configuration**: Persistent settings and configuration management

### Technical Details

- Python 3.8+ support
- tkinter-based GUI
- Thread-safe operations
- Comprehensive error handling
- Logging with rotation
- Configuration file management
- Modular architecture
- Type hints throughout
- Comprehensive documentation

### Installation

```bash
# From source
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer
pip install -e .

# From PyPI (when published)
pip install file-organizer
```

### Usage

```bash
# GUI mode
python -m file_organizer

# CLI mode
python -m file_organizer --organize /path/to/directory
python -m file_organizer --preview /path/to/directory
```

### Documentation

- Complete API reference
- User guide with examples
- Installation instructions
- Troubleshooting guide
- Configuration documentation
