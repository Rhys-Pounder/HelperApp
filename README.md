# AWS Log Checker Helper Application

A Python GUI application that reminds users every 2 hours to check AWS logs and provides a convenient interface to log check results with persistent storage.

## Features

- **Automatic Reminders**: Get reminded every 2 hours to check AWS logs
- **User-Friendly GUI**: Clean, tabbed interface built with tkinter
- **Data Entry Form**: Log check results with timestamp, outcome, and notes
- **Persistent Storage**: SQLite database stores all check records locally
- **Check History**: View and review previous log checks
- **Cross-Platform**: Works on both macOS and Ubuntu (and other Linux distributions)
- **Snooze Functionality**: Can snooze reminders for 10 minutes
- **No External Dependencies**: Uses built-in Python libraries for maximum compatibility

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python, install with `sudo apt install python3-tk` on Ubuntu)
- Built-in modules: sqlite3, threading, datetime

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Rhys-Pounder/HelperApp.git
   cd HelperApp
   ```

2. On Ubuntu, ensure tkinter is installed:
   ```bash
   sudo apt update
   sudo apt install python3-tk
   ```

3. Run the application:
   ```bash
   python3 main.py
   ```

## Usage

### Starting the Application

Run the main application:
```bash
python3 main.py
```

### Using the Interface

The application has three main tabs:

#### 1. Log Check Tab
- Enter the date and time of your check (click "Now" for current time)
- Select an outcome from the dropdown menu
- Add any relevant notes
- Click "Save Check" to store the record

#### 2. History Tab  
- View all previous check records
- Double-click any record to see full details
- Click "Refresh" to update the list

#### 3. Settings Tab
- Start/Stop automatic reminders
- Test the reminder system
- View application information

### Reminder System

- Once started, reminders appear every 2 hours
- When prompted, you can:
  - **Yes**: Open the log entry form
  - **No**: Snooze for 10 minutes  
  - **Cancel**: Dismiss the reminder

### Data Storage

- All data is stored locally in `~/.aws_log_helper/checks.db`
- Uses SQLite database for reliability and portability
- No external servers or cloud storage required

## File Structure

- `main.py` - Application entry point
- `gui.py` - GUI components and main window
- `database.py` - Database operations and schema
- `reminder.py` - Background reminder system
- `config.py` - Application configuration
- `test.py` - Test suite for validation
- `requirements.txt` - Dependencies documentation

## Testing

Run the test suite to verify functionality:
```bash
python3 test.py
```

## Configuration

Edit `config.py` to customize:
- Reminder interval (default: 2 hours)
- Snooze duration (default: 10 minutes)
- Window dimensions
- Available check outcomes
- Database location

## Troubleshooting

### GUI Not Starting
- Ensure tkinter is installed: `python3 -c "import tkinter; print('OK')"`
- On Ubuntu: `sudo apt install python3-tk`
- On macOS: tkinter should be included with Python

### Permission Issues
- Make sure you have write permissions to your home directory
- The app creates `~/.aws_log_helper/` for data storage

### Import Errors
- Ensure all files are in the same directory
- Check Python version: `python3 --version` (requires 3.6+)

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.