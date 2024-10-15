import pytest
import os
import shutil
from pathlib import Path
import json
import yaml
import tomllib
from datetime import datetime, timedelta

from pdj_sitegen.config import Config
from pdj_sitegen.consts import FORMAT_MAP, FORMAT_PARSERS, FRONTMATTER_DELIMS, FRONTMATTER_REGEX
import pdj_sitegen.consts as consts
import pdj_sitegen.config as pdjsg_config

os.makedirs("tests/_temp", exist_ok=True)

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
    assert result == ["--toc", "--variable", "key=value", "--filter", "filter1", "--filter", "filter2"]

# Test for convert_single_markdown_file and convert_markdown_files
def test_convert_markdown_files(tmp_path, monkeypatch):
    from pdj_sitegen.build import convert_markdown_files, convert_single_markdown_file
    from jinja2 import Environment, FileSystemLoader
    
    # Setup test environment
    content_dir = tmp_path / "content"
    output_dir = tmp_path / "output"
    templates_dir = tmp_path / "templates"
    content_dir.mkdir()
    output_dir.mkdir()
    templates_dir.mkdir()
    
    # Create a test markdown file
    test_md = content_dir / "test.md"
    test_md.write_text("""---
title: Test Page
---
# Test Content
This is a test.""")
    
    # Create a test template
    template = templates_dir / "default.html.jinja2"
    template.write_text("""<!DOCTYPE html>
<html>
<head><title>{{ frontmatter.title }}</title></head>
<body>{{ __content__ }}</body>
</html>""")
    
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
                    "modified_time": test_md.stat().st_mtime
                }
            }
        }
    
    monkeypatch.setattr("pdj_sitegen.build.build_document_tree", mock_build_document_tree)
    
    # Run the conversion
    docs = mock_build_document_tree()
    convert_markdown_files(docs, jinja_env, config, False, 0)
    
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
    resources_dir = Path("resources")
    
    for d in [content_dir, output_dir, templates_dir]:
        d.mkdir(parents=True, exist_ok=True)
    resources_dir_absolute = content_dir / "resources"
    resources_dir_absolute.mkdir(parents=True, exist_ok=True)
    
    # Create a test config file
    config = Config(
        content_dir=content_dir,
        output_dir=output_dir,
        templates_dir=templates_dir,
        resources_dir=resources_dir
    )
    config.save(config_path, "yaml")
    
    # Create a test markdown file
    test_md = content_dir / "test.md"
    test_md.write_text("""---
title: Test Page
---
# Test Content
This is a test.""")
    
    # Create a test template
    template = templates_dir / "default.html.jinja2"
    template.write_text("""<!DOCTYPE html>
<html>
<head><title>{{ frontmatter.title }}</title></head>
<body>{{ __content__ }}</body>
</html>""")
    
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