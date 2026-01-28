# pyright: reportMissingParameterType=false
"""Shared pytest fixtures for pdj-sitegen tests."""

import pytest
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from pdj_sitegen.config import Config


@pytest.fixture
def temp_site_structure(tmp_path):
	"""Create a minimal site structure for testing."""
	content_dir = tmp_path / "content"
	templates_dir = tmp_path / "templates"
	output_dir = tmp_path / "output"
	resources_dir = content_dir / "resources"

	for d in [content_dir, templates_dir, output_dir, resources_dir]:
		d.mkdir(parents=True)

	return {
		"root": tmp_path,
		"content_dir": content_dir,
		"templates_dir": templates_dir,
		"output_dir": output_dir,
		"resources_dir": resources_dir,
	}


@pytest.fixture
def default_template(temp_site_structure):
	"""Create a default HTML template."""
	template_path = temp_site_structure["templates_dir"] / "default.html.jinja2"
	template_path.write_text(
		"""<!DOCTYPE html>
<html>
<head><title>{{ frontmatter.title | default('Untitled') }}</title></head>
<body>{{ __content__ }}</body>
</html>"""
	)
	return template_path


@pytest.fixture
def basic_config(temp_site_structure):
	"""Create a basic Config for testing."""
	return Config(
		content_dir=temp_site_structure["content_dir"],
		templates_dir=temp_site_structure["templates_dir"],
		output_dir=temp_site_structure["output_dir"],
		default_template=Path("default.html.jinja2"),
	)


@pytest.fixture
def jinja_env(temp_site_structure):
	"""Create a Jinja2 Environment for testing."""
	return Environment(loader=FileSystemLoader(temp_site_structure["templates_dir"]))


@pytest.fixture
def sample_markdown_file(temp_site_structure):
	"""Create a sample markdown file with frontmatter."""
	md_file = temp_site_structure["content_dir"] / "sample.md"
	md_file.write_text(
		"""---
title: Sample Page
author: Test
---
# Sample Content

This is sample content.
"""
	)
	return md_file
