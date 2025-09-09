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
        # Modern Light theme
        self.themes["light"] = {
            "name": "Modern Light",
            "colors": {
                "bg_primary": "#ffffff",
                "bg_secondary": "#f8fafc",
                "bg_tertiary": "#f1f5f9",
                "bg_card": "#ffffff",
                "bg_sidebar": "#f8fafc",
                "bg_hover": "#f1f5f9",
                "bg_active": "#e2e8f0",
                "text_primary": "#1e293b",
                "text_secondary": "#64748b",
                "text_muted": "#94a3b8",
                "text_inverse": "#ffffff",
                "accent_primary": "#3b82f6",
                "accent_secondary": "#6366f1",
                "accent_light": "#dbeafe",
                "accent_success": "#10b981",
                "accent_success_light": "#d1fae5",
                "accent_warning": "#f59e0b",
                "accent_warning_light": "#fef3c7",
                "accent_danger": "#ef4444",
                "accent_danger_light": "#fee2e2",
                "accent_info": "#06b6d4",
                "accent_info_light": "#cffafe",
                "border": "#e2e8f0",
                "border_light": "#f1f5f9",
                "border_focus": "#3b82f6",
                "shadow": "#00000008",
                "shadow_medium": "#00000012",
                "shadow_strong": "#00000020",
                "gradient_start": "#3b82f6",
                "gradient_end": "#6366f1"
            },
            "fonts": {
                "family": "SF Pro Display, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
                "size_xsmall": 10,
                "size_small": 12,
                "size_normal": 14,
                "size_medium": 16,
                "size_large": 18,
                "size_xlarge": 24,
                "size_title": 28,
                "weight_light": "normal",
                "weight_normal": "normal",
                "weight_medium": "bold",
                "weight_bold": "bold",
                "weight_heavy": "bold"
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
        return theme["fonts"].get(font_property, "TkDefaultFont")

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
