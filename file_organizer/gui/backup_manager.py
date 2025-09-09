"""
Backup Management UI for TidyDesk
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from typing import Optional, Callable
import os
from datetime import datetime

from ..core.backup_manager import BackupManager


class BackupManagerWindow:
    """Window for managing backups"""
    
    def __init__(self, parent, theme_manager, on_backup_created: Optional[Callable] = None):
        self.parent = parent
        self.theme_manager = theme_manager
        self.on_backup_created = on_backup_created
        
        self.backup_manager = BackupManager()
        
        self.window = tk.Toplevel(parent)
        self.window.title("Backup Manager - TidyDesk")
        self.window.geometry("800x600")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (300)
        self.window.geometry(f"800x600+{x}+{y}")
        
        self._create_widgets()
        self._apply_theme()
        self._load_backups()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self._create_header(main_frame)
        
        # Backup list
        self._create_backup_list(main_frame)
        
        # Backup actions
        self._create_backup_actions(main_frame)
        
        # Storage info
        self._create_storage_info(main_frame)

    def _create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Backup Manager",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_title"), "bold"),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Manage your file backups and restore previous versions",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_secondary"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))

    def _create_backup_list(self, parent):
        """Create backup list section"""
        list_frame = tk.LabelFrame(parent, text="Available Backups", font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_large"), "bold"))
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # List with scrollbar
        list_container = tk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for backup list
        columns = ("Name", "Created", "Source", "Size", "Files")
        self.backup_tree = ttk.Treeview(list_container, columns=columns, show="headings", height=10)
        
        # Configure columns
        self.backup_tree.heading("Name", text="Backup Name")
        self.backup_tree.heading("Created", text="Created")
        self.backup_tree.heading("Source", text="Source Path")
        self.backup_tree.heading("Size", text="Size (MB)")
        self.backup_tree.heading("Files", text="Files")
        
        self.backup_tree.column("Name", width=150)
        self.backup_tree.column("Created", width=120)
        self.backup_tree.column("Source", width=200)
        self.backup_tree.column("Size", width=80)
        self.backup_tree.column("Files", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.backup_tree.yview)
        self.backup_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.backup_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection
        self.backup_tree.bind("<<TreeviewSelect>>", self._on_backup_select)

    def _create_backup_actions(self, parent):
        """Create backup action buttons"""
        actions_frame = tk.Frame(parent)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create backup button
        create_btn_style = self.theme_manager.get_button_style("primary")
        self.create_btn = tk.Button(
            actions_frame,
            text="Create Backup",
            command=self._create_backup,
            **create_btn_style
        )
        self.create_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Restore backup button
        restore_btn_style = self.theme_manager.get_button_style("secondary")
        self.restore_btn = tk.Button(
            actions_frame,
            text="Restore Backup",
            command=self._restore_backup,
            state="disabled",
            **restore_btn_style
        )
        self.restore_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Delete backup button
        delete_btn_style = self.theme_manager.get_button_style("danger")
        self.delete_btn = tk.Button(
            actions_frame,
            text="Delete Backup",
            command=self._delete_backup,
            state="disabled",
            **delete_btn_style
        )
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cleanup old backups button
        cleanup_btn_style = self.theme_manager.get_button_style("ghost")
        self.cleanup_btn = tk.Button(
            actions_frame,
            text="Cleanup Old",
            command=self._cleanup_old_backups,
            **cleanup_btn_style
        )
        self.cleanup_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        refresh_btn_style = self.theme_manager.get_button_style("ghost")
        self.refresh_btn = tk.Button(
            actions_frame,
            text="Refresh",
            command=self._load_backups,
            **refresh_btn_style
        )
        self.refresh_btn.pack(side=tk.RIGHT)

    def _create_storage_info(self, parent):
        """Create storage information section"""
        storage_frame = tk.LabelFrame(parent, text="Storage Information", font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_large"), "bold"))
        storage_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_frame = tk.Frame(storage_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.storage_label = tk.Label(
            info_frame,
            text="Loading storage information...",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_secondary"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        self.storage_label.pack(anchor=tk.W)
        
        # Update storage info
        self._update_storage_info()

    def _apply_theme(self):
        """Apply theme to all widgets"""
        theme = self.theme_manager.get_theme()
        colors = theme["colors"]
        
        # Configure window
        self.window.configure(bg=colors["bg_primary"])
        
        # Configure frames
        for widget in self.window.winfo_children():
            self._apply_theme_to_widget(widget, colors)

    def _apply_theme_to_widget(self, widget, colors):
        """Recursively apply theme to widget and children"""
        try:
            if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                widget.configure(bg=colors["bg_primary"])
            elif isinstance(widget, tk.Label):
                widget.configure(
                    bg=colors["bg_primary"],
                    fg=colors["text_primary"]
                )
        except:
            pass
        
        # Apply to children
        for child in widget.winfo_children():
            self._apply_theme_to_widget(child, colors)

    def _load_backups(self):
        """Load backups into the list"""
        # Clear existing items
        for item in self.backup_tree.get_children():
            self.backup_tree.delete(item)
        
        # Load backups
        try:
            backups = self.backup_manager.list_backups()
            
            for backup in backups:
                created_date = backup["created_at"]
                if created_date != "Unknown":
                    try:
                        dt = datetime.fromisoformat(created_date)
                        created_date = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                
                self.backup_tree.insert("", "end", values=(
                    backup["backup_name"],
                    created_date,
                    os.path.basename(backup["source_path"]),
                    f"{backup['size_mb']:.1f}",
                    backup["file_count"]
                ))
            
            self._update_storage_info()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load backups: {e}")

    def _on_backup_select(self, event):
        """Handle backup selection"""
        selection = self.backup_tree.selection()
        if selection:
            self.restore_btn.config(state="normal")
            self.delete_btn.config(state="normal")
        else:
            self.restore_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")

    def _create_backup(self):
        """Create a new backup"""
        source_path = filedialog.askdirectory(
            title="Select directory to backup",
            initialdir=os.path.expanduser("~")
        )
        
        if not source_path:
            return
        
        # Get backup name
        backup_name = simpledialog.askstring(
            "Backup Name",
            "Enter backup name:",
            initialvalue=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if not backup_name:
            return
        
        try:
            backup_path = self.backup_manager.create_backup(source_path, backup_name)
            messagebox.showinfo("Success", f"Backup created successfully!\nLocation: {backup_path}")
            
            self._load_backups()
            
            if self.on_backup_created:
                self.on_backup_created(backup_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {e}")

    def _restore_backup(self):
        """Restore selected backup"""
        selection = self.backup_tree.selection()
        if not selection:
            return
        
        item = self.backup_tree.item(selection[0])
        backup_name = item["values"][0]
        
        # Ask for restore location
        restore_path = filedialog.askdirectory(
            title="Select restore location",
            initialdir=os.path.expanduser("~")
        )
        
        if not restore_path:
            return
        
        try:
            # Find backup file
            backups = self.backup_manager.list_backups()
            backup_info = next((b for b in backups if b["backup_name"] == backup_name), None)
            
            if not backup_info:
                messagebox.showerror("Error", "Backup not found!")
                return
            
            restored_path = self.backup_manager.restore_backup(
                backup_info["backup_path"],
                os.path.join(restore_path, backup_name)
            )
            
            messagebox.showinfo("Success", f"Backup restored successfully!\nLocation: {restored_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore backup: {e}")

    def _delete_backup(self):
        """Delete selected backup"""
        selection = self.backup_tree.selection()
        if not selection:
            return
        
        item = self.backup_tree.item(selection[0])
        backup_name = item["values"][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete backup '{backup_name}'?"):
            try:
                if self.backup_manager.delete_backup(backup_name):
                    messagebox.showinfo("Success", "Backup deleted successfully!")
                    self._load_backups()
                else:
                    messagebox.showerror("Error", "Failed to delete backup!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete backup: {e}")

    def _cleanup_old_backups(self):
        """Cleanup old backups"""
        keep_count = simpledialog.askinteger(
            "Cleanup Old Backups",
            "How many recent backups to keep?",
            initialvalue=10,
            minvalue=1,
            maxvalue=100
        )
        
        if keep_count is None:
            return
        
        try:
            deleted_count = self.backup_manager.cleanup_old_backups(keep_count)
            messagebox.showinfo("Success", f"Cleaned up {deleted_count} old backups!")
            self._load_backups()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cleanup backups: {e}")

    def _update_storage_info(self):
        """Update storage information"""
        try:
            storage_info = self.backup_manager.get_backup_size()
            
            info_text = f"Total Backups: {storage_info['backup_count']} | "
            info_text += f"Total Size: {storage_info['total_size_mb']:.1f} MB"
            
            if storage_info['total_size_gb'] >= 1:
                info_text += f" ({storage_info['total_size_gb']:.2f} GB)"
            
            self.storage_label.config(text=info_text)
            
        except Exception as e:
            self.storage_label.config(text=f"Error loading storage info: {e}")

    def _on_closing(self):
        """Handle window closing"""
        self.window.destroy()
