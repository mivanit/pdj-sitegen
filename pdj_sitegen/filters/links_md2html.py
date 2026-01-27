from typing import Any

from pandocfilters import Link, toJSONFilter  # type: ignore[import-untyped]


def links_md2html(key: str, value: Any, format: str, meta: Any) -> Any | None:
	"""convert dendron links to markdown links"""
	if key == "Link":
		link_txt: Any = value[1][0]
		link_tgt: str = value[2][0]
		if link_tgt.endswith("md"):
			return Link(
				["", [], []],
				[link_txt],
				[
					f"{link_tgt.removesuffix('md')}{'html'}",
					"",
				],
			)
		else:
			return None
	else:
		return None


if __name__ == "__main__":
	toJSONFilter(links_md2html)
