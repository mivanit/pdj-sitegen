# pyright: reportMissingParameterType=false
"""Tests for pdj_sitegen.filters.links_md2html"""

from pdj_sitegen.filters.links_md2html import links_md2html


class TestLinksMd2Html:
	"""Tests for the links_md2html pandoc filter."""

	def test_convert_md_link_to_html(self):
		"""Test that .md links are converted to .html"""
		# Pandoc Link AST structure: [attributes, [link_text], [target, title]]
		value = [
			["", [], []],  # attributes
			[{"t": "Str", "c": "Link Text"}],  # link text
			["page.md", ""],  # target, title
		]
		result = links_md2html("Link", value, "html", {})
		assert result is not None
		# Check the target was changed to .html
		assert result["c"][2][0] == "page.html"

	def test_preserve_non_md_links(self):
		"""Test that non-.md links are not modified (returns None)"""
		value = [
			["", [], []],
			[{"t": "Str", "c": "External"}],
			["https://example.com", ""],
		]
		result = links_md2html("Link", value, "html", {})
		assert result is None

	def test_preserve_html_links(self):
		"""Test that .html links are not modified"""
		value = [
			["", [], []],
			[{"t": "Str", "c": "Already HTML"}],
			["page.html", ""],
		]
		result = links_md2html("Link", value, "html", {})
		assert result is None

	def test_non_link_elements_ignored(self):
		"""Test that non-Link AST elements return None"""
		result = links_md2html("Str", "some text", "html", {})
		assert result is None

		result = links_md2html("Para", [], "html", {})
		assert result is None

		result = links_md2html("CodeBlock", [["", [], []], "code"], "html", {})
		assert result is None

	def test_nested_path_md_link(self):
		"""Test links with directory paths"""
		value = [
			["", [], []],
			[{"t": "Str", "c": "Nested"}],
			["docs/subdir/page.md", ""],
		]
		result = links_md2html("Link", value, "html", {})
		assert result is not None
		assert result["c"][2][0] == "docs/subdir/page.html"

	def test_link_preserves_text(self):
		"""Test that link text is preserved"""
		link_text = [{"t": "Str", "c": "My Link"}]
		value = [
			["", [], []],
			link_text,
			["file.md", ""],
		]
		result = links_md2html("Link", value, "html", {})
		assert result is not None
		assert result["c"][1] == link_text

	def test_link_with_title(self):
		"""Test that link title is handled (though lost in current impl)"""
		value = [
			["", [], []],
			[{"t": "Str", "c": "Link"}],
			["page.md", "Original Title"],
		]
		result = links_md2html("Link", value, "html", {})
		assert result is not None
		assert result["c"][2][0] == "page.html"
		# Current implementation sets title to empty string
		assert result["c"][2][1] == ""

	def test_readme_link_not_converted(self):
		"""Test that links like 'readme' (not ending in .md) are not converted"""
		value = [
			["", [], []],
			[{"t": "Str", "c": "Readme"}],
			["readme", ""],
		]
		result = links_md2html("Link", value, "html", {})
		assert result is None

	def test_various_formats_unchanged(self):
		"""Test various non-md formats are unchanged"""
		formats = ["page.pdf", "image.png", "doc.txt", "file.markdown"]
		for target in formats:
			value = [
				["", [], []],
				[{"t": "Str", "c": "Link"}],
				[target, ""],
			]
			result = links_md2html("Link", value, "html", {})
			assert result is None, f"Should not convert {target}"

	def test_words_ending_in_md_not_converted(self):
		"""Test that words ending in 'md' but not '.md' are not converted"""
		# These should NOT be converted - they don't have the .md extension
		non_md_targets = ["readme", "cmd", "ammad", "amd"]
		for target in non_md_targets:
			value = [
				["", [], []],
				[{"t": "Str", "c": "Link"}],
				[target, ""],
			]
			result = links_md2html("Link", value, "html", {})
			assert (
				result is None
			), f"Should not convert '{target}' - it doesn't end with .md"

	def test_malformed_link_empty_value(self):
		"""Test that malformed links with empty value don't crash"""
		result = links_md2html("Link", [], "html", {})
		assert result is None

	def test_malformed_link_missing_indices(self):
		"""Test that malformed links with missing indices don't crash"""
		# Missing value[1] and value[2]
		result = links_md2html("Link", [["", [], []]], "html", {})
		assert result is None

		# value[1] exists but value[2] is missing
		result = links_md2html("Link", [["", [], []], []], "html", {})
		assert result is None

	def test_malformed_link_empty_nested_lists(self):
		"""Test that malformed links with empty nested lists don't crash"""
		# value[1] and value[2] exist but are empty
		value = [
			["", [], []],
			[],  # Empty link text list
			[],  # Empty target list
		]
		result = links_md2html("Link", value, "html", {})
		assert result is None

	def test_malformed_link_none_value(self):
		"""Test that None value doesn't crash"""
		result = links_md2html("Link", None, "html", {})
		assert result is None

	def test_malformed_link_non_indexable(self):
		"""Test that non-indexable value doesn't crash"""
		result = links_md2html("Link", "not a list", "html", {})
		assert result is None

		result = links_md2html("Link", 123, "html", {})
		assert result is None
