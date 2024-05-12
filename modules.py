import json
import importlib.abc
import importlib.util
import sys

class JSONFileFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if path is None:
            path = sys.path

        module_path = fullname + ".json"
        
        for dir_path in path:
            json_file_path = dir_path + "/" + module_path  # Assuming JSON files are in the same directory as Python files
            
            try:
                with open(json_file_path, "r") as json_file:
                    json_data = json.load(json_file)
                    module_spec = importlib.util.spec_from_loader(fullname, loader=None, origin=json_file_path)
                    module_spec.loader = JSONLoader(json_data)
                    return module_spec
            except FileNotFoundError:
                pass
        
        return None

class JSONLoader(importlib.abc.Loader):
    def __init__(self, json_data):
        self.json_data = json_data

    def create_module(self, spec):
        module = type(spec.name, (object,), {})
        for key, value in self.json_data.items():
            setattr(module, key, value)
        return module

    def exec_module(self, module):
        pass  # Nothing to execute since data is loaded directly into module

# Register the custom finder
sys.meta_path.append(JSONFileFinder())

# Usage example
import data  # Assuming there is a config.json file in the current directory
print(data.api_key)  # Accessing JSON data as if it were Python attributes
