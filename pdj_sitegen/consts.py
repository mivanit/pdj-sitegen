"type definitions, format maps and parsers, and frontmatter regex"

import json
import re
import tomllib
from typing import Any, Callable, Literal

import yaml  # type: ignore[import-untyped]

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

FRONTMATTER_REGEX: re.Pattern[str] = re.compile(
	r"^(?P<delimiter>{delims})\n(?P<frontmatter>.*?)\n(?P=delimiter)\n(?P<body>.*)".format(
		delims="|".join([re.escape(d) for d in FRONTMATTER_DELIMS.keys()]),
	),
	re.DOTALL,
)
