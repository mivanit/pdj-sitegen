"""CLI for scaffolding a new pdj-sitegen site.

Creates default configuration, templates, and content files to get started quickly.
Run with `python -m pdj_sitegen.setup_site [directory]` to scaffold a new site.
"""

import argparse
import importlib.resources
from pathlib import Path

import pdj_sitegen
from pdj_sitegen.config import Config

#: Default configuration instance used to determine output paths
DEFAULT_CONFIG: Config = Config()

#: Subdirectory for CSS and other static resources within content
RESOURCES_DIR: Path = Path("resources")

#: Mapping of source filenames (in package data) to their destination paths
FILE_LOCATIONS: dict[str, Path] = {
	"config.yml": Path("config.yml"),
	"default.html.jinja2": DEFAULT_CONFIG.templates_dir / "default.html.jinja2",
	"index.md": DEFAULT_CONFIG.content_dir / "index.md",
	"style.css": DEFAULT_CONFIG.content_dir / RESOURCES_DIR / "style.css",
	"syntax.css": DEFAULT_CONFIG.content_dir / RESOURCES_DIR / "syntax.css",
}


def setup_site(root: Path = Path(".")) -> None:  # pyright: ignore[reportCallInDefaultInitializer]
	"""Scaffold a new pdj-sitegen site with default files.

	Copies bundled template files from the package to the specified root directory,
	creating the necessary directory structure.

	# Parameters:
	 - `root : Path`
	   Root directory to create site files in. Defaults to current directory.

	# Creates:
	 - `config.yml` - default site configuration
	 - `templates/default.html.jinja2` - default HTML template
	 - `content/index.md` - sample index page
	 - `content/resources/style.css` - basic stylesheet
	 - `content/resources/syntax.css` - code syntax highlighting
	"""
	for file, path_rel in FILE_LOCATIONS.items():
		path: Path = root / path_rel
		if path.exists():
			print(f"Skipping existing file: {path}")
			continue

		contents: str = (
			importlib.resources.files(pdj_sitegen).joinpath("data", file).read_text()
		)
		path.parent.mkdir(parents=True, exist_ok=True)
		with open(path, "w", encoding="utf-8") as f:
			f.write(contents)


def main() -> None:
	"""CLI entry point for setup_site."""
	arg_parser: argparse.ArgumentParser = argparse.ArgumentParser(
		description="Set up a new pdj-sitegen site with default config and templates.",
		epilog=(
			"Creates:\n"
			"  config.yml                         - default configuration\n"
			"  templates/default.html.jinja2      - default HTML template\n"
			"  content/index.md                   - sample index page\n"
			"  content/resources/style.css        - basic stylesheet\n"
			"  content/resources/syntax.css       - code syntax highlighting"
		),
		formatter_class=argparse.RawDescriptionHelpFormatter,
	)
	arg_parser.add_argument(
		"root",
		type=str,
		nargs="?",
		default=".",
		help="root directory to create site files in (default: current directory)",
	)
	args: argparse.Namespace = arg_parser.parse_args()
	setup_site(Path(args.root))


if __name__ == "__main__":
	main()
