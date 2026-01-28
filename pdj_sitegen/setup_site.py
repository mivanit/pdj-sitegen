"cli for setting up a site"

import importlib.resources
from pathlib import Path

import pdj_sitegen
from pdj_sitegen.config import Config

DEFAULT_CONFIG: Config = Config()
RESOURCES_DIR: Path = Path("resources")

FILE_LOCATIONS: dict[str, Path] = {
	"config.yml": Path("config.yml"),
	"default.html.jinja2": DEFAULT_CONFIG.templates_dir / "default.html.jinja2",
	"index.md": DEFAULT_CONFIG.content_dir / "index.md",
	"style.css": DEFAULT_CONFIG.content_dir / RESOURCES_DIR / "style.css",
	"syntax.css": DEFAULT_CONFIG.content_dir / RESOURCES_DIR / "syntax.css",
}


def setup_site(root: Path = Path(".")) -> None:
	for file, path_rel in FILE_LOCATIONS.items():
		contents: str = (
			importlib.resources.files(pdj_sitegen).joinpath("data", file).read_text()
		)

		path: Path = root / path_rel
		path.parent.mkdir(parents=True, exist_ok=True)
		with open(path, "w", encoding="utf-8") as f:
			f.write(contents)


if __name__ == "__main__":
	import sys

	root: Path
	if len(sys.argv) == 1:
		root = Path(".")
	elif len(sys.argv) == 2:
		root = Path(sys.argv[1])
	else:
		raise ValueError(f"Too many arguments: {sys.argv}")

	setup_site(root)
