from typing import Any

from pandocfilters import Link, toJSONFilter  # type: ignore[import-untyped]


def links_md2html(key: str, value: Any, format: str, meta: Any) -> Any | None:
	"""convert .md links to .html links"""
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
	toJSONFilter(links_md2html)


if __name__ == "__main__":
	main()
