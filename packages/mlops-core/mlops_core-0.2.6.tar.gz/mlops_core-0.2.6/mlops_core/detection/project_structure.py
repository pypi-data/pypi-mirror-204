import os

from mlops_core.utils.strings import to_snake_case

class ProjectStructure():
    """
    This class is used to detect the project structure and create the required directories.
    The project structure is as follows:
    - .github
        - pull_request_template.md
    - .vscode
        - tasks.json
    - files
        - config
            - environment
                - {dev,preprod,prod}.{yaml,yml,json,toml,ini}
            - databricks
                - backend_config.json
            - ml_workspace
                - backend_config.json
        - data
        - sql
    - source_packages
        - ingestion.py
        - feature_engineering.py
        - training.py
        - evaluation.py
        - publish.pys
    - research
        - 01_EDA
        - 02_feature_engineering
        - 03_modeling
        - 04_evaluation
        - 05_deployment
    - tests
    """

    def __init__(self, project_root: str, project_name: str = None):
        self.project_root = project_root
        if project_name is None:
            self.project_name = os.path.basename(project_root)
        else:
            self.project_name = project_name

    def get_files_dir(self) -> str:
        return os.path.join(self.project_root, "files")

    def get_data_dir(self) -> str:
        return os.path.join(self.project_root, "files/data")

    def get_sql_dir(self) -> str:
        return os.path.join(self.project_root, "files/sql")

    def get_config_dir(self) -> str:
        return os.path.join(self.project_root, "files/config")

    def get_environment_config_dir(self) -> str:
        return os.path.join(self.project_root, "files/config/environment")

    def get_databricks_config_dir(self) -> str:
        return os.path.join(self.project_root, "files/config/databricks")

    def get_AML_config_dir(self) -> str:
        return os.path.join(self.project_root, "files/config/ml_workspace")

    def get_source_packages_dir(self) -> str:
        return os.path.join(self.project_root, to_snake_case(self.project_name))

    def get_research_dir(self) -> str:
        return os.path.join(self.project_root, "research")

    def get_tests_dir(self) -> str:
        return os.path.join(self.project_root, "tests")

    def databricks_config_dir_exists(self) -> bool:
        return os.path.exists(self.get_databricks_config_dir())

    def AML_config_dir_exists(self) -> bool:
        return os.path.exists(self.get_AML_config_dir())

    def config_dir_exists(self) -> bool:
        return os.path.exists(self.get_config_dir())

    def files_dir_exists(self) -> bool:
        return os.path.exists(self.get_files_dir())

    def sql_dir_exists(self) -> bool:
        return os.path.exists(self.get_sql_dir())

    def source_packages_dir_exists(self) -> bool:
        return os.path.exists(self.get_source_packages_dir())

    def environment_config_dir_exists(self) -> bool:
        return os.path.exists(self.get_environment_config_dir())

    def data_dir_exists(self) -> bool:
        return os.path.exists(self.get_data_dir())

    def detected_environment_configs(self) -> list:
        environments = {
            "dev": ["dev", "development", "local", "sandbox"],
            "preprod": ["test", "qa", "staging", "preprod", "nonprod"],
            "prod": ["prod", "production", "live", "release"]
        }
        formats = ["yaml", "yml", "json", "toml", "ini"]
        matching_files = []
        if not self.environment_config_dir_exists():
            return matching_files
        for root, _, files in os.walk(self.get_environment_config_dir()):
            for file in files:
                for env, names in environments.items():
                    if any(name in file for name in names) and file.endswith(tuple(formats)):
                        matching_files.append(env)
        return matching_files

    def find_config_file(self, env: str) -> str:
        if not self.environment_config_dir_exists():
            return None
        for root, _, files in os.walk(self.get_environment_config_dir()):
            for file in files:
                if file.startswith(env) and file.endswith(tuple(['yaml', 'yml', 'json', 'toml', 'ini'])):
                    return os.path.join(root, file)
        return None
