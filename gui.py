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
    print("Successfully imported customtkinter and evidence_pack_tab")
except ImportError as e:
    EVIDENCE_PACK_AVAILABLE = False
    print(f"Warning: Evidence Pack Generator not available: {e}")
except Exception as e:
    EVIDENCE_PACK_AVAILABLE = False
    print(f"Error loading Evidence Pack Generator: {e}")


class ModernFrame(tk.Frame):
    """Custom frame with modern styling"""
    def __init__(self, parent, bg_color="#2d2d2d", corner_radius=10, **kwargs):
        super().__init__(parent, bg=bg_color, relief="flat", bd=0, **kwargs)
        self.bg_color = bg_color
        self.corner_radius = corner_radius


class ModernButton(tk.Button):
    """Custom button with modern styling"""
    def __init__(self, parent, **kwargs):
        # Set default modern styling
        style_kwargs = {
            'bg': '#4f8cff',
            'fg': '#ffffff',
            'relief': 'flat',
            'bd': 0,
            'font': ('Segoe UI', 11),
            'cursor': 'hand2',
            'activebackground': '#3465a4',
            'activeforeground': '#ffffff'
        }
        style_kwargs.update(kwargs)
        super().__init__(parent, **style_kwargs)


class ModernEntry(tk.Entry):
    """Custom entry with modern styling"""
    def __init__(self, parent, **kwargs):
        style_kwargs = {
            'bg': '#3c4043',
            'fg': '#e6e6e6',
            'relief': 'flat',
            'bd': 1,
            'font': ('Segoe UI', 11),
            'insertbackground': '#e6e6e6',
            'highlightthickness': 1,
            'highlightcolor': '#4f8cff',
            'highlightbackground': '#2d2d2d'
        }
        style_kwargs.update(kwargs)
        super().__init__(parent, **style_kwargs)


class ModernLabel(tk.Label):
    """Custom label with modern styling"""
    def __init__(self, parent, **kwargs):
        style_kwargs = {
            'bg': '#2d2d2d',
            'fg': '#e6e6e6',
            'font': ('Segoe UI', 11)
        }
        style_kwargs.update(kwargs)
        super().__init__(parent, **style_kwargs)


class ModernText(scrolledtext.ScrolledText):
    """Custom text widget with modern styling"""
    def __init__(self, parent, **kwargs):
        style_kwargs = {
            'bg': '#3c4043',
            'fg': '#e6e6e6',
            'relief': 'flat',
            'bd': 1,
            'font': ('Segoe UI', 11),
            'insertbackground': '#e6e6e6',
            'selectbackground': '#4f8cff',
            'selectforeground': '#ffffff'
        }
        style_kwargs.update(kwargs)
        super().__init__(parent, **style_kwargs)


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.db = DatabaseManager()
        self.reminder_manager = ReminderManager(self.root)
        self.dark_mode = True  # Start with dark mode
        self.setup_modern_theme()  # Use modern theme
        self.setup_window()
        self.create_widgets()
        self.setup_reminder_system()
        self.refresh_history()
    
    def setup_modern_theme(self):
        """Set modern dark theme with rounded corners and custom styling"""
        # Modern color scheme
        self.colors = {
            'bg': '#23272e',
            'card_bg': '#2d2d2d',
            'input_bg': '#3c4043',
            'accent': '#4f8cff',
            'text': '#e6e6e6',
            'text_secondary': '#b3b3b3',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles for modern look
        style = ttk.Style(self.root)
        style.theme_use('clam')
        
        # Configure ttk styles to match modern theme
        style.configure('.', background=self.colors['card_bg'], foreground=self.colors['text'], 
                       font=('Segoe UI', 11))
        style.configure('TLabel', background=self.colors['card_bg'], foreground=self.colors['text'])
        style.configure('TFrame', background=self.colors['card_bg'], relief='flat', borderwidth=0)
        style.configure('TLabelframe', background=self.colors['card_bg'], foreground=self.colors['text'],
                       relief='flat', borderwidth=1)
        style.configure('TLabelframe.Label', background=self.colors['card_bg'], 
                       foreground=self.colors['text'])
        style.configure('TButton', background=self.colors['accent'], foreground=self.colors['text'],
                       relief='flat', borderwidth=0, padding=[12, 8])
        style.configure('TNotebook', background=self.colors['bg'], borderwidth=0, tabmargins=[0, 5, 0, 0])
        style.configure('TNotebook.Tab', background=self.colors['card_bg'], foreground=self.colors['text'], 
                       padding=[20, 12], borderwidth=0)
        style.configure('TEntry', background=self.colors['input_bg'], foreground=self.colors['text'], 
                       insertcolor=self.colors['text'], fieldbackground=self.colors['input_bg'], 
                       borderwidth=1, relief='flat')
        style.configure('TCombobox', background=self.colors['input_bg'], foreground=self.colors['text'], 
                       selectbackground=self.colors['accent'], selectforeground=self.colors['text'], 
                       fieldbackground=self.colors['input_bg'], borderwidth=1, relief='flat')
        style.configure('TSpinbox', background=self.colors['input_bg'], foreground=self.colors['text'], 
                       insertcolor=self.colors['text'], fieldbackground=self.colors['input_bg'], 
                       borderwidth=1, relief='flat')
        style.configure('Treeview', background=self.colors['input_bg'], foreground=self.colors['text'], 
                       fieldbackground=self.colors['input_bg'], borderwidth=0)
        style.configure('Treeview.Heading', background=self.colors['card_bg'], 
                       foreground=self.colors['text'], borderwidth=0, relief='flat')
        
        # Configure style mappings for hover effects
        style.map('TButton', 
                 background=[('active', '#3465a4'), ('pressed', '#2851a3')])
        style.map('TNotebook.Tab', 
                 background=[('selected', self.colors['accent']), ('active', '#3465a4')])
        style.map('TEntry', 
                 fieldbackground=[('readonly', self.colors['input_bg']), ('focus', self.colors['input_bg'])])
        style.map('TCombobox', 
                 fieldbackground=[('readonly', self.colors['input_bg']), ('focus', self.colors['input_bg'])])
        
        # Set default font
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=11)
        self.root.option_add("*Font", default_font)
    
    def create_modern_section(self, parent, title, content_height=None):
        """Create a modern section with title and content area"""
        # Section container
        section_frame = ModernFrame(parent, bg_color=self.colors['card_bg'])
        section_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Title
        title_label = ModernLabel(section_frame, text=title, 
                                 font=('Segoe UI', 16, 'bold'),
                                 bg=self.colors['card_bg'])
        title_label.pack(pady=(20, 15), padx=20, anchor="w")
        
        # Content frame
        content_frame = ModernFrame(section_frame, bg_color=self.colors['card_bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        return section_frame, content_frame
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_container = ModernFrame(self.root, bg_color=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # App title
        app_title = ModernLabel(main_container, text="AWS Log Checker Helper", 
                               font=('Segoe UI', 24, 'bold'),
                               bg=self.colors['bg'])
        app_title.pack(pady=(20, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Create tabs
        self.create_entry_tab(self.notebook)
        self.create_history_tab(self.notebook)
        self.create_queries_tab(self.notebook)
        self.create_evidence_tab(self.notebook)
        self.create_settings_tab(self.notebook)
    
    def on_tab_changed(self, event):
        """Handle tab change events to ensure proper content loading"""
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        
        # Force canvas updates based on which tab is selected
        self.root.after(1, self.refresh_current_tab_content)
    
    def refresh_current_tab_content(self):
        """Refresh the content of the currently selected tab"""
        try:
            current_tab = self.notebook.select()
            tab_text = self.notebook.tab(current_tab, "text")
            
            # Update scrollregion for each tab's canvas
            if "📝 Log Check" in tab_text and hasattr(self, 'entry_canvas'):
                self.entry_canvas.configure(scrollregion=self.entry_canvas.bbox("all"))
                self.entry_canvas.update_idletasks()
            elif "🔍 AWS Queries" in tab_text and hasattr(self, 'queries_canvas'):
                self.queries_canvas.configure(scrollregion=self.queries_canvas.bbox("all"))
                self.queries_canvas.update_idletasks()
            elif "⚙️ Settings" in tab_text and hasattr(self, 'settings_canvas'):
                self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox("all"))
                self.settings_canvas.update_idletasks()
            elif "📊 History" in tab_text:
                # Refresh history data when tab is selected
                self.refresh_history()
            elif "📋 Evidence Pack" in tab_text and hasattr(self, 'evidence_pack_generator'):
                # Force immediate refresh and update of the Evidence Pack tab
                self.evidence_pack_generator.force_update()
        except Exception as e:
            print(f"Error refreshing tab content: {e}")
    
    def create_entry_tab(self, parent):
        """Create the log entry tab with modern styling"""
        self.entry_frame = ModernFrame(parent, bg_color=self.colors['bg'])
        parent.add(self.entry_frame, text="📝 Log Check")
        
        # Create scrollable content
        canvas = tk.Canvas(self.entry_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.entry_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ModernFrame(canvas, bg_color=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enhanced mousewheel scrolling for macOS
        def _on_mousewheel(event):
            if hasattr(event, 'delta') and event.delta:
                # Windows/macOS with delta
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif hasattr(event, 'num'):
                # Linux scroll events
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        # Bind mousewheel to the entire tab area
        def bind_mousewheel_to_all(widget):
            try:
                widget.bind("<MouseWheel>", _on_mousewheel, add=True)
                widget.bind("<Button-4>", _on_mousewheel, add=True)
                widget.bind("<Button-5>", _on_mousewheel, add=True)
                for child in widget.winfo_children():
                    bind_mousewheel_to_all(child)
            except:
                pass
        
        # Apply comprehensive mousewheel binding
        def setup_mousewheel():
            bind_mousewheel_to_all(self.entry_frame)
            bind_mousewheel_to_all(canvas)
            bind_mousewheel_to_all(scrollable_frame)
        
        # Entry form section
        form_section, form_content = self.create_modern_section(scrollable_frame, "Check Details")
        
        # Date and time row
        datetime_row = ModernFrame(form_content, bg_color=self.colors['card_bg'])
        datetime_row.pack(fill=tk.X, pady=10)
        
        ModernLabel(datetime_row, text="Date & Time:", bg=self.colors['card_bg']).pack(side=tk.LEFT)
        self.datetime_var = tk.StringVar()
        self.datetime_entry = ModernEntry(datetime_row, textvariable=self.datetime_var, width=20)
        self.datetime_entry.pack(side=tk.LEFT, padx=(15, 10))
        
        now_btn = ModernButton(datetime_row, text="Now", command=self.set_current_datetime)
        now_btn.pack(side=tk.LEFT)
        
        # Outcome row
        outcome_row = ModernFrame(form_content, bg_color=self.colors['card_bg'])
        outcome_row.pack(fill=tk.X, pady=10)
        
        ModernLabel(outcome_row, text="Outcome:", bg=self.colors['card_bg']).pack(side=tk.LEFT)
        self.outcome_var = tk.StringVar()
        self.outcome_combo = ttk.Combobox(outcome_row, textvariable=self.outcome_var,
                                         values=CHECK_OUTCOMES, state="readonly", width=20)
        self.outcome_combo.pack(side=tk.LEFT, padx=(15, 0))
        self.outcome_combo.set(CHECK_OUTCOMES[0])
        
        # Notes section
        notes_label = ModernLabel(form_content, text="Notes:", bg=self.colors['card_bg'])
        notes_label.pack(anchor=tk.W, pady=(15, 5))
        
        self.notes_text = ModernText(form_content, height=6, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Buttons row
        button_row = ModernFrame(form_content, bg_color=self.colors['card_bg'])
        button_row.pack(fill=tk.X, pady=(10, 0))
        
        # Create buttons with explicit styling to override macOS defaults
        save_btn = tk.Button(button_row, 
                            text="💾 Save Check", 
                            command=self.save_check,
                            bg=self.colors['success'], 
                            fg='#ffffff',
                            activebackground='#218838', 
                            activeforeground='#ffffff',
                            relief='flat',
                            bd=0,
                            font=('Segoe UI', 11),
                            cursor='hand2',
                            padx=15,
                            pady=8)
        save_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        clear_btn = tk.Button(button_row, 
                             text="🗑️ Clear Form", 
                             command=self.clear_form,
                             bg=self.colors['danger'], 
                             fg='#ffffff',
                             activebackground='#c82333', 
                             activeforeground='#ffffff',
                             relief='flat',
                             bd=0,
                             font=('Segoe UI', 11),
                             cursor='hand2',
                             padx=15,
                             pady=8)
        clear_btn.pack(side=tk.LEFT)
        
        # Pack scrollable content
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initialize with current date/time
        self.set_current_datetime()
        
        # Store canvas reference for tab refresh
        self.entry_canvas = canvas
        
        # Force initial update and ensure proper scrolling setup
        def setup_scrolling():
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.update_idletasks()
            setup_mousewheel()
        
        self.root.after(50, setup_scrolling)
    
    def create_history_tab(self, parent):
        """Create the history viewing tab with modern styling"""
        self.history_frame = ModernFrame(parent, bg_color=self.colors['bg'])
        parent.add(self.history_frame, text="📊 History")
        
        # History section
        history_section, history_content = self.create_modern_section(self.history_frame, "Check History")
        
        # Controls row
        controls_row = ModernFrame(history_content, bg_color=self.colors['card_bg'])
        controls_row.pack(fill=tk.X, pady=(0, 15))
        
        export_btn = ModernButton(controls_row, text="📤 Export CSV", command=self.export_to_csv)
        export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_btn = ModernButton(controls_row, text="🗑️ Delete Selected", 
                                 command=self.delete_selected_record, bg=self.colors['danger'])
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_btn = ModernButton(controls_row, text="🔄 Refresh", command=self.refresh_history)
        refresh_btn.pack(side=tk.LEFT)
        
        # History list container
        list_container = ModernFrame(history_content, bg_color=self.colors['input_bg'])
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for history
        columns = ("ID", "Date/Time", "Outcome", "Notes")
        self.history_tree = ttk.Treeview(list_container, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.history_tree.heading("ID", text="ID")
        self.history_tree.heading("Date/Time", text="Date/Time")
        self.history_tree.heading("Outcome", text="Outcome")
        self.history_tree.heading("Notes", text="Notes")
        
        self.history_tree.column("ID", width=60)
        self.history_tree.column("Date/Time", width=180)
        self.history_tree.column("Outcome", width=150)
        self.history_tree.column("Notes", width=300)
        
        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0, 10))
        
        # Bind double-click to view details
        self.history_tree.bind("<Double-1>", self.on_history_double_click)
    
    def create_queries_tab(self, parent):
        """Create the AWS queries tab with modern styling"""
        self.queries_frame = ModernFrame(parent, bg_color=self.colors['bg'])
        parent.add(self.queries_frame, text="🔍 AWS Queries")
        
        # Create scrollable frame
        canvas = tk.Canvas(self.queries_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.queries_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ModernFrame(canvas, bg_color=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enhanced mousewheel scrolling for macOS
        def _on_mousewheel(event):
            if hasattr(event, 'delta') and event.delta:
                # Windows/macOS with delta
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif hasattr(event, 'num'):
                # Linux scroll events
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        # Bind mousewheel to the entire tab area
        def bind_mousewheel_to_all(widget):
            try:
                widget.bind("<MouseWheel>", _on_mousewheel, add=True)
                widget.bind("<Button-4>", _on_mousewheel, add=True)
                widget.bind("<Button-5>", _on_mousewheel, add=True)
                for child in widget.winfo_children():
                    bind_mousewheel_to_all(child)
            except:
                pass
        
        # Apply comprehensive mousewheel binding
        def setup_mousewheel():
            bind_mousewheel_to_all(self.queries_frame)
            bind_mousewheel_to_all(canvas)
            bind_mousewheel_to_all(scrollable_frame)
        
        # CloudWatch Insights Queries
        insights_section, insights_content = self.create_modern_section(scrollable_frame, "CloudWatch Insights Queries")
        
        self.add_modern_query_section(insights_content, "🔴 Error Detection", 
            "fields @timestamp, @message\n"
            "| filter @message like /(?i)(error|exception|fail|failed)/\n"
            "| sort @timestamp desc\n"
            "| limit 10")
        
        self.add_modern_query_section(insights_content, "⚡ Performance Issues", 
            "fields @timestamp, @message, elapsed_ms\n"
            "| filter ispresent(elapsed_ms)\n"
            "| sort elapsed_ms desc\n"
            "| limit 10")
        
        self.add_modern_query_section(insights_content, "💾 Memory Usage", 
            "fields @timestamp, @message\n"
            "| filter @message like /memory/\n"
            "| sort @timestamp desc\n"
            "| limit 10")
        
        # AWS CLI Commands
        cli_section, cli_content = self.create_modern_section(scrollable_frame, "AWS CLI Commands")
        
        self.add_modern_query_section(cli_content, "🔐 CloudTrail Failed Logins",
            "aws logs start-query \\\n"
            "--log-group-name YOUR_CLOUDTRAIL_LOG_GROUP \\\n"
            "--start-time $(date -v-2H +%s) \\\n"
            "--end-time $(date +%s) \\\n"
            '--query-string "fields @timestamp, @message | filter eventName = \'ConsoleLogin\' and errorMessage = \'Failed authentication\'"')
        
        self.add_modern_query_section(cli_content, "🖥️ SSM Session History",
            "aws ssm describe-sessions \\\n"
            '--state "History" \\\n'
            "--filters key=Owner,value=* \\\n"
            '--query "Sessions[?StartDate>=`date -v-2H +%Y-%m-%dT%H:%M:%SZ`].[SessionId,Owner,StartDate]" \\\n'
            "--output table")
        
        # Apply mousewheel to new content
        bind_mousewheel_to_all(insights_content)
        bind_mousewheel_to_all(cli_content)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Store canvas reference for tab refresh
        self.queries_canvas = canvas
        
        # Force initial update and ensure proper scrolling setup
        def setup_scrolling():
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.update_idletasks()
            setup_mousewheel()
        
        self.root.after(50, setup_scrolling)
    
    def add_modern_query_section(self, parent, title, query):
        """Add a modern query section with copy button"""
        # Query container
        query_container = ModernFrame(parent, bg_color=self.colors['input_bg'])
        query_container.pack(fill=tk.X, pady=10)
        
        # Header with title and copy button
        header_frame = ModernFrame(query_container, bg_color=self.colors['input_bg'])
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        title_label = ModernLabel(header_frame, text=title, font=('Segoe UI', 12, 'bold'),
                                 bg=self.colors['input_bg'])
        title_label.pack(side=tk.LEFT)
        
        copy_btn = ModernButton(header_frame, text="📋 Copy", 
                               command=lambda: self.copy_to_clipboard(query),
                               bg=self.colors['success'])
        copy_btn.pack(side=tk.RIGHT)
        
        # Query text
        query_text = tk.Text(query_container, height=len(query.split('\n')), wrap=tk.WORD,
                           font=('Consolas', 10), state=tk.DISABLED,
                           bg=self.colors['card_bg'], fg=self.colors['text'],
                           relief='flat', bd=0)
        query_text.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Insert query text
        query_text.config(state=tk.NORMAL)
        query_text.insert(1.0, query)
        query_text.config(state=tk.DISABLED)
    
    def create_evidence_tab(self, parent):
        """Create the evidence pack tab with modern styling"""
        if EVIDENCE_PACK_AVAILABLE:
            # Use CustomTkinter for the evidence pack tab
            self.evidence_frame = ctk.CTkFrame(parent, fg_color="transparent")
            parent.add(self.evidence_frame, text="📋 Evidence Pack")
            
            # Create the evidence pack generator
            self.evidence_pack_generator = EvidencePackTab(self.evidence_frame)
            self.evidence_pack_generator.pack(fill="both", expand=True)
        else:
            # Fallback message if customtkinter is not available
            self.evidence_frame = ModernFrame(parent, bg_color=self.colors['bg'])
            parent.add(self.evidence_frame, text="📋 Evidence Pack")
            
            unavailable_section, unavailable_content = self.create_modern_section(
                self.evidence_frame, "Evidence Pack Generator"
            )
            
            message_label = ModernLabel(
                unavailable_content,
                text="Evidence Pack Generator is not available.\n\n"
                     "To enable this feature, please install the required dependencies:\n"
                     "pip install customtkinter pyperclip",
                font=('Segoe UI', 12),
                justify=tk.CENTER,
                bg=self.colors['card_bg']
            )
            message_label.pack(pady=50, padx=20)
    
    def create_settings_tab(self, parent):
        """Create the settings tab with modern styling"""
        self.settings_frame = ModernFrame(parent, bg_color=self.colors['bg'])
        parent.add(self.settings_frame, text="⚙️ Settings")
        
        # Create scrollable content
        canvas = tk.Canvas(self.settings_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ModernFrame(canvas, bg_color=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enhanced mousewheel scrolling for macOS
        def _on_mousewheel(event):
            if hasattr(event, 'delta') and event.delta:
                # Windows/macOS with delta
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif hasattr(event, 'num'):
                # Linux scroll events
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        # Bind mousewheel to the entire tab area
        def bind_mousewheel_to_all(widget):
            try:
                widget.bind("<MouseWheel>", _on_mousewheel, add=True)
                widget.bind("<Button-4>", _on_mousewheel, add=True)
                widget.bind("<Button-5>", _on_mousewheel, add=True)
                for child in widget.winfo_children():
                    bind_mousewheel_to_all(child)
            except:
                pass
        
        # Apply comprehensive mousewheel binding
        def setup_mousewheel():
            bind_mousewheel_to_all(self.settings_frame)
            bind_mousewheel_to_all(canvas)
            bind_mousewheel_to_all(scrollable_frame)
        
        # Reminder Settings Section
        reminder_section, reminder_content = self.create_modern_section(scrollable_frame, "Reminder Settings")
        
        # Enable reminders checkbox
        reminder_row = ModernFrame(reminder_content, bg_color=self.colors['card_bg'])
        reminder_row.pack(fill=tk.X, pady=10)
        
        self.reminder_enabled_var = tk.BooleanVar(value=True)
        reminder_check = tk.Checkbutton(
            reminder_row,
            text="Enable automatic check reminders",
            variable=self.reminder_enabled_var,
            command=self.toggle_reminders,
            bg=self.colors['card_bg'],
            fg=self.colors['text'],
            selectcolor=self.colors['input_bg'],
            activebackground=self.colors['card_bg'],
            activeforeground=self.colors['text'],
            font=('Segoe UI', 11)
        )
        reminder_check.pack(side=tk.LEFT)
        
        # Reminder interval
        interval_row = ModernFrame(reminder_content, bg_color=self.colors['card_bg'])
        interval_row.pack(fill=tk.X, pady=10)
        
        ModernLabel(interval_row, text="Reminder interval (hours):", bg=self.colors['card_bg']).pack(side=tk.LEFT)
        self.reminder_interval_var = tk.StringVar(value="24")
        interval_spinbox = ttk.Spinbox(
            interval_row,
            from_=1, to=168, width=10,
            textvariable=self.reminder_interval_var,
            command=self.update_reminder_interval
        )
        interval_spinbox.pack(side=tk.LEFT, padx=(15, 0))
        
        # Database Settings Section
        db_section, db_content = self.create_modern_section(scrollable_frame, "Database Settings")
        
        # Database location
        db_row = ModernFrame(db_content, bg_color=self.colors['card_bg'])
        db_row.pack(fill=tk.X, pady=10)
        
        ModernLabel(db_row, text="Database location:", bg=self.colors['card_bg']).pack(side=tk.LEFT)
        db_location_label = ModernLabel(
            db_row, 
            text=self.db.db_path, 
            font=('Consolas', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['card_bg']
        )
        db_location_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Database actions
        db_actions_row = ModernFrame(db_content, bg_color=self.colors['card_bg'])
        db_actions_row.pack(fill=tk.X, pady=(15, 0))
        
        backup_btn = ModernButton(db_actions_row, text="💾 Backup Database", command=self.backup_database,
                                 bg=self.colors['accent'], fg='#ffffff')
        backup_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clean_btn = ModernButton(db_actions_row, text="🧹 Clean Old Records", 
                                command=self.clean_old_records, bg=self.colors['warning'], fg='#000000')
        clean_btn.pack(side=tk.LEFT)
        
        # Application Info Section
        info_section, info_content = self.create_modern_section(scrollable_frame, "Application Information")
        
        # Version info
        version_label = ModernLabel(
            info_content,
            text=f"{APP_NAME}\nVersion 1.0.0\n\nA tool for tracking AWS log checks and generating evidence packs.",
            justify=tk.LEFT,
            bg=self.colors['card_bg']
        )
        version_label.pack(pady=10, anchor="w")
        
        # Apply mousewheel to new content
        bind_mousewheel_to_all(reminder_content)
        bind_mousewheel_to_all(db_content)
        bind_mousewheel_to_all(info_content)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Store canvas reference for tab refresh
        self.settings_canvas = canvas
        
        # Force initial update and ensure proper scrolling setup
        def setup_scrolling():
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.update_idletasks()
            setup_mousewheel()
        
        self.root.after(50, setup_scrolling)
    
    # Event handlers and utility methods
    def set_current_datetime(self):
        """Set current date and time in the entry field"""
        now = datetime.datetime.now()
        self.datetime_var.set(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    def save_check(self):
        """Save a log check to the database"""
        try:
            # Get values
            datetime_str = self.datetime_var.get().strip()
            outcome = self.outcome_var.get()
            notes = self.notes_text.get("1.0", tk.END).strip()
            
            # Validate inputs
            if not datetime_str:
                messagebox.showerror("Error", "Please enter a date and time.")
                return
            
            if not outcome:
                messagebox.showerror("Error", "Please select an outcome.")
                return
            
            # Parse datetime
            try:
                check_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Error", "Invalid date/time format. Use YYYY-MM-DD HH:MM:SS")
                return
            
            # Save to database
            self.db.add_check(check_datetime, outcome, notes)
            
            # Refresh history and clear form
            self.refresh_history()
            self.clear_form()
            
            # Show success message
            messagebox.showinfo("Success", "Log check saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save check: {str(e)}")
    
    def clear_form(self):
        """Clear the entry form"""
        self.notes_text.delete("1.0", tk.END)
        self.outcome_combo.set(CHECK_OUTCOMES[0])
        self.set_current_datetime()
    
    def refresh_history(self):
        """Refresh the history display"""
        try:
            # Clear existing items
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Get and display records
            records = self.db.get_all_checks()
            for record in records:
                self.history_tree.insert("", "end", values=record)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh history: {str(e)}")
    
    def on_history_double_click(self, event):
        """Handle double-click on history item"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            values = item['values']
            
            # Show details in a popup
            self.show_check_details(values)
    
    def show_check_details(self, record):
        """Show detailed view of a check record"""
        details_window = tk.Toplevel(self.root)
        details_window.title("Check Details")
        details_window.geometry("500x400")
        details_window.configure(bg=self.colors['bg'])
        details_window.transient(self.root)
        details_window.grab_set()
        
        # Content frame
        content_frame = ModernFrame(details_window, bg_color=self.colors['card_bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ModernLabel(content_frame, text="Check Details", 
                                 font=('Segoe UI', 16, 'bold'), bg=self.colors['card_bg'])
        title_label.pack(pady=(10, 20))
        
        # Details
        details = [
            ("ID:", record[0]),
            ("Date/Time:", record[1]),
            ("Outcome:", record[2])
        ]
        
        for label, value in details:
            row = ModernFrame(content_frame, bg_color=self.colors['card_bg'])
            row.pack(fill=tk.X, pady=5)
            
            ModernLabel(row, text=label, font=('Segoe UI', 11, 'bold'), 
                       bg=self.colors['card_bg']).pack(side=tk.LEFT)
            ModernLabel(row, text=str(value), bg=self.colors['card_bg']).pack(side=tk.LEFT, padx=(10, 0))
        
        # Notes section
        notes_label = ModernLabel(content_frame, text="Notes:", font=('Segoe UI', 11, 'bold'),
                                 bg=self.colors['card_bg'])
        notes_label.pack(pady=(20, 5), anchor="w")
        
        notes_text = ModernText(content_frame, height=8, wrap=tk.WORD)
        notes_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        notes_text.insert("1.0", record[3] if record[3] else "No notes")
        notes_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = ModernButton(content_frame, text="Close", command=details_window.destroy)
        close_btn.pack(pady=(10, 0))
    
    def delete_selected_record(self):
        """Delete the selected history record"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            try:
                item = self.history_tree.item(selection[0])
                record_id = item['values'][0]
                
                self.db.delete_check(record_id)
                self.refresh_history()
                
                messagebox.showinfo("Success", "Record deleted successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete record: {str(e)}")
    
    def export_to_csv(self):
        """Export history to CSV file"""
        try:
            from tkinter import filedialog
            import csv
            
            # Get file path
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export History to CSV"
            )
            
            if file_path:
                records = self.db.get_all_checks()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["ID", "Date/Time", "Outcome", "Notes"])
                    writer.writerows(records)
                
                messagebox.showinfo("Success", f"History exported to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export history: {str(e)}")
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Success", "Query copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
    
    def setup_reminder_system(self):
        """Initialize the reminder system"""
        try:
            # Set up periodic reminders
            self.reminder_manager.schedule_reminder(
                hours=int(self.reminder_interval_var.get()),
                message="Time for your regular AWS log check!"
            )
        except Exception as e:
            print(f"Warning: Could not set up reminders: {e}")
    
    def toggle_reminders(self):
        """Toggle reminder system on/off"""
        if self.reminder_enabled_var.get():
            self.setup_reminder_system()
        else:
            self.reminder_manager.cancel_reminders()
    
    def update_reminder_interval(self):
        """Update reminder interval"""
        if self.reminder_enabled_var.get():
            self.setup_reminder_system()
    
    def backup_database(self):
        """Create a backup of the database"""
        try:
            from tkinter import filedialog
            import shutil
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")],
                title="Backup Database"
            )
            
            if file_path:
                shutil.copy2(self.db.db_path, file_path)
                messagebox.showinfo("Success", f"Database backed up to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup database: {str(e)}")
    
    def clean_old_records(self):
        """Clean old records from the database"""
        try:
            # Ask for number of days
            from tkinter import simpledialog
            
            days = simpledialog.askinteger(
                "Clean Old Records",
                "Delete records older than how many days?",
                initialvalue=90,
                minvalue=1,
                maxvalue=365
            )
            
            if days:
                cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
                deleted_count = self.db.clean_old_records(cutoff_date)
                
                if deleted_count > 0:
                    self.refresh_history()
                    messagebox.showinfo("Success", f"Deleted {deleted_count} old records.")
                else:
                    messagebox.showinfo("Info", "No old records found to delete.")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clean old records: {str(e)}")
    
    def on_closing(self):
        """Handle application closing"""
        try:
            # Clean up reminders
            self.reminder_manager.cancel_reminders()
            
            # Close database connection
            self.db.close()
            
            # Destroy window
            self.root.destroy()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()


def main():
    """Main entry point"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()