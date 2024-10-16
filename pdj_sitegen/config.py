"define the config, and also provide CLI for printing template"

import importlib.resources
import json
import sys
import tomllib
from pathlib import Path
from typing import Any, Optional
import warnings

import yaml  # type: ignore[import-untyped]

from muutils.json_serialize.serializable_dataclass import (
	SerializableDataclass,
	serializable_dataclass,
	serializable_field,
	ZanjMissingWarning,
)

import pdj_sitegen
from pdj_sitegen.consts import (  # StructureFormat,
	_PATH_FIELD_SERIALIZATION_KWARGS,
	FORMAT_MAP,
	Format,
)

# we don't care about zanj being missing when we call `serializable_dataclass`
warnings.filterwarnings("ignore", category=ZanjMissingWarning)

DEFAULT_CONFIG_YAML: str = (
	importlib.resources.files(pdj_sitegen).joinpath("data", "config.yml").read_text()
)


def read_data_file(file_path: Path, fmt: Optional[Format] = None) -> dict[str, Any]:
	"read a file from any of json, yaml, or toml"
	if fmt is None:
		fmt = FORMAT_MAP[file_path.suffix.lstrip(".")]

	match fmt:
		case "yaml":
			with open(file_path, "r") as f:
				return yaml.safe_load(f)
		case "json":
			with open(file_path, "r") as f:
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
	data: dict[str, Any], file_path: Path, fmt: Optional[Format] = None
) -> None:
	"save a file as json or yaml"
	if fmt is None:
		fmt = FORMAT_MAP[file_path.suffix.lstrip(".")]

	emitted_data: str = emit_data_file(data, fmt)
	with open(file_path, "w") as f:
		f.write(emitted_data)


@serializable_dataclass
class Config(SerializableDataclass):
	"configuration for the site generator"

	# paths
	# unpacking dicts here causes mypy to complain, so we ignore it
	# ==================================================

	content_dir: Path = serializable_field(  # type: ignore[call-overload]
		default=Path("content"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	resources_dir: Path = serializable_field(  # type: ignore[call-overload]
		default=Path("resources"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	templates_dir: Path = serializable_field(  # type: ignore[call-overload]
		default=Path("templates"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	default_template: Path = serializable_field(  # type: ignore[call-overload]
		default=Path("default.html.jinja2"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	intermediates_dir: Optional[Path] = serializable_field(  # type: ignore[call-overload]
		default=None,
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	output_dir: Path = serializable_field(  # type: ignore[call-overload]
		default=Path("output"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	build_time_fname: Path = serializable_field(  # type: ignore[call-overload]
		default=Path(".build_time"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	# structure: StructureFormat = serializable_field(
	# 	default="dotlist",
	# 	assert_type=False,
	# )

	# jinja2 settings and extra globals
	# ==================================================

	jinja_env_kwargs: dict[str, Any] = serializable_field(
		default_factory=dict,
	)
	globals_: dict[str, Any] = serializable_field(
		default_factory=dict,
	)

	# whether to prettify html with bs4
	# ==================================================
	prettify: bool = serializable_field(
		default=False,
	)

	# pandoc settings
	# ==================================================

	__pandoc__: dict[str, Any] = serializable_field(
		default_factory=lambda: {"mathjax": True},
	)
	pandoc_fmt_from: str = serializable_field(
		default="markdown+smart",
	)
	pandoc_fmt_to: str = serializable_field(
		default="html",
	)

	@classmethod
	def read(cls, config_path: Path, fmt: Optional[Format] = None) -> "Config":
		return cls.load(read_data_file(config_path, fmt))

	def as_str(self, fmt: Format) -> str:
		return emit_data_file(self.serialize(), fmt)

	def save(self, config_path: Path, fmt: Optional[Format] = "json") -> None:
		save_data_file(self.serialize(), config_path, fmt)

	def __post_init__(self):
		self.validate_fields_types()


if __name__ == "__main__":
	import sys

	if len(sys.argv) > 1:
		fmt: str = sys.argv[1]
		config: Config = Config()
		# fmt being an invalid `Format` will be handled downstream when we call `emit_data_file`
		config_str: str = config.as_str(fmt)  # type: ignore[arg-type]
		print(config_str)
	else:
		print(DEFAULT_CONFIG_YAML)
