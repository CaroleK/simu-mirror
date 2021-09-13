import toml
from pathlib import Path


def get_project_root() -> str:
    return str(Path(__file__).parent.parent)


def load_config():
    return dict(toml.load(Path(get_project_root()) / "config.toml"))