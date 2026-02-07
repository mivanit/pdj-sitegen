# pyright: reportMissingParameterType=false
import json
from pathlib import Path

import pytest
import yaml

import pdj_sitegen.config as pdjsg_config
import pdj_sitegen.consts as consts
from pdj_sitegen.config import Config


# Tests for Config class
def test_config_default_values():
	config = Config()
	assert config.content_dir == Path("content")
	assert config.templates_dir == Path("templates")
	assert config.default_template == Path("default.html.jinja2")
	assert config.output_dir == Path("output")
	assert config.build_time_fname == Path(".build_time")
	assert config.jinja_env_kwargs == {}
	assert config.globals_ == {}
	assert config.__pandoc__ == {"mathjax": True}
	assert config.pandoc_fmt_from == "markdown+smart"
	assert config.pandoc_fmt_to == "html"


def test_config_custom_values():
	custom_config = {
		"__format__": "Config(SerializableDataclass)",
		"content_dir": "custom_content",
		"templates_dir": "custom_templates",
		"default_template": "custom_default.html.jinja2",
		"output_dir": "custom_output",
		"build_time_fname": "custom_build_time",
		"jinja_env_kwargs": {"autoescape": True, "trim_blocks": True},
		"globals_": {"site_name": "My Site", "author": "John Doe"},
		"__pandoc__": {"mathjax": False, "toc": True, "number-sections": True},
		"pandoc_fmt_from": "markdown",
		"pandoc_fmt_to": "html5",
		"intermediates_dir": None,
		"prettify": False,
		"copy_include": [],
		"copy_exclude": ["*.md"],
		"normalize_index_names": True,
	}
	config = Config.load(custom_config)

	assert custom_config == config.serialize()

	# Check individual attributes
	assert config.content_dir == Path("custom_content")
	assert config.templates_dir == Path("custom_templates")
	assert config.default_template == Path("custom_default.html.jinja2")
	assert config.output_dir == Path("custom_output")
	assert config.build_time_fname == Path("custom_build_time")
	assert config.jinja_env_kwargs == {"autoescape": True, "trim_blocks": True}
	assert config.globals_ == {"site_name": "My Site", "author": "John Doe"}
	assert config.__pandoc__ == {
		"mathjax": False,
		"toc": True,
		"number-sections": True,
	}
	assert config.pandoc_fmt_from == "markdown"
	assert config.pandoc_fmt_to == "html5"


def test_config_partial_custom_values():
	partial_config = {
		"__format__": "Config(SerializableDataclass)",
		"content_dir": "custom_content",
		"jinja_env_kwargs": {"autoescape": True},
	}
	config = Config.load(partial_config)

	assert config.content_dir == Path("custom_content")
	assert config.jinja_env_kwargs == {"autoescape": True}
	# Check that other values remain default
	assert config.__pandoc__ == {"mathjax": True}


@pytest.mark.parametrize("fmt", ["yaml", "json"])
def test_config_read_save(fmt, tmp_path):
	config_path = tmp_path / f"config.{fmt}"
	original_config = Config(
		content_dir=Path("test_content"),
		output_dir=Path("test_output"),
		globals_={"test_key": "test_value"},
	)
	original_config.save(config_path, fmt)

	loaded_config = Config.read(config_path, fmt)
	assert loaded_config.content_dir == original_config.content_dir
	assert loaded_config.output_dir == original_config.output_dir
	assert loaded_config.globals_ == original_config.globals_

	# Test serialization/deserialization of all fields
	assert loaded_config.serialize() == original_config.serialize()


def test_config_invalid_format():
	with pytest.raises(ValueError, match="Unknown file format"):
		Config.read(Path("non_existent.txt"))


def test_config_non_existent_file():
	with pytest.raises(FileNotFoundError):
		Config.read(Path("non_existent.yaml"))


# Tests for utility functions
@pytest.mark.parametrize("fmt", ["yaml", "json"])
def test_read_data_file(fmt, tmp_path):
	data = {
		"string": "value",
		"integer": 42,
		"float": 3.14,
		"boolean": True,
		"null": None,
		"list": [1, 2, 3],
		"nested": {"key": "value"},
	}

	file_path = tmp_path / f"test.{fmt}"

	if fmt == "yaml":
		with open(file_path, "w") as f:
			yaml.dump(data, f)
	else:  # json
		with open(file_path, "w") as f:
			json.dump(data, f)

	assert pdjsg_config.read_data_file(file_path) == data


def test_read_data_file_invalid_format():
	with pytest.raises(ValueError, match="Unknown file format"):
		pdjsg_config.read_data_file(Path("test.txt"))


def test_read_data_file_non_existent():
	with pytest.raises(FileNotFoundError):
		pdjsg_config.read_data_file(Path("non_existent.yaml"))


@pytest.mark.parametrize("fmt", ["yaml", "json"])
def test_emit_data_file(fmt):
	data = {
		"string": "value",
		"integer": 42,
		"float": 3.14,
		"boolean": True,
		"null": None,
		"list": [1, 2, 3],
		"nested": {"key": "value"},
	}
	result = pdjsg_config.emit_data_file(data, fmt)
	assert consts.FORMAT_PARSERS[fmt](result) == data


def test_emit_data_file_toml():
	with pytest.raises(NotImplementedError):
		pdjsg_config.emit_data_file({}, "toml")


def test_emit_data_file_invalid_format():
	with pytest.raises(ValueError):
		pdjsg_config.emit_data_file({}, "invalid")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


@pytest.mark.parametrize("fmt", ["yaml", "json"])
def test_save_data_file(fmt, tmp_path):
	data = {
		"string": "value",
		"integer": 42,
		"float": 3.14,
		"boolean": True,
		"null": None,
		"list": [1, 2, 3],
		"nested": {"key": "value"},
	}

	file_path = tmp_path / f"test.{fmt}"
	pdjsg_config.save_data_file(data, file_path)
	assert pdjsg_config.read_data_file(file_path) == data


def test_save_data_file_invalid_format(tmp_path):
	with pytest.raises(ValueError, match="Unknown file format"):
		pdjsg_config.save_data_file({}, tmp_path / "test.txt")
