"""
Configuration settings for AWS Log Checker Helper Application
"""

import os
from pathlib import Path

# Application settings
APP_NAME = "AWS Log Checker Helper"
APP_VERSION = "1.0.0"

# Reminder settings (in seconds)
REMINDER_INTERVAL = 2 * 60 * 60  # 2 hours
SNOOZE_INTERVAL = 10 * 60        # 10 minutes

# Database settings
DATA_DIR = Path.home() / ".aws_log_helper"
DATABASE_PATH = DATA_DIR / "checks.db"

# GUI settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 400

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Check outcomes
CHECK_OUTCOMES = [
    "All Good",
    "Issues Found",
    "Needs Investigation", 
    "Action Required",
    "No Access"
]