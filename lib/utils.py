import toml
from pathlib import Path


def get_project_root() -> str:
    return str(Path(__file__).parent.parent)


def load_toml(name):
    return dict(toml.load(Path(get_project_root()) / f"{name}.toml"))