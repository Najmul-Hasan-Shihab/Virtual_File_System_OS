### vfs_core.py
import os
import time
import shutil

class VFS:
    def __init__(self, root_directory=None):
        self.root_directory = root_directory or os.getcwd()

    def create_file(self, file_name, content=""):
        file_path = os.path.join(self.root_directory, file_name)
        with open(file_path, "w") as file:
            file.write(content)

    def read_file(self, file_name):
        file_path = os.path.join(self.root_directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read()
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    def update_file(self, file_name, content):
        file_path = os.path.join(self.root_directory, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_name}' does not exist.")
        # Ensure .versions directory exists
        versions_dir = os.path.join(self.root_directory, ".versions")
        os.makedirs(versions_dir, exist_ok=True)
        # Generate version file name
        base, ext = os.path.splitext(file_name)
        timestamp = time.strftime("%Y%m%d%H%M%S")
        version_filename = f"{base}_v{timestamp}{ext}"
        version_path = os.path.join(versions_dir, version_filename)
        # Copy current version to .versions before overwriting
        shutil.copy(file_path, version_path)
        # Overwrite the file with new content
        with open(file_path, "w") as file:
            file.write(content)

    def delete_file(self, file_name):
        file_path = os.path.join(self.root_directory, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"File '{file_name}' does not exist.")

    def search_files(self, file_name):
        file_path = os.path.join(self.root_directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                content = file.read()
            metadata = {
                "size": os.path.getsize(file_path),
                "creation_time": time.ctime(os.path.getctime(file_path)),
                "content": content,
            }
            return True, metadata
        return False, {}

    def set_root_directory(self, directory_path):
        if os.path.exists(directory_path):
            self.root_directory = directory_path
        else:
            raise ValueError(f"Provided directory '{directory_path}' does not exist.")

    def list_files(self):
        return [f for f in os.listdir(self.root_directory) if os.path.isfile(os.path.join(self.root_directory, f))]

    def get_file_versions(self, file_name):
        versions_dir = os.path.join(self.root_directory, ".versions")
        if not os.path.exists(versions_dir):
            return []
        base_name, ext = os.path.splitext(file_name)
        version_files = []
        for fname in os.listdir(versions_dir):
            if fname.startswith(base_name + "_v") and fname.endswith(ext):
                version_files.append(os.path.join(versions_dir, fname))
        return sorted(version_files)
