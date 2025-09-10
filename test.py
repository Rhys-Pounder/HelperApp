#!/usr/bin/env python3
"""
Test script for AWS Log Checker Helper Application
"""

import datetime
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from config import CHECK_OUTCOMES


def test_database():
    """Test database operations"""
    print("Testing database operations...")
    
    db = DatabaseManager()
    
    # Test adding a record
    test_outcome = CHECK_OUTCOMES[0]
    test_notes = "Test check - automated test"
    record_id = db.add_check_record(test_outcome, test_notes)
    print(f"Added record with ID: {record_id}")
    
    # Test retrieving records
    records = db.get_check_records(limit=5)
    print(f"Retrieved {len(records)} records")
    
    if records:
        latest = records[0]
        print(f"Latest record: {latest['timestamp']} - {latest['outcome']}")
    
    # Test getting count
    count = db.get_records_count()
    print(f"Total records in database: {count}")
    
    print("Database tests completed successfully!")


def test_config():
    """Test configuration"""
    print("Testing configuration...")
    
    import config
    print(f"App name: {config.APP_NAME}")
    print(f"Reminder interval: {config.REMINDER_INTERVAL / 3600} hours")
    print(f"Database path: {config.DATABASE_PATH}")
    print(f"Available outcomes: {config.CHECK_OUTCOMES}")
    
    print("Configuration tests completed successfully!")


def main():
    """Run all tests"""
    print("=== AWS Log Checker Helper - Test Suite ===\\n")
    
    try:
        test_config()
        print()
        test_database()
        print()
        print("All tests passed! ✓")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())