"""python pandoc filter replicating [pandoc-csv2table](https://hackage.haskell.org/package/pandoc-csv2table)

By [@mivanit](mivanit.github.io)
"""

import csv
import io
import json
import os
import sys
from typing import Any

from pandocfilters import toJSONFilter  # type: ignore[import-untyped]

ALIGN_MAP: dict[str, str] = {
	"L": "AlignLeft",
	"C": "AlignCenter",
	"R": "AlignRight",
	"D": "AlignDefault",
}


def emptyblock() -> list[Any]:
	return ["", [], []]


def Plain_factory(val: str) -> dict[str, Any]:
	return {
		"t": "Plain",
		"c": [
			{"t": "Str", "c": val.strip()}
			# for w in val.split()
		],
	}


def table_cell_factory(val: str) -> list[Any]:
	return [
		emptyblock(),
		{"t": "AlignDefault"},
		1,
		1,
		[Plain_factory(val)],
	]


def table_row_factory(lst_vals: list[str]) -> list[Any]:
	return [emptyblock(), [table_cell_factory(val) for val in lst_vals]]


def header_factory(lst_vals: list[str]) -> list[Any]:
	return [
		emptyblock(),
		[table_row_factory(lst_vals)],
	]


def body_factory(table_vals: list[list[str]]) -> list[Any]:
	return [
		[
			emptyblock(),
			0,
			[],
			[table_row_factory(row) for row in table_vals],
		]
	]


def keyvals_process(keyvals: list[tuple[str, str]]) -> dict[str, str]:
	return {key: val for key, val in keyvals}


def codeblock_process(
	key: str, value: Any, format_: str, _: Any
) -> dict[str, Any] | None:
	# figure out whether this block should be processed
	if not (key == "CodeBlock"):
		return None

	try:
		[[ident, classes, lst_keyvals], code] = value
	except (ValueError, TypeError) as e:
		raise ValueError(
			f"Unexpected CodeBlock structure. Expected [[ident, classes, keyvals], code], got: {value!r}"
		) from e
	# ident: str, classes: list[str], lst_keyvals: list[tuple[str, str]], code: str

	if "csv_table" not in classes:
		return None

	# read the keyvals
	keyvals: dict[str, str] = keyvals_process(lst_keyvals)
	header_val: str = keyvals.get("header", "1")
	try:
		header: bool = bool(int(header_val))
	except ValueError:
		if header_val.lower() in ("true", "yes", "1"):
			header = True
		elif header_val.lower() in ("false", "no", "0"):
			header = False
		else:
			raise ValueError(
				f"Invalid header value: {header_val!r}. Use 0/1, true/false, or yes/no."
			)
	source: str | None = keyvals.get("source")
	aligns: list[str] | None = (
		list(keyvals.get("aligns", "")) if "aligns" in keyvals else None
	)
	caption: str | None = keyvals.get("caption", None)

	# read the csv source into a table
	table_data: list[list[str]]
	if source is None:
		table_data = list(csv.reader(io.StringIO(code)))
	else:
		if os.path.isfile(source):
			with open(source, "r", encoding="utf-8") as f:
				table_data = list(csv.reader(f))
		else:
			raise FileNotFoundError(f"csv source file not found: {source}")

	# validate the csv table
	if not table_data:
		raise ValueError("CSV data is empty")
	n_cols: int = len(table_data[0])
	if not all(len(row) == n_cols for row in table_data):
		raise ValueError("CSV table is not rectangular")

	if aligns is None:
		aligns = ["D" for _ in range(n_cols)]
	else:
		if len(aligns) == 1:
			aligns = [aligns[0].upper() for _ in range(n_cols)]
		elif len(aligns) == n_cols:
			aligns = [aln.upper() for aln in aligns]
		else:
			raise ValueError(
				f"aligns length mismatch: expected {n_cols}, got {len(aligns)}: {aligns}"
			)

	row_header: list[str]
	table_rows: list[list[str]]
	if header:
		row_header = table_data[0]
		table_rows = table_data[1:]
	else:
		raise NotImplementedError("Tables without headers are not yet supported")

	# write the table
	return {
		"t": "Table",
		"c": [
			# idk
			emptyblock(),
			# caption
			[
				None,
				[] if caption is None else [Plain_factory(caption)],
			],
			# aligns
			[
				[
					{"t": ALIGN_MAP[aln]},
					{"t": "ColWidthDefault"},
				]
				for aln in aligns
			],
			# header
			header_factory(row_header),
			# rows
			body_factory(table_rows),
			# ???
			[emptyblock(), []],
		],
	}


def test_filter() -> None:
	if len(sys.argv) < 2:
		print("Usage: python csv_code_table.py <json_file>", file=sys.stderr)
		sys.exit(1)
	with open(sys.argv[1], encoding="utf-8") as f:
		data: Any = json.load(f)
	key: str = data["blocks"][0]["t"]
	value: Any = data["blocks"][0]["c"]
	newdata: dict[str, Any] | None = codeblock_process(key, value, "", "")
	print(json.dumps(newdata, indent=2))


def main() -> None:
	toJSONFilter(codeblock_process)


if __name__ == "__main__":
	main()
	# test_filter()
