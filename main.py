#!/usr/bin/env python3
"""
AWS Log Checker Helper Application

A GUI application that reminds users every 2 hours to check AWS logs
and provides a form to log check results with persistent storage.

Usage:
    python3 main.py

Features:
- 2-hour reminder notifications
- GUI form for logging check results
- SQLite database storage
- Cross-platform compatibility (macOS/Ubuntu)
- Check history viewer
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui import MainWindow
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required files are present:")
    print("- gui.py")
    print("- database.py") 
    print("- reminder.py")
    print("- config.py")
    sys.exit(1)


def main():
    """Main application entry point"""
    try:
        # Create and run the main application
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()