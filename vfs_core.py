### vfs_core.py
import os
import time

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
        if os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write(content)
        else:
            raise FileNotFoundError(f"File '{file_name}' does not exist.")

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
