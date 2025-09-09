"""
Main entry point for the file organizer application
"""

import sys
import argparse
import logging
from pathlib import Path

from .core.config import Config
from .core.file_organizer import FileOrganizer
from .core.scheduler import Scheduler
from .gui.main_window import MainWindow
from .utils.logger import setup_logging, get_default_log_file
from .utils.exceptions import FileOrganizerError


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="File Organizer - A production-ready file organization tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m file_organizer                    # Start GUI
  python -m file_organizer --gui              # Start GUI
  python -m file_organizer --organize /path   # Organize directory
  python -m file_organizer --preview /path    # Preview organization
  python -m file_organizer --scheduler start  # Start scheduler
  python -m file_organizer --scheduler stop   # Stop scheduler
        """
    )
    
    parser.add_argument(
        "--gui", 
        action="store_true", 
        help="Start the GUI application (default)"
    )
    
    parser.add_argument(
        "--organize", 
        metavar="DIRECTORY",
        help="Organize files in the specified directory"
    )
    
    parser.add_argument(
        "--preview", 
        metavar="DIRECTORY",
        help="Preview organization without moving files"
    )
    
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Preview mode - don't actually move files"
    )
    
    parser.add_argument(
        "--no-backup", 
        action="store_true",
        help="Don't create backup before organizing"
    )
    
    parser.add_argument(
        "--config", 
        metavar="FILE",
        help="Use custom configuration file"
    )
    
    parser.add_argument(
        "--log-level", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set logging level"
    )
    
    parser.add_argument(
        "--log-file", 
        metavar="FILE",
        help="Log to file (default: auto-generated path)"
    )
    
    parser.add_argument(
        "--scheduler",
        choices=["start", "stop", "status"],
        help="Manage the scheduler"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="File Organizer 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = args.log_file or get_default_log_file()
    logger = setup_logging(
        log_level=args.log_level,
        log_file=log_file
    )
    
    try:
        # Load configuration
        config = Config(args.config) if args.config else Config()
        
        # Handle scheduler commands
        if args.scheduler:
            handle_scheduler_command(args.scheduler, config, logger)
            return
        
        # Handle CLI commands
        if args.organize or args.preview:
            handle_cli_command(args, config, logger)
            return
        
        # Default: start GUI
        start_gui(config, logger)
        
    except FileOrganizerError as e:
        logger.error(f"File Organizer Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


def handle_scheduler_command(command: str, config: Config, logger: logging.Logger):
    """Handle scheduler commands"""
    scheduler = Scheduler(config, lambda: None)  # Dummy callback for CLI
    
    if command == "start":
        if scheduler.is_running():
            print("Scheduler is already running")
        else:
            scheduler.start()
            print("Scheduler started")
    
    elif command == "stop":
        if not scheduler.is_running():
            print("Scheduler is not running")
        else:
            scheduler.stop()
            print("Scheduler stopped")
    
    elif command == "status":
        info = scheduler.get_schedule_info()
        print(f"Scheduler Status: {scheduler.get_status()}")
        print(f"Enabled: {info['enabled']}")
        print(f"Running: {info['running']}")
        if info['next_run']:
            print(f"Next Run: {info['next_run']}")


def handle_cli_command(args, config: Config, logger: logging.Logger):
    """Handle CLI commands"""
    directory = args.organize or args.preview
    
    if not directory or not Path(directory).exists():
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)
    
    # Update config for CLI
    if args.dry_run:
        config.update_config(dry_run=True)
    if args.no_backup:
        config.update_config(backup_before_organize=False)
    
    # Create file organizer
    organizer = FileOrganizer(config, progress_callback=cli_progress_callback)
    
    try:
        if args.preview:
            print(f"Previewing organization for: {directory}")
            preview = organizer.preview_organization(directory)
            
            if preview:
                print(f"\nFound {len(preview)} files to organize:")
                for item in preview:
                    print(f"  {item['file_name']} -> {item['target_folder']}")
            else:
                print("No files found to organize")
        
        else:  # args.organize
            print(f"Organizing files in: {directory}")
            stats = organizer.organize_directory(directory, dry_run=args.dry_run)
            
            print(f"\nOrganization completed!")
            print(f"Files processed: {stats['files_processed']}")
            print(f"Files moved: {stats['files_moved']}")
            print(f"Files skipped: {stats['files_skipped']}")
            print(f"Errors: {stats['errors']}")
            
            if stats['errors'] > 0:
                print(f"Check the log file for details: {get_default_log_file()}")
    
    except Exception as e:
        logger.error(f"Error during organization: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def cli_progress_callback(progress: float, message: str):
    """Progress callback for CLI"""
    print(f"\r{message}... {progress:.1f}%", end="", flush=True)


def start_gui(config: Config, logger: logging.Logger):
    """Start the GUI application"""
    try:
        app = MainWindow()
        logger.info("Starting GUI application")
        app.run()
    except Exception as e:
        logger.error(f"Error starting GUI: {e}")
        raise


if __name__ == "__main__":
    main()
