import json
import re
import tomllib
from pathlib import Path
from typing import Any, Callable, Literal

import yaml

Format = Literal["yaml", "json", "toml"]

StructureFormat = Literal["dotlist", "tree"]

FORMAT_MAP: dict[str, Format] = {
	"yaml": "yaml",
	"yml": "yaml",
	"json": "json",
	"toml": "toml",
}

FRONTMATTER_PARSERS: dict[str, Callable[[str], dict[str, Any]]] = {
	"---": lambda x: yaml.safe_load(x),
	";;;": lambda x: json.loads(x),
	"+++": lambda x: tomllib.loads(x),
}

FRONTMATTER_REGEX: re.Pattern = re.compile(
	r"^(?P<delimiter>{delims})\n(?P<frontmatter>.*?)\n(?P=delimiter)\n(?P<body>.*)".format(
		delims="|".join([re.escape(d) for d in FRONTMATTER_PARSERS.keys()]),
	),
	re.DOTALL,
)

_PATH_FIELD_SERIALIZATION_KWARGS: dict[str, Callable] = dict(
	serialization_fn=lambda x: x.as_posix(),
	deserialize_fn=lambda x: Path(x),
)
