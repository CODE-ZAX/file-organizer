"""
Modern main window for TidyDesk
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from pathlib import Path
from typing import Optional

from ..core.file_organizer import FileOrganizer
from ..core.scheduler import Scheduler
from ..core.config import Config
from .theme_manager import ThemeManager
from .rules_manager import RulesManagerWindow
# QuickRuleDialog removed as requested
from .backup_manager import BackupManagerWindow


class MainWindow:
    """Modern main application window"""

    def __init__(self, config: Config = None):
        try:
            self.root = tk.Tk()
            self.config = config or Config()
            self.theme_manager = ThemeManager()
            self.file_organizer = None
            self.scheduler = None
            self.current_directory = None
            
            # Set modern theme
            self.theme_manager.set_theme("light")
            
            # Setup window
            self._setup_window()
            self._create_widgets()
            self._apply_theme()
            
            # Initialize scheduler
            self._init_scheduler()
            
        except Exception as e:
            print(f"Error initializing MainWindow: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _setup_window(self):
        """Setup the main window with modern styling"""
        self.root.title("TidyDesk")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Modern window styling
        self.root.configure(bg=self.theme_manager.get_color("bg_primary"))
        
        # Set app icon
        self._set_app_icon()
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _set_app_icon(self):
        """Set the application icon"""
        try:
            custom_icon = os.path.join(os.path.dirname(__file__), "..", "..", "TidyDesk.png")
            if os.path.exists(custom_icon):
                from PIL import Image
                img = Image.open(custom_icon)
                ico_path = custom_icon.replace('.png', '.ico')
                img.save(ico_path, format='ICO')
                self.root.iconbitmap(ico_path)
                print(f"Using custom icon: {custom_icon}")
        except Exception as e:
            print(f"Could not load icon: {e}")

    def _create_widgets(self):
        """Create modern UI widgets"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.theme_manager.get_color("bg_primary"))
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self._create_header(main_container)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=self.theme_manager.get_color("bg_primary"))
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left sidebar
        self._create_sidebar(content_frame)
        
        # Main content
        self._create_main_content(content_frame)
        
        # Status bar
        self._create_status_bar(main_container)

    def _create_header(self, parent):
        """Create modern header section"""
        header_frame = tk.Frame(parent, bg=self.theme_manager.get_color("bg_primary"))
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # App title and subtitle
        title_frame = tk.Frame(header_frame, bg=self.theme_manager.get_color("bg_primary"))
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(
            title_frame,
            text="TidyDesk",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_title"), self.theme_manager.get_font("weight_bold")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Intelligent File Organization",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_secondary"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        subtitle_label.pack(anchor=tk.W)

    def _create_sidebar(self, parent):
        """Create modern sidebar with navigation"""
        sidebar_frame = tk.Frame(parent, bg=self.theme_manager.get_color("bg_sidebar"), width=250)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar_frame.pack_propagate(False)
        
        # Directory selection section
        dir_section = tk.LabelFrame(
            sidebar_frame,
            text="Directory",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_medium"), self.theme_manager.get_font("weight_medium")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_sidebar"),
            relief="flat",
            bd=0
        )
        dir_section.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        # Directory selection button
        self.dir_btn = tk.Button(
            dir_section,
            text="Select Directory",
            command=self._select_directory,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            bg=self.theme_manager.get_color("accent_primary"),
            fg=self.theme_manager.get_color("primary"),
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2"
        )
        self.dir_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Current directory display
        self.dir_label = tk.Label(
            dir_section,
            text="No directory selected",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_small")),
            fg=self.theme_manager.get_color("text_muted"),
            bg=self.theme_manager.get_color("bg_sidebar"),
            wraplength=200,
            justify=tk.LEFT
        )
        self.dir_label.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Organization section
        org_section = tk.LabelFrame(
            sidebar_frame,
            text="Organization",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_medium"), self.theme_manager.get_font("weight_medium")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_sidebar"),
            relief="flat",
            bd=0
        )
        org_section.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        # Organization buttons
        self.organize_btn = tk.Button(
            org_section,
            text="Organize Now",
            command=self._organize_files,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal"), self.theme_manager.get_font("weight_medium")),
            bg=self.theme_manager.get_color("accent_success"),
            fg=self.theme_manager.get_color("primary"),
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2"
        )
        self.organize_btn.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.preview_btn = tk.Button(
            org_section,
            text="Preview",
            command=self._preview_organization,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            bg=self.theme_manager.get_color("bg_card"),
            fg=self.theme_manager.get_color("text_primary"),
            relief="flat",
            bd=1,
            padx=20,
            pady=12,
            cursor="hand2"
        )
        self.preview_btn.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Tools section
        tools_section = tk.LabelFrame(
            sidebar_frame,
            text="Tools",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_medium"), self.theme_manager.get_font("weight_medium")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_sidebar"),
            relief="flat",
            bd=0
        )
        tools_section.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        # Tool buttons
        self.rules_btn = tk.Button(
            tools_section,
            text="Custom Rules",
            command=self._open_rules_manager,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            bg=self.theme_manager.get_color("bg_card"),
            fg=self.theme_manager.get_color("text_primary"),
            relief="flat",
            bd=1,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.rules_btn.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Quick Rule button removed as requested
        
        self.backup_btn = tk.Button(
            tools_section,
            text="Backups",
            command=self._open_backup_manager,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            bg=self.theme_manager.get_color("bg_card"),
            fg=self.theme_manager.get_color("text_primary"),
            relief="flat",
            bd=1,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.backup_btn.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Settings section
        settings_section = tk.LabelFrame(
            sidebar_frame,
            text="Settings",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_medium"), self.theme_manager.get_font("weight_medium")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_sidebar"),
            relief="flat",
            bd=0
        )
        settings_section.pack(fill=tk.X, padx=10)
        
        self.settings_btn = tk.Button(
            settings_section,
            text="Settings",
            command=self._open_settings,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            bg=self.theme_manager.get_color("bg_card"),
            fg=self.theme_manager.get_color("text_primary"),
            relief="flat",
            bd=1,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.settings_btn.pack(fill=tk.X, padx=10, pady=(10, 10))

    def _create_main_content(self, parent):
        """Create main content area"""
        content_frame = tk.Frame(parent, bg=self.theme_manager.get_color("bg_primary"))
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Log area
        log_card = tk.Frame(
            content_frame,
            bg=self.theme_manager.get_color("bg_card"),
            relief="flat",
            bd=1
        )
        log_card.pack(fill=tk.BOTH, expand=True)
        
        # Log header
        log_header = tk.Frame(log_card, bg=self.theme_manager.get_color("bg_card"))
        log_header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        log_title = tk.Label(
            log_header,
            text="Activity Log",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_large"), self.theme_manager.get_font("weight_bold")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_card")
        )
        log_title.pack(side=tk.LEFT)
        
        # Clear log button
        clear_log_btn = tk.Button(
            log_header,
            text="Clear Log",
            command=self._clear_log,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_small")),
            bg=self.theme_manager.get_color("bg_secondary"),
            fg=self.theme_manager.get_color("text_primary"),
            relief="flat",
            bd=1,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        clear_log_btn.pack(side=tk.RIGHT)
        
        # Log text area with scrollbar
        log_frame = tk.Frame(log_card, bg=self.theme_manager.get_color("bg_card"))
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create text widget and scrollbar
        self.log_text = tk.Text(
            log_frame,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_small")),
            bg=self.theme_manager.get_color("bg_primary"),
            fg=self.theme_manager.get_color("text_primary"),
            relief="flat",
            bd=1,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        
        log_scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Pack text and scrollbar
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add initial log message
        self._add_log("TidyDesk started. Select a directory to begin organizing files.")
        
        # Progress section (initially hidden)
        self.progress_frame = tk.Frame(
            content_frame,
            bg=self.theme_manager.get_color("bg_card"),
            relief="flat",
            bd=1
        )
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="Organizing files...",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_medium"), self.theme_manager.get_font("weight_medium")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_card")
        )
        self.progress_label.pack(pady=20)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress_bar.pack(pady=(0, 20))

    def _create_status_bar(self, parent):
        """Create modern status bar"""
        status_frame = tk.Frame(parent, bg=self.theme_manager.get_color("bg_secondary"), height=40)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_small")),
            fg=self.theme_manager.get_color("text_secondary"),
            bg=self.theme_manager.get_color("bg_secondary")
        )
        self.status_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Update button states
        self._update_button_states()

    def _apply_theme(self):
        """Apply modern theme to all widgets"""
        theme = self.theme_manager.get_theme()
        colors = theme["colors"]
        
        # Configure root window
        self.root.configure(bg=colors["bg_primary"])
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure progress bar
        style.configure("TProgressbar",
                       background=colors["accent_primary"],
                       troughcolor=colors["bg_tertiary"],
                       borderwidth=0,
                       lightcolor=colors["accent_primary"],
                       darkcolor=colors["accent_primary"])

    def _update_button_states(self):
        """Update button states based on current state"""
        has_directory = self.current_directory is not None
        
        # Enable/disable buttons
        self.organize_btn.config(state=tk.NORMAL if has_directory else tk.DISABLED)
        self.preview_btn.config(state=tk.NORMAL if has_directory else tk.DISABLED)
        
        # Update button colors based on state
        if has_directory:
            self.organize_btn.config(bg=self.theme_manager.get_color("accent_success"))
        else:
            self.organize_btn.config(bg=self.theme_manager.get_color("bg_tertiary"))

    def _select_directory(self):
        """Select directory to organize"""
        directory = filedialog.askdirectory(title="Select Directory to Organize")
        if directory:
            self.current_directory = directory
            self.dir_label.config(
                text=directory,
                fg=self.theme_manager.get_color("text_primary")
            )
            self._update_button_states()
            self._add_log(f"Directory selected: {Path(directory).name}")
            self._update_status(f"Selected: {Path(directory).name}")

    def _organize_files(self):
        """Organize files in the selected directory"""
        if not self.current_directory:
            self._add_log("ERROR: No directory selected for organization")
            messagebox.showwarning("No Directory", "Please select a directory first.")
            return
        
        self._add_log(f"Starting organization of: {Path(self.current_directory).name}")
        
        # Show progress
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))
        self.progress_bar.start()
        self._update_status("Organizing files...")
        
        # Disable buttons during organization
        self.organize_btn.config(state=tk.DISABLED)
        self.preview_btn.config(state=tk.DISABLED)
        
        # Run organization in separate thread
        thread = threading.Thread(target=self._run_organization)
        thread.daemon = True
        thread.start()

    def _run_organization(self):
        """Run file organization in background thread"""
        try:
            self.file_organizer = FileOrganizer(self.config, self._update_progress)
            result = self.file_organizer.organize_directory(self.current_directory)
            
            # Update UI in main thread
            self.root.after(0, self._organization_complete, result)
            
        except Exception as e:
            self.root.after(0, self._organization_error, str(e))

    def _organization_complete(self, result):
        """Handle organization completion"""
        self.progress_frame.pack_forget()
        self.progress_bar.stop()
        
        # Re-enable buttons
        self._update_button_states()
        
        # Show results
        files_moved = result.get('files_moved', 0)
        files_processed = result.get('files_processed', 0)
        
        self._add_log(f"Organization complete: {files_moved}/{files_processed} files organized")
        self._update_status(f"Organization complete: {files_moved}/{files_processed} files organized")
        
        messagebox.showinfo(
            "Organization Complete",
            f"Successfully organized {files_moved} out of {files_processed} files."
        )

    def _organization_error(self, error_msg):
        """Handle organization error"""
        self.progress_frame.pack_forget()
        self.progress_bar.stop()
        
        # Re-enable buttons
        self._update_button_states()
        
        self._add_log(f"ERROR: Organization failed - {error_msg}")
        self._update_status("Organization failed")
        messagebox.showerror("Organization Error", f"Failed to organize files: {error_msg}")

    def _preview_organization(self):
        """Preview organization without making changes"""
        if not self.current_directory:
            self._add_log("ERROR: No directory selected for preview")
            messagebox.showwarning("No Directory", "Please select a directory first.")
            return
        
        try:
            self._add_log(f"Starting preview for: {Path(self.current_directory).name}")
            self.file_organizer = FileOrganizer(self.config, self._update_preview_progress)
            result = self.file_organizer.organize_directory(self.current_directory, dry_run=True)
            
            files_moved = result.get('files_moved', 0)
            files_processed = result.get('files_processed', 0)
            
            self._add_log(f"Preview complete: {files_moved}/{files_processed} files would be organized")
            
            # Show detailed preview in log instead of popup
            if files_moved > 0:
                self._add_log("Files that would be moved:")
                # This would need to be implemented in the file organizer to return file details
                self._add_log("(Detailed file list would be shown here)")
            else:
                self._add_log("No files need to be organized in this directory")
            
        except Exception as e:
            self._add_log(f"ERROR: Preview failed - {e}")
            messagebox.showerror("Preview Error", f"Failed to preview organization: {e}")

    def _update_progress(self, current: int, total: int, filename: str):
        """Update progress during organization"""
        self.root.after(0, lambda: self._update_status(f"Processing: {filename} ({current}/{total})"))

    def _update_status(self, message: str):
        """Update status bar message"""
        self.status_label.config(text=message)
        self._add_log(message)

    def _add_log(self, message: str):
        """Add message to log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _clear_log(self):
        """Clear the log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self._add_log("Log cleared")

    def _update_preview_progress(self, current: int, total: int, filename: str):
        """Update progress during preview"""
        self.root.after(0, lambda: self._add_log(f"Preview: Processing {filename} ({current}/{total})"))

    def _open_rules_manager(self):
        """Open rules manager window"""
        RulesManagerWindow(
            self.root,
            self.theme_manager,
            config=self.config,
            on_rules_updated=self._on_rules_updated
        )

    def _open_backup_manager(self):
        """Open backup manager window"""
        BackupManagerWindow(
            self.root,
            self.theme_manager,
            on_backup_created=self._on_backup_created
        )

    def _open_settings(self):
        """Open settings window"""
        SettingsWindow(self.root, self.config, self.theme_manager)

    def _on_rules_updated(self):
        """Handle rules update"""
        self._update_status("Rules updated successfully")

    # Quick rule method removed as requested

    def _on_backup_created(self, backup_path):
        """Handle backup creation"""
        self._update_status(f"Backup created: {Path(backup_path).name}")

    def _init_scheduler(self):
        """Initialize scheduler"""
        try:
            # Create a dummy organize callback for the scheduler
            def dummy_organize_callback():
                pass
            
            self.scheduler = Scheduler(self.config, dummy_organize_callback)
            # Check if scheduler is enabled in config
            if hasattr(self.config.config.scheduler, 'enabled') and self.config.config.scheduler.enabled:
                self.scheduler.start()
        except Exception as e:
            print(f"Failed to initialize scheduler: {e}")

    def _on_closing(self):
        """Handle window closing"""
        if self.scheduler and self.scheduler.is_running():
            self.scheduler.stop()
        
        # Save window size if enabled
        remember_size = self.config.config.ui.remember_window_size if hasattr(self.config.config.ui, 'remember_window_size') else self.config.config.ui.get('remember_window_size', True)
        if remember_size:
            geometry = self.root.geometry()
            width, height = geometry.split('x')[0], geometry.split('x')[1].split('+')[0]
            if hasattr(self.config.config.ui, '__dict__'):
                self.config.update_config(ui={
                    **self.config.config.ui.__dict__,
                    "window_width": int(width),
                    "window_height": int(height)
                })
            else:
                ui_config = self.config.config.ui.copy() if isinstance(self.config.config.ui, dict) else {}
                ui_config.update({
                    "window_width": int(width),
                    "window_height": int(height)
                })
                self.config.update_config(ui=ui_config)
        
        self.root.destroy()

    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error running GUI: {e}")
            import traceback
            traceback.print_exc()
            raise


class SettingsWindow:
    """Modern settings window"""
    
    def __init__(self, parent, config, theme_manager):
        self.parent = parent
        self.config = config
        self.theme_manager = theme_manager
        
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        self.window.configure(bg=self.theme_manager.get_color("bg_primary"))
        
        # Center window
        self.window.transient(parent)
        self.window.grab_set()
        
        self._create_widgets()
        self._apply_theme()
        
        # Center on parent
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Create settings widgets"""
        # Header
        header_frame = tk.Frame(self.window, bg=self.theme_manager.get_color("bg_primary"))
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Settings",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_xlarge"), self.theme_manager.get_font("weight_bold")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        )
        title_label.pack(anchor=tk.W)
        
        # Main content
        main_frame = tk.Frame(self.window, bg=self.theme_manager.get_color("bg_primary"))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        # Scheduler settings
        scheduler_frame = tk.LabelFrame(
            main_frame,
            text="Scheduler",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_medium"), self.theme_manager.get_font("weight_medium")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary"),
            relief="flat",
            bd=1
        )
        scheduler_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Scheduler enabled
        self.scheduler_enabled_var = tk.BooleanVar(value=self.config.config.scheduler.enabled)
        scheduler_check = tk.Checkbutton(
            scheduler_frame,
            text="Enable automatic organization",
            variable=self.scheduler_enabled_var,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary"),
            selectcolor=self.theme_manager.get_color("accent_primary"),
            activebackground=self.theme_manager.get_color("bg_primary"),
            activeforeground=self.theme_manager.get_color("text_primary")
        )
        scheduler_check.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Time settings
        time_frame = tk.Frame(scheduler_frame, bg=self.theme_manager.get_color("bg_primary"))
        time_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Label(
            time_frame,
            text="Time:",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.time_var = tk.StringVar(value=self.config.config.scheduler.time)
        time_entry = tk.Entry(
            time_frame,
            textvariable=self.time_var,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            width=10
        )
        time_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(
            time_frame,
            text="Interval (hours):",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary")
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.interval_var = tk.IntVar(value=self.config.config.scheduler.interval_hours)
        interval_spin = tk.Spinbox(
            time_frame,
            from_=1,
            to=24,
            textvariable=self.interval_var,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            width=5
        )
        interval_spin.pack(side=tk.LEFT)
        
        # Backup settings
        backup_frame = tk.LabelFrame(
            main_frame,
            text="Backup",
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_medium"), self.theme_manager.get_font("weight_medium")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary"),
            relief="flat",
            bd=1
        )
        backup_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.backup_var = tk.BooleanVar(value=self.config.config.backup_before_organize)
        backup_check = tk.Checkbutton(
            backup_frame,
            text="Create backup before organizing",
            variable=self.backup_var,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            fg=self.theme_manager.get_color("text_primary"),
            bg=self.theme_manager.get_color("bg_primary"),
            selectcolor=self.theme_manager.get_color("accent_primary"),
            activebackground=self.theme_manager.get_color("bg_primary"),
            activeforeground=self.theme_manager.get_color("text_primary")
        )
        backup_check.pack(anchor=tk.W, padx=20, pady=20)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme_manager.get_color("bg_primary"))
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        save_btn = tk.Button(
            button_frame,
            text="Save Settings",
            command=self._save_settings,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal"), self.theme_manager.get_font("weight_medium")),
            bg=self.theme_manager.get_color("accent_primary"),
            fg=self.theme_manager.get_color("text_inverse"),
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2"
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.window.destroy,
            font=(self.theme_manager.get_font("family"), self.theme_manager.get_font("size_normal")),
            bg=self.theme_manager.get_color("bg_card"),
            fg=self.theme_manager.get_color("text_primary"),
            relief="flat",
            bd=1,
            padx=30,
            pady=12,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.RIGHT)

    def _apply_theme(self):
        """Apply theme to settings window"""
        theme = self.theme_manager.get_theme()
        colors = theme["colors"]
        
        self.window.configure(bg=colors["bg_primary"])

    def _save_settings(self):
        """Save settings"""
        try:
            # Update scheduler
            self.config.update_config(scheduler={
                **self.config.config.scheduler.__dict__,
                "enabled": self.scheduler_enabled_var.get(),
                "time": self.time_var.get(),
                "interval_hours": self.interval_var.get()
            })
            
            # Update backup setting
            self.config.update_config(backup_before_organize=self.backup_var.get())
            
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")