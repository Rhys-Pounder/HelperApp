"""
Web-based version of AWS Log Checker Helper
Cross-platform Flask application - no GUI dependencies required
"""

from flask import Flask, render_template, request, jsonify, send_file
import datetime
import json
import os
from database import DatabaseManager
from typing import Dict, List
import tempfile
import csv

# Override database path for Docker environment
import config
DATABASE_PATH = os.path.join(os.getcwd(), 'data', 'checks.db')
config.DATABASE_PATH = DATABASE_PATH

app = Flask(__name__)

# Create data directory if it doesn't exist
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# Add debugging
print(f"Database path: {DATABASE_PATH}")
print(f"Current working directory: {os.getcwd()}")
print(f"Data directory exists: {os.path.exists(os.path.dirname(DATABASE_PATH))}")

# Force the database to use the correct path by passing it explicitly
class DockerDatabaseManager(DatabaseManager):
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()

db = DockerDatabaseManager()

# Check outcomes from config
CHECK_OUTCOMES = [
    "No Issues Found",
    "Minor Issues - Monitoring",
    "Issues Found - Action Required",
    "Critical Issues - Immediate Action",
    "System Unavailable",
    "Partial Check Completed"
]

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')

@app.route('/api/save_check', methods=['POST'])
def save_check():
    """Save a log check to the database"""
    try:
        data = request.json
        print(f"Received save_check request with data: {data}")
        
        datetime_str = data.get('datetime', '').strip()
        outcome = data.get('outcome', '')
        notes = data.get('notes', '').strip()
        
        print(f"Parsed data - datetime: {datetime_str}, outcome: {outcome}, notes: {notes}")
        
        if not datetime_str or not outcome:
            print("Error: Missing datetime or outcome")
            return jsonify({'error': 'Date/time and outcome are required'}), 400
        
        # Parse datetime
        try:
            check_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            print(f"Parsed datetime: {check_datetime}")
        except ValueError as e:
            print(f"DateTime parsing error: {e}")
            return jsonify({'error': 'Invalid date/time format. Use YYYY-MM-DD HH:MM:SS'}), 400
        
        # Save to database
        print("Attempting to save to database...")
        record_id = db.add_check(check_datetime, outcome, notes)
        print(f"Saved with record ID: {record_id}")
        
        return jsonify({'success': True, 'id': record_id})
        
    except Exception as e:
        print(f"Exception in save_check: {e}")
        return jsonify({'error': f'Failed to save check: {str(e)}'}), 500

@app.route('/api/get_history')
def get_history():
    """Get check history"""
    try:
        print("Getting history from database...")
        records = db.get_all_checks()
        print(f"Retrieved {len(records)} records: {records}")
        return jsonify({'records': records})
    except Exception as e:
        print(f"Exception in get_history: {e}")
        return jsonify({'error': f'Failed to get history: {str(e)}'}), 500

@app.route('/api/delete_check/<int:record_id>', methods=['DELETE'])
def delete_check(record_id):
    """Delete a check record"""
    try:
        success = db.delete_check(record_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to delete record: {str(e)}'}), 500

@app.route('/api/export_csv')
def export_csv():
    """Export history to CSV"""
    try:
        records = db.get_all_checks()
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='')
        
        writer = csv.writer(temp_file)
        writer.writerow(["ID", "Date/Time", "Outcome", "Notes"])
        writer.writerows(records)
        temp_file.close()
        
        return send_file(temp_file.name, as_attachment=True, 
                        download_name=f'aws_log_checks_{datetime.datetime.now().strftime("%Y%m%d")}.csv',
                        mimetype='text/csv')
                        
    except Exception as e:
        return jsonify({'error': f'Failed to export CSV: {str(e)}'}), 500

@app.route('/api/generate_evidence_pack', methods=['POST'])
def generate_evidence_pack():
    """Generate evidence pack"""
    try:
        data = request.json
        
        # Build evidence pack content
        content = "AWS Log Checker Helper - Evidence Pack\n\n"
        content += "EVIDENCE DOCUMENTATION:\n"
        content += "=" * 33 + "\n\n"
        
        content += f"Date/Time: {data.get('datetime', '[YYYY-MM-DD HH:MM:SS]')}\n"
        content += f"Checker: {data.get('checker', '[Your Name]')}\n"
        content += f"Environment: {data.get('environment', '[Production/Staging/Development]')}\n"
        content += f"AWS Account: {data.get('account', '[Account ID or Name]')}\n\n"
        
        content += "LOG SOURCES CHECKED:\n"
        content += f"- CloudWatch Logs: {data.get('cloudwatch_logs', '[Log Group Names]')}\n"
        content += f"- CloudTrail: {data.get('cloudtrail', '[Trail Names]')}\n"
        content += f"- Application Logs: {data.get('app_logs', '[Service Names]')}\n"
        content += f"- Security Logs: {data.get('security_logs', '[WAF, GuardDuty, etc.]')}\n\n"
        
        content += "FINDINGS:\n"
        findings = data.get('findings', [])
        if findings:
            for i, finding in enumerate(findings, 1):
                content += f"- Finding {i}: {finding}\n"
        else:
            content += "- No findings reported\n"
        content += "\n"
        
        content += "ACTIONS TAKEN:\n"
        actions = data.get('actions', [])
        if actions:
            for i, action in enumerate(actions, 1):
                content += f"- Action {i}: {action}\n"
        else:
            content += "- No actions taken\n"
        content += "\n"
        
        content += "FOLLOW-UP REQUIRED:\n"
        followups = data.get('followups', [])
        if followups:
            for i, followup in enumerate(followups, 1):
                content += f"- Follow-up {i}: {followup}\n"
        else:
            content += "- No follow-up required\n"
        content += "\n"
        
        content += f"SCREENSHOTS/LOGS:\n{data.get('evidence', '[Attach or reference any supporting evidence]')}\n\n"
        
        content += "SIGN-OFF:\n"
        content += f"Checked by: {data.get('checked_by', '[Name]')}\n"
        content += f"Reviewed by: {data.get('reviewed_by', '[Name]')}\n"
        content += f"Date: {data.get('signoff_date', '[YYYY-MM-DD]')}\n"
        
        return jsonify({'content': content})
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate evidence pack: {str(e)}'}), 500

@app.route('/api/queries')
def get_queries():
    """Get AWS queries"""
    queries = {
        "cloudwatch_insights": [
            {
                "title": "🔴 Error Detection",
                "query": "fields @timestamp, @message\n| filter @message like /(?i)(error|exception|fail|failed)/\n| sort @timestamp desc\n| limit 10"
            },
            {
                "title": "⚡ Performance Issues", 
                "query": "fields @timestamp, @message, elapsed_ms\n| filter ispresent(elapsed_ms)\n| sort elapsed_ms desc\n| limit 10"
            },
            {
                "title": "💾 Memory Usage",
                "query": "fields @timestamp, @message\n| filter @message like /memory/\n| sort @timestamp desc\n| limit 10"
            }
        ],
        "aws_cli": [
            {
                "title": "🔐 CloudTrail Failed Logins",
                "query": "aws logs start-query \\\n--log-group-name YOUR_CLOUDTRAIL_LOG_GROUP \\\n--start-time $(date -v-2H +%s) \\\n--end-time $(date +%s) \\\n--query-string \"fields @timestamp, @message | filter eventName = 'ConsoleLogin' and errorMessage = 'Failed authentication'\""
            },
            {
                "title": "🖥️ SSM Session History",
                "query": "aws ssm describe-sessions \\\n--state \"History\" \\\n--filters key=Owner,value=* \\\n--query \"Sessions[?StartDate>=`date -v-2H +%Y-%m-%dT%H:%M:%SZ`].[SessionId,Owner,StartDate]\" \\\n--output table"
            }
        ]
    }
    return jsonify(queries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)