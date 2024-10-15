"type definitions, format maps and parsers, and frontmatter regex"

import json
import re
import tomllib
from pathlib import Path
from typing import Any, Callable, Literal

import yaml

Format = Literal["yaml", "json", "toml"]

# StructureFormat = Literal["dotlist", "tree"]

FORMAT_MAP: dict[str, Format] = {
	"yaml": "yaml",
	"yml": "yaml",
	"YAML": "yaml",
	"YML": "yaml",
	"json": "json",
	"JSON": "json",
	"toml": "toml",
	"tml": "toml",
	"TOML": "toml",
	"TML": "toml",
}

FORMAT_PARSERS: dict[Format, Callable[[str], dict[str, Any]]] = {
	"yaml": yaml.safe_load,
	"json": json.loads,
	"toml": tomllib.loads,
}

FRONTMATTER_DELIMS: dict[str, Format] = {
	"---": "yaml",
	";;;": "json",
	"+++": "toml",
}

FRONTMATTER_REGEX: re.Pattern = re.compile(
	r"^(?P<delimiter>{delims})\n(?P<frontmatter>.*?)\n(?P=delimiter)\n(?P<body>.*)".format(
		delims="|".join([re.escape(d) for d in FRONTMATTER_DELIMS.keys()]),
	),
	re.DOTALL,
)

_PATH_FIELD_SERIALIZATION_KWARGS: dict[str, Callable] = dict(
	serialization_fn=lambda x: x.as_posix(),
	deserialize_fn=lambda x: Path(x),
)
