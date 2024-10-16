import os

import pytest
import yaml  # type: ignore[import-untyped]

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

	# Test for case insensitivity
	assert FORMAT_MAP["YAML"] == "yaml"
	assert FORMAT_MAP["JSON"] == "json"
	assert FORMAT_MAP["TOML"] == "toml"

	# Test for unknown format
	with pytest.raises(KeyError):
		FORMAT_MAP["unknown"]


# Tests for FORMAT_PARSERS
@pytest.mark.parametrize(
	"fmt,content,expected",
	[
		# YAML tests
		("yaml", "key: value", {"key": "value"}),
		("yaml", "key: 42", {"key": 42}),
		("yaml", "key: true", {"key": True}),
		("yaml", "key: null", {"key": None}),
		("yaml", "- item1\n- item2", ["item1", "item2"]),
		("yaml", "key:\n  nested: value", {"key": {"nested": "value"}}),
		("yaml", "", None),  # Empty YAML
		# JSON tests
		("json", '{"key": "value"}', {"key": "value"}),
		("json", '{"key": 42}', {"key": 42}),
		("json", '{"key": true}', {"key": True}),
		("json", '{"key": null}', {"key": None}),
		("json", '["item1", "item2"]', ["item1", "item2"]),
		("json", '{"key": {"nested": "value"}}', {"key": {"nested": "value"}}),
		("json", "{}", {}),  # Empty JSON
		# TOML tests
		("toml", 'key = "value"', {"key": "value"}),
		("toml", "key = 42", {"key": 42}),
		("toml", "key = true", {"key": True}),
		("toml", 'key = [ "item1", "item2" ]', {"key": ["item1", "item2"]}),
		("toml", '[table]\nkey = "value"', {"table": {"key": "value"}}),
		("toml", "", {}),  # Empty TOML
	],
)
def test_format_parsers(fmt, content, expected):
	assert FORMAT_PARSERS[fmt](content) == expected


def test_format_parsers_errors():
	with pytest.raises(yaml.scanner.ScannerError):  # Invalid YAML
		FORMAT_PARSERS["yaml"]("key: : value")

	with pytest.raises(ValueError):  # Invalid JSON
		FORMAT_PARSERS["json"]('{"key": value}')

	with pytest.raises(ValueError):  # Invalid TOML
		FORMAT_PARSERS["toml"]("key = = value")


# Tests for FRONTMATTER_DELIMS
def test_frontmatter_delims():
	assert FRONTMATTER_DELIMS["---"] == "yaml"
	assert FRONTMATTER_DELIMS[";;;"] == "json"
	assert FRONTMATTER_DELIMS["+++"] == "toml"

	# Test for unknown delimiter
	with pytest.raises(KeyError):
		FRONTMATTER_DELIMS["==="]


# Tests for FRONTMATTER_REGEX
@pytest.mark.parametrize(
	"content,expected",
	[
		# Basic cases
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
		# Empty body
		(
			"---\nkey: value\n---\n",
			{"delimiter": "---", "frontmatter": "key: value", "body": ""},
		),
		# Multiple frontmatter delimiters in body
		(
			"---\nkey: value\n---\nBody with ---\nMore content",
			{
				"delimiter": "---",
				"frontmatter": "key: value",
				"body": "Body with ---\nMore content",
			},
		),
		# Frontmatter with multiple lines
		(
			"---\nkey1: value1\nkey2: value2\n---\nBody content",
			{
				"delimiter": "---",
				"frontmatter": "key1: value1\nkey2: value2",
				"body": "Body content",
			},
		),
		# Frontmatter with nested structures
		(
			"---\nkey:\n  nested: value\n---\nBody content",
			{
				"delimiter": "---",
				"frontmatter": "key:\n  nested: value",
				"body": "Body content",
			},
		),
		# Different indentation in frontmatter
		(
			"---\n  key: value\n---\nBody content",
			{"delimiter": "---", "frontmatter": "  key: value", "body": "Body content"},
		),
	],
)
def test_frontmatter_regex(content, expected):
	match = FRONTMATTER_REGEX.match(content)
	assert match is not None
	assert match.groupdict() == expected


def test_frontmatter_regex_no_match():
	# Test cases where the regex should not match
	no_match_cases = [
		"No frontmatter here",
		"---\nIncomplete frontmatter",
		"---\nMissing closing delimiter\nBody content",
		"-- -\nInvalid delimiter\n---\nBody content",
	]
	for case in no_match_cases:
		assert FRONTMATTER_REGEX.match(case) is None
