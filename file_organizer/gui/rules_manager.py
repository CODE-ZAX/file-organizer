"""
Custom Rules Management UI for TidyDesk
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Optional, Callable
import json
import os

from ..core.config import Config, OrganizationRule
from .rule_helper import RuleHelperDialog, QuickRuleDialog


class RulesManagerWindow:
    """Window for managing custom organization rules"""
    
    def __init__(self, parent, config: Config, theme_manager, on_rules_updated: Optional[Callable] = None):
        self.parent = parent
        self.config = config
        self.theme_manager = theme_manager
        self.on_rules_updated = on_rules_updated
        
        self.window = tk.Toplevel(parent)
        self.window.title("Custom Rules Manager - TidyDesk")
        self.window.geometry("900x700")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (450)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (350)
        self.window.geometry(f"900x700+{x}+{y}")
        
        self._create_widgets()
        self._apply_theme()
        self._load_rules()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self._create_header(main_frame)
        
        # Rules list and controls
        self._create_rules_section(main_frame)
        
        # Rule editor
        self._create_rule_editor(main_frame)
        
        # Buttons
        self._create_buttons(main_frame)

    def _create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Custom Rules Manager",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_title"), self.theme_manager.get_font("weight_bold")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Create and manage custom file organization rules",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_secondary"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))

    def _create_rules_section(self, parent):
        """Create rules list section"""
        rules_frame = tk.LabelFrame(parent, text="Existing Rules", font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_large"), "bold"))
        rules_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Rules list with scrollbar
        list_frame = tk.Frame(rules_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for rules list
        columns = ("Name", "Extensions", "Target Folder", "Enabled")
        self.rules_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        self.rules_tree.heading("Name", text="Rule Name")
        self.rules_tree.heading("Extensions", text="File Extensions")
        self.rules_tree.heading("Target Folder", text="Target Folder")
        self.rules_tree.heading("Enabled", text="Enabled")
        
        self.rules_tree.column("Name", width=150)
        self.rules_tree.column("Extensions", width=200)
        self.rules_tree.column("Target Folder", width=150)
        self.rules_tree.column("Enabled", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.rules_tree.yview)
        self.rules_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.rules_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection
        self.rules_tree.bind("<<TreeviewSelect>>", self._on_rule_select)
        
        # Rules controls
        controls_frame = tk.Frame(rules_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Add rule button
        add_btn_style = self.theme_manager.get_button_style("primary")
        self.add_btn = tk.Button(
            controls_frame,
            text="Add New Rule",
            command=self._add_rule,
            **add_btn_style
        )
        self.add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Rule helper button
        helper_btn_style = self.theme_manager.get_button_style("secondary")
        self.helper_btn = tk.Button(
            controls_frame,
            text="Rule Helper",
            command=self._open_rule_helper,
            **helper_btn_style
        )
        self.helper_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Edit rule button
        edit_btn_style = self.theme_manager.get_button_style("secondary")
        self.edit_btn = tk.Button(
            controls_frame,
            text="Edit Rule",
            command=self._edit_rule,
            state="disabled",
            **edit_btn_style
        )
        self.edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Delete rule button
        delete_btn_style = self.theme_manager.get_button_style("danger")
        self.delete_btn = tk.Button(
            controls_frame,
            text="Delete Rule",
            command=self._delete_rule,
            state="disabled",
            **delete_btn_style
        )
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Import/Export buttons
        import_btn_style = self.theme_manager.get_button_style("ghost")
        self.import_btn = tk.Button(
            controls_frame,
            text="Import Rules",
            command=self._import_rules,
            **import_btn_style
        )
        self.import_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.export_btn = tk.Button(
            controls_frame,
            text="Export Rules",
            command=self._export_rules,
            **import_btn_style
        )
        self.export_btn.pack(side=tk.RIGHT)

    def _create_rule_editor(self, parent):
        """Create rule editor section"""
        editor_frame = tk.LabelFrame(parent, text="Rule Editor", font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_large"), "bold"))
        editor_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Editor content
        content_frame = tk.Frame(editor_frame)
        content_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Rule name
        name_frame = tk.Frame(content_frame)
        name_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            name_frame,
            text="Rule Name:",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        ).pack(anchor=tk.W)
        
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(
            name_frame,
            textvariable=self.name_var,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_secondary"),
            relief="flat",
            bd=1
        )
        self.name_entry.pack(fill=tk.X, pady=(5, 0))
        
        # File extensions
        extensions_frame = tk.Frame(content_frame)
        extensions_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            extensions_frame,
            text="File Extensions (comma-separated):",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        ).pack(anchor=tk.W)
        
        self.extensions_var = tk.StringVar()
        self.extensions_entry = tk.Entry(
            extensions_frame,
            textvariable=self.extensions_var,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_secondary"),
            relief="flat",
            bd=1
        )
        self.extensions_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Helper text for extensions
        helper_label = tk.Label(
            extensions_frame,
            text="Example: .jpg, .png, .gif, .bmp",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_small")),
            fg=self.theme_manager.get_color("text_muted"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        helper_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Target folder
        target_frame = tk.Frame(content_frame)
        target_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            target_frame,
            text="Target Folder:",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        ).pack(anchor=tk.W)
        
        self.target_var = tk.StringVar()
        self.target_entry = tk.Entry(
            target_frame,
            textvariable=self.target_var,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_secondary"),
            relief="flat",
            bd=1
        )
        self.target_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Helper text for target folder
        target_helper_label = tk.Label(
            target_frame,
            text="Example: Images, Documents, Videos",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_small")),
            fg=self.theme_manager.get_color("text_muted"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        target_helper_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Enabled checkbox
        checkbox_frame = tk.Frame(content_frame)
        checkbox_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.enabled_var = tk.BooleanVar(value=True)
        self.enabled_check = tk.Checkbutton(
            checkbox_frame,
            text="Enable this rule",
            variable=self.enabled_var,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary"),
            activebackground=self.theme_manager.get_color("bg_primary"),
            activeforeground=self.theme_manager.get_color("text_primary"),
            selectcolor=self.theme_manager.get_color("bg_secondary"),
            relief="flat",
            bd=0
        )
        self.enabled_check.pack(anchor=tk.W)
        
        # Preview section
        preview_frame = tk.Frame(content_frame)
        preview_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            preview_frame,
            text="Rule Preview:",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal"), "bold"),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        ).pack(anchor=tk.W)
        
        self.preview_text = tk.Text(
            preview_frame,
            height=3,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_small")),
            fg=self.theme_manager.get_color("text_secondary"),
            bg=self.theme_manager.get_color("bg_secondary"),
            relief="flat",
            bd=1,
            state=tk.DISABLED
        )
        self.preview_text.pack(fill=tk.X, pady=(5, 0))
        
        # Bind changes to update preview
        self.name_var.trace("w", self._update_preview)
        self.extensions_var.trace("w", self._update_preview)
        self.target_var.trace("w", self._update_preview)
        self.enabled_var.trace("w", self._update_preview)

    def _create_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Save button
        save_btn_style = self.theme_manager.get_button_style("primary")
        self.save_btn = tk.Button(
            button_frame,
            text="Save Rule",
            command=self._save_rule,
            state="disabled",
            **save_btn_style
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn_style = self.theme_manager.get_button_style("secondary")
        self.cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self._cancel_edit,
            state="disabled",
            **cancel_btn_style
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        close_btn_style = self.theme_manager.get_button_style("ghost")
        self.close_btn = tk.Button(
            button_frame,
            text="Close",
            command=self._on_closing,
            **close_btn_style
        )
        self.close_btn.pack(side=tk.RIGHT)

    def _apply_theme(self):
        """Apply theme to all widgets"""
        theme = self.theme_manager.get_theme()
        colors = theme["colors"]
        fonts = theme["fonts"]
        
        # Configure window
        self.window.configure(bg=colors["bg_primary"])
        
        # Configure frames
        for widget in self.window.winfo_children():
            self._apply_theme_to_widget(widget, colors, fonts)

    def _apply_theme_to_widget(self, widget, colors, fonts):
        """Recursively apply theme to widget and children"""
        try:
            if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                widget.configure(bg=colors["bg_primary"])
            elif isinstance(widget, tk.Label):
                widget.configure(
                    bg=colors["bg_primary"],
                    fg=colors["text_primary"]
                )
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=colors["bg_secondary"],
                    fg=colors["text_primary"],
                    insertbackground=colors["text_primary"]
                )
            elif isinstance(widget, tk.Text):
                widget.configure(
                    bg=colors["bg_secondary"],
                    fg=colors["text_primary"],
                    insertbackground=colors["text_primary"]
                )
        except:
            pass
        
        # Apply to children
        for child in widget.winfo_children():
            self._apply_theme_to_widget(child, colors, fonts)

    def _load_rules(self):
        """Load existing rules into the tree"""
        # Clear existing items
        for item in self.rules_tree.get_children():
            self.rules_tree.delete(item)
        
        # Load rules from config
        for rule in self.config.config.organization_rules:
            extensions_str = ", ".join(rule.file_extensions)
            enabled_str = "Yes" if rule.enabled else "No"
            
            self.rules_tree.insert("", "end", values=(
                rule.name,
                extensions_str,
                rule.target_folder,
                enabled_str
            ))

    def _on_rule_select(self, event):
        """Handle rule selection"""
        selection = self.rules_tree.selection()
        if selection:
            self.edit_btn.config(state="normal")
            self.delete_btn.config(state="normal")
        else:
            self.edit_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")

    def _add_rule(self):
        """Add a new rule"""
        self._clear_editor()
        self._set_editor_mode("add")
        self.name_entry.focus()
    
    def _open_rule_helper(self):
        """Open rule helper dialog"""
        RuleHelperDialog(self.window, self._on_rule_created)
    
    def _on_rule_created(self, rule: OrganizationRule):
        """Handle rule created from helper"""
        # Check for duplicate names
        if self.config.get_organization_rule(rule.name):
            messagebox.showerror("Error", "A rule with this name already exists!")
            return
        
        # Add the rule
        self.config.add_organization_rule(rule)
        self._load_rules()
        
        if self.on_rules_updated:
            self.on_rules_updated()
        
        messagebox.showinfo("Success", f"Rule '{rule.name}' added successfully!")

    def _edit_rule(self):
        """Edit selected rule"""
        selection = self.rules_tree.selection()
        if not selection:
            return
        
        # Get rule name from selection
        item = self.rules_tree.item(selection[0])
        rule_name = item["values"][0]
        
        # Find rule in config
        rule = self.config.get_organization_rule(rule_name)
        if not rule:
            messagebox.showerror("Error", "Rule not found!")
            return
        
        # Populate editor
        self.name_var.set(rule.name)
        self.extensions_var.set(", ".join(rule.file_extensions))
        self.target_var.set(rule.target_folder)
        self.enabled_var.set(rule.enabled)
        
        self._set_editor_mode("edit")
        self.current_rule_name = rule_name

    def _delete_rule(self):
        """Delete selected rule"""
        selection = self.rules_tree.selection()
        if not selection:
            return
        
        # Get rule name from selection
        item = self.rules_tree.item(selection[0])
        rule_name = item["values"][0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the rule '{rule_name}'?"):
            self.config.remove_organization_rule(rule_name)
            self._load_rules()
            self._clear_editor()
            self._set_editor_mode("none")
            if self.on_rules_updated:
                self.on_rules_updated()

    def _save_rule(self):
        """Save current rule"""
        # Validate inputs
        name = self.name_var.get().strip()
        extensions_str = self.extensions_var.get().strip()
        target = self.target_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Rule name is required!")
            return
        
        if not extensions_str:
            messagebox.showerror("Error", "File extensions are required!")
            return
        
        if not target:
            messagebox.showerror("Error", "Target folder is required!")
            return
        
        # Parse extensions
        extensions = [ext.strip() for ext in extensions_str.split(",") if ext.strip()]
        if not extensions:
            messagebox.showerror("Error", "At least one file extension is required!")
            return
        
        # Ensure extensions start with dot
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
        
        # Create rule
        rule = OrganizationRule(
            name=name,
            file_extensions=extensions,
            target_folder=target,
            enabled=self.enabled_var.get()
        )
        
        # Check for duplicate names
        if hasattr(self, 'current_rule_name') and self.current_rule_name != name:
            if self.config.get_organization_rule(name):
                messagebox.showerror("Error", "A rule with this name already exists!")
                return
        elif not hasattr(self, 'current_rule_name'):
            if self.config.get_organization_rule(name):
                messagebox.showerror("Error", "A rule with this name already exists!")
                return
        
        # Save rule
        if hasattr(self, 'current_rule_name') and self.current_rule_name:
            # Update existing rule
            self.config.remove_organization_rule(self.current_rule_name)
        
        self.config.add_organization_rule(rule)
        self._load_rules()
        self._clear_editor()
        self._set_editor_mode("none")
        
        if self.on_rules_updated:
            self.on_rules_updated()
        
        messagebox.showinfo("Success", "Rule saved successfully!")

    def _cancel_edit(self):
        """Cancel current edit"""
        self._clear_editor()
        self._set_editor_mode("none")

    def _clear_editor(self):
        """Clear the rule editor"""
        self.name_var.set("")
        self.extensions_var.set("")
        self.target_var.set("")
        self.enabled_var.set(True)
        self._update_preview()

    def _set_editor_mode(self, mode):
        """Set editor mode (add, edit, none)"""
        if mode == "add":
            self.save_btn.config(state="normal", text="Add Rule")
            self.cancel_btn.config(state="normal")
        elif mode == "edit":
            self.save_btn.config(state="normal", text="Update Rule")
            self.cancel_btn.config(state="normal")
        else:  # none
            self.save_btn.config(state="disabled", text="Save Rule")
            self.cancel_btn.config(state="disabled")
            if hasattr(self, 'current_rule_name'):
                delattr(self, 'current_rule_name')

    def _update_preview(self, *args):
        """Update rule preview"""
        name = self.name_var.get().strip()
        extensions_str = self.extensions_var.get().strip()
        target = self.target_var.get().strip()
        enabled = self.enabled_var.get()
        
        if not name and not extensions_str and not target:
            preview_text = "Enter rule details to see preview..."
        else:
            extensions = [ext.strip() for ext in extensions_str.split(",") if ext.strip()]
            extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
            
            preview_text = f"Rule: {name or 'Untitled'}\n"
            preview_text += f"Extensions: {', '.join(extensions) if extensions else 'None'}\n"
            preview_text += f"Target: {target or 'None'} | Enabled: {'Yes' if enabled else 'No'}"
        
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, preview_text)
        self.preview_text.config(state=tk.DISABLED)

    def _import_rules(self):
        """Import rules from file"""
        file_path = filedialog.askopenfilename(
            title="Import Rules",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                messagebox.showerror("Error", "Invalid rules file format!")
                return
            
            imported_count = 0
            for rule_data in data:
                try:
                    rule = OrganizationRule(**rule_data)
                    # Check for duplicates
                    if not self.config.get_organization_rule(rule.name):
                        self.config.add_organization_rule(rule)
                        imported_count += 1
                except Exception as e:
                    print(f"Error importing rule: {e}")
                    continue
            
            self._load_rules()
            if self.on_rules_updated:
                self.on_rules_updated()
            
            messagebox.showinfo("Success", f"Imported {imported_count} rules successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import rules: {e}")

    def _export_rules(self):
        """Export rules to file"""
        file_path = filedialog.asksaveasfilename(
            title="Export Rules",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            rules_data = []
            for rule in self.config.config.organization_rules:
                rules_data.append({
                    "name": rule.name,
                    "file_extensions": rule.file_extensions,
                    "target_folder": rule.target_folder,
                    "enabled": rule.enabled
                })
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(rules_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Exported {len(rules_data)} rules successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export rules: {e}")

    def _on_closing(self):
        """Handle window closing"""
        self.window.destroy()
