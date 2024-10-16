"cli for setting up a site"

import importlib.resources
from pathlib import Path

import pdj_sitegen


def setup_site(root: Path = ".") -> None:
	config_yaml: str = (
		importlib.resources.files(pdj_sitegen)
		.joinpath("data", "config.yml")
		.read_text()
	)

	default_template: str = (
		importlib.resources.files(pdj_sitegen)
		.joinpath("data", "default.html.jinja2")
		.read_text()
	)

	default_index: str = (
		importlib.resources.files(pdj_sitegen).joinpath("data", "index.md").read_text()
	)

	root.mkdir(parents=True, exist_ok=True)
	with open(root / "config.yaml", "w", encoding="utf-8") as f:
		f.write(config_yaml)

	(root / "templates").mkdir(exist_ok=True)
	with open(root / "templates/default.html.jinja2", "w", encoding="utf-8") as f:
		f.write(default_template)

	(root / "content").mkdir(exist_ok=True)
	(root / "content" / "resources").mkdir(exist_ok=True)
	with open(root / "content/index.md", "w", encoding="utf-8") as f:
		f.write(default_index)


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
