# pyright: reportMissingParameterType=false
import os
from pathlib import Path

import pytest
from jinja2 import Environment

from pdj_sitegen.config import Config

os.makedirs("tests/_temp", exist_ok=True)


# Tests for render function
class TestRender:
    """Tests for the render function."""

    def test_render_simple_template(self):
        """Test rendering a simple template."""
        from pdj_sitegen.build import render

        jinja_env = Environment()
        content = "Hello, {{ name }}!"
        context = {"name": "World"}
        result = render(content, context, jinja_env)
        assert result == "Hello, World!"

    def test_render_with_conditionals(self):
        """Test rendering with conditionals."""
        from pdj_sitegen.build import render

        jinja_env = Environment()
        content = "{% if show %}Visible{% endif %}"
        result = render(content, {"show": True}, jinja_env)
        assert result == "Visible"
        result = render(content, {"show": False}, jinja_env)
        assert result == ""

    def test_render_with_loops(self):
        """Test rendering with loops."""
        from pdj_sitegen.build import render

        jinja_env = Environment()
        content = "{% for item in items %}{{ item }},{% endfor %}"
        result = render(content, {"items": ["a", "b", "c"]}, jinja_env)
        assert result == "a,b,c,"

    def test_render_error_invalid_template(self):
        """Test that invalid template syntax raises RenderError."""
        from pdj_sitegen.build import render
        from pdj_sitegen.exceptions import RenderError

        jinja_env = Environment()
        content = "{{ unclosed"
        with pytest.raises(RenderError) as exc_info:
            render(content, {}, jinja_env)
        assert exc_info.value.kind == "create_template"

    def test_render_error_undefined_variable_method(self):
        """Test that calling method on undefined variable raises RenderError."""
        from pdj_sitegen.build import render
        from pdj_sitegen.exceptions import RenderError

        jinja_env = Environment()
        content = "{{ undefined_var.method() }}"
        with pytest.raises(RenderError) as exc_info:
            render(content, {}, jinja_env)
        assert exc_info.value.kind == "render_template"


# Tests for build_document_tree function
class TestBuildDocumentTree:
    """Tests for the build_document_tree function."""

    def test_empty_directory(self, tmp_path):
        """Test with no markdown files."""
        from pdj_sitegen.build import build_document_tree

        jinja_env = Environment()
        result = build_document_tree(
            content_dir=tmp_path,
            frontmatter_context={},
            jinja_env=jinja_env,
            verbose=False,
        )
        assert result == {}

    def test_single_markdown_file(self, tmp_path):
        """Test with one markdown file."""
        from pdj_sitegen.build import build_document_tree

        md_file = tmp_path / "test.md"
        md_file.write_text("---\ntitle: Test\n---\nBody content")

        jinja_env = Environment()
        result = build_document_tree(
            content_dir=tmp_path,
            frontmatter_context={},
            jinja_env=jinja_env,
            verbose=False,
        )

        assert "test" in result
        assert result["test"]["frontmatter"]["title"] == "Test"
        assert result["test"]["body"] == "Body content"
        assert "file_meta" in result["test"]

    def test_nested_markdown_files(self, tmp_path):
        """Test with nested directory structure."""
        from pdj_sitegen.build import build_document_tree

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "root.md").write_text("---\ntitle: Root\n---\nRoot body")
        (subdir / "nested.md").write_text("---\ntitle: Nested\n---\nNested body")

        jinja_env = Environment()
        result = build_document_tree(
            content_dir=tmp_path,
            frontmatter_context={},
            jinja_env=jinja_env,
            verbose=False,
        )

        assert "root" in result
        assert "subdir/nested" in result

    def test_file_meta_structure(self, tmp_path):
        """Test that file_meta contains expected keys."""
        from pdj_sitegen.build import build_document_tree

        md_file = tmp_path / "test.md"
        md_file.write_text("---\ntitle: Test\n---\nBody")

        jinja_env = Environment()
        result = build_document_tree(
            content_dir=tmp_path,
            frontmatter_context={},
            jinja_env=jinja_env,
            verbose=False,
        )

        file_meta = result["test"]["file_meta"]
        assert "path" in file_meta
        assert "path_html" in file_meta
        assert "path_raw" in file_meta
        assert "modified_time" in file_meta
        assert "modified_time_str" in file_meta
        assert file_meta["path"] == "test"
        assert file_meta["path_html"] == "test.html"

    def test_frontmatter_with_jinja_templates(self, tmp_path):
        """Test frontmatter rendering with Jinja2."""
        from pdj_sitegen.build import build_document_tree

        md_file = tmp_path / "test.md"
        md_file.write_text("---\ntitle: {{ config.name }}\n---\nBody")

        jinja_env = Environment()
        result = build_document_tree(
            content_dir=tmp_path,
            frontmatter_context={"config": {"name": "MySite"}},
            jinja_env=jinja_env,
            verbose=False,
        )

        assert result["test"]["frontmatter"]["title"] == "MySite"

    def test_json_frontmatter(self, tmp_path):
        """Test JSON frontmatter format."""
        from pdj_sitegen.build import build_document_tree

        md_file = tmp_path / "test.md"
        md_file.write_text(';;;\n{"title": "JSON Test"}\n;;;\nBody')

        jinja_env = Environment()
        result = build_document_tree(
            content_dir=tmp_path,
            frontmatter_context={},
            jinja_env=jinja_env,
            verbose=False,
        )

        assert result["test"]["frontmatter"]["title"] == "JSON Test"

    def test_toml_frontmatter(self, tmp_path):
        """Test TOML frontmatter format."""
        from pdj_sitegen.build import build_document_tree

        md_file = tmp_path / "test.md"
        md_file.write_text('+++\ntitle = "TOML Test"\n+++\nBody')

        jinja_env = Environment()
        result = build_document_tree(
            content_dir=tmp_path,
            frontmatter_context={},
            jinja_env=jinja_env,
            verbose=False,
        )

        assert result["test"]["frontmatter"]["title"] == "TOML Test"

    def test_multiple_files_same_level(self, tmp_path):
        """Test multiple markdown files at the same level."""
        from pdj_sitegen.build import build_document_tree

        (tmp_path / "a.md").write_text("---\ntitle: A\n---\nBody A")
        (tmp_path / "b.md").write_text("---\ntitle: B\n---\nBody B")
        (tmp_path / "c.md").write_text("---\ntitle: C\n---\nBody C")

        jinja_env = Environment()
        result = build_document_tree(
            content_dir=tmp_path,
            frontmatter_context={},
            jinja_env=jinja_env,
            verbose=False,
        )

        assert len(result) == 3
        assert result["a"]["frontmatter"]["title"] == "A"
        assert result["b"]["frontmatter"]["title"] == "B"
        assert result["c"]["frontmatter"]["title"] == "C"


# Tests for dump_intermediate function
class TestDumpIntermediate:
    """Tests for the dump_intermediate function."""

    def test_no_dump_when_dir_is_none(self, tmp_path):
        """Test that nothing is written when intermediates_dir is None."""
        from pdj_sitegen.build import dump_intermediate

        dump_intermediate(
            content="test content",
            intermediates_dir=None,
            fmt="md",
            path="test",
        )
        # Should not raise, should just do nothing
        # Verify no files were created anywhere
        assert not any(tmp_path.iterdir())

    def test_dump_creates_file(self, tmp_path):
        """Test that intermediate file is created."""
        from pdj_sitegen.build import dump_intermediate

        dump_intermediate(
            content="test content",
            intermediates_dir=tmp_path,
            fmt="md",
            path="test",
        )

        output_file = tmp_path / "md" / "test.md"
        assert output_file.exists()
        assert output_file.read_text() == "test content"

    def test_dump_nested_path(self, tmp_path):
        """Test dump with nested path creates parent directories."""
        from pdj_sitegen.build import dump_intermediate

        dump_intermediate(
            content="nested content",
            intermediates_dir=tmp_path,
            fmt="html",
            path="subdir/nested",
        )

        output_file = tmp_path / "html" / "subdir" / "nested.html"
        assert output_file.exists()
        assert output_file.read_text() == "nested content"

    def test_dump_different_formats(self, tmp_path):
        """Test dumping different file formats."""
        from pdj_sitegen.build import dump_intermediate

        formats = ["md", "html", "txt", "json"]
        for fmt in formats:
            dump_intermediate(
                content=f"content for {fmt}",
                intermediates_dir=tmp_path,
                fmt=fmt,
                path="test",
            )
            output_file = tmp_path / fmt / f"test.{fmt}"
            assert output_file.exists()
            assert output_file.read_text() == f"content for {fmt}"


# Tests for process_pandoc_args edge cases
class TestProcessPandocArgsEdgeCases:
    """Additional edge case tests for process_pandoc_args."""

    def test_bool_false_excluded(self):
        """Test that False boolean values are excluded."""
        from pdj_sitegen.build import process_pandoc_args

        args = {"toc": False, "mathjax": True}
        result = process_pandoc_args(args)
        assert "--toc" not in result
        assert "--mathjax" in result

    def test_empty_dict(self):
        """Test with empty dict."""
        from pdj_sitegen.build import process_pandoc_args

        result = process_pandoc_args({})
        assert result == []

    def test_invalid_type_raises(self):
        """Test that invalid types raise ValueError."""
        from pdj_sitegen.build import process_pandoc_args

        with pytest.raises(ValueError, match="Invalid type"):
            process_pandoc_args({"invalid": 42})

    def test_single_filter_string(self):
        """Test single filter as string."""
        from pdj_sitegen.build import process_pandoc_args

        args = {"filter": "my_filter"}
        result = process_pandoc_args(args)
        assert result == ["--filter", "my_filter"]

    def test_builtin_filter_single_string(self):
        """Test builtin filter resolution with single string."""
        from pdj_sitegen.build import process_pandoc_args

        args = {"filter": "csv_code_table"}
        result = process_pandoc_args(args)
        assert result == ["--filter", "pdj-csv-code-table"]


# Tests for should_copy function
def test_should_copy_default_behavior():
	"""Test default behavior: copy everything except what's excluded."""
	from pdj_sitegen.build import should_copy

	# Default: empty include, exclude *.md
	include: list[str] = []
	exclude = ["*.md"]

	assert should_copy("style.css", include, exclude) is True
	assert should_copy("script.js", include, exclude) is True
	assert should_copy("images/logo.png", include, exclude) is True
	assert should_copy("index.md", include, exclude) is False
	assert should_copy("blog/post.md", include, exclude) is False


def test_should_copy_include_wins():
	"""Test that explicit include overrides exclude."""
	from pdj_sitegen.build import should_copy

	# Include *.md, but also exclude *.md - include should win
	include = ["*.md"]
	exclude = ["*.md"]

	assert should_copy("index.md", include, exclude) is True
	assert should_copy("style.css", include, exclude) is False  # Not in include


def test_should_copy_specific_includes():
	"""Test copying only specific file types."""
	from pdj_sitegen.build import should_copy

	include = ["*.css", "*.js"]
	exclude: list[str] = []

	assert should_copy("style.css", include, exclude) is True
	assert should_copy("script.js", include, exclude) is True
	assert should_copy("image.png", include, exclude) is False
	assert should_copy("index.md", include, exclude) is False


def test_should_copy_complex_exclude():
	"""Test complex exclusion patterns."""
	from pdj_sitegen.build import should_copy

	include: list[str] = []
	exclude = ["*.md", "*.tmp", ".git*"]

	assert should_copy("style.css", include, exclude) is True
	assert should_copy("index.md", include, exclude) is False
	assert should_copy("temp.tmp", include, exclude) is False
	assert should_copy(".gitignore", include, exclude) is False


def test_copy_content_files(tmp_path):
	"""Test copying content files with patterns."""
	from pdj_sitegen.build import copy_content_files

	content_dir = tmp_path / "content"
	output_dir = tmp_path / "output"
	content_dir.mkdir()
	output_dir.mkdir()

	# Create test files
	(content_dir / "index.md").write_text("# Index")
	(content_dir / "style.css").write_text("body {}")
	(content_dir / "script.js").write_text("console.log('hi')")
	(content_dir / "images").mkdir()
	(content_dir / "images" / "logo.png").write_bytes(b"PNG")

	# Run with default patterns (copy all except *.md)
	count = copy_content_files(
		content_dir=content_dir,
		output_dir=output_dir,
		include=[],
		exclude=["*.md"],
		verbose=False,
	)

	assert count == 3  # css, js, png
	assert not (output_dir / "index.md").exists()
	assert (output_dir / "style.css").exists()
	assert (output_dir / "script.js").exists()
	assert (output_dir / "images" / "logo.png").exists()


def test_config_read_toml(tmp_path):
	"""Test reading config from TOML file."""
	config_toml = tmp_path / "config.toml"
	config_toml.write_text('''
content_dir = "my_content"
output_dir = "my_output"
templates_dir = "my_templates"
default_template = "base.html.jinja2"
copy_include = []
copy_exclude = ["*.md", "*.tmp"]

[globals_]
site_name = "Test Site"

[__pandoc__]
mathjax = true
toc = true
''')

	loaded_config = Config.read(config_toml)
	assert loaded_config.content_dir == Path("my_content")
	assert loaded_config.output_dir == Path("my_output")
	assert loaded_config.globals_["site_name"] == "Test Site"
	assert loaded_config.__pandoc__["toc"] is True
	assert loaded_config.copy_exclude == ["*.md", "*.tmp"]


# Additional tests for main functionality
def test_split_md():
	from pdj_sitegen.build import split_md

	content = """---
title: Test
---
This is the body."""

	frontmatter, body, fmt = split_md(content)
	assert frontmatter == "title: Test"
	assert body == "This is the body."
	assert fmt == "yaml"


def test_process_pandoc_args():
	from pdj_sitegen.build import process_pandoc_args

	args = {
		"toc": True,
		"variable": "key=value",
		"filter": ["filter1", "filter2"],
	}

	result = process_pandoc_args(args)
	assert result == [
		"--toc",
		"--variable",
		"key=value",
		"--filter",
		"filter1",
		"--filter",
		"filter2",
	]


def test_resolve_filter():
	from pdj_sitegen.build import resolve_filter

	# Simple names resolve to entry points
	assert resolve_filter("csv_code_table") == "pdj-csv-code-table"
	assert resolve_filter("links_md2html") == "pdj-links-md2html"

	# Full module paths resolve to entry points
	assert resolve_filter("pdj_sitegen.filters.csv_code_table") == "pdj-csv-code-table"
	assert resolve_filter("pdj_sitegen.filters.links_md2html") == "pdj-links-md2html"

	# External filters pass through unchanged
	assert resolve_filter("some_external_filter") == "some_external_filter"
	assert resolve_filter("/path/to/filter.py") == "/path/to/filter.py"


def test_process_pandoc_args_with_builtin_filters():
	from pdj_sitegen.build import process_pandoc_args

	args = {
		"filter": ["csv_code_table", "some_external_filter"],
	}

	result = process_pandoc_args(args)
	assert result == [
		"--filter",
		"pdj-csv-code-table",  # resolved
		"--filter",
		"some_external_filter",  # passed through
	]


# Test for convert_single_markdown_file and convert_markdown_files
def test_convert_markdown_files(tmp_path, monkeypatch):
	from jinja2 import Environment, FileSystemLoader

	from pdj_sitegen.build import convert_markdown_files

	# Setup test environment
	content_dir = tmp_path / "content"
	output_dir = tmp_path / "output"
	templates_dir = tmp_path / "templates"
	content_dir.mkdir()
	output_dir.mkdir()
	templates_dir.mkdir()

	# Create a test markdown file
	test_md = content_dir / "test.md"
	test_md.write_text(
		"""---
title: Test Page
---
# Test Content
This is a test."""
	)

	# Create a test template
	template = templates_dir / "default.html.jinja2"
	template.write_text(
		"""<!DOCTYPE html>
<html>
<head><title>{{ frontmatter.title }}</title></head>
<body>{{ __content__ }}</body>
</html>"""
	)

	# Setup config
	config = Config(
		content_dir=content_dir,
		output_dir=output_dir,
		templates_dir=templates_dir,
		default_template=Path("default.html.jinja2"),
	)

	# Setup Jinja environment
	jinja_env = Environment(loader=FileSystemLoader(templates_dir))

	# Mock build_document_tree function
	def mock_build_document_tree(*args, **kwargs):
		return {
			"test": {
				"frontmatter": {"title": "Test Page"},
				"body": "# Test Content\nThis is a test.",
				"file_meta": {
					"path": "test",
					"path_html": "test.html",
					"path_raw": str(test_md),
					"modified_time": test_md.stat().st_mtime,
				},
			}
		}

	monkeypatch.setattr(
		"pdj_sitegen.build.build_document_tree", mock_build_document_tree
	)

	# Run the conversion
	docs = mock_build_document_tree()
	convert_markdown_files(
		docs=docs,
		jinja_env=jinja_env,
		config=config,
		output_root=tmp_path,
		smart_rebuild=False,
		rebuild_time=0,
		verbose=True,
	)

	# Check if the output file was created
	output_file = output_dir / "test.html"
	assert output_file.exists()

	# Check the content of the output file
	content = output_file.read_text()
	assert "<title>Test Page</title>" in content
	assert '<h1 id="test-content">Test Content</h1>' in content
	assert "<p>This is a test.</p>" in content


# Test for main function
def test_main(monkeypatch):
	from pdj_sitegen.build import main

	tmp_path = Path("tests/_temp/test_main/")
	# Setup test environment
	config_path = tmp_path / "config.yaml"
	content_dir = tmp_path / "content"
	output_dir = tmp_path / "output"
	templates_dir = tmp_path / "templates"

	for d in [content_dir, output_dir, templates_dir]:
		d.mkdir(parents=True, exist_ok=True)
	resources_dir_absolute = content_dir / "resources"
	resources_dir_absolute.mkdir(parents=True, exist_ok=True)

	# Create a test config file
	config = Config()
	config.save(config_path, "yaml")

	# Create a test markdown file
	test_md = content_dir / "test.md"
	test_md.write_text(
		"""---
title: Test Page
---
# Test Content
This is a test."""
	)

	# Create a test template
	template = templates_dir / "default.html.jinja2"
	template.write_text(
		"""<!DOCTYPE html>
<html>
<head><title>{{ frontmatter.title }}</title></head>
<body>{{ __content__ }}</body>
</html>"""
	)

	# Create a test resource file
	resource_file = resources_dir_absolute / "style.css"
	resource_file.write_text("body { font-family: Arial, sans-serif; }")

	# Mock sys.argv
	monkeypatch.setattr("sys.argv", ["pdj_sitegen", str(config_path)])

	# Run the main function
	main()

	# Check if the output file was created
	output_file = output_dir / "test.html"
	assert output_file.exists()

	# Check the content of the output file
	content = output_file.read_text()
	assert "<title>Test Page</title>" in content
	assert '<h1 id="test-content">Test Content</h1>' in content
	assert "<p>This is a test.</p>" in content

	# Check if the resource file was copied
	copied_resource = output_dir / "resources" / "style.css"
	assert copied_resource.exists()
	assert copied_resource.read_text() == "body { font-family: Arial, sans-serif; }"
