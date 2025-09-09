"""
File Organizer - A production-ready file organization tool
"""

__version__ = "1.0.0"
__author__ = "File Organizer Team"
__email__ = "contact@fileorganizer.com"

from .core.file_organizer import FileOrganizer
from .core.config import Config
from .gui.main_window import MainWindow

__all__ = ["FileOrganizer", "Config", "MainWindow"]
