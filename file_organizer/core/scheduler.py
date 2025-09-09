"""
Scheduler functionality for automatic file organization
"""

import schedule
import threading
import time
import logging
from datetime import datetime, timedelta
from typing import Callable, Optional, List
from .config import Config, SchedulerConfig


class Scheduler:
    """Scheduler for automatic file organization"""
    
    def __init__(self, config: Config, organize_callback: Callable):
        self.config = config
        self.organize_callback = organize_callback
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._thread = None
        self._stop_event = threading.Event()

    def start(self):
        """Start the scheduler"""
        if self._running:
            self.logger.warning("Scheduler is already running")
            return
        
        if not self.config.config.scheduler.enabled:
            self.logger.info("Scheduler is disabled in configuration")
            return
        
        self._setup_schedule()
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._thread.start()
        
        self.logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler"""
        if not self._running:
            return
        
        self._running = False
        self._stop_event.set()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        
        schedule.clear()
        self.logger.info("Scheduler stopped")

    def is_running(self) -> bool:
        """Check if scheduler is running"""
        return self._running

    def _setup_schedule(self):
        """Setup the schedule based on configuration"""
        scheduler_config = self.config.config.scheduler
        
        if scheduler_config.interval_hours > 0:
            # Interval-based scheduling
            schedule.every(scheduler_config.interval_hours).hours.do(self._run_organization)
        else:
            # Time-based scheduling
            time_str = scheduler_config.time
            days = scheduler_config.days
            
            if days and len(days) > 0:
                # Specific days
                for day in days:
                    day_name = self._get_day_name(day)
                    getattr(schedule.every(), day_name).at(time_str).do(self._run_organization)
            else:
                # Daily
                schedule.every().day.at(time_str).do(self._run_organization)

    def _get_day_name(self, day_num: int) -> str:
        """Convert day number to schedule day name"""
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        return days[day_num % 7]

    def _run_scheduler(self):
        """Main scheduler loop"""
        self.logger.info("Scheduler thread started")
        
        while self._running and not self._stop_event.is_set():
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)
        
        self.logger.info("Scheduler thread stopped")

    def _run_organization(self):
        """Run the organization task"""
        try:
            self.logger.info("Running scheduled organization")
            self.organize_callback()
        except Exception as e:
            self.logger.error(f"Error in scheduled organization: {e}")

    def get_next_run_time(self) -> Optional[datetime]:
        """Get the next scheduled run time"""
        if not self._running:
            return None
        
        jobs = schedule.get_jobs()
        if not jobs:
            return None
        
        # Get the earliest next run time
        next_runs = [job.next_run for job in jobs if job.next_run]
        if next_runs:
            return min(next_runs)
        
        return None

    def get_schedule_info(self) -> dict:
        """Get information about the current schedule"""
        scheduler_config = self.config.config.scheduler
        
        info = {
            'enabled': scheduler_config.enabled,
            'running': self._running,
            'next_run': self.get_next_run_time(),
            'jobs': []
        }
        
        for job in schedule.get_jobs():
            job_info = {
                'function': job.job_func.__name__,
                'next_run': job.next_run,
                'interval': str(job.interval) if hasattr(job, 'interval') else None,
                'unit': job.unit if hasattr(job, 'unit') else None
            }
            info['jobs'].append(job_info)
        
        return info

    def update_schedule(self, new_config: SchedulerConfig):
        """Update the schedule with new configuration"""
        self.stop()
        self.config.config.scheduler = new_config
        self.config.save_config()
        
        if new_config.enabled:
            self.start()

    def run_now(self):
        """Manually trigger organization now"""
        self.logger.info("Manual organization triggered")
        self._run_organization()

    def get_status(self) -> str:
        """Get human-readable status of the scheduler"""
        if not self.config.config.scheduler.enabled:
            return "Disabled"
        
        if not self._running:
            return "Stopped"
        
        next_run = self.get_next_run_time()
        if next_run:
            return f"Running - Next: {next_run.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            return "Running - No jobs scheduled"
