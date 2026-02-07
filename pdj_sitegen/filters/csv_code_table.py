"""Pandoc filter to convert CSV code blocks to HTML tables.

Replicates functionality of [pandoc-csv2table](https://hackage.haskell.org/package/pandoc-csv2table).

This filter processes fenced code blocks with the `csv_table` class and converts
them to pandoc Table elements. CSV data can be inline or loaded from an external file.

Usage in markdown:

    ```{.csv_table header=1}
    Name,Age,City
    Alice,30,Boston
    Bob,25,Seattle
    ```

Or with external source:

    ```{.csv_table source="data.csv" header=1 aligns="LCR"}
    ```

Supported options:
- `header`: 1 (default) or 0 - whether first row is header
- `source`: path to external CSV file
- `aligns`: column alignments (L=left, C=center, R=right, D=default)
- `caption`: table caption

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
	"""Create an empty pandoc AST attribute block.

	Returns the standard empty attribute structure: ["", [], []]
	representing (identifier, classes, key-value pairs).
	"""
	return ["", [], []]


def Plain_factory(val: str) -> dict[str, Any]:
	"""Create a pandoc Plain block containing a single Str element.

	# Parameters:
	 - `val : str` - text content (will be stripped of whitespace)

	# Returns:
	 - `dict[str, Any]` - pandoc AST Plain block structure
	"""
	return {
		"t": "Plain",
		"c": [
			{"t": "Str", "c": val.strip()}
			# for w in val.split()
		],
	}


def table_cell_factory(val: str) -> list[Any]:
	"""Create a pandoc table cell with default alignment.

	# Parameters:
	 - `val : str` - cell text content

	# Returns:
	 - `list[Any]` - pandoc AST table cell structure
	"""
	return [
		emptyblock(),
		{"t": "AlignDefault"},
		1,
		1,
		[Plain_factory(val)],
	]


def table_row_factory(lst_vals: list[str]) -> list[Any]:
	"""Create a pandoc table row from a list of cell values.

	# Parameters:
	 - `lst_vals : list[str]` - list of cell text values

	# Returns:
	 - `list[Any]` - pandoc AST table row structure
	"""
	return [emptyblock(), [table_cell_factory(val) for val in lst_vals]]


def header_factory(lst_vals: list[str]) -> list[Any]:
	"""Create a pandoc table header from a list of column headers.

	# Parameters:
	 - `lst_vals : list[str]` - list of header text values

	# Returns:
	 - `list[Any]` - pandoc AST table header structure
	"""
	return [
		emptyblock(),
		[table_row_factory(lst_vals)],
	]


def body_factory(table_vals: list[list[str]]) -> list[Any]:
	"""Create a pandoc table body from a 2D list of cell values.

	# Parameters:
	 - `table_vals : list[list[str]]` - list of rows, each row is a list of cell values

	# Returns:
	 - `list[Any]` - pandoc AST table body structure
	"""
	return [
		[
			emptyblock(),
			0,
			[],
			[table_row_factory(row) for row in table_vals],
		]
	]


def keyvals_process(keyvals: list[tuple[str, str]]) -> dict[str, str]:
	"""Convert a list of key-value tuples to a dictionary.

	# Parameters:
	 - `keyvals : list[tuple[str, str]]` - list of (key, value) tuples from pandoc attributes

	# Returns:
	 - `dict[str, str]` - dictionary mapping keys to values
	"""
	return {key: val for key, val in keyvals}


def codeblock_process(
	key: str, value: Any, format_: str, _: Any
) -> dict[str, Any] | None:
	"""Process a CodeBlock and convert csv_table blocks to Table elements.

	This is the main pandoc filter function. It checks if a CodeBlock has the
	'csv_table' class and, if so, parses the CSV content (either inline or from
	a source file) and returns a pandoc Table AST element.

	# Parameters:
	 - `key : str` - pandoc AST element type (only 'CodeBlock' is processed)
	 - `value : Any` - pandoc AST element content
	 - `format_ : str` - output format (unused)
	 - `_ : Any` - document metadata (unused)

	# Returns:
	 - `dict[str, Any] | None` - pandoc Table element if processed, None otherwise

	# Raises:
	 - `ValueError` : if CSV data is empty, not rectangular, or has invalid options
	 - `FileNotFoundError` : if source CSV file does not exist
	 - `NotImplementedError` : if header=0 (tables without headers not yet supported)
	"""
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
	"""Debug helper to test the filter on a JSON file.

	Reads a pandoc JSON file from command line args, processes the first block,
	and prints the result. For development/debugging only.
	"""
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
	"""Entry point for the pdj-csv-code-table filter.

	Runs the codeblock_process filter on stdin/stdout using pandocfilters.
	"""
	toJSONFilter(codeblock_process)


if __name__ == "__main__":
	main()
	# test_filter()
