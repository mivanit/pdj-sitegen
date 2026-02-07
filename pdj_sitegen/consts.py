"""Type definitions, format maps, parsers, and frontmatter regex for pdj-sitegen.

This module defines:

- `Format`: Type alias for supported data formats ('yaml', 'json', 'toml')
- `FORMAT_MAP`: Maps file extensions to Format values for auto-detection
- `FORMAT_PARSERS`: Maps Format values to parser functions
- `FRONTMATTER_DELIMS`: Maps frontmatter delimiter strings to their Format
- `FRONTMATTER_REGEX`: Compiled regex for splitting frontmatter from content
"""

import json
import re
import tomllib
from typing import Any, Callable, Literal

import yaml  # type: ignore[import-untyped]

Format = Literal["yaml", "json", "toml"]
"""Type alias for supported data formats."""

# Maps file extensions (with case variations) to canonical Format values.
# Used to auto-detect format from file paths.
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

# Maps Format values to parser functions that convert strings to dicts.
# Each parser takes a string and returns a dictionary.
FORMAT_PARSERS: dict[Format, Callable[[str], dict[str, Any]]] = {
	"yaml": yaml.safe_load,
	"json": json.loads,
	"toml": tomllib.loads,
}

# Maps frontmatter delimiter strings to their associated Format.
# Used during markdown splitting to determine how to parse frontmatter.
# Examples:
#   --- (YAML frontmatter, most common)
#   ;;; (JSON frontmatter)
#   +++ (TOML frontmatter)
FRONTMATTER_DELIMS: dict[str, Format] = {
	"---": "yaml",
	";;;": "json",
	"+++": "toml",
}

# Regex to split markdown into frontmatter and body.
# Matches: delimiter + newline + frontmatter + newline + same delimiter + newline + body
# Named groups: 'delimiter', 'frontmatter', 'body'
FRONTMATTER_REGEX: re.Pattern[str] = re.compile(
	r"^(?P<delimiter>{delims})\n(?P<frontmatter>.*?)\n(?P=delimiter)\n(?P<body>.*)".format(
		delims="|".join([re.escape(d) for d in FRONTMATTER_DELIMS.keys()]),
	),
	re.DOTALL,
)
