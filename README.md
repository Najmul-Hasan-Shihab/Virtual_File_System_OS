# 🔮 Virtual File System (VFS)

## 🧾 Overview
The **Virtual File System (VFS)** is a Python-based simulation of a traditional file system with a **futuristic, cross-platform GUI** built using `ttkbootstrap`.  
It emulates file management operations inside a virtual environment and introduces modern features like **version control**, an **analytics dashboard**, and **CPU scheduling visualizations** — all in a sleek desktop interface.

---

## ✨ Features

### 📁 File & Directory Operations
- Create, read, update, and delete files
- Set shared root directory for workspace
- Navigate and manage files with a simplified UI

### ♻️ File Version Control
- Automatically saves historical versions on file update
- View previous versions and restore from any snapshot

### 📊 Analytics Panel
- Pie chart of file type distribution
- Line graph timeline of file creation dates
- View total file count, size, and most modified files

### ⚙️ CPU Scheduling Visualizer
- Select from key scheduling algorithms:
  - First-Come, First-Served (FCFS)
  - Shortest Job First (SJF)
  - Shortest Remaining Time First (SRTF)
  - Round Robin
  - Priority (Non-Preemptive)
  - Priority (Preemptive)
- Input process data and visualize Gantt Charts dynamically
- Understand execution order, preemption, and CPU utilization

### 📜 Metadata Handling
- View file size, creation date, and modification time
- Search files and inspect details instantly

### 🎨 Theme Switcher
- Choose from prebuilt themes: Darkly, Cyborg, Solar, Superhero, Morph
- Modern typography and polished design

### 💻 GUI Features
- Splash screen with branding
- Fixed window layout with status bar
- Built using `ttkbootstrap` for a professional, dark-themed appearance

### 💾 Persistence
- Saves the state of the virtual file system to disk and loads it upon startup

---

## ✅ Requirements

- Python 3.7 or above
- Packages:
  - `ttkbootstrap`
  - `matplotlib`

---

## Installation

1. **Clone the Repository**:

   ```bash
     git clone https://github.com/duttaturja/Virtual-File-System.git
   ```
2. **Navigate to the Project Directory**:

     ```bash
       cd Virtual-File-System
     ```
3. **Virtual Environment Setup:**
   
    ```bash  
         python -m venv venv
         venv\Scripts\activate
    ``` 
5. **Install Dependencies**:<br>
Install the required Python packages using pip:

     ```bash
     pip install -r requirements.txt
     ```
6. **Usage**: <br>
Run the Application:

     ```bash
       python vfs_app.py
     ```

## Graphical User Interface:
Once the application is running, use the top menu bar to:

### 📂 File Operations
-Create File: Add a new file to the virtual system
-Read File: View contents of an existing file
-Update File: Overwrite file content and trigger versioning
-Delete File: Permanently remove a file
-Search File: Find files and view metadata

### 🔄 Version Control
View File Versions: Browse historical versions and restore any

### 📊 Analytics
Analytics Panel: View charts, statistics, and insights about file activity

🧠 CPU Scheduling
Gantt Chart Visualizations for:
-FCFS
-SJF
-SRTF
-Round Robin (time quantum input)
-Priority Scheduling (both Preemptive & Non-Preemptive)

🎨 Theme
Switch Theme: Apply futuristic themes in real-time

## Project Structure
Virtual-File-System/
│
├── vfs_app.py              # Main GUI app (Neo UI)
├── vfs_core.py             # Core file logic & versioning
├── vfs_metadata.py         # Metadata indexing and file search
├── requirements.txt        # Python dependencies
├── vfs_root/               # Root directory of the virtual file system
└── assets/                 # (Optional) Icons, logos, splash media
### 🎨 Theme
Switch Theme: Apply futuristic themes in real-time

## Project Structure
### Virtual-File-System
- vfs_app.py              # Main GUI app (Neo UI)
- vfs_core.py             # Core file logic & versioning
- vfs_metadata.py         # Metadata indexing and file search
- requirements.txt        # Python dependencies
- vfs_root/               # Root directory of the virtual file system
- assets/                 # (Optional) Icons, logos, splash media

## Contributions
Contributions are welcome!
Feel free to fork the repo, open issues, or submit a pull request to suggest new features or enhancements.

