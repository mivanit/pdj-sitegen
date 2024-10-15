import json
import os
from pathlib import Path

import pytest
import yaml

import pdj_sitegen.config as pdjsg_config
import pdj_sitegen.consts as consts
from pdj_sitegen.config import Config

os.makedirs("tests/_temp", exist_ok=True)


# Tests for Config class
def test_config_default_values():
	config = Config()
	assert config.content_dir == Path("content")
	assert config.resources_dir == Path("resources")
	assert config.templates_dir == Path("templates")
	assert config.default_template == Path("default.html.jinja2")
	assert config.output_dir == Path("output")
	assert config.build_time_fname == Path(".build_time")
	assert config.jinja_env_kwargs == {}
	assert config.globals_ == {}
	assert config.pandoc_kwargs == {"mathjax": True}
	assert config.pandoc_fmt_from == "markdown+smart"
	assert config.pandoc_fmt_to == "html"


def test_config_custom_values():
	custom_config = {
		"__format__": "Config(SerializableDataclass)",
		"content_dir": "custom_content",
		"resources_dir": "custom_resources",
		"templates_dir": "custom_templates",
		"default_template": "custom_default.html.jinja2",
		"output_dir": "custom_output",
		"build_time_fname": "custom_build_time",
		"jinja_env_kwargs": {"autoescape": True},
		"globals_": {"site_name": "My Site"},
		"pandoc_kwargs": {"mathjax": False, "toc": True},
		"pandoc_fmt_from": "markdown",
		"pandoc_fmt_to": "html5",
	}
	config = Config.load(custom_config)

	assert custom_config == config.serialize()


@pytest.mark.parametrize("fmt", ["yaml", "json"])
def test_config_read_save(fmt):
	config_path = Path(f"tests/_temp/config.{fmt}")
	original_config = Config(
		content_dir=Path("test_content"), output_dir=Path("test_output")
	)
	original_config.save(config_path, fmt)

	loaded_config = Config.read(config_path, fmt)
	assert loaded_config.content_dir == original_config.content_dir
	assert loaded_config.output_dir == original_config.output_dir


# Tests for utility functions
def test_read_data_file(tmp_path):
	data = {"key": "value"}

	# Test YAML
	yaml_path = tmp_path / "test.yaml"
	with open(yaml_path, "w") as f:
		yaml.dump(data, f)
	assert pdjsg_config.read_data_file(yaml_path) == data

	# Test JSON
	json_path = tmp_path / "test.json"
	with open(json_path, "w") as f:
		json.dump(data, f)
	assert pdjsg_config.read_data_file(json_path) == data


@pytest.mark.parametrize("fmt", ["yaml", "json"])
def test_emit_data_file(fmt):
	data = {"key": "value"}
	result = pdjsg_config.emit_data_file(data, fmt)
	assert consts.FORMAT_PARSERS[fmt](result) == data


def test_emit_data_file_toml():
	with pytest.raises(NotImplementedError):
		pdjsg_config.emit_data_file({}, "toml")


def test_save_data_file(tmp_path):
	data = {"key": "value"}

	# Test YAML
	yaml_path = tmp_path / "test.yaml"
	pdjsg_config.save_data_file(data, yaml_path)
	assert pdjsg_config.read_data_file(yaml_path) == data

	# Test JSON
	json_path = tmp_path / "test.json"
	pdjsg_config.save_data_file(data, json_path)
	assert pdjsg_config.read_data_file(json_path) == data
