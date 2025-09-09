"""
Rule Helper Dialog for TidyDesk
Provides guided rule creation with common file types and templates
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Callable
import json
import os

from ..core.config import OrganizationRule


class RuleHelperDialog:
    """Dialog for guided rule creation"""
    
    def __init__(self, parent, on_rule_created: Callable):
        self.parent = parent
        self.on_rule_created = on_rule_created
        
        self.window = tk.Toplevel(parent)
        self.window.title("Rule Helper - TidyDesk")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (300)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (250)
        self.window.geometry(f"600x500+{x}+{y}")
        
        self._create_widgets()
        self._load_templates()

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Rule Helper",
            font=("TkDefaultFont", 16, "bold"),
            fg="#1d1d1f"
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Choose a template or create a custom rule",
            font=("TkDefaultFont", 11),
            fg="#6e6e73"
        )
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Template selection
        template_frame = tk.LabelFrame(main_frame, text="Choose Template", font=("TkDefaultFont", 12, "bold"))
        template_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Template list
        list_frame = tk.Frame(template_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.template_var = tk.StringVar()
        self.template_listbox = tk.Listbox(
            list_frame,
            listvariable=self.template_var,
            height=8,
            font=("TkDefaultFont", 10),
            selectmode=tk.SINGLE
        )
        self.template_listbox.pack(fill=tk.BOTH, expand=True)
        self.template_listbox.bind("<<ListboxSelect>>", self._on_template_select)
        
        # Template details
        details_frame = tk.LabelFrame(main_frame, text="Template Details", font=("TkDefaultFont", 12, "bold"))
        details_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.details_text = tk.Text(
            details_frame,
            height=6,
            font=("TkDefaultFont", 10),
            fg="#6e6e73",
            bg="#f5f5f7",
            relief="flat",
            bd=1,
            state=tk.DISABLED
        )
        self.details_text.pack(fill=tk.X, padx=10, pady=10)
        
        # Custom rule section
        custom_frame = tk.LabelFrame(main_frame, text="Custom Rule", font=("TkDefaultFont", 12, "bold"))
        custom_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Rule name
        name_frame = tk.Frame(custom_frame)
        name_frame.pack(fill=tk.X, padx=10, pady=(5, 5))
        
        tk.Label(name_frame, text="Rule Name:", font=("TkDefaultFont", 10)).pack(anchor=tk.W)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(name_frame, textvariable=self.name_var, font=("TkDefaultFont", 10))
        self.name_entry.pack(fill=tk.X, pady=(2, 0))
        
        # File extensions
        extensions_frame = tk.Frame(custom_frame)
        extensions_frame.pack(fill=tk.X, padx=10, pady=(5, 5))
        
        tk.Label(extensions_frame, text="File Extensions:", font=("TkDefaultFont", 10)).pack(anchor=tk.W)
        self.extensions_var = tk.StringVar()
        self.extensions_entry = tk.Entry(extensions_frame, textvariable=self.extensions_var, font=("TkDefaultFont", 10))
        self.extensions_entry.pack(fill=tk.X, pady=(2, 0))
        
        # Target folder
        target_frame = tk.Frame(custom_frame)
        target_frame.pack(fill=tk.X, padx=10, pady=(5, 5))
        
        tk.Label(target_frame, text="Target Folder:", font=("TkDefaultFont", 10)).pack(anchor=tk.W)
        self.target_var = tk.StringVar()
        self.target_entry = tk.Entry(target_frame, textvariable=self.target_var, font=("TkDefaultFont", 10))
        self.target_entry.pack(fill=tk.X, pady=(2, 0))
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Use template button
        self.use_template_btn = tk.Button(
            button_frame,
            text="Use Template",
            command=self._use_template,
            state="disabled",
            bg="#007aff",
            fg="white",
            font=("TkDefaultFont", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        )
        self.use_template_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create custom button
        self.create_custom_btn = tk.Button(
            button_frame,
            text="Create Custom Rule",
            command=self._create_custom,
            bg="#34c759",
            fg="white",
            font=("TkDefaultFont", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        )
        self.create_custom_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        self.close_btn = tk.Button(
            button_frame,
            text="Close",
            command=self.window.destroy,
            bg="#8e8e93",
            fg="white",
            font=("TkDefaultFont", 10),
            relief="flat",
            padx=20,
            pady=5
        )
        self.close_btn.pack(side=tk.RIGHT)

    def _load_templates(self):
        """Load predefined rule templates"""
        self.templates = [
            {
                "name": "Images",
                "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
                "target": "Images",
                "description": "Common image formats including photos, graphics, and vector images"
            },
            {
                "name": "Documents",
                "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"],
                "target": "Documents",
                "description": "Text documents, PDFs, and office files"
            },
            {
                "name": "Videos",
                "extensions": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mkv"],
                "target": "Videos",
                "description": "Video files in various formats"
            },
            {
                "name": "Audio",
                "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
                "target": "Audio",
                "description": "Audio files and music"
            },
            {
                "name": "Archives",
                "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
                "target": "Archives",
                "description": "Compressed files and archives"
            },
            {
                "name": "Code Files",
                "extensions": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".php", ".rb", ".go"],
                "target": "Code",
                "description": "Source code files and scripts"
            },
            {
                "name": "Spreadsheets",
                "extensions": [".xls", ".xlsx", ".csv", ".ods"],
                "target": "Spreadsheets",
                "description": "Excel files and data tables"
            },
            {
                "name": "Presentations",
                "extensions": [".ppt", ".pptx", ".odp"],
                "target": "Presentations",
                "description": "PowerPoint and presentation files"
            },
            {
                "name": "3D Models",
                "extensions": [".obj", ".fbx", ".dae", ".blend", ".3ds", ".max"],
                "target": "3D Models",
                "description": "3D model files and scenes"
            },
            {
                "name": "Fonts",
                "extensions": [".ttf", ".otf", ".woff", ".woff2"],
                "target": "Fonts",
                "description": "Font files and typefaces"
            }
        ]
        
        # Populate template list
        template_names = [template["name"] for template in self.templates]
        self.template_var.set(template_names)

    def _on_template_select(self, event):
        """Handle template selection"""
        selection = self.template_listbox.curselection()
        if selection:
            template = self.templates[selection[0]]
            
            # Update details
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete(1.0, tk.END)
            
            details = f"Name: {template['name']}\n"
            details += f"Extensions: {', '.join(template['extensions'])}\n"
            details += f"Target Folder: {template['target']}\n"
            details += f"Description: {template['description']}"
            
            self.details_text.insert(1.0, details)
            self.details_text.config(state=tk.DISABLED)
            
            # Enable use template button
            self.use_template_btn.config(state="normal")
            
            # Pre-fill custom fields
            self.name_var.set(template['name'])
            self.extensions_var.set(', '.join(template['extensions']))
            self.target_var.set(template['target'])

    def _use_template(self):
        """Use selected template"""
        selection = self.template_listbox.curselection()
        if not selection:
            return
        
        template = self.templates[selection[0]]
        self._create_rule_from_template(template)

    def _create_custom(self):
        """Create custom rule from form"""
        name = self.name_var.get().strip()
        extensions_str = self.extensions_var.get().strip()
        target = self.target_var.get().strip()
        
        if not name or not extensions_str or not target:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        # Parse extensions
        extensions = [ext.strip() for ext in extensions_str.split(",") if ext.strip()]
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
        
        template = {
            "name": name,
            "extensions": extensions,
            "target": target,
            "description": "Custom rule created by user"
        }
        
        self._create_rule_from_template(template)

    def _create_rule_from_template(self, template):
        """Create rule from template"""
        try:
            rule = OrganizationRule(
                name=template["name"],
                file_extensions=template["extensions"],
                target_folder=template["target"],
                enabled=True
            )
            
            self.on_rule_created(rule)
            messagebox.showinfo("Success", f"Rule '{template['name']}' created successfully!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create rule: {e}")


class QuickRuleDialog:
    """Quick rule creation dialog"""
    
    def __init__(self, parent, on_rule_created: Callable):
        self.parent = parent
        self.on_rule_created = on_rule_created
        
        self.window = tk.Toplevel(parent)
        self.window.title("Quick Rule - TidyDesk")
        self.window.geometry("400x300")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (200)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (150)
        self.window.geometry(f"400x300+{x}+{y}")
        
        self._create_widgets()

    def _create_widgets(self):
        """Create quick rule widgets"""
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Quick Rule Creation",
            font=("TkDefaultFont", 14, "bold"),
            fg="#1d1d1f"
        )
        title_label.pack(pady=(0, 20))
        
        # File extension input
        ext_frame = tk.Frame(main_frame)
        ext_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(ext_frame, text="File Extension:", font=("TkDefaultFont", 10)).pack(anchor=tk.W)
        self.ext_var = tk.StringVar()
        self.ext_entry = tk.Entry(ext_frame, textvariable=self.ext_var, font=("TkDefaultFont", 10))
        self.ext_entry.pack(fill=tk.X, pady=(2, 0))
        self.ext_entry.insert(0, ".example")
        
        # Target folder input
        target_frame = tk.Frame(main_frame)
        target_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(target_frame, text="Target Folder:", font=("TkDefaultFont", 10)).pack(anchor=tk.W)
        self.target_var = tk.StringVar()
        self.target_entry = tk.Entry(target_frame, textvariable=self.target_var, font=("TkDefaultFont", 10))
        self.target_entry.pack(fill=tk.X, pady=(2, 0))
        self.target_entry.insert(0, "Custom Files")
        
        # Rule name input
        name_frame = tk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(name_frame, text="Rule Name:", font=("TkDefaultFont", 10)).pack(anchor=tk.W)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(name_frame, textvariable=self.name_var, font=("TkDefaultFont", 10))
        self.name_entry.pack(fill=tk.X, pady=(2, 0))
        self.name_entry.insert(0, "Custom Rule")
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        create_btn = tk.Button(
            button_frame,
            text="Create Rule",
            command=self._create_rule,
            bg="#007aff",
            fg="white",
            font=("TkDefaultFont", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        )
        create_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.window.destroy,
            bg="#8e8e93",
            fg="white",
            font=("TkDefaultFont", 10),
            relief="flat",
            padx=20,
            pady=5
        )
        cancel_btn.pack(side=tk.LEFT)

    def _create_rule(self):
        """Create the rule"""
        name = self.name_var.get().strip()
        ext = self.ext_var.get().strip()
        target = self.target_var.get().strip()
        
        if not name or not ext or not target:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        # Ensure extension starts with dot
        if not ext.startswith("."):
            ext = f".{ext}"
        
        try:
            rule = OrganizationRule(
                name=name,
                file_extensions=[ext],
                target_folder=target,
                enabled=True
            )
            
            self.on_rule_created(rule)
            messagebox.showinfo("Success", f"Rule '{name}' created successfully!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create rule: {e}")
