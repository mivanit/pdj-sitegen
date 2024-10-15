"cli for setting up a site"

from pathlib import Path
import importlib.resources

import pdj_sitegen

def setup_site(root: Path = ".") -> None:

	config_yaml: str = importlib.resources.read_text(
		pdj_sitegen,
		"data/config.yaml",
		encoding='utf-8',
	)

	default_template: str = importlib.resources.read_text(
		pdj_sitegen,
		"data/default.html.jinja2",
		encoding='utf-8',
	)

	default_index: str = importlib.resources.read_text(
		pdj_sitegen,
		"data/index.md",
		encoding='utf-8',
	)

	with open(root / "config.yaml", "w", encoding="utf-8") as f:
		f.write(config_yaml)

	with open(root / "templates/default.html.jinja2", "w", encoding="utf-8") as f:
		f.write(default_template)

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