import os

import pytest

from pdj_sitegen.consts import (
	FORMAT_MAP,
	FORMAT_PARSERS,
	FRONTMATTER_DELIMS,
	FRONTMATTER_REGEX,
)

os.makedirs("tests/_temp", exist_ok=True)


# Tests for FORMAT_MAP
def test_format_map():
	assert FORMAT_MAP["yaml"] == "yaml"
	assert FORMAT_MAP["yml"] == "yaml"
	assert FORMAT_MAP["json"] == "json"
	assert FORMAT_MAP["toml"] == "toml"


# Tests for FORMAT_PARSERS
@pytest.mark.parametrize(
	"fmt,content,expected",
	[
		("yaml", "key: value", {"key": "value"}),
		("json", '{"key": "value"}', {"key": "value"}),
		("toml", 'key = "value"', {"key": "value"}),
	],
)
def test_format_parsers(fmt, content, expected):
	assert FORMAT_PARSERS[fmt](content) == expected


# Tests for FRONTMATTER_DELIMS
def test_frontmatter_delims():
	assert FRONTMATTER_DELIMS["---"] == "yaml"
	assert FRONTMATTER_DELIMS[";;;"] == "json"
	assert FRONTMATTER_DELIMS["+++"] == "toml"


# Tests for FRONTMATTER_REGEX
@pytest.mark.parametrize(
	"content,expected",
	[
		(
			"---\nkey: value\n---\nBody content",
			{"delimiter": "---", "frontmatter": "key: value", "body": "Body content"},
		),
		(
			';;;\n{"key": "value"}\n;;;\nBody content',
			{
				"delimiter": ";;;",
				"frontmatter": '{"key": "value"}',
				"body": "Body content",
			},
		),
		(
			'+++\nkey = "value"\n+++\nBody content',
			{
				"delimiter": "+++",
				"frontmatter": 'key = "value"',
				"body": "Body content",
			},
		),
	],
)
def test_frontmatter_regex(content, expected):
	match = FRONTMATTER_REGEX.match(content)
	assert match is not None
	assert match.groupdict() == expected
