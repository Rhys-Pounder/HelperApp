"""
GUI components for AWS Log Checker Helper Application
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime
from typing import Optional
from database import DatabaseManager
from reminder import ReminderManager
from config import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
    CHECK_OUTCOMES
)
import tkinter.font as tkfont

# Import for Evidence Pack Generator
try:
    import customtkinter as ctk
    from evidence_pack_tab import EvidencePackTab
    EVIDENCE_PACK_AVAILABLE = True
except ImportError:
    EVIDENCE_PACK_AVAILABLE = False
    print("Warning: Evidence Pack Generator not available. Install customtkinter and pyperclip to enable.")


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.db = DatabaseManager()
        self.reminder_manager = ReminderManager(self.root)
        self.dark_mode = True  # Start with dark mode
        self.setup_theme()  # Add dark mode and font styling
        self.setup_window()
        self.create_widgets()
        self.setup_reminder_system()
        self.refresh_history()
    
    def setup_theme(self):
        """Set dark mode and custom font"""
        style = ttk.Style(self.root)
        style.theme_use('clam')
        
        if self.dark_mode:
            dark_bg = "#23272e"
            dark_fg = "#e6e6e6"
            accent = "#4f8cff"
            entry_bg = "#3c4043"
            entry_fg = "#e6e6e6"
            tab_selected = "#4f8cff"
            tab_normal = "#2c313c"
        else:
            dark_bg = "#ffffff"
            dark_fg = "#000000"
            accent = "#0078d4"
            entry_bg = "#ffffff"
            entry_fg = "#000000"
            tab_selected = "#e1ecf4"
            tab_normal = "#f0f0f0"
        
        self.root.configure(bg=dark_bg)
        style.configure('.', background=dark_bg, foreground=dark_fg, font=('Segoe UI', 11))
        style.configure('TLabel', background=dark_bg, foreground=dark_fg)
        style.configure('TFrame', background=dark_bg)
        style.configure('TLabelframe', background=dark_bg, foreground=dark_fg)
        style.configure('TLabelframe.Label', background=dark_bg, foreground=dark_fg)
        style.configure('TButton', background=accent, foreground=dark_fg)
        style.configure('TNotebook', background=dark_bg, borderwidth=0)
        style.configure('TNotebook.Tab', background=tab_normal, foreground=dark_fg, padding=[12, 8])
        style.configure('TEntry', background=entry_bg, foreground=entry_fg, insertcolor=entry_fg, 
                       fieldbackground=entry_bg, borderwidth=1, relief='solid')
        style.configure('TCombobox', background=entry_bg, foreground=entry_fg, selectbackground=accent, 
                       selectforeground=dark_fg, fieldbackground=entry_bg, borderwidth=1, relief='solid')
        style.configure('TSpinbox', background=entry_bg, foreground=entry_fg, insertcolor=entry_fg,
                       fieldbackground=entry_bg, borderwidth=1, relief='solid')
        style.configure('Treeview', background=entry_bg, foreground=entry_fg, fieldbackground=entry_bg)
        style.configure('Treeview.Heading', background=tab_normal, foreground=dark_fg)
        
        style.map('TButton', background=[('active', accent), ('pressed', '#3465a4')])
        style.map('TNotebook.Tab', background=[('selected', tab_selected), ('active', accent)])
        style.map('TEntry', fieldbackground=[('readonly', entry_bg), ('focus', entry_bg)])
        style.map('TCombobox', fieldbackground=[('readonly', entry_bg), ('focus', entry_bg)])
        
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=11)
        self.root.option_add("*Font", default_font)
        
        # Configure ScrolledText widget colors
        if hasattr(self, 'notes_text'):
            if self.dark_mode:
                self.notes_text.configure(bg="#3c4043", fg="#e6e6e6", insertbackground="#e6e6e6")
            else:
                self.notes_text.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
    
    def _apply_scrolledtext_theme(self, widget):
        """Apply theme to ScrolledText widgets recursively"""
        if isinstance(widget, scrolledtext.ScrolledText):
            if self.dark_mode:
                widget.configure(bg="#3c4043", fg="#e6e6e6", insertbackground="#e6e6e6")
            else:
                widget.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
        elif hasattr(widget, 'winfo_children'):
            for child in widget.winfo_children():
                self._apply_scrolledtext_theme(child)
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_entry_tab(notebook)
        self.create_history_tab(notebook)
        self.create_queries_tab(notebook)
        self.create_settings_tab(notebook)
        
        # Add Evidence Pack Generator tab if available
        if EVIDENCE_PACK_AVAILABLE:
            self.create_evidence_pack_tab(notebook)
    
    def create_entry_tab(self, parent):
        """Create the log entry tab"""
        self.entry_frame = ttk.Frame(parent)
        parent.add(self.entry_frame, text="Log Check")
        
        # Main container with padding
        main_frame = ttk.Frame(self.entry_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="AWS Log Check Entry", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Entry form
        form_frame = ttk.LabelFrame(main_frame, text="Check Details", padding="10")
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Date and time
        datetime_frame = ttk.Frame(form_frame)
        datetime_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(datetime_frame, text="Date & Time:").pack(side=tk.LEFT)
        self.datetime_var = tk.StringVar()
        self.datetime_entry = ttk.Entry(datetime_frame, textvariable=self.datetime_var, width=20)
        self.datetime_entry.pack(side=tk.LEFT, padx=(10, 5))
        
        ttk.Button(datetime_frame, text="Now", command=self.set_current_datetime).pack(side=tk.LEFT)
        
        # Outcome
        outcome_frame = ttk.Frame(form_frame)
        outcome_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(outcome_frame, text="Outcome:").pack(side=tk.LEFT)
        self.outcome_var = tk.StringVar()
        self.outcome_combo = ttk.Combobox(outcome_frame, textvariable=self.outcome_var,
                                         values=CHECK_OUTCOMES, state="readonly", width=20)
        self.outcome_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.outcome_combo.set(CHECK_OUTCOMES[0])  # Set default
        
        # Notes
        notes_frame = ttk.Frame(form_frame)
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(notes_frame, text="Notes:").pack(anchor=tk.W)
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=6, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save Check", command=self.save_check).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=(10, 0))
        
        # Initialize with current date/time
        self.set_current_datetime()
    
    def create_history_tab(self, parent):
        """Create the history viewing tab"""
        self.history_frame = ttk.Frame(parent)
        parent.add(self.history_frame, text="History")
        
        # Main container
        main_frame = ttk.Frame(self.history_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and controls
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="Check History", 
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        # Button frame for controls
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="Export CSV", 
                  command=self.export_to_csv).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_selected_record).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Refresh", 
                  command=self.refresh_history).pack(side=tk.LEFT)
        
        # History list
        list_frame = ttk.LabelFrame(main_frame, text="Recent Checks", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for history
        columns = ("ID", "Date/Time", "Outcome", "Notes")
        self.history_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.history_tree.heading("ID", text="ID")
        self.history_tree.heading("Date/Time", text="Date/Time")
        self.history_tree.heading("Outcome", text="Outcome")
        self.history_tree.heading("Notes", text="Notes")
        
        self.history_tree.column("ID", width=50)
        self.history_tree.column("Date/Time", width=180)
        self.history_tree.column("Outcome", width=150)
        self.history_tree.column("Notes", width=300)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to view details
        self.history_tree.bind("<Double-1>", self.on_history_double_click)
    
    def create_queries_tab(self, parent):
        """Create the AWS queries tab"""
        self.queries_frame = ttk.Frame(parent)
        parent.add(self.queries_frame, text="AWS Queries")
        
        # Main container
        main_frame = ttk.Frame(self.queries_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_frame, text="AWS Query Templates", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # CloudWatch Insights Queries
        insights_frame = ttk.LabelFrame(scrollable_frame, text="CloudWatch Insights Queries", padding="10")
        insights_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.add_query_section(insights_frame, "Error Detection", 
            "fields @timestamp, @message\n"
            "| filter @message like /(?i)(error|exception|fail|failed)/\n"
            "| sort @timestamp desc\n"
            "| limit 10")
        
        self.add_query_section(insights_frame, "Performance Issues", 
            "fields @timestamp, @message, elapsed_ms\n"
            "| filter ispresent(elapsed_ms)\n"
            "| sort elapsed_ms desc\n"
            "| limit 10")
        
        self.add_query_section(insights_frame, "Recent Requests", 
            "fields @timestamp, @message\n"
            "| filter @timestamp > @timestamp - 1h\n"
            "| sort @timestamp desc\n"
            "| limit 20")
        
        self.add_query_section(insights_frame, "Memory Usage", 
            "fields @timestamp, @message\n"
            "| filter @message like /memory/\n"
            "| sort @timestamp desc\n"
            "| limit 10")
        
        # AWS CLI Commands
        cli_frame = ttk.LabelFrame(scrollable_frame, text="AWS CLI Commands", padding="10")
        cli_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.add_query_section(cli_frame, "CloudTrail Failed Logins",
            "aws logs start-query \\\n"
            "--log-group-name YOUR_CLOUDTRAIL_LOG_GROUP \\\n"
            "--start-time $(date -v-2H +%s) \\\n"
            "--end-time $(date +%s) \\\n"
            '--query-string "fields @timestamp, @message | filter eventName = \'ConsoleLogin\' and errorMessage = \'Failed authentication\'"')
        
        self.add_query_section(cli_frame, "SSM Session History",
            "aws ssm describe-sessions \\\n"
            '--state "History" \\\n'
            "--filters key=Owner,value=* \\\n"
            '--query "Sessions[?StartDate>=`date -v-2H +%Y-%m-%dT%H:%M:%SZ`].[SessionId,Owner,StartDate]" \\\n'
            "--output table")
        
        self.add_query_section(cli_frame, "Unhealthy Target Groups",
            "aws cloudwatch get-metric-statistics \\\n"
            "--namespace AWS/ApplicationELB \\\n"
            "--metric-name UnHealthyHostCount \\\n"
            "--dimensions Name=TargetGroup,Value=YOUR_TARGET_GROUP_ARN \\\n"
            "--start-time $(date -v-2H +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--end-time $(date +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--period 300 \\\n"
            "--statistics Sum")
        
        self.add_query_section(cli_frame, "Load Balancer 5XX Errors",
            "aws cloudwatch get-metric-statistics \\\n"
            "--namespace AWS/ApplicationELB \\\n"
            "--metric-name HTTPCode_Target_5XX_Count \\\n"
            "--dimensions Name=LoadBalancer,Value=YOUR_LOAD_BALANCER_ARN \\\n"
            "--start-time $(date -v-2H +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--end-time $(date +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--period 300 \\\n"
            "--statistics Sum")
        
        # Additional Monitoring
        monitoring_frame = ttk.LabelFrame(scrollable_frame, text="Additional Monitoring", padding="10")
        monitoring_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.add_query_section(monitoring_frame, "RDS Performance",
            "aws cloudwatch get-metric-statistics \\\n"
            "--namespace AWS/RDS \\\n"
            "--metric-name DatabaseConnections \\\n"
            "--dimensions Name=DBInstanceIdentifier,Value=YOUR_DB_INSTANCE \\\n"
            "--start-time $(date -v-1H +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--end-time $(date +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--period 300 \\\n"
            "--statistics Average,Maximum")
        
        self.add_query_section(monitoring_frame, "Lambda Errors",
            "aws cloudwatch get-metric-statistics \\\n"
            "--namespace AWS/Lambda \\\n"
            "--metric-name Errors \\\n"
            "--dimensions Name=FunctionName,Value=YOUR_FUNCTION_NAME \\\n"
            "--start-time $(date -v-1H +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--end-time $(date +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--period 300 \\\n"
            "--statistics Sum")
        
        self.add_query_section(monitoring_frame, "EC2 CPU Utilization",
            "aws cloudwatch get-metric-statistics \\\n"
            "--namespace AWS/EC2 \\\n"
            "--metric-name CPUUtilization \\\n"
            "--dimensions Name=InstanceId,Value=YOUR_INSTANCE_ID \\\n"
            "--start-time $(date -v-1H +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--end-time $(date +%Y-%m-%dT%H:%M:%SZ) \\\n"
            "--period 300 \\\n"
            "--statistics Average,Maximum")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_query_section(self, parent, title, query):
        """Add a query section with copy button"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title and copy button
        header_frame = ttk.Frame(section_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(header_frame, text=title, font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Copy", 
                  command=lambda: self.copy_to_clipboard(query)).pack(side=tk.RIGHT)
        
        # Query text
        query_text = tk.Text(section_frame, height=len(query.split('\n')), wrap=tk.WORD, 
                            font=("Consolas", 10), state=tk.DISABLED)
        query_text.pack(fill=tk.X, pady=(0, 5))
        
        # Insert query text
        query_text.config(state=tk.NORMAL)
        query_text.insert(1.0, query)
        query_text.config(state=tk.DISABLED)
        
        # Apply theme
        if self.dark_mode:
            query_text.configure(bg="#2d2d2d", fg="#e6e6e6")
        else:
            query_text.configure(bg="#f8f8f8", fg="#000000")
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()  # Required for clipboard to work
        
        # Show brief confirmation
        messagebox.showinfo("Copied", "Query copied to clipboard!")
    
    def create_settings_tab(self, parent):
        """Create the settings tab"""
        self.settings_frame = ttk.Frame(parent)
        parent.add(self.settings_frame, text="Settings")
        
        # Main container
        main_frame = ttk.Frame(self.settings_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_frame, text="Application Settings", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Reminder settings
        reminder_frame = ttk.LabelFrame(main_frame, text="Reminder Settings", padding="10")
        reminder_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Reminder interval
        interval_frame = ttk.Frame(reminder_frame)
        interval_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(interval_frame, text="Reminder Interval (hours):").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value=str(self.reminder_manager.get_interval()))
        interval_spinbox = ttk.Spinbox(interval_frame, from_=1, to=24, width=5, 
                                      textvariable=self.interval_var, 
                                      command=self.on_interval_changed)
        interval_spinbox.pack(side=tk.LEFT, padx=(10, 5))
        interval_spinbox.bind('<Return>', lambda e: self.on_interval_changed())
        interval_spinbox.bind('<FocusOut>', lambda e: self.on_interval_changed())
        
        # Reminder status
        status_frame = ttk.Frame(reminder_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.reminder_status_var = tk.StringVar(value="Stopped")
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_frame, textvariable=self.reminder_status_var)
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Reminder controls
        control_frame = ttk.Frame(reminder_frame)
        control_frame.pack(fill=tk.X)
        
        self.start_button = ttk.Button(control_frame, text="Start Reminders", 
                                      command=self.start_reminders)
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = ttk.Button(control_frame, text="Stop Reminders", 
                                     command=self.stop_reminders, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(control_frame, text="Test Reminder", 
                  command=self.test_reminder).pack(side=tk.LEFT)
        
        # Theme toggle
        theme_frame = ttk.LabelFrame(main_frame, text="Appearance", padding="10")
        theme_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(theme_frame, text="Toggle Light/Dark Mode", 
                  command=self.toggle_theme).pack(side=tk.LEFT)
        
        # Info
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="10")
        info_frame.pack(fill=tk.X)
        
        info_text = ("• Reminders will appear every 2 hours when active\n"
                    "• You can snooze reminders for 10 minutes\n"
                    "• Data is stored locally in your home directory\n"
                    "• Use 'Test Reminder' to see how notifications work")
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
    
    def create_evidence_pack_tab(self, parent):
        """Create the Evidence Pack Generator tab"""
        if not EVIDENCE_PACK_AVAILABLE:
            return
            
        try:
            # Set customtkinter appearance to match the current theme
            if self.dark_mode:
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
            
            # Create tab frame
            self.evidence_frame = ttk.Frame(parent)
            parent.add(self.evidence_frame, text="Evidence Pack Generator")
            
            # Create the Evidence Pack generator inside the ttk frame
            self.evidence_pack = EvidencePackTab(self.evidence_frame)
            self.evidence_pack.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            print(f"Error creating Evidence Pack tab: {e}")
            # If there's an error, create a simple error message tab
            error_frame = ttk.Frame(parent)
            parent.add(error_frame, text="Evidence Pack (Error)")
            
            error_label = ttk.Label(error_frame, 
                                  text=f"Evidence Pack Generator unavailable:\n{str(e)}\n\nPlease install: pip install customtkinter pyperclip",
                                  justify=tk.CENTER)
            error_label.pack(expand=True)
    
    def setup_reminder_system(self):
        """Setup the reminder system callbacks"""
        self.reminder_manager.set_reminder_callback(self.on_reminder_triggered)
    
    def set_current_datetime(self):
        """Set the datetime field to current date and time"""
        current_dt = datetime.datetime.now()
        self.datetime_var.set(current_dt.strftime("%Y-%m-%d %H:%M:%S"))
    
    def clear_form(self):
        """Clear the entry form"""
        self.set_current_datetime()
        self.outcome_combo.set(CHECK_OUTCOMES[0])
        self.notes_text.delete(1.0, tk.END)
    
    def save_check(self):
        """Save the current check entry"""
        try:
            # Parse datetime
            datetime_str = self.datetime_var.get().strip()
            if not datetime_str:
                messagebox.showerror("Error", "Please enter a date and time")
                return
            
            try:
                check_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Error", "Invalid date/time format. Use: YYYY-MM-DD HH:MM:SS")
                return
            
            # Get outcome
            outcome = self.outcome_var.get()
            if not outcome:
                messagebox.showerror("Error", "Please select an outcome")
                return
            
            # Get notes
            notes = self.notes_text.get(1.0, tk.END).strip()
            
            # Save to database
            record_id = self.db.add_check_record(outcome, notes, check_datetime)
            
            if record_id:
                messagebox.showinfo("Success", "Check record saved successfully!")
                self.clear_form()
                self.refresh_history()
            else:
                messagebox.showerror("Error", "Failed to save check record")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving check: {str(e)}")
    
    def refresh_history(self):
        """Refresh the history list"""
        try:
            # Clear existing items
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Get recent records
            records = self.db.get_check_records(limit=100)
            
            # Add records to tree
            for record in records:
                # Format datetime
                dt = datetime.datetime.fromisoformat(record['timestamp'])
                dt_str = dt.strftime("%Y-%m-%d %H:%M")
                
                # Truncate notes for display
                notes = record['notes'] or ""
                if len(notes) > 50:
                    notes = notes[:47] + "..."
                
                self.history_tree.insert("", tk.END, values=(record['id'], dt_str, record['outcome'], notes))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading history: {str(e)}")
    
    def export_to_csv(self):
        """Export history to CSV file"""
        try:
            from tkinter import filedialog
            
            # Ask user where to save the file
            filename = filedialog.asksaveasfilename(
                title="Export History to CSV",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"aws_log_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if filename:
                # Export to CSV using database manager
                if self.db.export_to_csv(filename):
                    messagebox.showinfo("Success", f"History exported successfully to:\n{filename}")
                else:
                    messagebox.showerror("Error", "Failed to export history to CSV")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting to CSV: {str(e)}")
    
    def delete_selected_record(self):
        """Delete the selected record(s) from history"""
        selected_items = self.history_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No records selected")
            return
        
        # Get count for confirmation message
        count = len(selected_items)
        if count == 1:
            confirm_msg = "Are you sure you want to delete this record?"
        else:
            confirm_msg = f"Are you sure you want to delete these {count} records?"
        
        confirm = messagebox.askyesno("Confirm Delete", confirm_msg)
        if confirm:
            try:
                deleted_count = 0
                for item_id in selected_items:
                    item = self.history_tree.item(item_id)
                    record_id = item['values'][0]
                    if self.db.delete_check_record(record_id):
                        deleted_count += 1
                
                self.refresh_history()
                if deleted_count == count:
                    if count == 1:
                        messagebox.showinfo("Success", "Record deleted successfully")
                    else:
                        messagebox.showinfo("Success", f"{deleted_count} records deleted successfully")
                else:
                    messagebox.showwarning("Partial Success", 
                                         f"Deleted {deleted_count} of {count} records. Some records may not have been found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting records: {str(e)}")
    
    def on_history_double_click(self, event):
        """Handle double-click on history item"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            values = item['values']
            
            # Show detailed view
            detail_window = tk.Toplevel(self.root)
            detail_window.title("Check Details")
            detail_window.geometry("400x300")
            detail_window.resizable(False, False)
            
            # Details
            frame = ttk.Frame(detail_window, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="Date/Time:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
            ttk.Label(frame, text=values[1]).pack(anchor=tk.W, pady=(0, 10))
            
            ttk.Label(frame, text="Outcome:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
            ttk.Label(frame, text=values[2]).pack(anchor=tk.W, pady=(0, 10))
            
            ttk.Label(frame, text="Notes:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
            notes_text = scrolledtext.ScrolledText(frame, height=8, wrap=tk.WORD, state=tk.DISABLED)
            notes_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            # Insert full notes (we need to get this from DB)
            # For now, show what we have
            notes_text.config(state=tk.NORMAL)
            notes_text.insert(1.0, values[3])
            notes_text.config(state=tk.DISABLED)
            
            # Apply theme to this window's ScrolledText
            if self.dark_mode:
                notes_text.configure(bg="#3c4043", fg="#e6e6e6")
            else:
                notes_text.configure(bg="#ffffff", fg="#000000")
            
            ttk.Button(frame, text="Close", command=detail_window.destroy).pack()
    
    def start_reminders(self):
        """Start the reminder system"""
        self.reminder_manager.start()
        self.reminder_status_var.set("Running")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
    
    def stop_reminders(self):
        """Stop the reminder system"""
        self.reminder_manager.stop()
        self.reminder_status_var.set("Stopped")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def test_reminder(self):
        """Test the reminder system"""
        self.reminder_manager.test_reminder()
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.setup_theme()
        
        # Update customtkinter theme if Evidence Pack is available
        if EVIDENCE_PACK_AVAILABLE:
            try:
                if self.dark_mode:
                    ctk.set_appearance_mode("dark")
                else:
                    ctk.set_appearance_mode("light")
            except Exception as e:
                print(f"Error updating customtkinter theme: {e}")
    
    def on_interval_changed(self):
        """Handle changes to the reminder interval"""
        try:
            interval = int(self.interval_var.get())
            self.reminder_manager.set_interval(interval)
        except ValueError:
            messagebox.showerror("Error", "Invalid interval value. Please enter a number between 1 and 24.")
    
    def on_reminder_triggered(self):
        """Handle when user responds to a reminder by wanting to log a check"""
        # Switch to the log entry tab
        # Find the notebook and select the first tab
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Notebook):
                widget.select(0)  # Select first tab (Log Check)
                break
        
        # Bring window to front
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_reminders()
        self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()