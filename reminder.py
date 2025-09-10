"""
Background reminder system for AWS Log Checker Helper Application
"""

import threading
import time
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional
from config import REMINDER_INTERVAL, SNOOZE_INTERVAL


class ReminderSystem:
    """Manages background reminders for checking AWS logs"""
    
    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback
        self.reminder_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.snooze_event = threading.Event()
        self.is_running = False
        
    def start_reminders(self):
        """Start the background reminder system"""
        if self.is_running:
            return
            
        self.is_running = True
        self.stop_event.clear()
        self.reminder_thread = threading.Thread(target=self._reminder_loop, daemon=True)
        self.reminder_thread.start()
    
    def stop_reminders(self):
        """Stop the background reminder system"""
        if not self.is_running:
            return
            
        self.is_running = False
        self.stop_event.set()
        self.snooze_event.set()  # Wake up if snoozed
        
        if self.reminder_thread and self.reminder_thread.is_alive():
            self.reminder_thread.join(timeout=1.0)
    
    def snooze_reminder(self):
        """Snooze the current reminder for the snooze interval"""
        self.snooze_event.set()
    
    def _reminder_loop(self):
        """Main reminder loop running in background thread"""
        while not self.stop_event.is_set():
            # Wait for the reminder interval
            if self.stop_event.wait(REMINDER_INTERVAL):
                break  # Stop event was set
            
            # Show reminder
            self._show_reminder()
            
            # Check if we should snooze
            if self.snooze_event.is_set():
                self.snooze_event.clear()
                # Wait for snooze interval
                if self.stop_event.wait(SNOOZE_INTERVAL):
                    break  # Stop event was set during snooze
    
    def _show_reminder(self):
        """Show reminder notification to user"""
        try:
            # Create a temporary root window if none exists
            temp_root = None
            try:
                # Try to get the current root window
                root = tk._default_root
                if root is None:
                    temp_root = tk.Tk()
                    temp_root.withdraw()  # Hide the temporary window
                    root = temp_root
            except:
                temp_root = tk.Tk()
                temp_root.withdraw()
                root = temp_root
            
            # Show the reminder dialog
            result = messagebox.askyesnocancel(
                "AWS Log Check Reminder",
                "Time to check AWS logs!\n\n"
                "Have you checked the AWS logs recently?\n\n"
                "Yes - Open log entry form\n"
                "No - Snooze for 10 minutes\n"
                "Cancel - Dismiss reminder",
                icon="question"
            )
            
            if result is True:  # Yes - open form
                if self.callback:
                    # Schedule callback in main thread
                    if root and hasattr(root, 'after'):
                        root.after(0, self.callback)
            elif result is False:  # No - snooze
                self.snooze_reminder()
            # result is None for Cancel - just dismiss
            
            # Clean up temporary window
            if temp_root:
                temp_root.destroy()
                
        except Exception as e:
            print(f"Error showing reminder: {e}")
    
    def force_reminder(self):
        """Force show a reminder immediately (for testing)"""
        self._show_reminder()


class ReminderManager:
    """High-level manager for reminder system with GUI integration"""
    
    def __init__(self, parent_window: tk.Tk):
        self.parent = parent_window
        self.reminder_system = ReminderSystem(callback=self._on_reminder_callback)
        self.on_reminder_callback: Optional[Callable] = None
    
    def set_reminder_callback(self, callback: Callable):
        """Set callback function to call when user responds to reminder"""
        self.on_reminder_callback = callback
    
    def start(self):
        """Start the reminder system"""
        self.reminder_system.start_reminders()
    
    def stop(self):
        """Stop the reminder system"""
        self.reminder_system.stop_reminders()
    
    def test_reminder(self):
        """Show a test reminder immediately"""
        self.reminder_system.force_reminder()
    
    def _on_reminder_callback(self):
        """Internal callback when user wants to log a check"""
        if self.on_reminder_callback:
            self.on_reminder_callback()