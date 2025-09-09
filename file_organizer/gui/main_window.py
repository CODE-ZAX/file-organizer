"""
Main GUI window for the file organizer
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
from typing import Optional, Callable

from ..core.config import Config
from ..core.file_organizer import FileOrganizer
from ..core.scheduler import Scheduler
from .theme_manager import ThemeManager


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.config = Config()
        self.theme_manager = ThemeManager()
        self.file_organizer = None
        self.scheduler = None
        self.current_directory = None
        
        # Set theme
        self.theme_manager.set_theme(self.config.config.ui.theme)
        
        # Setup window
        self._setup_window()
        self._create_widgets()
        self._apply_theme()
        
        # Initialize scheduler
        self._init_scheduler()

    def _setup_window(self):
        """Setup the main window"""
        self.root.title("TidyDesk")
        self.root.geometry(f"{self.config.config.ui.window_width}x{self.config.config.ui.window_height}")
        self.root.minsize(600, 400)
        
        # Set app icon
        self._set_app_icon()
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.config.config.ui.window_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.config.config.ui.window_height // 2)
        self.root.geometry(f"{self.config.config.ui.window_width}x{self.config.config.ui.window_height}+{x}+{y}")
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _set_app_icon(self):
        """Set the application icon"""
        try:
            # Try custom icon first (TidyDesk.png in root)
            custom_icon = os.path.join(os.path.dirname(__file__), "..", "..", "TidyDesk.png")
            if os.path.exists(custom_icon):
                # Convert PNG to ICO for Windows compatibility
                from PIL import Image
                img = Image.open(custom_icon)
                
                # Create icons directory if it doesn't exist
                icons_dir = os.path.join(os.path.dirname(__file__), "..", "icons")
                os.makedirs(icons_dir, exist_ok=True)
                
                # Save as ICO for Windows
                icon_path = os.path.join(icons_dir, "custom.ico")
                img.save(icon_path, format="ICO")
                self.root.iconbitmap(icon_path)
                print(f"Using custom icon: {custom_icon}")
            else:
                # Fallback to generated icon
                icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", "app.ico")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    print(f"Using generated icon: {icon_path}")
        except Exception as e:
            print(f"Could not set icon: {e}")
            pass  # Icon setting failed, continue without it

    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame, 
            text="File Organizer", 
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_title"), "bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # Directory selection frame
        self.dir_frame = ttk.LabelFrame(self.main_frame, text="Directory Selection", padding=10)
        self.dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.dir_var = tk.StringVar()
        self.dir_entry = ttk.Entry(self.dir_frame, textvariable=self.dir_var, state="readonly")
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.browse_btn = ttk.Button(self.dir_frame, text="Browse", command=self._browse_directory)
        self.browse_btn.pack(side=tk.RIGHT)
        
        # Options frame
        self.options_frame = ttk.LabelFrame(self.main_frame, text="Options", padding=10)
        self.options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Dry run checkbox
        self.dry_run_var = tk.BooleanVar(value=self.config.config.dry_run)
        self.dry_run_check = ttk.Checkbutton(
            self.options_frame, 
            text="Dry run (preview only)", 
            variable=self.dry_run_var,
            command=self._on_dry_run_change
        )
        self.dry_run_check.pack(anchor=tk.W, pady=(0, 5))
        
        # Backup checkbox
        self.backup_var = tk.BooleanVar(value=self.config.config.backup_before_organize)
        self.backup_check = ttk.Checkbutton(
            self.options_frame, 
            text="Create backup before organizing", 
            variable=self.backup_var,
            command=self._on_backup_change
        )
        self.backup_check.pack(anchor=tk.W)
        
        # Action buttons frame
        self.actions_frame = ttk.Frame(self.main_frame)
        self.actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.preview_btn = ttk.Button(
            self.actions_frame, 
            text="Preview", 
            command=self._preview_organization,
            state="disabled"
        )
        self.preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.organize_btn = ttk.Button(
            self.actions_frame, 
            text="Organize Files", 
            command=self._organize_files,
            state="disabled"
        )
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.settings_btn = ttk.Button(
            self.actions_frame, 
            text="Settings", 
            command=self._open_settings
        )
        self.settings_btn.pack(side=tk.RIGHT)
        
        # Progress frame
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding=10)
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            variable=self.progress_var, 
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_label = ttk.Label(self.progress_frame, text="Ready")
        self.progress_label.pack()
        
        # Log frame
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Log", padding=10)
        self.log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame, 
            height=10, 
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Theme toggle
        self.theme_btn = ttk.Button(
            self.status_frame, 
            text="🌙" if self.config.config.ui.theme == "light" else "☀️",
            command=self._toggle_theme,
            width=3
        )
        self.theme_btn.pack(side=tk.RIGHT)
        
        # Update button states
        self._update_button_states()

    def _apply_theme(self):
        """Apply the current theme to all widgets"""
        theme = self.theme_manager.get_theme()
        colors = theme["colors"]
        fonts = theme["fonts"]
        
        # Configure root window
        self.root.configure(bg=colors["bg_primary"])
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure frame styles
        style.configure('TFrame', background=colors["bg_primary"])
        style.configure('TLabelFrame', background=colors["bg_primary"], foreground=colors["text_primary"])
        style.configure('TLabelFrame.Label', background=colors["bg_primary"], foreground=colors["text_primary"])
        
        # Configure label styles
        style.configure('TLabel', background=colors["bg_primary"], foreground=colors["text_primary"])
        
        # Configure button styles
        style.configure('TButton', 
                       background=colors["accent_primary"], 
                       foreground=colors["text_primary"],
                       font=(fonts["family"], fonts["size_normal"]))
        
        # Configure entry styles
        style.configure('TEntry', 
                       fieldbackground=colors["bg_secondary"],
                       foreground=colors["text_primary"],
                       borderwidth=1,
                       insertcolor=colors["text_primary"])
        
        # Configure progress bar
        style.configure('TProgressbar', 
                       background=colors["accent_primary"],
                       troughcolor=colors["bg_secondary"])
        
        # Configure text widget
        self.log_text.configure(
            bg=colors["bg_secondary"],
            fg=colors["text_primary"],
            insertbackground=colors["text_primary"],
            selectbackground=colors["accent_primary"],
            selectforeground=colors["text_primary"]
        )

    def _init_scheduler(self):
        """Initialize the scheduler"""
        self.scheduler = Scheduler(self.config, self._scheduled_organize)
        if self.config.config.scheduler.enabled:
            self.scheduler.start()

    def _browse_directory(self):
        """Browse for directory"""
        directory = filedialog.askdirectory(
            title="Select Directory to Organize",
            initialdir=self.current_directory or os.path.expanduser("~")
        )
        
        if directory:
            self.current_directory = directory
            self.dir_var.set(directory)
            self._update_button_states()
            self._log(f"Selected directory: {directory}")

    def _update_button_states(self):
        """Update button states based on current state"""
        has_directory = bool(self.current_directory)
        self.preview_btn.config(state="normal" if has_directory else "disabled")
        self.organize_btn.config(state="normal" if has_directory else "disabled")

    def _preview_organization(self):
        """Preview organization without actually moving files"""
        if not self.current_directory:
            return
        
        try:
            self._log("Generating preview...")
            self.file_organizer = FileOrganizer(self.config, self._progress_callback)
            preview = self.file_organizer.preview_organization(self.current_directory)
            
            if preview:
                self._log(f"Preview: {len(preview)} files will be organized")
                for item in preview[:10]:  # Show first 10 items
                    self._log(f"  {item['file_name']} -> {item['target_folder']}")
                if len(preview) > 10:
                    self._log(f"  ... and {len(preview) - 10} more files")
            else:
                self._log("No files found to organize")
                
        except Exception as e:
            self._log(f"Error generating preview: {e}")
            messagebox.showerror("Error", f"Failed to generate preview: {e}")

    def _organize_files(self):
        """Organize files in the selected directory"""
        if not self.current_directory:
            return
        
        # Confirm action
        dry_run = self.dry_run_var.get()
        action = "Preview" if dry_run else "Organize"
        
        if not messagebox.askyesno("Confirm", f"Are you sure you want to {action.lower()} files in:\n{self.current_directory}"):
            return
        
        # Run in separate thread
        thread = threading.Thread(target=self._run_organization, daemon=True)
        thread.start()

    def _run_organization(self):
        """Run the organization process"""
        try:
            self._log("Starting organization...")
            self.file_organizer = FileOrganizer(self.config, self._progress_callback)
            
            dry_run = self.dry_run_var.get()
            stats = self.file_organizer.organize_directory(self.current_directory, dry_run=dry_run)
            
            self._log(f"Organization completed!")
            self._log(f"Files processed: {stats['files_processed']}")
            self._log(f"Files moved: {stats['files_moved']}")
            self._log(f"Files skipped: {stats['files_skipped']}")
            self._log(f"Errors: {stats['errors']}")
            
            if not dry_run and stats['files_moved'] > 0:
                messagebox.showinfo("Success", f"Successfully organized {stats['files_moved']} files!")
            
        except Exception as e:
            self._log(f"Error during organization: {e}")
            messagebox.showerror("Error", f"Organization failed: {e}")
        finally:
            self._progress_callback(0, "Ready")

    def _scheduled_organize(self):
        """Called by scheduler for automatic organization"""
        if self.current_directory and os.path.exists(self.current_directory):
            self._log("Running scheduled organization...")
            self._run_organization()

    def _progress_callback(self, progress: float, message: str):
        """Progress callback for file organizer"""
        self.root.after(0, lambda: self._update_progress(progress, message))

    def _update_progress(self, progress: float, message: str):
        """Update progress bar and label"""
        self.progress_var.set(progress)
        self.progress_label.config(text=message)
        self.status_label.config(text=message)

    def _log(self, message: str):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _on_dry_run_change(self):
        """Handle dry run checkbox change"""
        self.config.update_config(dry_run=self.dry_run_var.get())

    def _on_backup_change(self):
        """Handle backup checkbox change"""
        self.config.update_config(backup_before_organize=self.backup_var.get())

    def _toggle_theme(self):
        """Toggle between light and dark theme"""
        current_theme = self.config.config.ui.theme
        new_theme = "dark" if current_theme == "light" else "light"
        
        self.config.update_config(ui={**self.config.config.ui.__dict__, "theme": new_theme})
        self.theme_manager.set_theme(new_theme)
        self._apply_theme()
        
        # Update theme button
        self.theme_btn.config(text="🌙" if new_theme == "light" else "☀️")

    def _open_settings(self):
        """Open settings window"""
        SettingsWindow(self.root, self.config, self.theme_manager)

    def _on_closing(self):
        """Handle window closing"""
        if self.scheduler and self.scheduler.is_running():
            self.scheduler.stop()
        
        # Save window size if enabled
        if self.config.config.ui.remember_window_size:
            geometry = self.root.geometry()
            width, height = geometry.split('x')[0], geometry.split('x')[1].split('+')[0]
            self.config.update_config(ui={
                **self.config.config.ui.__dict__,
                "window_width": int(width),
                "window_height": int(height)
            })
        
        self.root.destroy()

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


class SettingsWindow:
    """Settings window for configuration"""
    
    def __init__(self, parent, config: Config, theme_manager: ThemeManager):
        self.parent = parent
        self.config = config
        self.theme_manager = theme_manager
        
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        self._create_widgets()
        self._apply_theme()
        
        # Center window
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (400 // 2)
        self.window.geometry(f"500x400+{x}+{y}")

    def _create_widgets(self):
        """Create settings widgets"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Theme selection
        ttk.Label(main_frame, text="Theme:").pack(anchor=tk.W, pady=(0, 5))
        self.theme_var = tk.StringVar(value=self.config.config.ui.theme)
        theme_combo = ttk.Combobox(
            main_frame, 
            textvariable=self.theme_var,
            values=["light", "dark"],
            state="readonly"
        )
        theme_combo.pack(fill=tk.X, pady=(0, 20))
        
        # Scheduler settings
        scheduler_frame = ttk.LabelFrame(main_frame, text="Scheduler", padding=10)
        scheduler_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.scheduler_enabled_var = tk.BooleanVar(value=self.config.config.scheduler.enabled)
        ttk.Checkbutton(
            scheduler_frame, 
            text="Enable automatic organization",
            variable=self.scheduler_enabled_var
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Time settings
        time_frame = ttk.Frame(scheduler_frame)
        time_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(time_frame, text="Time:").pack(side=tk.LEFT, padx=(0, 10))
        self.time_var = tk.StringVar(value=self.config.config.scheduler.time)
        time_entry = ttk.Entry(time_frame, textvariable=self.time_var, width=10)
        time_entry.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(time_frame, text="(HH:MM format)").pack(side=tk.LEFT)
        
        # Interval settings
        interval_frame = ttk.Frame(scheduler_frame)
        interval_frame.pack(fill=tk.X)
        
        ttk.Label(interval_frame, text="Interval (hours):").pack(side=tk.LEFT, padx=(0, 10))
        self.interval_var = tk.IntVar(value=self.config.config.scheduler.interval_hours)
        interval_spin = ttk.Spinbox(
            interval_frame, 
            from_=1, 
            to=168, 
            textvariable=self.interval_var,
            width=10
        )
        interval_spin.pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Save", command=self._save_settings).pack(side=tk.RIGHT)

    def _apply_theme(self):
        """Apply theme to settings window"""
        theme = self.theme_manager.get_theme()
        colors = theme["colors"]
        
        self.window.configure(bg=colors["bg_primary"])

    def _save_settings(self):
        """Save settings"""
        try:
            # Update theme
            new_theme = self.theme_var.get()
            if new_theme != self.config.config.ui.theme:
                self.config.update_config(ui={**self.config.config.ui.__dict__, "theme": new_theme})
            
            # Update scheduler
            self.config.update_config(scheduler={
                **self.config.config.scheduler.__dict__,
                "enabled": self.scheduler_enabled_var.get(),
                "time": self.time_var.get(),
                "interval_hours": self.interval_var.get()
            })
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
