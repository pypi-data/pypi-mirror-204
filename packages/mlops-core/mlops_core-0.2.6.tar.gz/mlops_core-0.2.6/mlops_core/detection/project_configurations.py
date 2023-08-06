
import os
import re
import yaml
import json
import tomli
import configparser

from mlops_core.detection.project_structure import ProjectStructure

class ConfigLoader:
    def __init__(self, project: ProjectStructure) -> None:
        self.project = project

    def load_config(self, env: str):
        file_path = self.project.find_config_file(env)
        if file_path is None:
            raise ValueError(
                f"No environment detected for {env} in {self.project.get_environment_config_dir()}")

        # Check for filepath or throw an error
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check for file read permissions
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"File not readable: {file_path}")

        # Determine the file type based on the file extension
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            self.file_type = 'yaml'
        elif file_path.endswith('.toml'):
            self.file_type = 'toml'
        elif file_path.endswith('.ini'):
            self.file_type = 'ini'
        elif file_path.endswith('.json'):
            self.file_type = 'json'
        else:
            raise TypeError(f"File format not supported: {file_path}")

        # Load the config data from the file
        with open(file_path) as f:
            if self.file_type == 'yaml':
                self.config_data = yaml.safe_load(f)
            elif self.file_type == 'toml':
                self.config_data = tomli.loads(f.read())
            elif self.file_type == 'ini':
                config_parser = configparser.ConfigParser()
                config_parser.read_file(f)
                self.config_data = {section: dict(config_parser.items(
                    section)) for section in config_parser.sections()}
            elif self.file_type == 'json':
                self.config_data = json.load(f)

    def get_value(self, key: str):
        if self.is_valid_config_key(key) is False:
            raise ValueError("Invalid config key")
        if self.config_data is None:
            raise ValueError("Config data not loaded")
        if self.file_type == 'yaml' or self.file_type == 'json':
            return self.traverse_dict(self.config_data, key.split('.'))
        elif self.file_type == 'toml':
            return self.traverse_dict(self.config_data, key.split('.'))
        elif self.file_type == 'ini':
            section, option = key.split('.', maxsplit=1)
            return self.config_data.get(section, {}).get(option)

    @staticmethod
    def is_valid_config_key(key: str) -> bool:
        if key is None or key == "" or len(key) == 0:
            return False

        # Pattern allows any case alphanumeric values seperated by dots
        pattern = r'^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*$'

        return bool(re.match(pattern, key))

    @staticmethod
    def traverse_dict(data, keys):
        for key in keys:
            if isinstance(data, dict):
                if "." in key:
                    key_parts = key.split(".")
                    for part in key_parts:
                        data = data.get(part)
                        if data is None:
                            break
                else:
                    data = data.get(key)
                if data is None:
                    break
            elif isinstance(data, list):
                data = data[int(key)]
            else:
                return None
        return data

    @staticmethod
    def load(project: ProjectStructure, env: str):
        return ConfigLoader(project).load_config(env)
