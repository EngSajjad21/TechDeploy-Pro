<div align="center">

<img src="https://img.shields.io/badge/TechDeploy_Pro-v2.0-blue?style=for-the-badge&logo=windows&logoColor=white" alt="Version"/>
<img src="https://img.shields.io/badge/License-GPL_v3-green?style=for-the-badge&logo=gnu&logoColor=white" alt="License"/>
<img src="https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Platform"/>
<img src="https://img.shields.io/badge/GUI-CustomTkinter-purple?style=for-the-badge&logo=tkinter&logoColor=white" alt="GUI"/>

<br/><br/>

# ⚡ TechDeploy Pro

### Windows Post-Installation Automation Tool

> **Automate your Windows setup in minutes.** Install apps, apply optimizations, tweak the registry, and check drivers — all from a sleek GUI.

<img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square&logo=github" alt="PRs Welcome"/>
<img src="https://img.shields.io/badge/Maintained-Yes-success?style=flat-square" alt="Maintained"/>
<img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" alt="Status"/>

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🖼 Screenshots](#-screenshots)
- [🚀 Getting Started](#-getting-started)
- [📦 Supported Applications](#-supported-applications)
- [⚙ System Optimizations](#-system-optimizations)
- [🔧 Registry Tweaks](#-registry-tweaks)
- [🖥 Driver Scanner](#-driver-scanner)
- [🗂 Project Structure](#-project-structure)
- [📄 License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📦 **App Installer** | Install popular apps via Winget with a single click |
| ⚙ **System Optimizer** | Disable telemetry, set performance power plan, tune visual effects |
| 🔧 **Registry Tweaks** | Apply common registry tweaks for speed & usability |
| 🖥 **Driver Scanner** | Detect missing or faulty device drivers instantly |
| 📋 **Live Log** | Real-time output log for all tasks |
| ✅ **Select & Control** | Checkboxes for everything — you decide what runs |

---

## 🖼 Screenshots

> _Coming soon – screenshots will be added after first stable release._

---

## 🚀 Getting Started

### Prerequisites

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white&style=flat-square)
![Winget](https://img.shields.io/badge/Winget-Required-orange?logo=windows&logoColor=white&style=flat-square)
![Admin](https://img.shields.io/badge/Run_As-Administrator-red?logo=windows&logoColor=white&style=flat-square)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/EngSajjad21/TechDeploy-Pro.git
cd TechDeploy-Pro

# 2. Install dependencies
pip install customtkinter rich

# 3. Run as Administrator
python main.py
```

> ⚠️ **Important:** Must be run as **Administrator** for system optimizations and registry tweaks to apply correctly.

---

## 📦 Supported Applications

| Category | Applications |
|----------|-------------|
| 🌐 Web Browsers | Google Chrome, Firefox, Brave, Microsoft Edge |
| 🛠 Development | VS Code, Git, Python 3.11, Node.js, Notepad++, PyCharm, Docker |
| 📦 Utilities | WinRAR, 7-Zip, VLC, PowerToys, Rufus, Greenshot, Everything |
| 💬 Communication | Discord, Zoom, Slack, Telegram |
| 📝 Productivity | Notion, Obsidian, Foxit Reader, Microsoft Teams |

---

## ⚙ System Optimizations

| Optimization | Description |
|---|---|
| 🔕 Disable Telemetry | Stops Windows diagnostic data collection |
| ⚡ High Performance Power Plan | Maximizes CPU & system performance |
| 🧹 Disable SysMain | Improves SSD responsiveness |
| 🎨 Optimize Visual Effects | Reduces animations for snappier UI |
| 🔄 Pause Windows Update | Pauses automatic updates for 7 days |

---

## 🔧 Registry Tweaks

| Tweak | Description |
|---|---|
| 🔍 Disable Bing in Start | Removes Bing web results from Windows Search |
| 📂 Show Hidden Files | Makes hidden files visible in Explorer |
| 🔒 Disable Lock Screen | Skips the Windows lock screen on wake |
| 🤫 Disable Cortana | Turns off Cortana completely |
| 🖱 Classic Right-Click Menu | Restores the full context menu in Windows 11 |
| 🎭 Disable Window Animations | Speeds up the UI |

---

## 🖥 Driver Scanner

Scans your system using WMI to detect any devices with missing or faulty drivers (`ConfigManagerErrorCode != 0`) and displays them in a clean table.

---

## 🗂 Project Structure

```
TechDeploy Pro/
├── main.py                  # Entry point
├── gui/
│   ├── __init__.py
│   └── main_gui.py          # Full CustomTkinter GUI
├── core/
│   ├── __init__.py
│   ├── pre_check.py         # Admin & internet pre-checks
│   ├── installer.py         # Application installer (Winget)
│   ├── drivers.py           # Driver scanner
│   ├── system_opt.py        # System optimizations
│   ├── app_selector.py      # Legacy app selector UI
│   └── utils.py             # PowerShell utility
├── scripts/
│   └── registry_tweaks.ps1  # PowerShell registry script
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📄 License

<div align="center">

[![GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge&logo=gnu)](https://www.gnu.org/licenses/gpl-3.0)

This project is licensed under the **GNU General Public License v3.0**.
See the [LICENSE](LICENSE) file for full details.

**TechDeploy Pro** © 2026 — Free & Open Source Software

</div>

---
