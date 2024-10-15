import json
import sys
import tomllib
from pathlib import Path
from typing import Any, Optional

import yaml
from muutils.json_serialize import (
	SerializableDataclass,
	serializable_dataclass,
	serializable_field,
)

from pdj_sitegen.consts import (
	_PATH_FIELD_SERIALIZATION_KWARGS,
	FORMAT_MAP,
	Format,
	# StructureFormat,
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


DEFAULT_CONFIG_YAML: str = """
# directory with markdown content files and resources, relative to cwd
content_dir: content
# directory with resources, relative to `content_dir`
resources_dir: resources
# templates directory, relative to cwd
templates_dir: templates
# default template file, relative to `templates_dir`
default_template: default.html.jinja2
# output directory, relative to cwd
output_dir: docs
# extra globals to pass -- this can be anything
globals_:
  globals_key: some value
# kwargs to pass to the Jinja2 environment
jinja_env_kwargs: {}
# pandoc formats
pandoc_fmt_from: markdown+smart
pandoc_fmt_to: html
# extra kwargs to pass to pandoc (this will be augmented with `pandoc_args` from the frontmatter of a file)
pandoc_kwargs:
  mathjax: true
"""


@serializable_dataclass
class Config(SerializableDataclass):
	"configuration for the site generator"

	# paths
	# ==================================================

	content_dir: Path = serializable_field(
		default=Path("content"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	resources_dir: Path = serializable_field(
		default=Path("resources"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	templates_dir: Path = serializable_field(
		default=Path("templates"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	default_template: Path = serializable_field(
		default=Path("default.html.jinja2"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	output_dir: Path = serializable_field(
		default=Path("output"),
		**_PATH_FIELD_SERIALIZATION_KWARGS,
	)
	build_time_fname: Path = serializable_field(
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

	# pandoc settings
	# ==================================================

	pandoc_kwargs: dict[str, Any] = serializable_field(
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
		config_str: str = config.as_str(fmt)
		print(config_str)
	else:
		print(DEFAULT_CONFIG_YAML)
		
