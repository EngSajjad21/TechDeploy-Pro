import customtkinter as ctk

# Categorized list of applications with their Winget/Chocolatey IDs
AVAILABLE_APPS = {
    "Web Browsers": {
        "Google.Chrome": "Google Chrome",
        "Mozilla.Firefox": "Mozilla Firefox",
        "Brave.Brave": "Brave Browser"
    },
    "Development": {
        "Microsoft.VisualStudioCode": "Visual Studio Code",
        "Git.Git": "Git",
        "Python.Python.3.11": "Python 3.11",
        "OpenJS.NodeJS": "Node.js",
        "Notepad++.Notepad++": "Notepad++"
    },
    "Utilities": {
        "RARLab.WinRAR": "WinRAR",
        "7zip.7zip": "7-Zip",
        "VideoLAN.VLC": "VLC Media Player",
        "Microsoft.PowerToys": "PowerToys",
        "Rufus.Rufus": "Rufus"
    },
    "Communication": {
        "Discord.Discord": "Discord",
        "Zoom.Zoom": "Zoom",
        "SlackTechnologies.Slack": "Slack"
    },
    "Productivity": {
        "Notion.Notion": "Notion",
        "Obsidian.Obsidian": "Obsidian",
        "Foxit.FoxitReader": "Foxit Reader"
    }
}

class AppSelectorUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TechDeploy Pro - Application Selection")
        self.geometry("600x650")
        self.selected_apps = {}
        
        self.vars = {}
        
        self._build_ui()
        
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self, text="Select Applications to Install", font=ctk.CTkFont(size=22, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Scrollable Frame for apps
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        row_idx = 0
        for category, apps in AVAILABLE_APPS.items():
            cat_label = ctk.CTkLabel(self.scroll_frame, text=category, font=ctk.CTkFont(size=17, weight="bold"), text_color="#1f538d")
            cat_label.grid(row=row_idx, column=0, padx=10, pady=(15, 5), sticky="w")
            row_idx += 1
            
            for app_id, app_name in apps.items():
                var = ctk.BooleanVar(value=False)
                # Defaults: Chrome, VS Code, WinRAR, Git
                if app_id in ["Google.Chrome", "Microsoft.VisualStudioCode", "RARLab.WinRAR", "Git.Git"]:
                    var.set(True)
                
                cb = ctk.CTkCheckBox(self.scroll_frame, text=app_name, variable=var, font=ctk.CTkFont(size=14))
                cb.grid(row=row_idx, column=0, padx=30, pady=5, sticky="w")
                
                self.vars[app_id] = (app_name, var)
                row_idx += 1
                
        # Buttons Frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.select_all_btn = ctk.CTkButton(btn_frame, text="Select All", command=self.select_all, width=120)
        self.select_all_btn.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.install_btn = ctk.CTkButton(btn_frame, text="Continue Installation", command=self.confirm_selection, fg_color="#28a745", hover_color="#218838")
        self.install_btn.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
    def select_all(self):
        # Toggle behavior based on current state
        all_selected = all(var.get() for _, var in self.vars.values())
        for app_id, (app_name, var) in self.vars.items():
            var.set(not all_selected)
        self.select_all_btn.configure(text="Deselect All" if not all_selected else "Select All")
            
    def confirm_selection(self):
        for app_id, (app_name, var) in self.vars.items():
            if var.get():
                self.selected_apps[app_id] = app_name
        self.destroy()

def get_selected_apps():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = AppSelectorUI()
    app.mainloop()
    return app.selected_apps

if __name__ == "__main__":
    print(get_selected_apps())
