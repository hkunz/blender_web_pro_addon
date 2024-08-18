import json
import os

class PackageJson:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PackageJson, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self.file_path = None
        self.data = {}
        self.data_cache = {}
        self.initialized = True

    def clear_cache_all(self):
        for key in list(self.data_cache.keys()):
            del self.data_cache[key]

    def clear_cache(self, directory_path):
        """Clear the cached data for all files in the specified directory."""
        # Collect all file paths to remove from cache
        file_paths_to_remove = [fp for fp in self.data_cache.keys() if os.path.dirname(fp) == directory_path]

        for file_path in file_paths_to_remove:
            print(f"Clear package.json cache for {file_path}")
            del self.data_cache[file_path]
            if self.file_path and os.path.dirname(self.file_path) == directory_path:
                self.data = {}

    def load_data(self, file_path, force_reload=False):
        """Load JSON data from the file and cache it."""
        if not force_reload and file_path in self.data_cache:
            # print("Using package.json cache since it's already loaded for: ", file_path)
            self.data = self.data_cache[file_path]
            return

        if not os.path.isfile(file_path):
            # print(f"File not found: {file_path}")
            self.data = {}
            return

        try:
            with open(file_path, 'r') as file:
                print(f"Load package.json: {file_path}")
                self.data = json.load(file)
                self.data_cache[file_path] = self.data
        except json.JSONDecodeError:
            print("Error decoding JSON")
            self.data = {}

    def set_directory(self, new_directory, force_reload=False):
        """Switch to a new directory and load the package.json file if not cached."""
        new_file_path = os.path.join(new_directory, 'package.json')
        self.file_path = new_file_path
        self.load_data(new_file_path, force_reload)

    def get_dependency_version(self, package_name):
        dependencies = self.data.get('dependencies', {})
        return dependencies.get(package_name, None)

    def get_dev_dependency_version(self, package_name):
        dev_dependencies = self.data.get('devDependencies', {})
        return dev_dependencies.get(package_name, None)

    def get_threejs_version(self):
        return self.get_dependency_version("three")

    def get_vite_version(self):
        return self.get_dev_dependency_version("vite")

    def check_dependencies(self):
        three_version = self.get_dependency_version('three')
        if three_version:
            print(f"'three' found in dependencies with version: {three_version}")
        else:
            print("'three' not found in dependencies")

    def check_dev_dependencies(self):
        vite_version = self.get_dev_dependency_version('vite')
        if vite_version:
            print(f"'vite' found in devDependencies with version: {vite_version}")
        else:
            print("'vite' not found in devDependencies")

# Example usage:
#
# package_json = PackageJson()
# package_json.set_directory('/path/to/directory')
# package_json.set_directory('/path/to/another-directory')
