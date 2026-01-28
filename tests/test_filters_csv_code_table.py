# pyright: reportMissingParameterType=false
"""Tests for pdj_sitegen.filters.csv_code_table"""

import pytest

from pdj_sitegen.filters.csv_code_table import (
	ALIGN_MAP,
	Plain_factory,
	body_factory,
	codeblock_process,
	emptyblock,
	header_factory,
	keyvals_process,
	table_cell_factory,
	table_row_factory,
)


class TestHelperFunctions:
	"""Tests for CSV table helper functions."""

	def test_emptyblock(self):
		"""Test emptyblock returns correct structure."""
		result = emptyblock()
		assert result == ["", [], []]

	def test_plain_factory(self):
		"""Test Plain_factory creates correct AST."""
		result = Plain_factory("test value")
		assert result["t"] == "Plain"
		assert len(result["c"]) == 1
		assert result["c"][0]["t"] == "Str"
		assert result["c"][0]["c"] == "test value"

	def test_plain_factory_strips_whitespace(self):
		"""Test Plain_factory strips surrounding whitespace."""
		result = Plain_factory("  test  ")
		assert result["c"][0]["c"] == "test"

	def test_plain_factory_empty_string(self):
		"""Test Plain_factory with empty string."""
		result = Plain_factory("")
		assert result["c"][0]["c"] == ""

	def test_table_cell_factory(self):
		"""Test table_cell_factory creates correct structure."""
		result = table_cell_factory("cell value")
		assert len(result) == 5
		assert result[0] == ["", [], []]  # emptyblock
		assert result[1] == {"t": "AlignDefault"}
		assert result[2] == 1  # colspan
		assert result[3] == 1  # rowspan
		# result[4] contains the Plain element in a list
		assert len(result[4]) == 1
		assert result[4][0]["t"] == "Plain"

	def test_table_row_factory(self):
		"""Test table_row_factory creates row with multiple cells."""
		result = table_row_factory(["a", "b", "c"])
		assert result[0] == ["", [], []]  # emptyblock
		assert len(result[1]) == 3  # three cells

	def test_table_row_factory_single_cell(self):
		"""Test table_row_factory with single cell."""
		result = table_row_factory(["only"])
		assert len(result[1]) == 1

	def test_header_factory(self):
		"""Test header_factory creates header structure."""
		result = header_factory(["Col1", "Col2"])
		assert result[0] == ["", [], []]
		assert len(result[1]) == 1  # one row in header
		assert len(result[1][0][1]) == 2  # two columns

	def test_body_factory(self):
		"""Test body_factory creates body with multiple rows."""
		data = [["r1c1", "r1c2"], ["r2c1", "r2c2"]]
		result = body_factory(data)
		assert len(result) == 1  # one body section
		body_section = result[0]
		assert body_section[0] == ["", [], []]  # emptyblock
		assert body_section[1] == 0
		assert body_section[2] == []
		assert len(body_section[3]) == 2  # two rows

	def test_body_factory_empty(self):
		"""Test body_factory with empty data."""
		result = body_factory([])
		assert len(result[0][3]) == 0

	def test_keyvals_process(self):
		"""Test keyvals_process converts list to dict."""
		keyvals = [("header", "1"), ("aligns", "LCR")]
		result = keyvals_process(keyvals)
		assert result == {"header": "1", "aligns": "LCR"}

	def test_keyvals_process_empty(self):
		"""Test keyvals_process with empty list."""
		result = keyvals_process([])
		assert result == {}


class TestAlignMap:
	"""Tests for alignment mapping."""

	def test_align_map_left(self):
		"""Test left alignment."""
		assert ALIGN_MAP["L"] == "AlignLeft"

	def test_align_map_center(self):
		"""Test center alignment."""
		assert ALIGN_MAP["C"] == "AlignCenter"

	def test_align_map_right(self):
		"""Test right alignment."""
		assert ALIGN_MAP["R"] == "AlignRight"

	def test_align_map_default(self):
		"""Test default alignment."""
		assert ALIGN_MAP["D"] == "AlignDefault"

	def test_align_map_all_keys(self):
		"""Test all expected keys are present."""
		assert set(ALIGN_MAP.keys()) == {"L", "C", "R", "D"}


class TestCodeblockProcess:
	"""Tests for the main codeblock_process filter function."""

	def test_non_codeblock_returns_none(self):
		"""Test non-CodeBlock elements return None."""
		result = codeblock_process("Para", [], "html", {})
		assert result is None

	def test_non_csv_table_codeblock_returns_none(self):
		"""Test CodeBlock without csv_table class returns None."""
		value = [["", ["python"], []], "print('hello')"]
		result = codeblock_process("CodeBlock", value, "html", {})
		assert result is None

	def test_codeblock_with_other_classes_returns_none(self):
		"""Test CodeBlock with other classes but not csv_table."""
		value = [["", ["javascript", "highlight"], []], "const x = 1;"]
		result = codeblock_process("CodeBlock", value, "html", {})
		assert result is None

	def test_basic_csv_table(self):
		"""Test basic CSV table conversion."""
		csv_content = "Name,Age\nAlice,30\nBob,25"
		value = [["", ["csv_table"], []], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		assert result["t"] == "Table"
		# Check structure: [emptyblock, caption, colspecs, header, body, ???]
		assert len(result["c"]) == 6

	def test_csv_table_default_aligns(self):
		"""Test CSV table uses AlignDefault when no aligns specified."""
		csv_content = "A,B,C\n1,2,3"
		value = [["", ["csv_table"], []], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		# All columns should have AlignDefault
		colspecs = result["c"][2]
		assert len(colspecs) == 3
		for col_spec in colspecs:
			assert col_spec[0]["t"] == "AlignDefault"

	def test_csv_table_with_single_align(self):
		"""Test CSV table with single alignment applied to all columns."""
		csv_content = "A,B,C\n1,2,3"
		value = [["", ["csv_table"], [("aligns", "C")]], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		# All columns should have AlignCenter
		colspecs = result["c"][2]
		for col_spec in colspecs:
			assert col_spec[0]["t"] == "AlignCenter"

	def test_csv_table_with_per_column_aligns(self):
		"""Test CSV table with per-column alignment."""
		csv_content = "Left,Center,Right\n1,2,3"
		value = [["", ["csv_table"], [("aligns", "LCR")]], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		colspecs = result["c"][2]
		assert colspecs[0][0]["t"] == "AlignLeft"
		assert colspecs[1][0]["t"] == "AlignCenter"
		assert colspecs[2][0]["t"] == "AlignRight"

	def test_csv_table_with_lowercase_aligns(self):
		"""Test CSV table with lowercase alignment (should be uppercased)."""
		csv_content = "A,B\n1,2"
		value = [["", ["csv_table"], [("aligns", "lr")]], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		colspecs = result["c"][2]
		assert colspecs[0][0]["t"] == "AlignLeft"
		assert colspecs[1][0]["t"] == "AlignRight"

	def test_csv_table_with_caption(self):
		"""Test CSV table with caption."""
		csv_content = "A,B\n1,2"
		value = [["", ["csv_table"], [("caption", "My Table")]], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		# Caption is at index 1: [None, [Plain_factory(caption)]]
		caption_content = result["c"][1][1]
		assert len(caption_content) == 1
		assert caption_content[0]["t"] == "Plain"
		assert caption_content[0]["c"][0]["c"] == "My Table"

	def test_csv_table_without_caption(self):
		"""Test CSV table without caption has empty caption."""
		csv_content = "A,B\n1,2"
		value = [["", ["csv_table"], []], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		# Caption should be [None, []]
		assert result["c"][1] == [None, []]

	def test_csv_table_from_file(self, tmp_path):
		"""Test CSV table reading from external file."""
		csv_file = tmp_path / "data.csv"
		csv_file.write_text("X,Y\n10,20\n30,40")

		value = [["", ["csv_table"], [("source", str(csv_file))]], ""]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		assert result["t"] == "Table"
		# Should have 2 columns
		assert len(result["c"][2]) == 2

	def test_csv_table_file_not_found(self):
		"""Test error when source file doesn't exist."""
		value = [["", ["csv_table"], [("source", "/nonexistent/file.csv")]], ""]
		with pytest.raises(Exception, match="csv source file not found"):
			codeblock_process("CodeBlock", value, "html", {})

	def test_csv_table_non_rectangular_raises(self):
		"""Test error for non-rectangular CSV data."""
		csv_content = "A,B,C\n1,2"  # Missing one cell
		value = [["", ["csv_table"], []], csv_content]
		with pytest.raises(ValueError, match="not rectangular"):
			codeblock_process("CodeBlock", value, "html", {})

	def test_csv_table_aligns_length_mismatch(self):
		"""Test error when aligns count doesn't match columns."""
		csv_content = "A,B,C\n1,2,3"
		value = [
			["", ["csv_table"], [("aligns", "LR")]],
			csv_content,
		]  # 2 aligns for 3 cols
		with pytest.raises(Exception, match="aligns length mismatch"):
			codeblock_process("CodeBlock", value, "html", {})

	def test_csv_table_no_header_raises(self):
		"""Test error when header=0 (not supported)."""
		csv_content = "1,2,3\n4,5,6"
		value = [["", ["csv_table"], [("header", "0")]], csv_content]
		with pytest.raises(NotImplementedError, match="Tables without headers"):
			codeblock_process("CodeBlock", value, "html", {})

	def test_csv_table_header_rows(self):
		"""Test that header row is separate from body rows."""
		csv_content = "H1,H2\nR1C1,R1C2\nR2C1,R2C2"
		value = [["", ["csv_table"], []], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		# Header at index 3
		header = result["c"][3]
		# Body at index 4
		body = result["c"][4]

		# Header should have 1 row with 2 cells
		assert len(header[1]) == 1  # 1 row
		assert len(header[1][0][1]) == 2  # 2 cells

		# Body should have 2 rows
		assert len(body[0][3]) == 2

	def test_csv_table_with_quoted_values(self):
		"""Test CSV with quoted values containing commas."""
		csv_content = 'Name,Description\nAlice,"Hello, World"\nBob,"Test, Value"'
		value = [["", ["csv_table"], []], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		assert result["t"] == "Table"

	def test_csv_table_with_ident_and_multiple_classes(self):
		"""Test CodeBlock with identifier and multiple classes including csv_table."""
		csv_content = "A,B\n1,2"
		value = [["my-table", ["csv_table", "data"], []], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		assert result["t"] == "Table"

	def test_csv_table_single_column(self):
		"""Test CSV table with single column."""
		csv_content = "Header\nRow1\nRow2"
		value = [["", ["csv_table"], []], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		assert len(result["c"][2]) == 1  # 1 column

	def test_csv_table_single_row(self):
		"""Test CSV table with header only (no body rows)."""
		csv_content = "H1,H2,H3"
		value = [["", ["csv_table"], []], csv_content]
		result = codeblock_process("CodeBlock", value, "html", {})

		assert result is not None
		# Body should have 0 rows
		body = result["c"][4]
		assert len(body[0][3]) == 0
