"""
TidyDesk - A production-ready file organization tool
"""

__version__ = "1.0.0"
__author__ = "TidyDesk Team"
__email__ = "contact@tiddesk.com"

from .core.file_organizer import FileOrganizer
from .core.config import Config
from .gui.main_window import MainWindow

__all__ = ["FileOrganizer", "Config", "MainWindow"]
