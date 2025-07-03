### vfs_metadata.py
import os
import time
import logging

class MetadataManager:
    def __init__(self, root_directory=None):
        self.root_directory = root_directory or os.getcwd()
        self.metadata_cache = self.index_files()

    def index_files(self):
        metadata = {}
        for root, _, files in os.walk(self.root_directory):
            for file in files:
                file_path = os.path.join(root, file)
                metadata[file_path] = self.get_metadata(file_path)
        return metadata

    def get_metadata(self, file_path):
        try:
            stats = os.stat(file_path)
            return {
                "size": stats.st_size,
                "creation_time": time.ctime(stats.st_ctime),
                "modification_time": time.ctime(stats.st_mtime),
            }
        except Exception as e:
            logging.error(f"Failed to fetch metadata for {file_path}: {e}")
            return {}

    def search_files(self, query, attribute="name"):
        results = []
        for file_path, meta in self.metadata_cache.items():
            if attribute == "name" and query.lower() in os.path.basename(file_path).lower():
                results.append((file_path, meta))
            elif attribute in meta and query.lower() in str(meta[attribute]).lower():
                results.append((file_path, meta))
        return results

    def refresh_cache(self):
        self.metadata_cache = self.index_files()

    def format_metadata(self, file_path, meta):
        return (
            f"File: {os.path.basename(file_path)}\n"
            f"Path: {file_path}\n"
            f"Size: {meta.get('size')} bytes\n"
            f"Created: {meta.get('creation_time')}\n"
            f"Modified: {meta.get('modification_time')}\n"
        )
