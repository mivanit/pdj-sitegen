# pyright: reportMissingParameterType=false
from pathlib import Path

import pdj_sitegen.setup_site
from pdj_sitegen.build import pipeline
from pdj_sitegen.setup_site import DEFAULT_CONFIG, FILE_LOCATIONS, RESOURCES_DIR, setup_site

TEMP_DIR: Path = Path("tests/_temp")


class TestFileLocations:
    """Tests for FILE_LOCATIONS constant."""

    def test_file_locations_contains_expected_files(self):
        """Test FILE_LOCATIONS contains all expected files."""
        expected_files = {
            "config.yml",
            "default.html.jinja2",
            "index.md",
            "style.css",
            "syntax.css",
        }
        assert set(FILE_LOCATIONS.keys()) == expected_files

    def test_file_locations_values_are_paths(self):
        """Test all FILE_LOCATIONS values are Path objects."""
        for key, path in FILE_LOCATIONS.items():
            assert isinstance(path, Path), f"{key} should map to Path"

    def test_config_path_is_root_level(self):
        """Test config.yml is at root level."""
        assert FILE_LOCATIONS["config.yml"] == Path("config.yml")

    def test_template_path_is_in_templates_dir(self):
        """Test template is in templates directory."""
        assert FILE_LOCATIONS["default.html.jinja2"].parent == DEFAULT_CONFIG.templates_dir

    def test_content_files_in_content_dir(self):
        """Test content files are in content directory."""
        assert FILE_LOCATIONS["index.md"].parent == DEFAULT_CONFIG.content_dir

    def test_resource_files_in_resources_dir(self):
        """Test resource files are in resources directory."""
        expected_parent = DEFAULT_CONFIG.content_dir / RESOURCES_DIR
        assert FILE_LOCATIONS["style.css"].parent == expected_parent
        assert FILE_LOCATIONS["syntax.css"].parent == expected_parent


class TestDefaultConfig:
    """Tests for DEFAULT_CONFIG constant."""

    def test_default_config_is_config_instance(self):
        """Test DEFAULT_CONFIG is a Config instance."""
        from pdj_sitegen.config import Config

        assert isinstance(DEFAULT_CONFIG, Config)

    def test_default_config_content_dir(self):
        """Test default content directory."""
        assert DEFAULT_CONFIG.content_dir == Path("content")

    def test_default_config_templates_dir(self):
        """Test default templates directory."""
        assert DEFAULT_CONFIG.templates_dir == Path("templates")

    def test_default_config_output_dir(self):
        """Test default output directory."""
        # DEFAULT_CONFIG is created from Config() class defaults, not from YAML
        assert DEFAULT_CONFIG.output_dir == Path("output")


class TestSetupSite:
    """Tests for setup_site function."""

    def test_setup_creates_all_files(self, tmp_path):
        """Test that setup_site creates all expected files."""
        setup_site(tmp_path)

        for file_name, rel_path in FILE_LOCATIONS.items():
            full_path = tmp_path / rel_path
            assert full_path.exists(), f"{file_name} should exist at {rel_path}"

    def test_setup_creates_parent_directories(self, tmp_path):
        """Test that parent directories are created."""
        setup_site(tmp_path)

        assert (tmp_path / "templates").is_dir()
        assert (tmp_path / "content").is_dir()
        assert (tmp_path / "content" / "resources").is_dir()

    def test_setup_file_contents_not_empty(self, tmp_path):
        """Test created files have content."""
        setup_site(tmp_path)

        for file_name, rel_path in FILE_LOCATIONS.items():
            full_path = tmp_path / rel_path
            content = full_path.read_text()
            assert len(content) > 0, f"{file_name} should not be empty"

    def test_setup_overwrites_existing_files(self, tmp_path):
        """Test that setup_site overwrites existing files."""
        config_path = tmp_path / "config.yml"
        config_path.write_text("old content")

        setup_site(tmp_path)

        new_content = config_path.read_text()
        assert new_content != "old content"

    def test_setup_with_nested_path(self, tmp_path):
        """Test setup_site with nested root path."""
        nested_root = tmp_path / "some" / "nested" / "path"
        setup_site(nested_root)

        assert (nested_root / "config.yml").exists()
        assert (nested_root / "templates" / "default.html.jinja2").exists()


# Original tests (kept for backwards compatibility)
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

	assert (root / "output" / "index.html").exists()
	assert (root / "output" / "resources" / "style.css").exists()
	assert (root / "output" / "resources" / "syntax.css").exists()
	assert (root / "output" / "resources" / "style.css").read_text() == (
		root / "content" / "resources" / "style.css"
	).read_text()
	assert (root / "output" / "resources" / "syntax.css").read_text() == (
		root / "content" / "resources" / "syntax.css"
	).read_text()
