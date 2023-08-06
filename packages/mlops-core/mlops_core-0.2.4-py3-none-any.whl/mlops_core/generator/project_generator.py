import os
from abc import ABC, abstractmethod

from jinja2 import Template

from mlops_core.utils.strings import to_snake_case
from mlops_core.detection.project_structure import ProjectStructure

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class ProjectStrategy(ABC):
    def __init__(self, project_root: str, project_name: str, template_flavour: str) -> None:
        super().__init__()
        self.project_root = project_root
        if project_name is None:
            self.project_name = os.path.basename(project_root)
        else:
            self.project_name = project_name
        self.template_flavour = template_flavour
        self.structure = ProjectStructure(self.project_root)

    def get_templates_dir(self) -> str:
        template_dir = os.path.realpath(
            os.path.join(CURRENT_DIR, "../../templates"))
        return template_dir

    def define_context(self) -> dict:
        return {
            "project_name": self.project_name,
            **dict(os.environ)
        }

    def render_all(self, file_map: dict, context: dict):
        for template_name, output_path in file_map.items():
            template_file = os.path.join(
                self.get_templates_dir(), template_name)
            output_file = os.path.join(self.project_root, output_path)
            self.render(template_file, output_file, context)

    def render(self, template_file: str, output_file: str, context: dict):
        # Check to see if the template file exists
        if not os.path.exists(template_file):
            raise FileNotFoundError(
                f"Template file {template_file} does not exist")
        # Check to see if the output directory exists
        if not os.path.exists(os.path.dirname(output_file)):
            # Create it if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Render the template
        Template(open(template_file).read()).stream(
            **context).dump(output_file)

        print(f"rendered: {output_file}")

    def create_dir(self, directory: str, relative_to_project_root: bool = True):
        if relative_to_project_root:
            dir = os.path.join(self.project_root, directory)
            if not os.path.exists(dir):
                os.makedirs(dir, exist_ok=True)
            print(f"created: {dir}")
        else:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            print(f"created: {directory}")

    def create_directory(self, dir_to_create: list):
        for directory in dir_to_create:
            self.create_dir(directory)

    def generate_github_configs(self):
        templates_to_render = {
            "ISSUE_TEMPLATE.md.jinja": ".github/ISSUE_TEMPLATE.md",
            "PULL_REQUEST_TEMPLATE.md.jinja": ".github/PULL_REQUEST_TEMPLATE.md",
        }
        self.render_all(templates_to_render, self.define_context())

    def generate_devcontainer_config(self):
        templates_to_render = {
            "devcontainer.json": ".devcontainer/devcontainer.json",
        }
        self.render_all(templates_to_render, self.define_context())

    def generate_default_packages(self):
        self.create_dir(self.structure.get_source_packages_dir(),
                        relative_to_project_root=False)
        self.create_dir(self.structure.get_tests_dir(),
                        relative_to_project_root=False)

    def generate_readme(self):
        templates_to_render = {
            "README.md.jinja": "README.md",
        }
        self.render_all(templates_to_render, self.define_context())

    @abstractmethod
    def generate(self, preview: bool = False):
        print(
            f"Generating project structure for {self.project_name} using default flavour in {'preview' if preview else 'regular'} mode")
        self.generate_readme()


class ProjectGeneratorFactory():
    @staticmethod
    def create(project_root: str, project_name: str = None, template_flavour: str = "default"):
        if template_flavour == "default":
            return DefaultProject(project_root=project_root, project_name=project_name)
        elif template_flavour == "model-development":
            return ModelDevelopmentProject(project_root=project_root, project_name=project_name)
        else:
            raise NotImplementedError(
                f"Project Generator for {template_flavour} is not implemented")


class DefaultProject(ProjectStrategy):
    def __init__(self, project_root: str, project_name: str = None) -> None:
        super().__init__(project_root=project_root,
                         project_name=project_name, template_flavour="default")

    def generate(self, preview: bool = False):
        super().generate(preview)
        self.generate_github_configs()
        self.generate_devcontainer_config()
        self.generate_default_packages()


class ModelDevelopmentProject(ProjectStrategy):
    def __init__(self, project_root: str, project_name: str = None) -> None:
        super().__init__(project_root=project_root,
                         project_name=project_name, template_flavour="model-development")

    def generate_configuration_directories(self):
        self.create_dir(self.structure.get_files_dir(),
                        relative_to_project_root=False)
        self.create_dir(self.structure.get_config_dir(),
                        relative_to_project_root=False)
        self.create_dir(self.structure.get_data_dir(),
                        relative_to_project_root=False)
        self.create_dir(self.structure.get_databricks_config_dir(),
                        relative_to_project_root=False)
        self.create_dir(self.structure.get_AML_config_dir(),
                        relative_to_project_root=False)
        self.create_dir(self.structure.get_environment_config_dir(),
                        relative_to_project_root=False)

    def generate_source_code(self):
        package_name = to_snake_case(self.structure.project_name)
        template_to_render = {
            "src/ingestion.py.jinja": f"{package_name}/ingestion.py",
            "src/train.py.jinja": f"{package_name}/train.py",
            "src/evaluate.py.jinja": f"{package_name}/evaluate.py",
        }
        self.render_all(template_to_render, self.define_context())

    def generate(self, preview: bool = False):
        super().generate(preview)
        self.generate_github_configs()
        self.generate_devcontainer_config()
        self.generate_default_packages()
        self.generate_configuration_directories()
        self.generate_source_code()
