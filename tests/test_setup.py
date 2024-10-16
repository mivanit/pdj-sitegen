from pathlib import Path

import pdj_sitegen.setup_site
from pdj_sitegen.build import pipeline

TEMP_DIR: Path = Path("tests/_temp")


def test_setup():
	root: Path = TEMP_DIR / "test_setup"
	root.mkdir(parents=True, exist_ok=True)
	pdj_sitegen.setup_site.setup_site(root)

	assert (root / "config.yml").exists()
	assert (root / "templates" / "default.html.jinja2").exists()
	assert (root / "content" / "index.md").exists()


def test_setup_and_pipeline():
	root: Path = TEMP_DIR / "test_setup_and_pipeline"
	root.mkdir(parents=True, exist_ok=True)
	pdj_sitegen.setup_site.setup_site(root)

	assert (root / "config.yml").exists()
	assert (root / "templates" / "default.html.jinja2").exists()
	assert (root / "content" / "index.md").exists()

	pipeline(
		config_path=root / "config.yml",
	)

	assert (root / "docs" / "index.html").exists()
	assert (root / "docs" / "resources" / "style.css").exists()
	assert (root / "docs" / "resources" / "syntax.css").exists()
	assert (root / "docs" / "resources" / "style.css").read_text() == (
		root / "content" / "resources" / "style.css"
	).read_text()
	assert (root / "docs" / "resources" / "syntax.css").read_text() == (
		root / "content" / "resources" / "syntax.css"
	).read_text()
