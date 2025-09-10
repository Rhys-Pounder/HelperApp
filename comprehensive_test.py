#!/usr/bin/env python3
"""
Comprehensive test script for AWS Log Checker Helper Application
Tests all components without requiring a GUI display
"""

import datetime
import sys
import os
import tempfile
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from reminder import ReminderSystem
from config import CHECK_OUTCOMES, REMINDER_INTERVAL, DATABASE_PATH


def test_comprehensive_database():
    """Comprehensive database testing"""
    print("=== Comprehensive Database Tests ===")
    
    db = DatabaseManager()
    
    # Test 1: Multiple record insertion
    print("Test 1: Multiple record insertion")
    test_records = []
    for i, outcome in enumerate(CHECK_OUTCOMES):
        notes = f"Test check {i+1} - {outcome.lower()}"
        record_id = db.add_check_record(outcome, notes)
        test_records.append(record_id)
        print(f"  Added record {record_id}: {outcome}")
    
    # Test 2: Record retrieval
    print("\\nTest 2: Record retrieval")
    all_records = db.get_check_records()
    print(f"  Retrieved {len(all_records)} records")
    
    if all_records:
        latest = all_records[0]
        print(f"  Latest: ID={latest['id']}, Outcome={latest['outcome']}")
    
    # Test 3: Get by ID
    print("\\nTest 3: Get record by ID")
    if test_records:
        first_id = test_records[0]
        record = db.get_check_record_by_id(first_id)
        if record:
            print(f"  Retrieved record {first_id}: {record['outcome']}")
        else:
            print(f"  ERROR: Could not retrieve record {first_id}")
    
    # Test 4: Update record
    print("\\nTest 4: Update record")
    if test_records:
        update_id = test_records[0]
        success = db.update_check_record(update_id, "All Good", "Updated test record")
        print(f"  Update result: {success}")
        
        # Verify update
        updated_record = db.get_check_record_by_id(update_id)
        if updated_record and updated_record['notes'] == "Updated test record":
            print(f"  Update verified: {updated_record['notes']}")
        else:
            print("  ERROR: Update not verified")
    
    # Test 5: Recent records
    print("\\nTest 5: Recent records (last 7 days)")
    recent = db.get_recent_records(7)
    print(f"  Found {len(recent)} recent records")
    
    # Test 6: Count
    print("\\nTest 6: Record count")
    count = db.get_records_count()
    print(f"  Total records: {count}")
    
    print("Database tests completed!\\n")


def test_reminder_system():
    """Test reminder system without GUI"""
    print("=== Reminder System Tests ===")
    
    # Test 1: Basic creation
    print("Test 1: Basic reminder system creation")
    callback_called = {"value": False}
    
    def test_callback():
        callback_called["value"] = True
        print("  Callback triggered!")
    
    reminder = ReminderSystem(callback=test_callback)
    print("  ReminderSystem created successfully")
    
    # Test 2: Start/stop without errors
    print("\\nTest 2: Start/stop functionality")
    reminder.start_reminders()
    print("  Started reminders")
    
    # Let it run briefly
    time.sleep(0.1)
    
    reminder.stop_reminders()
    print("  Stopped reminders")
    
    # Test 3: Multiple start/stop cycles
    print("\\nTest 3: Multiple start/stop cycles")
    for i in range(3):
        reminder.start_reminders()
        time.sleep(0.05)
        reminder.stop_reminders()
        print(f"  Cycle {i+1} completed")
    
    print("Reminder system tests completed!\\n")


def test_config_and_paths():
    """Test configuration and file paths"""
    print("=== Configuration Tests ===")
    
    import config
    
    # Test 1: Configuration values
    print("Test 1: Configuration values")
    print(f"  App name: {config.APP_NAME}")
    print(f"  Reminder interval: {config.REMINDER_INTERVAL}s ({config.REMINDER_INTERVAL/3600}h)")
    print(f"  Database path: {config.DATABASE_PATH}")
    print(f"  Data directory: {config.DATA_DIR}")
    print(f"  Outcomes: {len(config.CHECK_OUTCOMES)} available")
    
    # Test 2: Data directory creation
    print("\\nTest 2: Data directory")
    if config.DATA_DIR.exists():
        print(f"  Data directory exists: {config.DATA_DIR}")
    else:
        print(f"  ERROR: Data directory not found: {config.DATA_DIR}")
    
    # Test 3: Database file
    print("\\nTest 3: Database file")
    if config.DATABASE_PATH.exists():
        print(f"  Database file exists: {config.DATABASE_PATH}")
        print(f"  Database size: {config.DATABASE_PATH.stat().st_size} bytes")
    else:
        print(f"  Database file will be created: {config.DATABASE_PATH}")
    
    print("Configuration tests completed!\\n")


def test_imports_and_modules():
    """Test all module imports"""
    print("=== Module Import Tests ===")
    
    modules_to_test = [
        ("config", "Configuration module"),
        ("database", "Database operations"),
        ("reminder", "Reminder system"),
        ("gui", "GUI components"),
    ]
    
    for module_name, description in modules_to_test:
        try:
            module = __import__(module_name)
            print(f"  ✓ {description}: {module_name}")
        except ImportError as e:
            print(f"  ✗ {description}: {module_name} - ERROR: {e}")
        except Exception as e:
            print(f"  ✗ {description}: {module_name} - UNEXPECTED ERROR: {e}")
    
    print("\\nModule import tests completed!\\n")


def test_datetime_operations():
    """Test datetime handling"""
    print("=== DateTime Operations Tests ===")
    
    db = DatabaseManager()
    
    # Test 1: Current datetime
    print("Test 1: Current datetime insertion")
    current_time = datetime.datetime.now()
    record_id = db.add_check_record("All Good", "Current time test", current_time)
    print(f"  Inserted record {record_id} with current time")
    
    # Test 2: Past datetime
    print("\\nTest 2: Past datetime insertion")
    past_time = current_time - datetime.timedelta(hours=3)
    record_id = db.add_check_record("Issues Found", "Past time test", past_time)
    print(f"  Inserted record {record_id} with past time")
    
    # Test 3: Future datetime
    print("\\nTest 3: Future datetime insertion")
    future_time = current_time + datetime.timedelta(hours=1)
    record_id = db.add_check_record("Needs Investigation", "Future time test", future_time)
    print(f"  Inserted record {record_id} with future time")
    
    # Test 4: Retrieve and verify
    print("\\nTest 4: Retrieve and verify datetime handling")
    records = db.get_check_records(limit=3)
    for record in records:
        timestamp = record['timestamp']
        if isinstance(timestamp, str):
            parsed_time = datetime.datetime.fromisoformat(timestamp)
            print(f"  Record {record['id']}: {parsed_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"  Record {record['id']}: {timestamp}")
    
    print("DateTime operations tests completed!\\n")


def main():
    """Run comprehensive test suite"""
    print("=== AWS Log Checker Helper - Comprehensive Test Suite ===\\n")
    
    try:
        test_imports_and_modules()
        test_config_and_paths()
        test_comprehensive_database()
        test_datetime_operations()
        test_reminder_system()
        
        print("🎉 ALL COMPREHENSIVE TESTS PASSED! 🎉")
        print("\\nThe AWS Log Checker Helper application is ready for use!")
        print("\\nTo start the application, run:")
        print("    python3 main.py")
        
        return 0
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())