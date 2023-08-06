from mlops_core.generator.project_generator import ProjectGeneratorFactory


def generate_project(project_root, project_name: str = None, preview: bool = True, flavour: str = "default") -> bool:
    generator = ProjectGeneratorFactory.create(
        project_root, project_name, flavour)
    generator.generate(preview=preview)
