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


@serializable_dataclass
class Config(SerializableDataclass):
	"configuration for the site generator"

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
	jinja_env_kwargs: dict[str, Any] = serializable_field(
		default_factory=dict,
	)
	# structure: StructureFormat = serializable_field(
	# 	default="dotlist",
	# 	assert_type=False,
	# )
	globals_: dict[str, Any] = serializable_field(
		default_factory=dict,
	)
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


if __name__ == "__main__":
	import sys

	fmt: str = sys.argv[1] if len(sys.argv) > 1 else "yaml"
	config: Config = Config()
	config_str: str = config.as_str(fmt)
	print(config_str)
