import customtkinter as ctk
import threading
import os
import sys
import json

# Ensure the root directory is in the sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_powershell

# ── App categories & IDs ──────────────────────────────────────────────────────
AVAILABLE_APPS = {
    "🌐 Web Browsers": {
        "Google.Chrome": "Google Chrome",
        "Mozilla.Firefox": "Mozilla Firefox",
        "Brave.Brave": "Brave Browser",
        "Microsoft.Edge": "Microsoft Edge",
    },
    "🛠 Development": {
        "Microsoft.VisualStudioCode": "Visual Studio Code",
        "Git.Git": "Git",
        "Python.Python.3.11": "Python 3.11",
        "OpenJS.NodeJS": "Node.js",
        "Notepad++.Notepad++": "Notepad++",
        "JetBrains.PyCharm.Community": "PyCharm Community",
        "Docker.DockerDesktop": "Docker Desktop",
    },
    "📦 Utilities": {
        "RARLab.WinRAR": "WinRAR",
        "7zip.7zip": "7-Zip",
        "VideoLAN.VLC": "VLC Media Player",
        "Microsoft.PowerToys": "PowerToys",
        "Rufus.Rufus": "Rufus",
        "Greenshot.Greenshot": "Greenshot (Screenshots)",
        "voidtools.Everything": "Everything (File Search)",
    },
    "💬 Communication": {
        "Discord.Discord": "Discord",
        "Zoom.Zoom": "Zoom",
        "SlackTechnologies.Slack": "Slack",
        "Telegram.TelegramDesktop": "Telegram",
    },
    "📝 Productivity": {
        "Notion.Notion": "Notion",
        "Obsidian.Obsidian": "Obsidian",
        "Foxit.FoxitReader": "Foxit Reader",
        "Microsoft.Teams": "Microsoft Teams",
    },
}

DEFAULTS = {
    "Google.Chrome", "Microsoft.VisualStudioCode",
    "RARLab.WinRAR", "Git.Git"
}

# ── Registry tweaks definitions ───────────────────────────────────────────────
REGISTRY_TWEAKS = {
    "disable_bing": {
        "label": "Disable Bing Search in Start Menu",
        "desc": "Remove Bing web results from Windows Search",
        "ps": 'Set-ItemProperty -Path "HKCU:\\Software\\Policies\\Microsoft\\Windows\\Explorer" -Name "DisableSearchBoxSuggestions" -Value 1 -Type DWord -Force'
    },
    "show_hidden": {
        "label": "Show Hidden Files & Folders",
        "desc": "Make hidden files visible in Explorer",
        "ps": 'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "Hidden" -Value 1 -Type DWord -Force'
    },
    "disable_lock": {
        "label": "Disable Lock Screen",
        "desc": "Skip the Windows lock screen on wake",
        "ps": 'New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Personalization" -Force | Out-Null; Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Personalization" -Name "NoLockScreen" -Value 1 -Type DWord -Force'
    },
    "disable_cortana": {
        "label": "Disable Cortana",
        "desc": "Turn off Cortana completely",
        "ps": 'New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" -Force | Out-Null; Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" -Name "AllowCortana" -Value 0 -Type DWord -Force'
    },
    "classic_rightclick": {
        "label": "Restore Classic Right-Click Menu (Win11)",
        "desc": "Show the full context menu by default in Windows 11",
        "ps": 'New-Item -Path "HKCU:\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32" -Force | Out-Null'
    },
    "disable_animations": {
        "label": "Disable Window Animations",
        "desc": "Speed up the UI by turning off animations",
        "ps": 'Set-ItemProperty -Path "HKCU:\\Control Panel\\Desktop\\WindowMetrics" -Name "MinAnimate" -Value 0 -Type String -Force'
    },
}

# ── Optimization options ──────────────────────────────────────────────────────
OPTIMIZATIONS = {
    "telemetry": {
        "label": "Disable Windows Telemetry",
        "desc": "Stop diagnostic data collection by Microsoft",
        "ps": '''Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Type DWord -Value 0 -ErrorAction SilentlyContinue
Stop-Service -Name "DiagTrack" -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
Set-Service -Name "DiagTrack" -StartupType Disabled -ErrorAction SilentlyContinue'''
    },
    "high_perf": {
        "label": "High Performance Power Plan",
        "desc": "Set power plan to maximum performance",
        "ps": "powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    },
    "disable_superfetch": {
        "label": "Disable SysMain (Superfetch)",
        "desc": "Can improve responsiveness on SSDs",
        "ps": 'Stop-Service -Name "SysMain" -ErrorAction SilentlyContinue; Set-Service -Name "SysMain" -StartupType Disabled -ErrorAction SilentlyContinue'
    },
    "visual_effects": {
        "label": "Optimize Visual Effects for Performance",
        "desc": "Reduce animations & transparency effects",
        "ps": 'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name "VisualFXSetting" -Value 2 -Type DWord -Force'
    },
    "disable_wu_auto": {
        "label": "Pause Windows Update (7 days)",
        "desc": "Temporarily pause automatic Windows updates",
        "ps": 'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\WindowsUpdate\\UX\\Settings" -Name "PauseUpdatesExpiryTime" -Value ((Get-Date).AddDays(7).ToString("yyyy-MM-ddTHH:mm:ssZ")) -Type String -Force'
    },
}


class TechDeployApp(ctk.CTk):
    
    ACCENT  = "#1f6feb"
    SUCCESS = "#28a745"
    WARN    = "#ffc107"
    DANGER  = "#dc3545"
    
    def __init__(self):
        super().__init__()
        self.title("TechDeploy Pro  ·  Post-Installation Automation")
        self.geometry("900x680")
        self.minsize(850, 600)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self._app_vars   = {}   # app_id -> BooleanVar
        self._opt_vars   = {}   # key -> BooleanVar
        self._reg_vars   = {}   # key -> BooleanVar
        self._log_lines  = []
        
        self._build_layout()
    
    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        hdr = ctk.CTkFrame(self, corner_radius=0, height=64, fg_color="#0d1117")
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(hdr, text="⚡ TechDeploy Pro",
                     font=ctk.CTkFont("Segoe UI", 22, "bold"),
                     text_color="#58a6ff").grid(row=0, column=0, padx=24, pady=14)
        ctk.CTkLabel(hdr, text="Post-Installation Automation Tool v2.0",
                     font=ctk.CTkFont("Segoe UI", 13),
                     text_color="#8b949e").grid(row=0, column=1, sticky="w")
        
        # Tab view
        self.tabs = ctk.CTkTabview(self, anchor="nw")
        self.tabs.grid(row=1, column=0, padx=16, pady=12, sticky="nsew")
        
        for name in ["📦 Applications", "⚙ Optimizations", "🔧 Registry Tweaks", "🖥 Drivers", "📋 Log"]:
            self.tabs.add(name)
            self.tabs.tab(name).grid_columnconfigure(0, weight=1)
            self.tabs.tab(name).grid_rowconfigure(0, weight=1)
        
        self._build_apps_tab()
        self._build_opt_tab()
        self._build_reg_tab()
        self._build_drivers_tab()
        self._build_log_tab()
        
        # Footer
        ftr = ctk.CTkFrame(self, corner_radius=0, height=52, fg_color="#161b22")
        ftr.grid(row=2, column=0, sticky="ew")
        ftr.grid_columnconfigure(0, weight=1)
        
        self._run_btn = ctk.CTkButton(
            ftr, text="🚀  Run Selected Tasks", height=36,
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            fg_color=self.ACCENT, hover_color="#388bfd",
            command=self._run_all)
        self._run_btn.grid(row=0, column=0, padx=24, pady=8)
    
    # ── Applications Tab ──────────────────────────────────────────────────────
    def _build_apps_tab(self):
        tab = self.tabs.tab("📦 Applications")
        tab.grid_rowconfigure(0, weight=1)
        
        sf = ctk.CTkScrollableFrame(tab, label_text="Select applications to install")
        sf.grid(row=0, column=0, sticky="nsew", padx=4, pady=(4, 0))
        sf.grid_columnconfigure((0, 1), weight=1)
        
        row = 0
        for category, apps in AVAILABLE_APPS.items():
            ctk.CTkLabel(sf, text=category,
                         font=ctk.CTkFont("Segoe UI", 15, "bold"),
                         text_color="#79c0ff").grid(
                row=row, column=0, columnspan=2,
                padx=12, pady=(14, 4), sticky="w")
            row += 1
            col = 0
            for app_id, app_name in apps.items():
                var = ctk.BooleanVar(value=(app_id in DEFAULTS))
                self._app_vars[app_id] = (app_name, var)
                cb = ctk.CTkCheckBox(sf, text=app_name, variable=var,
                                     font=ctk.CTkFont("Segoe UI", 13),
                                     checkbox_width=20, checkbox_height=20)
                cb.grid(row=row, column=col, padx=20, pady=4, sticky="w")
                col += 1
                if col == 2:
                    col = 0
                    row += 1
            if col != 0:
                row += 1
        
        btn_fr = ctk.CTkFrame(tab, fg_color="transparent")
        btn_fr.grid(row=1, column=0, pady=8)
        ctk.CTkButton(btn_fr, text="Select All",   width=130,
                      command=lambda: self._toggle_all(self._app_vars, True)).pack(side="left", padx=8)
        ctk.CTkButton(btn_fr, text="Deselect All", width=130,
                      fg_color="#21262d", hover_color="#30363d",
                      command=lambda: self._toggle_all(self._app_vars, False)).pack(side="left", padx=8)
    
    # ── Optimizations Tab ─────────────────────────────────────────────────────
    def _build_opt_tab(self):
        tab = self.tabs.tab("⚙ Optimizations")
        tab.grid_rowconfigure(0, weight=1)
        
        sf = ctk.CTkScrollableFrame(tab, label_text="System optimizations")
        sf.grid(row=0, column=0, sticky="nsew", padx=4, pady=(4, 0))
        sf.grid_columnconfigure(0, weight=1)
        
        for i, (key, info) in enumerate(OPTIMIZATIONS.items()):
            var = ctk.BooleanVar(value=True)
            self._opt_vars[key] = var
            card = ctk.CTkFrame(sf, corner_radius=8, fg_color="#21262d")
            card.grid(row=i, column=0, padx=12, pady=6, sticky="ew")
            card.grid_columnconfigure(1, weight=1)
            
            ctk.CTkCheckBox(card, text="", variable=var,
                            checkbox_width=22, checkbox_height=22).grid(
                row=0, column=0, padx=14, pady=12)
            ctk.CTkLabel(card, text=info["label"],
                         font=ctk.CTkFont("Segoe UI", 14, "bold")).grid(
                row=0, column=1, sticky="w")
            ctk.CTkLabel(card, text=info["desc"],
                         font=ctk.CTkFont("Segoe UI", 12),
                         text_color="#8b949e").grid(
                row=1, column=1, sticky="w", padx=0, pady=(0, 10))
        
        btn_fr = ctk.CTkFrame(tab, fg_color="transparent")
        btn_fr.grid(row=1, column=0, pady=8)
        ctk.CTkButton(btn_fr, text="Select All",   width=130,
                      command=lambda: self._toggle_plain(self._opt_vars, True)).pack(side="left", padx=8)
        ctk.CTkButton(btn_fr, text="Deselect All", width=130,
                      fg_color="#21262d", hover_color="#30363d",
                      command=lambda: self._toggle_plain(self._opt_vars, False)).pack(side="left", padx=8)
    
    # ── Registry Tweaks Tab ───────────────────────────────────────────────────
    def _build_reg_tab(self):
        tab = self.tabs.tab("🔧 Registry Tweaks")
        tab.grid_rowconfigure(0, weight=1)
        
        sf = ctk.CTkScrollableFrame(tab, label_text="Registry tweaks")
        sf.grid(row=0, column=0, sticky="nsew", padx=4, pady=(4, 0))
        sf.grid_columnconfigure(0, weight=1)
        
        for i, (key, info) in enumerate(REGISTRY_TWEAKS.items()):
            var = ctk.BooleanVar(value=True)
            self._reg_vars[key] = var
            card = ctk.CTkFrame(sf, corner_radius=8, fg_color="#21262d")
            card.grid(row=i, column=0, padx=12, pady=6, sticky="ew")
            card.grid_columnconfigure(1, weight=1)
            
            ctk.CTkCheckBox(card, text="", variable=var,
                            checkbox_width=22, checkbox_height=22).grid(
                row=0, column=0, padx=14, pady=12)
            ctk.CTkLabel(card, text=info["label"],
                         font=ctk.CTkFont("Segoe UI", 14, "bold")).grid(
                row=0, column=1, sticky="w")
            ctk.CTkLabel(card, text=info["desc"],
                         font=ctk.CTkFont("Segoe UI", 12),
                         text_color="#8b949e").grid(
                row=1, column=1, sticky="w", padx=0, pady=(0, 10))
        
        btn_fr = ctk.CTkFrame(tab, fg_color="transparent")
        btn_fr.grid(row=1, column=0, pady=8)
        ctk.CTkButton(btn_fr, text="Select All",   width=130,
                      command=lambda: self._toggle_plain(self._reg_vars, True)).pack(side="left", padx=8)
        ctk.CTkButton(btn_fr, text="Deselect All", width=130,
                      fg_color="#21262d", hover_color="#30363d",
                      command=lambda: self._toggle_plain(self._reg_vars, False)).pack(side="left", padx=8)
    
    # ── Drivers Tab ───────────────────────────────────────────────────────────
    def _build_drivers_tab(self):
        tab = self.tabs.tab("🖥 Drivers")
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(tab, text="Missing / Faulty Device Drivers",
                     font=ctk.CTkFont("Segoe UI", 16, "bold")).grid(
            row=0, column=0, pady=(14, 6))
        
        self._driver_box = ctk.CTkTextbox(tab, state="disabled",
                                          font=ctk.CTkFont("Consolas", 12),
                                          fg_color="#0d1117", text_color="#c9d1d9")
        self._driver_box.grid(row=1, column=0, sticky="nsew", padx=16, pady=4)
        
        ctk.CTkButton(tab, text="🔍  Scan for Missing Drivers", height=36,
                      command=self._scan_drivers_thread).grid(
            row=2, column=0, pady=10)
    
    # ── Log Tab ───────────────────────────────────────────────────────────────
    def _build_log_tab(self):
        tab = self.tabs.tab("📋 Log")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        
        self._log_box = ctk.CTkTextbox(tab, state="disabled",
                                       font=ctk.CTkFont("Consolas", 12),
                                       fg_color="#0d1117", text_color="#c9d1d9")
        self._log_box.grid(row=0, column=0, sticky="nsew", padx=16, pady=12)
        
        ctk.CTkButton(tab, text="Clear Log", width=120,
                      fg_color="#21262d", hover_color="#30363d",
                      command=self._clear_log).grid(row=1, column=0, pady=(0, 10))
    
    # ── Helpers ───────────────────────────────────────────────────────────────
    def _toggle_all(self, var_dict, state: bool):
        for _, var in var_dict.values():
            var.set(state)
    
    def _toggle_plain(self, var_dict, state: bool):
        for var in var_dict.values():
            var.set(state)
    
    def _log(self, text: str, color: str = "#c9d1d9"):
        self._log_box.configure(state="normal")
        self._log_box.insert("end", text + "\n")
        self._log_box.see("end")
        self._log_box.configure(state="disabled")
    
    def _driver_log(self, text: str):
        self._driver_box.configure(state="normal")
        self._driver_box.insert("end", text + "\n")
        self._driver_box.see("end")
        self._driver_box.configure(state="disabled")
    
    def _clear_log(self):
        self._log_box.configure(state="normal")
        self._log_box.delete("1.0", "end")
        self._log_box.configure(state="disabled")
    
    # ── Run Tasks ─────────────────────────────────────────────────────────────
    def _run_all(self):
        self._run_btn.configure(state="disabled", text="⏳  Running...")
        threading.Thread(target=self._run_all_thread, daemon=True).start()
    
    def _run_all_thread(self):
        self.tabs.set("📋 Log")
        self._log("=" * 60)
        self._log("  TechDeploy Pro  –  Task Runner Started")
        self._log("=" * 60)
        
        # 1. Applications
        selected_apps = {aid: name for aid, (name, var) in self._app_vars.items() if var.get()}
        if selected_apps:
            self._log("\n📦  Installing Applications...")
            for app_id, app_name in selected_apps.items():
                self._log(f"  → Installing {app_name} ({app_id})…")
                code, out, err = run_powershell(f"winget install --id {app_id} -e --accept-package-agreements --accept-source-agreements --silent")
                if code == 0:
                    self._log(f"  ✓ {app_name} installed successfully.")
                else:
                    self._log(f"  ✗ {app_name} failed: {err.strip() or out.strip()}")
        else:
            self._log("\n📦  No applications selected – skipping.")
        
        # 2. Optimizations
        selected_opts = {k: v for k, v in self._opt_vars.items() if v.get()}
        if selected_opts:
            self._log("\n⚙  Applying System Optimizations...")
            for key, var in selected_opts.items():
                info = OPTIMIZATIONS[key]
                self._log(f"  → {info['label']}…")
                code, _, err = run_powershell(info["ps"])
                if code == 0:
                    self._log(f"  ✓ Done.")
                else:
                    self._log(f"  ✗ Failed: {err.strip()}")
        else:
            self._log("\n⚙  No optimizations selected – skipping.")
        
        # 3. Registry Tweaks
        selected_reg = {k: v for k, v in self._reg_vars.items() if v.get()}
        if selected_reg:
            self._log("\n🔧  Applying Registry Tweaks...")
            for key, var in selected_reg.items():
                info = REGISTRY_TWEAKS[key]
                self._log(f"  → {info['label']}…")
                code, _, err = run_powershell(info["ps"])
                if code == 0:
                    self._log(f"  ✓ Done.")
                else:
                    self._log(f"  ✗ Failed: {err.strip()}")
        else:
            self._log("\n🔧  No registry tweaks selected – skipping.")
        
        self._log("\n" + "=" * 60)
        self._log("  ✅  All selected tasks completed!")
        self._log("=" * 60)
        self.after(0, lambda: self._run_btn.configure(state="normal", text="🚀  Run Selected Tasks"))
    
    # ── Driver Scanner ────────────────────────────────────────────────────────
    def _scan_drivers_thread(self):
        threading.Thread(target=self._scan_drivers, daemon=True).start()
    
    def _scan_drivers(self):
        self._driver_box.configure(state="normal")
        self._driver_box.delete("1.0", "end")
        self._driver_box.configure(state="disabled")
        self._driver_log("🔍  Scanning for missing / faulty drivers…\n")
        
        script = """
        Get-WmiObject Win32_PnPEntity |
          Where-Object { $_.ConfigManagerErrorCode -ne 0 } |
          Select-Object Name, DeviceID, ConfigManagerErrorCode |
          ConvertTo-Json
        """
        code, stdout, stderr = run_powershell(script)
        
        if code != 0:
            self._driver_log(f"✗ Scan failed: {stderr.strip()}")
            return
        
        if not stdout.strip() or stdout.strip() == "null":
            self._driver_log("✅  All devices have proper drivers installed.\n    No errors found.")
            return
        
        try:
            data = json.loads(stdout)
            if isinstance(data, dict):
                data = [data]
            self._driver_log(f"⚠  Found {len(data)} device(s) with issues:\n")
            self._driver_log(f"{'Device Name':<40}  {'Error Code':>10}")
            self._driver_log("-" * 55)
            for item in data:
                name = str(item.get("Name", "Unknown"))[:38]
                code_n = item.get("ConfigManagerErrorCode", "?")
                self._driver_log(f"{name:<40}  {code_n:>10}")
        except json.JSONDecodeError:
            self._driver_log(f"✗ Could not parse output:\n{stdout}")


def launch():
    app = TechDeployApp()
    app.mainloop()


if __name__ == "__main__":
    launch()
