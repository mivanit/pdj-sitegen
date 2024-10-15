import os
import re
import json
import yaml
import tomllib
import subprocess
import sys
from pathlib import Path

from muutils.json_serialize import SerializableDataclass, serializable_dataclass, serializable_field
from muutils.dictmagic import dotlist_to_nested_dict, update_with_nested_dict, kwargs_to_nested_dict
from typing import Any, Literal, Optional, Callable, Tuple, Dict
from jinja2 import Environment, FileSystemLoader, Template

Format = Literal['yaml', 'json', 'toml']

StructureFormat = Literal['dotlist', 'tree']

FORMAT_MAP: Dict[str, Format] = {
    'yaml': 'yaml',
    'yml': 'yaml',
    'json': 'json',
    'toml': 'toml'
}

FRONTMATTER_PARSERS: Dict[str, Callable[[str], Dict[str, Any]]] = {
    '---': lambda x: yaml.safe_load(x),
    ';;;': lambda x: json.loads(x),
    '+++': lambda x: tomllib.loads(x),
}

FRONTMATTER_REGEX: re.Pattern = re.compile(
    r'^(?P<delimiter>{delims})\n(?P<frontmatter>.*?)\n(?P=delimiter)\n(?P<body>.*)'.format(
        delims='|'.join([
            re.escape(d) for d in
            FRONTMATTER_PARSERS.keys()
        ]),
    ),
    re.DOTALL
)

_PATH_FIELD_SERIALIZATION_KWARGS: Dict[str, Callable] = dict(
    serialization_fn=lambda x: x.as_posix(),
    deserialize_fn=lambda x: Path(x),
)
