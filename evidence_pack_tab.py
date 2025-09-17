"""
Evidence Pack Generator Tab for AWS Log Checker Helper Application
Uses customtkinter for modern UI components
"""

import customtkinter as ctk
import pyperclip  # For clipboard functionality
from datetime import datetime
from typing import List, Dict, Any


class EvidencePackTab(ctk.CTkFrame):
    """
    Evidence Pack Generator tab that creates Markdown-formatted reports for Slack
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
    # Store dynamic widgets for findings and recommendations
        self.findings_frames: List[ctk.CTkFrame] = []
        self.recommendations_frames: List[ctk.CTkFrame] = []
        
        # Configure the main frame
        self.configure(fg_color="transparent")
        
        # Create scrollable frame for the content
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=800, height=600)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Initialize UI components
        self.setup_widgets()
    
    def setup_widgets(self):
        """Create and arrange all UI widgets"""
        
        # Main title
        title_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text="Evidence Pack Generator", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Section 1: Executive Summary
        self.create_executive_summary_section()
        
        # Section 2: Scope of Investigation
        self.create_scope_section()
        
        # Section 3: Detailed Findings
        self.create_findings_section()
        
        # Section 4: Evidence & Analysis
        self.create_evidence_section()
        
        # Section 5: Actions & Recommendations
        self.create_recommendations_section()
        
        # Action buttons
        self.create_action_buttons()
    
    def create_executive_summary_section(self):
        """Create Executive Summary section widgets"""
        
        # Section frame
        exec_frame = ctk.CTkFrame(self.scrollable_frame)
        exec_frame.pack(fill="x", pady=10, padx=20)
        
        # Section title
        exec_title = ctk.CTkLabel(
            exec_frame, 
            text="1. Executive Summary", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        exec_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Analyst entry
        analyst_label = ctk.CTkLabel(exec_frame, text="Analyst:")
        analyst_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.analyst_entry = ctk.CTkEntry(exec_frame, width=300)
        self.analyst_entry.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Reason for scan entry
        reason_label = ctk.CTkLabel(exec_frame, text="Reason for Scan:")
        reason_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.reason_entry = ctk.CTkEntry(exec_frame, width=400)
        self.reason_entry.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Overall finding combo box
        finding_label = ctk.CTkLabel(exec_frame, text="Overall Finding:")
        finding_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.finding_combo = ctk.CTkComboBox(
            exec_frame,
            values=["Minor Anomalies Detected", "Significant Incident Identified", "No Anomalies Detected"],
            width=300
        )
        self.finding_combo.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Criticality combo box
        criticality_label = ctk.CTkLabel(exec_frame, text="Criticality:")
        criticality_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.criticality_combo = ctk.CTkComboBox(
            exec_frame,
            values=["Critical", "High", "Medium", "Low", "None"],
            width=200
        )
        self.criticality_combo.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Key takeaway text box
        takeaway_label = ctk.CTkLabel(exec_frame, text="Key Takeaway:")
        takeaway_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.takeaway_textbox = ctk.CTkTextbox(exec_frame, width=600, height=80)
        self.takeaway_textbox.pack(pady=(0, 15), padx=20, anchor="w")
    
    def create_scope_section(self):
        """Create Scope of Investigation section widgets"""
        
        # Section frame
        scope_frame = ctk.CTkFrame(self.scrollable_frame)
        scope_frame.pack(fill="x", pady=10, padx=20)
        
        # Section title
        scope_title = ctk.CTkLabel(
            scope_frame, 
            text="2. Scope of Investigation", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        scope_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Systems scanned text box
        systems_label = ctk.CTkLabel(scope_frame, text="Systems Scanned:")
        systems_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.systems_textbox = ctk.CTkTextbox(scope_frame, width=600, height=100)
        self.systems_textbox.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Log sources text box
        sources_label = ctk.CTkLabel(scope_frame, text="Log Sources Reviewed:")
        sources_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.sources_textbox = ctk.CTkTextbox(scope_frame, width=600, height=100)
        self.sources_textbox.pack(pady=(0, 15), padx=20, anchor="w")
    
    def create_findings_section(self):
        """Create Detailed Findings section widgets"""
        
        # Section frame
        self.findings_section = ctk.CTkFrame(self.scrollable_frame)
        self.findings_section.pack(fill="x", pady=10, padx=20)
        
        # Section title
        findings_title = ctk.CTkLabel(
            self.findings_section, 
            text="3. Detailed Findings", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        findings_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Container for dynamic findings
        self.findings_container = ctk.CTkFrame(self.findings_section)
        self.findings_container.pack(fill="x", pady=10, padx=20)
        
        # Add finding button
        add_finding_btn = ctk.CTkButton(
            self.findings_section,
            text="+ Add Finding",
            command=self.add_finding,
            width=150,
            height=35
        )
        add_finding_btn.pack(pady=(0, 15), padx=20, anchor="w")
    
    def create_evidence_section(self):
        """Create Evidence & Analysis section widgets"""
        
        # Section frame
        evidence_frame = ctk.CTkFrame(self.scrollable_frame)
        evidence_frame.pack(fill="x", pady=10, padx=20)
        
        # Section title
        evidence_title = ctk.CTkLabel(
            evidence_frame, 
            text="4. Evidence & Analysis", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        evidence_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Large text box for analysis
        analysis_label = ctk.CTkLabel(evidence_frame, text="Detailed Analysis & Log Snippets:")
        analysis_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.analysis_textbox = ctk.CTkTextbox(evidence_frame, width=700, height=200)
        self.analysis_textbox.pack(pady=(0, 15), padx=20, anchor="w")
    
    def create_recommendations_section(self):
        """Create Actions & Recommendations section widgets"""
        
        # Section frame
        self.recommendations_section = ctk.CTkFrame(self.scrollable_frame)
        self.recommendations_section.pack(fill="x", pady=10, padx=20)
        
        # Section title
        recommendations_title = ctk.CTkLabel(
            self.recommendations_section, 
            text="5. Actions & Recommendations", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        recommendations_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Container for dynamic recommendations
        self.recommendations_container = ctk.CTkFrame(self.recommendations_section)
        self.recommendations_container.pack(fill="x", pady=10, padx=20)
        
        # Add recommendation button
        add_recommendation_btn = ctk.CTkButton(
            self.recommendations_section,
            text="+ Add Recommendation",
            command=self.add_recommendation,
            width=200,
            height=35
        )
        add_recommendation_btn.pack(pady=(0, 15), padx=20, anchor="w")
    
    def create_action_buttons(self):
        """Create main action buttons at the bottom"""
        
        # Button frame
        button_frame = ctk.CTkFrame(self.scrollable_frame)
        button_frame.pack(fill="x", pady=20, padx=20)
        
        # Generate button
        generate_btn = ctk.CTkButton(
            button_frame,
            text="Generate Text for Slack",
            command=self.generate_markdown,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        generate_btn.pack(side="left", pady=15, padx=(20, 10))
        
        # Clear button
        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            width=150,
            height=40,
            fg_color="gray"
        )
        clear_btn.pack(side="left", pady=15, padx=10)
    
    def add_finding(self):
        """Add a new finding entry dynamically"""
        
        # Create finding frame
        finding_frame = ctk.CTkFrame(self.findings_container)
        finding_frame.pack(fill="x", pady=5, padx=10)
        
        # Finding number label
        finding_num = len(self.findings_frames) + 1
        num_label = ctk.CTkLabel(finding_frame, text=f"Finding #{finding_num}:")
        num_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        # Timestamp entry
        timestamp_label = ctk.CTkLabel(finding_frame, text="Timestamp (UTC):")
        timestamp_label.pack(pady=(5, 0), padx=10, anchor="w")
        timestamp_entry = ctk.CTkEntry(finding_frame, width=200, placeholder_text="YYYY-MM-DD HH:MM:SS")
        timestamp_entry.pack(pady=(0, 5), padx=10, anchor="w")
        
        # Severity combo box
        severity_label = ctk.CTkLabel(finding_frame, text="Severity:")
        severity_label.pack(pady=(5, 0), padx=10, anchor="w")
        severity_combo = ctk.CTkComboBox(
            finding_frame,
            values=["High", "Medium", "Low", "Info"],
            width=150
        )
        severity_combo.pack(pady=(0, 5), padx=10, anchor="w")
        
        # Description entry
        desc_label = ctk.CTkLabel(finding_frame, text="Finding Description:")
        desc_label.pack(pady=(5, 0), padx=10, anchor="w")
        desc_entry = ctk.CTkEntry(finding_frame, width=500)
        desc_entry.pack(pady=(0, 5), padx=10, anchor="w")
        
        # Source entry
        source_label = ctk.CTkLabel(finding_frame, text="Source System / Log:")
        source_label.pack(pady=(5, 0), padx=10, anchor="w")
        source_entry = ctk.CTkEntry(finding_frame, width=300)
        source_entry.pack(pady=(0, 10), padx=10, anchor="w")
        
        # Remove button
        remove_btn = ctk.CTkButton(
            finding_frame,
            text="Remove",
            command=lambda: self.remove_finding(finding_frame),
            width=80,
            height=25,
            fg_color="red"
        )
        remove_btn.pack(pady=(0, 10), padx=10, anchor="e")
        
        # Store references to the widgets
        finding_data = {
            'frame': finding_frame,
            'timestamp': timestamp_entry,
            'severity': severity_combo,
            'description': desc_entry,
            'source': source_entry
        }
        
        self.findings_frames.append(finding_data)
    
    def add_recommendation(self):
        """Add a new recommendation entry dynamically"""
        
        # Create recommendation frame
        rec_frame = ctk.CTkFrame(self.recommendations_container)
        rec_frame.pack(fill="x", pady=5, padx=10)
        
        # Recommendation number label
        rec_num = len(self.recommendations_frames) + 1
        num_label = ctk.CTkLabel(rec_frame, text=f"Recommendation #{rec_num}:")
        num_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        # Priority combo box
        priority_label = ctk.CTkLabel(rec_frame, text="Priority:")
        priority_label.pack(pady=(5, 0), padx=10, anchor="w")
        priority_combo = ctk.CTkComboBox(
            rec_frame,
            values=["High", "Medium", "Low"],
            width=150
        )
        priority_combo.pack(pady=(0, 5), padx=10, anchor="w")
        
        # Recommendation entry
        rec_label = ctk.CTkLabel(rec_frame, text="Recommendation:")
        rec_label.pack(pady=(5, 0), padx=10, anchor="w")
        rec_entry = ctk.CTkEntry(rec_frame, width=500)
        rec_entry.pack(pady=(0, 5), padx=10, anchor="w")
        
        # Owner entry
        owner_label = ctk.CTkLabel(rec_frame, text="Owner:")
        owner_label.pack(pady=(5, 0), padx=10, anchor="w")
        owner_entry = ctk.CTkEntry(rec_frame, width=200)
        owner_entry.pack(pady=(0, 10), padx=10, anchor="w")
        
        # Remove button
        remove_btn = ctk.CTkButton(
            rec_frame,
            text="Remove",
            command=lambda: self.remove_recommendation(rec_frame),
            width=80,
            height=25,
            fg_color="red"
        )
        remove_btn.pack(pady=(0, 10), padx=10, anchor="e")
        
        # Store references to the widgets
        rec_data = {
            'frame': rec_frame,
            'priority': priority_combo,
            'recommendation': rec_entry,
            'owner': owner_entry
        }
        
        self.recommendations_frames.append(rec_data)
    
    def remove_finding(self, finding_frame):
        """Remove a finding entry"""
        # Find and remove from the list
        self.findings_frames = [f for f in self.findings_frames if f['frame'] != finding_frame]
        # Destroy the frame
        finding_frame.destroy()
        # Update numbering
        self.update_finding_numbers()
    
    def remove_recommendation(self, rec_frame):
        """Remove a recommendation entry"""
        # Find and remove from the list
        self.recommendations_frames = [r for r in self.recommendations_frames if r['frame'] != rec_frame]
        # Destroy the frame
        rec_frame.destroy()
        # Update numbering
        self.update_recommendation_numbers()
    
    def update_finding_numbers(self):
        """Update finding numbers after removal"""
        for i, finding in enumerate(self.findings_frames, 1):
            # Find and update the number label
            for widget in finding['frame'].winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Finding #" in widget.cget("text"):
                    widget.configure(text=f"Finding #{i}:")
                    break
    
    def update_recommendation_numbers(self):
        """Update recommendation numbers after removal"""
        for i, rec in enumerate(self.recommendations_frames, 1):
            # Find and update the number label
            for widget in rec['frame'].winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Recommendation #" in widget.cget("text"):
                    widget.configure(text=f"Recommendation #{i}:")
                    break
    
    def generate_markdown(self):
        """Generate Markdown formatted text for Slack"""
        
        # Collect all form data
        analyst = self.analyst_entry.get().strip()
        reason = self.reason_entry.get().strip()
        finding = self.finding_combo.get()
        criticality = self.criticality_combo.get()
        takeaway = self.takeaway_textbox.get("1.0", "end-1c").strip()
        
        systems = self.systems_textbox.get("1.0", "end-1c").strip()
        sources = self.sources_textbox.get("1.0", "end-1c").strip()
        analysis = self.analysis_textbox.get("1.0", "end-1c").strip()
        
        # Build Markdown content
        markdown_content = "*Log Scan Evidence Pack*\n"
        markdown_content += "---\n"
        
        # Executive Summary
        markdown_content += "*1. Executive Summary*\n"
        if analyst:
            markdown_content += f"*Analyst:* {analyst}\n"
        if reason:
            markdown_content += f"*Reason for Scan:* {reason}\n"
        if finding:
            markdown_content += f"*Overall Finding:* {finding}\n"
        if criticality:
            markdown_content += f"*Criticality:* {criticality}\n"
        if takeaway:
            markdown_content += f"\n> {takeaway}\n"
        
        markdown_content += "\n---\n"
        
        # Scope of Investigation
        markdown_content += "*2. Scope of Investigation*\n"
        if systems:
            markdown_content += "*Systems Scanned:*\n"
            for line in systems.split('\n'):
                if line.strip():
                    markdown_content += f"- {line.strip()}\n"
            markdown_content += "\n"
        
        if sources:
            markdown_content += "*Log Sources Reviewed:*\n"
            for line in sources.split('\n'):
                if line.strip():
                    markdown_content += f"- {line.strip()}\n"
        
        markdown_content += "\n---\n"
        
        # Detailed Findings
        markdown_content += "*3. Detailed Findings*\n"
        if self.findings_frames:
            markdown_content += "| Timestamp (UTC) | Severity | Description | Source |\n"
            markdown_content += "| :--- | :--- | :--- | :--- |\n"
            
            for finding in self.findings_frames:
                timestamp = finding['timestamp'].get().strip()
                severity = finding['severity'].get()
                description = finding['description'].get().strip()
                source = finding['source'].get().strip()
                
                markdown_content += f"| {timestamp or 'N/A'} | {severity or 'N/A'} | {description or 'N/A'} | {source or 'N/A'} |\n"
        else:
            markdown_content += "No specific findings documented.\n"
        
        markdown_content += "\n---\n"
        
        # Evidence & Analysis
        if analysis:
            markdown_content += "*4. Evidence & Analysis*\n"
            markdown_content += f"{analysis}\n"
            markdown_content += "\n---\n"
        
        # Actions & Recommendations
        markdown_content += "*5. Actions & Recommendations*\n"
        if self.recommendations_frames:
            markdown_content += "| Priority | Recommendation | Owner |\n"
            markdown_content += "| :--- | :--- | :--- |\n"
            
            for rec in self.recommendations_frames:
                priority = rec['priority'].get()
                recommendation = rec['recommendation'].get().strip()
                owner = rec['owner'].get().strip()
                
                markdown_content += f"| {priority or 'N/A'} | {recommendation or 'N/A'} | {owner or 'N/A'} |\n"
        else:
            markdown_content += "No specific recommendations at this time.\n"
        
        # Copy to clipboard and print to console
        try:
            pyperclip.copy(markdown_content)
            print("Evidence Pack copied to clipboard!")
            print("\n" + "="*60)
            print("GENERATED EVIDENCE PACK:")
            print("="*60)
            print(markdown_content)
            print("="*60)
            
            # Show success message
            success_window = ctk.CTkToplevel(self)
            success_window.title("Success")
            success_window.geometry("400x150")
            success_window.transient(self)
            success_window.grab_set()
            
            success_label = ctk.CTkLabel(
                success_window, 
                text="Evidence Pack generated successfully!\nContent copied to clipboard.",
                font=ctk.CTkFont(size=14)
            )
            success_label.pack(pady=40)
            
            ok_btn = ctk.CTkButton(
                success_window,
                text="OK",
                command=success_window.destroy,
                width=100
            )
            ok_btn.pack(pady=10)
            
        except Exception as e:
            print(f"Error generating evidence pack: {e}")
            # Show error message
            error_window = ctk.CTkToplevel(self)
            error_window.title("Error")
            error_window.geometry("400x150")
            error_window.transient(self)
            error_window.grab_set()
            
            error_label = ctk.CTkLabel(
                error_window, 
                text=f"Error generating evidence pack:\n{str(e)}",
                font=ctk.CTkFont(size=14)
            )
            error_label.pack(pady=40)
            
            ok_btn = ctk.CTkButton(
                error_window,
                text="OK",
                command=error_window.destroy,
                width=100
            )
            ok_btn.pack(pady=10)
    
    def clear_form(self):
        """Clear all form fields and remove dynamic entries"""
        
        # Clear basic entries
        self.analyst_entry.delete(0, "end")
        self.reason_entry.delete(0, "end")
        
        # Reset combo boxes
        self.finding_combo.set("")
        self.criticality_combo.set("")
        
        # Clear text boxes
        self.takeaway_textbox.delete("1.0", "end")
        self.systems_textbox.delete("1.0", "end")
        self.sources_textbox.delete("1.0", "end")
        self.analysis_textbox.delete("1.0", "end")
        
        # Remove all dynamic findings
        for finding in self.findings_frames[:]:
            finding['frame'].destroy()
        self.findings_frames.clear()
        
        # Remove all dynamic recommendations
        for rec in self.recommendations_frames[:]:
            rec['frame'].destroy()
        self.recommendations_frames.clear()
        
        print("Form cleared successfully!")


# Example usage and testing
if __name__ == "__main__":
    # Initialize customtkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create test window
    root = ctk.CTk()
    root.title("Evidence Pack Generator Test")
    root.geometry("900x700")
    
    # Create tabview for testing
    tabview = ctk.CTkTabview(root)
    tabview.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Add the evidence pack tab
    evidence_tab = tabview.add("Evidence Pack")
    evidence_pack_generator = EvidencePackTab(evidence_tab)
    evidence_pack_generator.pack(fill="both", expand=True)
    
    # Start the application
    root.mainloop()
