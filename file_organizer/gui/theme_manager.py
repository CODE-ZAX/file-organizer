"""
Theme management for the GUI
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class ThemeManager:
    """Manages themes for the GUI"""
    
    def __init__(self):
        self.themes = {}
        self.current_theme = "light"
        self._load_themes()

    def _load_themes(self):
        """Load built-in themes"""
        # Light theme
        self.themes["light"] = {
            "name": "Light",
            "colors": {
                "bg_primary": "#ffffff",
                "bg_secondary": "#f8f9fa",
                "bg_tertiary": "#e9ecef",
                "text_primary": "#212529",
                "text_secondary": "#6c757d",
                "text_muted": "#adb5bd",
                "accent_primary": "#007bff",
                "accent_secondary": "#6c757d",
                "accent_success": "#28a745",
                "accent_warning": "#ffc107",
                "accent_danger": "#dc3545",
                "accent_info": "#17a2b8",
                "border": "#dee2e6",
                "border_focus": "#007bff",
                "shadow": "rgba(0, 0, 0, 0.1)"
            },
            "fonts": {
                "family": "Segoe UI, Arial, sans-serif",
                "size_small": 9,
                "size_normal": 11,
                "size_large": 14,
                "size_title": 16,
                "weight_normal": "normal",
                "weight_bold": "bold"
            }
        }
        
        # Dark theme
        self.themes["dark"] = {
            "name": "Dark",
            "colors": {
                "bg_primary": "#1e1e1e",
                "bg_secondary": "#2d2d2d",
                "bg_tertiary": "#3c3c3c",
                "text_primary": "#ffffff",
                "text_secondary": "#b3b3b3",
                "text_muted": "#808080",
                "accent_primary": "#0d6efd",
                "accent_secondary": "#6c757d",
                "accent_success": "#198754",
                "accent_warning": "#fd7e14",
                "accent_danger": "#dc3545",
                "accent_info": "#0dcaf0",
                "border": "#495057",
                "border_focus": "#0d6efd",
                "shadow": "rgba(0, 0, 0, 0.3)"
            },
            "fonts": {
                "family": "Segoe UI, Arial, sans-serif",
                "size_small": 9,
                "size_normal": 11,
                "size_large": 14,
                "size_title": 16,
                "weight_normal": "normal",
                "weight_bold": "bold"
            }
        }

    def get_theme(self, theme_name: str = None) -> Dict[str, Any]:
        """Get theme by name or current theme"""
        if theme_name is None:
            theme_name = self.current_theme
        
        return self.themes.get(theme_name, self.themes["light"])

    def set_theme(self, theme_name: str):
        """Set the current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
        else:
            raise ValueError(f"Theme '{theme_name}' not found")

    def get_available_themes(self) -> list:
        """Get list of available theme names"""
        return list(self.themes.keys())

    def get_color(self, color_name: str, theme_name: str = None) -> str:
        """Get a specific color from the theme"""
        theme = self.get_theme(theme_name)
        return theme["colors"].get(color_name, "#000000")

    def get_font(self, font_property: str, theme_name: str = None) -> Any:
        """Get a specific font property from the theme"""
        theme = self.get_theme(theme_name)
        return theme["fonts"].get(font_property, "Arial")

    def create_tkinter_style(self, theme_name: str = None) -> Dict[str, Any]:
        """Create tkinter-compatible style dictionary"""
        theme = self.get_theme(theme_name)
        colors = theme["colors"]
        fonts = theme["fonts"]
        
        return {
            "bg": colors["bg_primary"],
            "fg": colors["text_primary"],
            "selectbackground": colors["accent_primary"],
            "selectforeground": colors["text_primary"],
            "insertbackground": colors["text_primary"],
            "highlightbackground": colors["border"],
            "highlightcolor": colors["border_focus"],
            "highlightthickness": 1,
            "relief": "flat",
            "borderwidth": 1,
            "font": (fonts["family"], fonts["size_normal"])
        }

    def get_button_style(self, button_type: str = "primary", theme_name: str = None) -> Dict[str, Any]:
        """Get button-specific styling"""
        theme = self.get_theme(theme_name)
        colors = theme["colors"]
        fonts = theme["fonts"]
        
        base_style = {
            "font": (fonts["family"], fonts["size_normal"], fonts["weight_normal"]),
            "relief": "flat",
            "borderwidth": 1,
            "cursor": "hand2"
        }
        
        if button_type == "primary":
            return {
                **base_style,
                "bg": colors["accent_primary"],
                "fg": colors["text_primary"],
                "activebackground": self._darken_color(colors["accent_primary"]),
                "activeforeground": colors["text_primary"]
            }
        elif button_type == "secondary":
            return {
                **base_style,
                "bg": colors["accent_secondary"],
                "fg": colors["text_primary"],
                "activebackground": self._darken_color(colors["accent_secondary"]),
                "activeforeground": colors["text_primary"]
            }
        elif button_type == "success":
            return {
                **base_style,
                "bg": colors["accent_success"],
                "fg": colors["text_primary"],
                "activebackground": self._darken_color(colors["accent_success"]),
                "activeforeground": colors["text_primary"]
            }
        elif button_type == "danger":
            return {
                **base_style,
                "bg": colors["accent_danger"],
                "fg": colors["text_primary"],
                "activebackground": self._darken_color(colors["accent_danger"]),
                "activeforeground": colors["text_primary"]
            }
        else:
            return {
                **base_style,
                "bg": colors["bg_secondary"],
                "fg": colors["text_primary"],
                "activebackground": colors["bg_tertiary"],
                "activeforeground": colors["text_primary"]
            }

    def _darken_color(self, color: str, factor: float = 0.8) -> str:
        """Darken a hex color by a factor"""
        if not color.startswith("#"):
            return color
        
        try:
            # Remove # and convert to RGB
            hex_color = color[1:]
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Darken
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            # Convert back to hex
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color
