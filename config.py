"""
Configuration settings for AWS Log Checker Helper Application
"""

import os
import sys
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

# Determine if running as compiled executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = sys._MEIPASS
    EVIDENCE_PACK_PATH = os.path.join(application_path, "evidence_pack.txt")
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))
    EVIDENCE_PACK_PATH = os.path.join(application_path, "evidence_pack.txt")