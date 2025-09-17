"""
Evidence Pack Generator Tab for AWS Log Checker Helper Application
Uses customtkinter for modern UI components
"""

import customtkinter as ctk
import pyperclip  # For clipboard functionality
from datetime import datetime
from typing import List, Dict, Any
import tkinter.filedialog as filedialog
import os


class EvidencePackTab(ctk.CTkFrame):
    """
    Evidence Pack Generator tab that creates structured reports
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Store dynamic widgets for findings, actions, and follow-ups
        self.findings_frames: List[Dict] = []
        self.actions_frames: List[Dict] = []
        self.followup_frames: List[Dict] = []
        self.imported_images: List[str] = []
        
        # Log groups for dropdown
        self.log_groups = [
            "/aws/lambda/aws-controltower-NotificationForwarder",
            "/aws/lambda/bank-app-sb-staging-cognito-pre-token",
            "/ecs/vemimoney-api-test-staging-lg",
            "/ecs/vemimoney-api-test2-staging-lg",
            "/ecs/vemimoney-communication-staging-lg",
            "/ecs/vemimoney-digitalidentity-staging-lg",
            "/ecs/vemimoney-directus-cms-staging-lg",
            "/ecs/vemimoney-grafana-staging-lg",
            "/ecs/vemimoney-mobilebffauth-staging-lg",
            "/ecs/vemimoney-mobilebffcustomer-staging-lg",
            "/ecs/vemimoney-mobileonboarding-staging-lg",
            "/ecs/vemimoney-onboarding-staging-lg",
            "/ecs/vemimoney-syntheticevents-staging-lg"
        ]
        
        # Configure the main frame
        self.configure(fg_color="transparent")
        
        # Create scrollable frame for the content
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=800, height=600)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Fix mousewheel scrolling for macOS
        self.setup_mousewheel_scrolling()
        
        # Initialize UI components
        self.setup_widgets()
    
    def setup_widgets(self):
        """Create and arrange all UI widgets"""
        
        # Main title
        title_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text="Evidence Pack Documentation", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Basic Information Section
        self.create_basic_info_section()
        
        # Log Sources Section
        self.create_log_sources_section()
        
        # Findings Section
        self.create_findings_section()
        
        # Actions Taken Section
        self.create_actions_section()
        
        # Follow-up Section
        self.create_followup_section()
        
        # Screenshots/Logs Section
        self.create_evidence_section()
        
        # Sign-off Section
        self.create_signoff_section()
        
        # Action buttons
        self.create_action_buttons()
    
    def create_basic_info_section(self):
        """Create basic information section"""
        
        # Section frame
        basic_frame = ctk.CTkFrame(self.scrollable_frame)
        basic_frame.pack(fill="x", pady=10, padx=20)
        
        # Section title
        basic_title = ctk.CTkLabel(
            basic_frame, 
            text="Basic Information", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        basic_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Date/Time with auto button
        datetime_frame = ctk.CTkFrame(basic_frame)
        datetime_frame.pack(fill="x", pady=5, padx=20)
        
        datetime_label = ctk.CTkLabel(datetime_frame, text="Date/Time:")
        datetime_label.pack(side="left", padx=(10, 5))
        
        self.datetime_entry = ctk.CTkEntry(datetime_frame, width=200, placeholder_text="YYYY-MM-DD HH:MM:SS")
        self.datetime_entry.pack(side="left", padx=5)
        
        auto_datetime_btn = ctk.CTkButton(
            datetime_frame,
            text="Auto Fill",
            command=self.set_current_datetime,
            width=80,
            height=28
        )
        auto_datetime_btn.pack(side="left", padx=5)
        
        # Checker
        checker_label = ctk.CTkLabel(basic_frame, text="Checker:")
        checker_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.checker_entry = ctk.CTkEntry(basic_frame, width=300, placeholder_text="Your Name")
        self.checker_entry.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Environment
        env_label = ctk.CTkLabel(basic_frame, text="Environment:")
        env_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.environment_combo = ctk.CTkComboBox(
            basic_frame,
            values=["Production", "Staging", "Development", "Test"],
            width=200
        )
        self.environment_combo.pack(pady=(0, 10), padx=20, anchor="w")
        
        # AWS Account
        account_label = ctk.CTkLabel(basic_frame, text="AWS Account:")
        account_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.account_entry = ctk.CTkEntry(basic_frame, width=300, placeholder_text="Account ID or Name")
        self.account_entry.pack(pady=(0, 15), padx=20, anchor="w")
    
    def create_log_sources_section(self):
        """Create log sources section with dropdown"""
        
        # Section frame
        logs_frame = ctk.CTkFrame(self.scrollable_frame)
        logs_frame.pack(fill="x", pady=10, padx=20)
        
        # Section title
        logs_title = ctk.CTkLabel(
            logs_frame, 
            text="Log Sources Checked", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        logs_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # CloudWatch Logs
        cw_frame = ctk.CTkFrame(logs_frame)
        cw_frame.pack(fill="x", pady=5, padx=20)
        
        cw_label = ctk.CTkLabel(cw_frame, text="CloudWatch Logs:")
        cw_label.pack(side="left", padx=(10, 5))
        
        self.log_group_combo = ctk.CTkComboBox(
            cw_frame,
            values=self.log_groups,
            width=400
        )
        self.log_group_combo.pack(side="left", padx=5)
        
        add_log_btn = ctk.CTkButton(
            cw_frame,
            text="Add",
            command=self.add_log_group,
            width=60,
            height=28
        )
        add_log_btn.pack(side="left", padx=5)
        
        # Selected log groups display
        self.selected_logs_text = ctk.CTkTextbox(logs_frame, width=600, height=80)
        self.selected_logs_text.pack(pady=5, padx=20)
        
        # CloudTrail
        trail_label = ctk.CTkLabel(logs_frame, text="CloudTrail:")
        trail_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.cloudtrail_entry = ctk.CTkEntry(logs_frame, width=400, placeholder_text="Trail Names")
        self.cloudtrail_entry.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Application Logs
        app_label = ctk.CTkLabel(logs_frame, text="Application Logs:")
        app_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.app_logs_entry = ctk.CTkEntry(logs_frame, width=400, placeholder_text="Service Names")
        self.app_logs_entry.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Security Logs
        sec_label = ctk.CTkLabel(logs_frame, text="Security Logs:")
        sec_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.security_logs_entry = ctk.CTkEntry(logs_frame, width=400, placeholder_text="WAF, GuardDuty, etc.")
        self.security_logs_entry.pack(pady=(0, 15), padx=20, anchor="w")
    
    def create_findings_section(self):
        """Create findings section with dynamic add/remove"""
        
        # Section frame
        self.findings_section = ctk.CTkFrame(self.scrollable_frame)
        self.findings_section.pack(fill="x", pady=10, padx=20)
        
        # Section title
        findings_title = ctk.CTkLabel(
            self.findings_section, 
            text="Findings", 
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
    
    def create_actions_section(self):
        """Create actions taken section with dynamic add/remove"""
        
        # Section frame
        self.actions_section = ctk.CTkFrame(self.scrollable_frame)
        self.actions_section.pack(fill="x", pady=10, padx=20)
        
        # Section title
        actions_title = ctk.CTkLabel(
            self.actions_section, 
            text="Actions Taken", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        actions_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Container for dynamic actions
        self.actions_container = ctk.CTkFrame(self.actions_section)
        self.actions_container.pack(fill="x", pady=10, padx=20)
        
        # Add action button
        add_action_btn = ctk.CTkButton(
            self.actions_section,
            text="+ Add Action",
            command=self.add_action,
            width=150,
            height=35
        )
        add_action_btn.pack(pady=(0, 15), padx=20, anchor="w")
    
    def create_followup_section(self):
        """Create follow-up section with dynamic add/remove like actions"""
        
        # Section frame
        self.followup_section = ctk.CTkFrame(self.scrollable_frame)
        self.followup_section.pack(fill="x", pady=10, padx=20)
        
        # Section title
        followup_title = ctk.CTkLabel(
            self.followup_section, 
            text="Follow-up Required", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        followup_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Container for dynamic follow-ups
        self.followup_container = ctk.CTkFrame(self.followup_section)
        self.followup_container.pack(fill="x", pady=10, padx=20)
        
        # Add follow-up button
        add_followup_btn = ctk.CTkButton(
            self.followup_section,
            text="+ Add Follow-up",
            command=self.add_followup,
            width=150,
            height=35
        )
        add_followup_btn.pack(pady=(0, 15), padx=20, anchor="w")
    
    def create_evidence_section(self):
        """Create screenshots/logs evidence section with import functionality"""
        
        # Section frame
        evidence_frame = ctk.CTkFrame(self.scrollable_frame)
        evidence_frame.pack(fill="x", pady=10, padx=20)
        
        # Section title
        evidence_title = ctk.CTkLabel(
            evidence_frame, 
            text="Screenshots/Logs", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        evidence_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Import button frame
        import_frame = ctk.CTkFrame(evidence_frame)
        import_frame.pack(fill="x", pady=5, padx=20)
        
        import_btn = ctk.CTkButton(
            import_frame,
            text="Import Images",
            command=self.import_images,
            width=120,
            height=28
        )
        import_btn.pack(side="left", padx=(10, 5))
        
        clear_images_btn = ctk.CTkButton(
            import_frame,
            text="Clear Images",
            command=self.clear_imported_images,
            width=120,
            height=28,
            fg_color="gray"
        )
        clear_images_btn.pack(side="left", padx=5)
        
        # Evidence text area
        self.evidence_text = ctk.CTkTextbox(evidence_frame, width=600, height=100)
        self.evidence_text.pack(pady=5, padx=20)
        self.evidence_text.insert("1.0", "[Attach or reference any supporting evidence]")
        
        # Imported images display
        self.images_label = ctk.CTkLabel(evidence_frame, text="No images imported")
        self.images_label.pack(pady=(5, 15), padx=20, anchor="w")
    
    def create_signoff_section(self):
        """Create sign-off section"""
        
        # Section frame
        signoff_frame = ctk.CTkFrame(self.scrollable_frame)
        signoff_frame.pack(fill="x", pady=10, padx=20)
        
        # Section title
        signoff_title = ctk.CTkLabel(
            signoff_frame, 
            text="Sign-off", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        signoff_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Checked by
        checked_label = ctk.CTkLabel(signoff_frame, text="Checked by:")
        checked_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.checked_by_entry = ctk.CTkEntry(signoff_frame, width=300, placeholder_text="Name")
        self.checked_by_entry.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Reviewed by
        reviewed_label = ctk.CTkLabel(signoff_frame, text="Reviewed by:")
        reviewed_label.pack(pady=(5, 0), padx=20, anchor="w")
        self.reviewed_by_entry = ctk.CTkEntry(signoff_frame, width=300, placeholder_text="Name")
        self.reviewed_by_entry.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Sign-off date with auto button
        signoff_date_frame = ctk.CTkFrame(signoff_frame)
        signoff_date_frame.pack(fill="x", pady=5, padx=20)
        
        signoff_date_label = ctk.CTkLabel(signoff_date_frame, text="Date:")
        signoff_date_label.pack(side="left", padx=(10, 5))
        
        self.signoff_date_entry = ctk.CTkEntry(signoff_date_frame, width=200, placeholder_text="YYYY-MM-DD")
        self.signoff_date_entry.pack(side="left", padx=5)
        
        auto_signoff_date_btn = ctk.CTkButton(
            signoff_date_frame,
            text="Today",
            command=self.set_current_date,
            width=80,
            height=28
        )
        auto_signoff_date_btn.pack(side="left", padx=(5, 10))
    
    def create_action_buttons(self):
        """Create main action buttons"""
        
        # Button frame
        button_frame = ctk.CTkFrame(self.scrollable_frame)
        button_frame.pack(fill="x", pady=20, padx=20)
        
        # Generate button
        generate_btn = ctk.CTkButton(
            button_frame,
            text="Generate Evidence Pack",
            command=self.generate_evidence_pack,
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
    
    def set_current_datetime(self):
        """Set current date and time"""
        current_dt = datetime.now()
        self.datetime_entry.delete(0, "end")
        self.datetime_entry.insert(0, current_dt.strftime("%Y-%m-%d %H:%M:%S"))
    
    def set_current_date(self):
        """Set current date"""
        current_date = datetime.now()
        self.signoff_date_entry.delete(0, "end")
        self.signoff_date_entry.insert(0, current_date.strftime("%Y-%m-%d"))
    
    def add_log_group(self):
        """Add selected log group to the list"""
        selected_log = self.log_group_combo.get()
        if selected_log:
            current_text = self.selected_logs_text.get("1.0", "end-1c")
            if current_text.strip():
                new_text = current_text + f"\n- {selected_log}"
            else:
                new_text = f"- {selected_log}"
            
            self.selected_logs_text.delete("1.0", "end")
            self.selected_logs_text.insert("1.0", new_text)
    
    def add_finding(self):
        """Add a new finding entry"""
        
        # Create finding frame
        finding_frame = ctk.CTkFrame(self.findings_container)
        finding_frame.pack(fill="x", pady=5, padx=10)
        
        # Finding number
        finding_num = len(self.findings_frames) + 1
        num_label = ctk.CTkLabel(finding_frame, text=f"Finding {finding_num}:")
        num_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        # Description and impact
        desc_entry = ctk.CTkEntry(finding_frame, width=500, placeholder_text="Description and impact")
        desc_entry.pack(pady=(0, 10), padx=10, anchor="w")
        
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
        
        # Store reference
        finding_data = {
            'frame': finding_frame,
            'description': desc_entry,
            'number_label': num_label
        }
        
        self.findings_frames.append(finding_data)
    
    def add_action(self):
        """Add a new action entry"""
        
        # Create action frame
        action_frame = ctk.CTkFrame(self.actions_container)
        action_frame.pack(fill="x", pady=5, padx=10)
        
        # Action number
        action_num = len(self.actions_frames) + 1
        num_label = ctk.CTkLabel(action_frame, text=f"Action {action_num}:")
        num_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        # Description
        desc_entry = ctk.CTkEntry(action_frame, width=500, placeholder_text="Description")
        desc_entry.pack(pady=(0, 10), padx=10, anchor="w")
        
        # Remove button
        remove_btn = ctk.CTkButton(
            action_frame,
            text="Remove",
            command=lambda: self.remove_action(action_frame),
            width=80,
            height=25,
            fg_color="red"
        )
        remove_btn.pack(pady=(0, 10), padx=10, anchor="e")
        
        # Store reference
        action_data = {
            'frame': action_frame,
            'description': desc_entry,
            'number_label': num_label
        }
        
        self.actions_frames.append(action_data)
    
    def add_followup(self):
        """Add a new follow-up entry"""
        
        # Create follow-up frame
        followup_frame = ctk.CTkFrame(self.followup_container)
        followup_frame.pack(fill="x", pady=5, padx=10)
        
        # Follow-up number
        followup_num = len(self.followup_frames) + 1
        num_label = ctk.CTkLabel(followup_frame, text=f"Follow-up {followup_num}:")
        num_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        # Description with due date and owner
        desc_entry = ctk.CTkEntry(followup_frame, width=500, placeholder_text="Description: Due date and owner")
        desc_entry.pack(pady=(0, 10), padx=10, anchor="w")
        
        # Remove button
        remove_btn = ctk.CTkButton(
            followup_frame,
            text="Remove",
            command=lambda: self.remove_followup(followup_frame),
            width=80,
            height=25,
            fg_color="red"
        )
        remove_btn.pack(pady=(0, 10), padx=10, anchor="e")
        
        # Store reference
        followup_data = {
            'frame': followup_frame,
            'description': desc_entry,
            'number_label': num_label
        }
        
        self.followup_frames.append(followup_data)
    
    def remove_finding(self, finding_frame):
        """Remove a finding entry"""
        self.findings_frames = [f for f in self.findings_frames if f['frame'] != finding_frame]
        finding_frame.destroy()
        self.update_finding_numbers()
    
    def remove_action(self, action_frame):
        """Remove an action entry"""
        self.actions_frames = [a for a in self.actions_frames if a['frame'] != action_frame]
        action_frame.destroy()
        self.update_action_numbers()
    
    def remove_followup(self, followup_frame):
        """Remove a follow-up entry"""
        self.followup_frames = [f for f in self.followup_frames if f['frame'] != followup_frame]
        followup_frame.destroy()
        self.update_followup_numbers()
    
    def update_finding_numbers(self):
        """Update finding numbers after removal"""
        for i, finding in enumerate(self.findings_frames, 1):
            finding['number_label'].configure(text=f"Finding {i}:")
    
    def update_action_numbers(self):
        """Update action numbers after removal"""
        for i, action in enumerate(self.actions_frames, 1):
            action['number_label'].configure(text=f"Action {i}:")
    
    def update_followup_numbers(self):
        """Update follow-up numbers after removal"""
        for i, followup in enumerate(self.followup_frames, 1):
            followup['number_label'].configure(text=f"Follow-up {i}:")
    
    def import_images(self):
        """Import image files for evidence"""
        try:
            file_types = [
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
            
            filenames = filedialog.askopenfilenames(
                title="Select Images for Evidence",
                filetypes=file_types
            )
            
            if filenames:
                self.imported_images.extend(filenames)
                self.update_images_display()
                
        except Exception as e:
            error_window = ctk.CTkToplevel(self)
            error_window.title("Error")
            error_window.geometry("400x150")
            error_window.transient(self)
            error_window.grab_set()
            
            error_label = ctk.CTkLabel(
                error_window, 
                text=f"Error importing images:\n{str(e)}",
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
    
    def clear_imported_images(self):
        """Clear all imported images"""
        self.imported_images.clear()
        self.update_images_display()
    
    def update_images_display(self):
        """Update the display of imported images"""
        if self.imported_images:
            image_names = [os.path.basename(img) for img in self.imported_images]
            if len(image_names) <= 3:
                display_text = f"Images: {', '.join(image_names)}"
            else:
                display_text = f"Images: {', '.join(image_names[:3])} ... ({len(image_names)} total)"
        else:
            display_text = "No images imported"
        
        self.images_label.configure(text=display_text)
    
    def generate_evidence_pack(self):
        """Generate the complete evidence pack"""
        
        # Collect all data
        datetime_val = self.datetime_entry.get().strip()
        checker = self.checker_entry.get().strip()
        environment = self.environment_combo.get()
        account = self.account_entry.get().strip()
        
        cloudwatch_logs = self.selected_logs_text.get("1.0", "end-1c").strip()
        cloudtrail = self.cloudtrail_entry.get().strip()
        app_logs = self.app_logs_entry.get().strip()
        security_logs = self.security_logs_entry.get().strip()
        
        evidence = self.evidence_text.get("1.0", "end-1c").strip()
        
        checked_by = self.checked_by_entry.get().strip()
        reviewed_by = self.reviewed_by_entry.get().strip()
        signoff_date = self.signoff_date_entry.get().strip()
        
        # Build evidence pack content
        content = "AWS Log Checker Helper - Evidence Pack\n\n"
        content += "EVIDENCE DOCUMENTATION:\n"
        content += "=" * 33 + "\n\n"
        
        content += f"Date/Time: {datetime_val or '[YYYY-MM-DD HH:MM:SS]'}\n"
        content += f"Checker: {checker or '[Your Name]'}\n"
        content += f"Environment: {environment or '[Production/Staging/Development]'}\n"
        content += f"AWS Account: {account or '[Account ID or Name]'}\n\n"
        
        content += "LOG SOURCES CHECKED:\n"
        if cloudwatch_logs:
            content += f"- CloudWatch Logs:\n{cloudwatch_logs}\n"
        else:
            content += "- CloudWatch Logs: [Log Group Names]\n"
        
        content += f"- CloudTrail: {cloudtrail or '[Trail Names]'}\n"
        content += f"- Application Logs: {app_logs or '[Service Names]'}\n"
        content += f"- Security Logs: {security_logs or '[WAF, GuardDuty, etc.]'}\n\n"
        
        content += "FINDINGS:\n"
        if self.findings_frames:
            for i, finding in enumerate(self.findings_frames, 1):
                desc = finding['description'].get().strip()
                content += f"- Finding {i}: {desc or '[Description and impact]'}\n"
        else:
            content += "- [Finding 1]: Description and impact\n"
            content += "- [Finding 2]: Description and impact\n"
        content += "\n"
        
        content += "ACTIONS TAKEN:\n"
        if self.actions_frames:
            for i, action in enumerate(self.actions_frames, 1):
                desc = action['description'].get().strip()
                content += f"- Action {i}: {desc or '[Description]'}\n"
        else:
            content += "- [Action 1]: Description\n"
            content += "- [Action 2]: Description\n"
        content += "\n"
        
        content += "FOLLOW-UP REQUIRED:\n"
        if self.followup_frames:
            for i, followup in enumerate(self.followup_frames, 1):
                desc = followup['description'].get().strip()
                content += f"- Follow-up {i}: {desc or '[Description: Due date and owner]'}\n"
        else:
            content += "- [Follow-up 1]: Description: Due date and owner\n"
            content += "- [Follow-up 2]: Description: Due date and owner\n"
        content += "\n"
        
        content += "SCREENSHOTS/LOGS:\n"
        if evidence and not evidence.startswith("[Attach or reference"):
            content += f"{evidence}\n"
        else:
            content += "[Attach or reference any supporting evidence]\n"
        
        # Add imported images
        if self.imported_images:
            content += "\nAttached Images:\n"
            for img in self.imported_images:
                content += f"- {os.path.basename(img)} ({img})\n"
        content += "\n"
        
        content += "SIGN-OFF:\n"
        content += f"Checked by: {checked_by or '[Name]'}\n"
        content += f"Reviewed by: {reviewed_by or '[Name]'}\n"
        content += f"Date: {signoff_date or '[YYYY-MM-DD]'}\n"
        
        # Copy to clipboard
        try:
            pyperclip.copy(content)
            
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
        """Clear all form fields"""
        
        # Clear basic info
        self.datetime_entry.delete(0, "end")
        self.checker_entry.delete(0, "end")
        self.environment_combo.set("")
        self.account_entry.delete(0, "end")
        
        # Clear log sources
        self.selected_logs_text.delete("1.0", "end")
        self.cloudtrail_entry.delete(0, "end")
        self.app_logs_entry.delete(0, "end")
        self.security_logs_entry.delete(0, "end")
        
        # Clear text areas
        self.evidence_text.delete("1.0", "end")
        self.evidence_text.insert("1.0", "[Attach or reference any supporting evidence]")
        
        # Clear sign-off
        self.checked_by_entry.delete(0, "end")
        self.reviewed_by_entry.delete(0, "end")
        self.signoff_date_entry.delete(0, "end")
        
        # Remove all dynamic entries
        for finding in self.findings_frames[:]:
            finding['frame'].destroy()
        self.findings_frames.clear()
        
        for action in self.actions_frames[:]:
            action['frame'].destroy()
        self.actions_frames.clear()
        
        for followup in self.followup_frames[:]:
            followup['frame'].destroy()
        self.followup_frames.clear()
        
        # Clear imported images
        self.clear_imported_images()
    
    def setup_mousewheel_scrolling(self):
        """Setup mousewheel scrolling for macOS compatibility"""
        def _on_mousewheel(event):
            # Handle mousewheel scrolling for the CTkScrollableFrame
            try:
                # For CustomTkinter scrollable frames, we need to access the internal canvas differently
                if hasattr(self.scrollable_frame, '_parent_canvas') and self.scrollable_frame._parent_canvas:
                    canvas = self.scrollable_frame._parent_canvas
                    if hasattr(event, 'delta') and event.delta:
                        # Windows/macOS with delta
                        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                    elif hasattr(event, 'num'):
                        # Linux scroll events
                        if event.num == 4:
                            canvas.yview_scroll(-1, "units")
                        elif event.num == 5:
                            canvas.yview_scroll(1, "units")
                elif hasattr(self.scrollable_frame, '_scrollbar'):
                    # Alternative approach - use the scrollbar
                    scrollbar = self.scrollable_frame._scrollbar
                    if hasattr(event, 'delta') and event.delta:
                        scrollbar.set(scrollbar.get()[0] - (event.delta / 1200), scrollbar.get()[1] - (event.delta / 1200))
            except Exception as e:
                print(f"Scroll error: {e}")
        
        # Bind mousewheel events to the scrollable frame and its children
        def bind_mousewheel_recursive(widget):
            try:
                widget.bind("<MouseWheel>", _on_mousewheel, add=True)  # Windows/macOS
                widget.bind("<Button-4>", _on_mousewheel, add=True)   # Linux scroll up
                widget.bind("<Button-5>", _on_mousewheel, add=True)   # Linux scroll down
                
                # Recursively bind to all children
                for child in widget.winfo_children():
                    try:
                        bind_mousewheel_recursive(child)
                    except:
                        pass  # Skip widgets that don't support binding
            except:
                pass  # Skip widgets that don't support binding
        
        # Apply bindings with delay to ensure widgets exist
        def apply_bindings():
            try:
                bind_mousewheel_recursive(self.scrollable_frame)
                bind_mousewheel_recursive(self)
                
                # Also bind to the main frame
                self.bind("<MouseWheel>", _on_mousewheel, add=True)
                self.bind("<Button-4>", _on_mousewheel, add=True)
                self.bind("<Button-5>", _on_mousewheel, add=True)
            except Exception as e:
                print(f"Binding error: {e}")
        
        # Apply bindings with delay to ensure widgets exist
        self.after(50, apply_bindings)
    
    def refresh_content(self):
        """Refresh the content and ensure proper scrolling"""
        try:
            # Force update of the scrollable frame
            self.scrollable_frame.update_idletasks()
            
            # Re-apply mousewheel scrolling to any new widgets
            self.after(10, self.setup_mousewheel_scrolling)
            
            # Force geometry update
            self.update_idletasks()
            
            # Update the scrollable region
            if hasattr(self.scrollable_frame, '_parent_canvas') and self.scrollable_frame._parent_canvas:
                canvas = self.scrollable_frame._parent_canvas
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.update_idletasks()
        except Exception as e:
            print(f"Refresh error: {e}")
    
    def force_update(self):
        """Force immediate update of the content"""
        self.update()
        self.update_idletasks()
        if hasattr(self.scrollable_frame, 'update'):
            self.scrollable_frame.update()
            self.scrollable_frame.update_idletasks()
        self.refresh_content()


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
