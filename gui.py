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
        self.create_settings_tab(notebook)
    
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
    
    def delete_selected_record(self):
        """Delete the selected record from history"""
        selected_item = self.history_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No record selected")
            return
        
        item = self.history_tree.item(selected_item[0])
        record_id = item['values'][0]
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if confirm:
            try:
                self.db.delete_check_record(record_id)
                self.refresh_history()
                messagebox.showinfo("Success", "Record deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting record: {str(e)}")
    
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