"""Configuration dataclass and utilities for pdj-sitegen.

This module provides:

- `Config`: Dataclass holding all site generation settings
- `read_data_file()`: Read YAML/JSON/TOML files into dicts
- `emit_data_file()`: Serialize dicts to YAML/JSON strings
- `save_data_file()`: Save dicts to YAML/JSON files
- CLI for printing default config templates (python -m pdj_sitegen.config)
"""

import importlib.resources
import json
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

import pdj_sitegen
from pdj_sitegen.consts import (
	FORMAT_MAP,
	Format,
)

DEFAULT_CONFIG_YAML: str = (
	importlib.resources.files(pdj_sitegen).joinpath("data", "config.yml").read_text()
)

DEFAULT_CONFIG_TOML: str = (
	importlib.resources.files(pdj_sitegen).joinpath("data", "config.toml").read_text()
)


def read_data_file(file_path: Path, fmt: Format | None = None) -> dict[str, Any]:
	"read a file from any of json, yaml, or toml"
	if fmt is None:
		suffix: str = file_path.suffix.lstrip(".")
		if suffix not in FORMAT_MAP:
			raise ValueError(
				f"Unknown file format: '.{suffix}'. Supported formats: {', '.join(FORMAT_MAP.keys())}"
			)
		fmt = FORMAT_MAP[suffix]

	match fmt:
		case "yaml":
			with open(file_path, "r", encoding="utf-8") as f:
				return yaml.safe_load(f)
		case "json":
			with open(file_path, "r", encoding="utf-8") as f:
				return json.load(f)
		case "toml":
			with open(file_path, "rb") as f:
				return tomllib.load(f)
		case _:
			raise ValueError(f"Unsupported format: {fmt}")


def emit_data_file(data: dict[str, Any], fmt: Format) -> str:
	"emit a file as json or yaml"
	match fmt:
		case "yaml":
			return yaml.safe_dump(data)
		case "json":
			return json.dumps(data, indent="\t")
		case "toml":
			raise NotImplementedError("Saving to TOML is not implemented.")
		case _:
			raise ValueError(f"Unsupported format: {fmt}")


def save_data_file(
	data: dict[str, Any], file_path: Path, fmt: Format | None = None
) -> None:
	"save a file as json or yaml"
	if fmt is None:
		suffix: str = file_path.suffix.lstrip(".")
		if suffix not in FORMAT_MAP:
			raise ValueError(
				f"Unknown file format: '.{suffix}'. Supported formats: {', '.join(FORMAT_MAP.keys())}"
			)
		fmt = FORMAT_MAP[suffix]

	emitted_data: str = emit_data_file(data, fmt)
	with open(file_path, "w", encoding="utf-8") as f:
		f.write(emitted_data)


_PATH_FIELDS: tuple[str, ...] = (
	"content_dir",
	"templates_dir",
	"default_template",
	"intermediates_dir",
	"output_dir",
	"build_time_fname",
)


@dataclass
class Config:
	"configuration for the site generator"

	# paths
	content_dir: Path = field(default_factory=lambda: Path("content"))
	templates_dir: Path = field(default_factory=lambda: Path("templates"))
	default_template: Path = field(default_factory=lambda: Path("default.html.jinja2"))
	intermediates_dir: Path | None = None
	output_dir: Path = field(default_factory=lambda: Path("output"))
	build_time_fname: Path = field(default_factory=lambda: Path(".build_time"))

	# jinja2 settings and extra globals
	jinja_env_kwargs: dict[str, Any] = field(default_factory=dict)
	globals_: dict[str, Any] = field(default_factory=dict)

	# whether to prettify html with bs4
	prettify: bool = False

	# content mirroring settings
	# copy_include: patterns to include (empty = everything)
	# copy_exclude: patterns to exclude (*.md excluded by default)
	# if a file matches both, include wins
	copy_include: list[str] = field(default_factory=list)
	copy_exclude: list[str] = field(default_factory=lambda: ["*.md"])

	# index file normalization: if True, _index.md files are renamed to index.html
	normalize_index_names: bool = True

	# pandoc settings
	__pandoc__: dict[str, Any] = field(default_factory=lambda: {"mathjax": True})
	pandoc_fmt_from: str = "markdown+smart"
	pandoc_fmt_to: str = "html"

	@classmethod
	def load(cls, data: dict[str, Any]) -> "Config":
		"""Load Config from a dictionary."""
		# Filter out __format__ key if present (legacy support)
		filtered = {k: v for k, v in data.items() if k != "__format__"}

		# Convert path strings to Path objects
		for field_name in _PATH_FIELDS:
			if field_name in filtered and filtered[field_name] is not None:
				filtered[field_name] = Path(filtered[field_name])

		return cls(**filtered)

	def serialize(self) -> dict[str, Any]:
		"""Serialize Config to a dictionary."""
		result: dict[str, Any] = {"__format__": "Config(SerializableDataclass)"}

		for field_name in self.__dataclass_fields__:
			value = getattr(self, field_name)
			if field_name in _PATH_FIELDS:
				result[field_name] = value.as_posix() if value else None
			else:
				result[field_name] = value

		return result

	@classmethod
	def read(cls, config_path: Path, fmt: Format | None = None) -> "Config":
		"""Read a Config from a file.

		# Parameters:
		 - `config_path : Path` - path to the configuration file
		 - `fmt : Format | None` - format to parse as; if None, inferred from extension

		# Returns:
		 - `Config` - parsed configuration object
		"""
		return cls.load(read_data_file(config_path, fmt))

	def as_str(self, fmt: Format) -> str:
		"""Serialize this Config to a string in the specified format.

		# Parameters:
		 - `fmt : Format` - output format ('yaml' or 'json')

		# Returns:
		 - `str` - serialized configuration string

		# Raises:
		 - `NotImplementedError` : if fmt is 'toml'
		"""
		return emit_data_file(self.serialize(), fmt)

	def save(self, config_path: Path, fmt: Format | None = "json") -> None:
		"""Save this Config to a file.

		# Parameters:
		 - `config_path : Path` - destination file path
		 - `fmt : Format | None` - output format; if None, inferred from extension

		# Raises:
		 - `NotImplementedError` : if fmt is 'toml'
		"""
		save_data_file(self.serialize(), config_path, fmt)


def main() -> None:
	"""CLI entry point for printing default config templates."""
	import argparse

	parser = argparse.ArgumentParser(
		description="Print a default pdj-sitegen configuration file to stdout.",
		epilog="""\
Examples:
  python -m pdj_sitegen.config              # Print TOML config (default)
  python -m pdj_sitegen.config toml         # Print TOML config
  python -m pdj_sitegen.config yaml         # Print YAML config
  python -m pdj_sitegen.config toml > config.toml  # Save to file

Supported formats: toml (default), yaml
Note: JSON config files are supported for reading but not generated as templates.
""",
		formatter_class=argparse.RawDescriptionHelpFormatter,
	)
	parser.add_argument(
		"format",
		nargs="?",
		default="toml",
		choices=["toml", "yaml"],
		help="output format for the config file (default: toml)",
	)
	args = parser.parse_args()

	if args.format == "toml":
		print(DEFAULT_CONFIG_TOML)
	elif args.format == "yaml":
		print(DEFAULT_CONFIG_YAML)


if __name__ == "__main__":
	main()
