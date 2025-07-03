# Virtual File System

## Overview

The Virtual File System (VFS) is a Python-based simulation of a traditional file system, designed to emulate file management operations within a virtual environment. This project provides a command-line interface (CLI) for users to interact with the VFS, supporting various file operations such as creation, reading, writing, and deletion.

## Features

- **File Operations**: Create, read, write, and delete files within the virtual environment.
- **Directory Management**: Navigate through directories and manage directory structures.
- **Metadata Handling**: Maintain and retrieve metadata information for files and directories.
- **Persistence**: Save the state of the virtual file system to disk and load it upon initialization.

## Requirements

- **Python**: Ensure that Python is installed on your system. You can download it from the official [Python website](https://www.python.org/downloads/).

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

Once the application is running, you can use the following commands to interact with the VFS:

Set Shared Directory: Change the current directory.
Create File: Create a new file.
Update File: Update an existing file.
Read File: Read the content of a file.
Delete File: Delete a file.
Search File: Search an existing file and its details.
exit: Exit the virtual file system.

## Project Structure
vfs_app.py: Contains the main application logic and command-line interface.
vfs_core.py: Implements the core functionalities of the virtual file system.
vfs_metadata.py: Manages metadata related to files and directories.
requirements.txt: Lists the Python dependencies required for the project.
vfs_root/: Directory representing the root of the virtual file system.
Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.


