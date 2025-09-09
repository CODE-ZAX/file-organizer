#!/usr/bin/env python3
"""
TidyDesk Rules Demo Script
Demonstrates the custom rules functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_organizer.core.config import Config, OrganizationRule
from file_organizer.gui.main_window import MainWindow
from file_organizer.gui.theme_manager import ThemeManager
import tkinter as tk

def create_sample_rules():
    """Create some sample rules for demonstration"""
    config = Config()
    
    # Sample rules
    sample_rules = [
        OrganizationRule(
            name="Images",
            file_extensions=[".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            target_folder="Images",
            enabled=True
        ),
        OrganizationRule(
            name="Documents",
            file_extensions=[".pdf", ".doc", ".docx", ".txt"],
            target_folder="Documents",
            enabled=True
        ),
        OrganizationRule(
            name="Code Files",
            file_extensions=[".py", ".js", ".html", ".css"],
            target_folder="Code",
            enabled=True
        ),
        OrganizationRule(
            name="Archives",
            file_extensions=[".zip", ".rar", ".7z"],
            target_folder="Archives",
            enabled=True
        )
    ]
    
    # Add rules to config
    for rule in sample_rules:
        config.add_organization_rule(rule)
    
    return config

def main():
    """Run the demo"""
    print("🚀 TidyDesk Rules Demo")
    print("=" * 40)
    
    # Create sample configuration
    config = create_sample_rules()
    print(f"✅ Created {len(config.config.organization_rules)} sample rules")
    
    # Create theme manager
    theme_manager = ThemeManager()
    print("✅ Theme manager initialized")
    
    # Create and run GUI
    root = tk.Tk()
    app = MainWindow(root, config, theme_manager)
    
    print("✅ TidyDesk GUI started")
    print("\n🎯 Demo Features:")
    print("   - Quick Rule: Create rules quickly")
    print("   - Custom Rules: Full rule management")
    print("   - Rule Helper: Guided rule creation")
    print("   - Import/Export: Share rule sets")
    print("\n📝 Try creating your own rules!")
    
    root.mainloop()

if __name__ == "__main__":
    main()
