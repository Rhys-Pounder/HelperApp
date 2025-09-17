"""
Database operations for AWS Log Checker Helper Application
"""

import sqlite3
import datetime
import csv
from typing import List, Dict, Optional
from config import DATABASE_PATH


class DatabaseManager:
    """Manages SQLite database operations for check records"""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS check_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    outcome TEXT NOT NULL,
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def add_check_record(self, outcome: str, notes: str = "", timestamp: Optional[datetime.datetime] = None) -> int:
        """Add a new check record to the database"""
        if timestamp is None:
            timestamp = datetime.datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO check_records (timestamp, outcome, notes)
                VALUES (?, ?, ?)
            """, (timestamp, outcome, notes))
            conn.commit()
            return cursor.lastrowid
    
    def get_check_records(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Retrieve check records from the database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            cursor = conn.execute("""
                SELECT id, timestamp, outcome, notes, created_at
                FROM check_records
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_check_record_by_id(self, record_id: int) -> Optional[Dict]:
        """Get a specific check record by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT id, timestamp, outcome, notes, created_at
                FROM check_records
                WHERE id = ?
            """, (record_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_check_record(self, record_id: int, outcome: str, notes: str = "", 
                          timestamp: Optional[datetime.datetime] = None) -> bool:
        """Update an existing check record"""
        if timestamp is None:
            timestamp = datetime.datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                UPDATE check_records
                SET timestamp = ?, outcome = ?, notes = ?
                WHERE id = ?
            """, (timestamp, outcome, notes, record_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_check_record(self, record_id: int) -> bool:
        """Delete a check record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM check_records WHERE id = ?", (record_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_records_count(self) -> int:
        """Get total number of check records"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM check_records")
            return cursor.fetchone()[0]
    
    def get_recent_records(self, days: int = 7) -> List[Dict]:
        """Get check records from the last N days"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT id, timestamp, outcome, notes, created_at
                FROM check_records
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
            """, (cutoff_date,))
            return [dict(row) for row in cursor.fetchall()]
    
    def export_to_csv(self, filepath: str, limit: int = None) -> bool:
        """Export check records to CSV file"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                if limit:
                    cursor = conn.execute("""
                        SELECT id, timestamp, outcome, notes, created_at
                        FROM check_records
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """, (limit,))
                else:
                    cursor = conn.execute("""
                        SELECT id, timestamp, outcome, notes, created_at
                        FROM check_records
                        ORDER BY timestamp DESC
                    """)
                
                records = cursor.fetchall()
                
                with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['ID', 'Timestamp', 'Outcome', 'Notes', 'Created At']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for record in records:
                        writer.writerow({
                            'ID': record['id'],
                            'Timestamp': record['timestamp'],
                            'Outcome': record['outcome'],
                            'Notes': record['notes'] or '',
                            'Created At': record['created_at']
                        })
                
                return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    def add_check(self, timestamp: datetime.datetime, outcome: str, notes: str = "") -> int:
        """Add a new check record (alias for GUI compatibility)"""
        return self.add_check_record(outcome, notes, timestamp)
    
    def get_all_checks(self) -> List[tuple]:
        """Get all check records in tuple format for GUI compatibility"""
        records = self.get_check_records(limit=1000)  # Get more records
        # Convert to tuple format expected by GUI: (id, timestamp, outcome, notes)
        return [(record['id'], record['timestamp'], record['outcome'], record['notes']) 
                for record in records]
    
    def delete_check(self, record_id: int) -> bool:
        """Delete a check record (alias for GUI compatibility)"""
        return self.delete_check_record(record_id)
    
    def clean_old_records(self, cutoff_date: datetime.datetime) -> int:
        """Clean old records before cutoff date"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM check_records 
                WHERE timestamp < ?
            """, (cutoff_date,))
            conn.commit()
            return cursor.rowcount
    
    def close(self):
        """Close database connection (for compatibility)"""
        # SQLite connections are closed automatically with context managers
        pass