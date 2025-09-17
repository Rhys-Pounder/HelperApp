"""
Integration example for adding the Evidence Pack Generator tab to the existing AWS Log Checker Helper application.

This file shows how to modify your existing GUI to include the new Evidence Pack tab.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from evidence_pack_tab import EvidencePackTab


class IntegratedMainWindow:
    """
    Example of how to integrate the Evidence Pack Generator with your existing application.
    This shows a hybrid approach using both tkinter/ttk and customtkinter.
    """
    
    def __init__(self):
        # Your existing initialization code would go here
        self.setup_integrated_ui()
    
    def setup_integrated_ui(self):
        """
        Set up the integrated UI with both existing tabs and the new Evidence Pack tab.
        This example shows how to add a customtkinter tab to your existing tabview.
        """
        
        # Option 1: Add to existing ttk.Notebook
        # If you want to keep your existing ttk interface and just add the Evidence Pack tab
        
        # Create main window (your existing setup)
        self.root = tk.Tk()
        self.root.title("AWS Log Checker Helper - With Evidence Pack")
        self.root.geometry("1000x800")
        
        # Your existing notebook/tabview
        self.notebook = ttk.Notebook(self.root)
        
        # Your existing tabs would be added here
        # existing_tab1 = ttk.Frame(self.notebook)
        # self.notebook.add(existing_tab1, text="Log Checker")
        
        # Add the Evidence Pack tab
        evidence_frame = ttk.Frame(self.notebook)
        self.notebook.add(evidence_frame, text="Evidence Pack Generator")
        
        # Create the Evidence Pack generator inside the ttk frame
        self.evidence_pack = EvidencePackTab(evidence_frame)
        self.evidence_pack.pack(fill="both", expand=True)
        
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    def run(self):
        """Start the application"""
        # Set customtkinter appearance for the Evidence Pack tab
        ctk.set_appearance_mode("dark")  # or "light" to match your theme
        ctk.set_default_color_theme("blue")
        
        self.root.mainloop()


class FullCustomTkinterApp:
    """
    Alternative approach: Convert the entire application to use customtkinter.
    This provides a more consistent modern UI experience.
    """
    
    def __init__(self):
        # Set customtkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("AWS Log Checker Helper - Modern UI")
        self.root.geometry("1200x800")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the full customtkinter UI"""
        
        # Create main tabview
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add your existing tabs (would need to be converted to customtkinter)
        log_checker_tab = self.tabview.add("Log Checker")
        self.setup_log_checker_tab(log_checker_tab)
        
        # Add other existing tabs...
        # history_tab = self.tabview.add("History")
        # settings_tab = self.tabview.add("Settings")
        
        # Add the Evidence Pack tab
        evidence_tab = self.tabview.add("Evidence Pack Generator")
        self.evidence_pack = EvidencePackTab(evidence_tab)
        self.evidence_pack.pack(fill="both", expand=True)
    
    def setup_log_checker_tab(self, tab_frame):
        """
        Example of how you might convert your existing log checker tab to customtkinter.
        This is just a placeholder - you would adapt your existing functionality.
        """
        
        # Title
        title = ctk.CTkLabel(tab_frame, text="AWS Log Checker", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Your existing log checker widgets would be converted here
        # For example:
        check_frame = ctk.CTkFrame(tab_frame)
        check_frame.pack(fill="x", padx=20, pady=10)
        
        # Example widgets (replace with your actual functionality)
        ctk.CTkLabel(check_frame, text="Log File Path:").pack(pady=5, anchor="w", padx=20)
        path_entry = ctk.CTkEntry(check_frame, width=400)
        path_entry.pack(pady=5, padx=20, anchor="w")
        
        check_button = ctk.CTkButton(check_frame, text="Check Logs", width=150)
        check_button.pack(pady=10, padx=20, anchor="w")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


# Demo function to show the Evidence Pack tab in isolation
def demo_evidence_pack_only():
    """
    Simple demo to test just the Evidence Pack Generator tab
    """
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Evidence Pack Generator - Standalone Demo")
    root.geometry("900x700")
    
    # Create the Evidence Pack tab directly
    evidence_pack = EvidencePackTab(root)
    evidence_pack.pack(fill="both", expand=True, padx=10, pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    # Choose which demo to run:
    
    # Option 1: Standalone Evidence Pack demo
    demo_evidence_pack_only()
    
    # Option 2: Integrated with existing ttk interface
    # app = IntegratedMainWindow()
    # app.run()
    
    # Option 3: Full customtkinter conversion
    # app = FullCustomTkinterApp()
    # app.run()
