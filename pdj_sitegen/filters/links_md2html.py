"""Pandoc filter to convert .md links to .html links.

This filter processes pandoc AST Link elements and rewrites any link targets
ending in `.md` to end in `.html` instead. This allows authors to write
cross-references using the original markdown filenames while producing
correct HTML links in the output.

Usage:
    Enable in frontmatter or config:

    __pandoc__:
      filter: links_md2html

    Or run directly:

    pandoc --filter pdj-links-md2html input.md
"""

from typing import Any

from pandocfilters import Link, toJSONFilter  # type: ignore[import-untyped]  # pyright: ignore[reportMissingTypeStubs]


def links_md2html(key: str, value: Any, _format: str, _meta: Any) -> Any | None:
	"""Convert .md links to .html links in pandoc AST Link elements.

	When a Link element's target URL ends with '.md', this filter rewrites
	it to end with '.html' instead, preserving the rest of the URL.

	# Parameters:
	 - `key : str` - pandoc AST element type (only 'Link' is processed)
	 - `value : Any` - pandoc AST element content (link attributes, text, and target)
	 - `format : str` - output format (unused)
	 - `meta : Any` - document metadata (unused)

	# Returns:
	 - `Any | None` - modified Link element if URL was rewritten, None otherwise
	"""
	if key == "Link":
		try:
			link_txt: Any = value[1][0]
			link_tgt: str = value[2][0]
		except (IndexError, TypeError):
			return None  # Malformed link structure, skip
		if link_tgt.endswith(".md"):
			return Link(
				["", [], []],
				[link_txt],
				[link_tgt[:-3] + ".html", ""],
			)
	return None


def main() -> None:
	"""Entry point for the pdj-links-md2html filter.

	Runs the links_md2html filter on stdin/stdout using pandocfilters.
	"""
	toJSONFilter(links_md2html)


if __name__ == "__main__":
	main()
