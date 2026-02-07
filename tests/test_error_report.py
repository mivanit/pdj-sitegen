"""Tests for error_report module."""

import json
import shutil
from pathlib import Path
from typing import Any

import pytest
from jinja2 import Environment, UndefinedError

from pdj_sitegen.build import render
from pdj_sitegen.error_report import (
	create_dump_dir,
	dump_error_context,
	extract_file_path,
	extract_line_from_traceback,
	extract_line_number,
	format_location,
	format_multiple_errors,
	format_single_error,
	get_root_cause_message,
	get_source_info,
	handle_build_error,
	sanitize_filename,
)
from pdj_sitegen.exceptions import ConversionError, MultipleExceptions, RenderError


# Path to persistent test temp directory
TESTS_TEMP_DIR = Path(__file__).parent / ".temp"


@pytest.fixture
def temp_test_dir():
	"""Provide a persistent test directory that won't be cleaned up.

	Creates tests/.temp/ if it doesn't exist.
	Each test gets a unique subdirectory.
	"""
	TESTS_TEMP_DIR.mkdir(parents=True, exist_ok=True)
	return TESTS_TEMP_DIR


@pytest.fixture
def test_site_dir(temp_test_dir: Path, request: pytest.FixtureRequest) -> Path:
	"""Create a test site directory structure.

	Uses the test name as subdirectory to keep outputs separate.
	"""
	site_dir = temp_test_dir / request.node.name
	if site_dir.exists():
		shutil.rmtree(site_dir)
	site_dir.mkdir(parents=True)

	# Create basic structure
	(site_dir / "content").mkdir()
	(site_dir / "templates").mkdir()
	(site_dir / "output").mkdir()

	return site_dir


class TestExtractLineFromTraceback:
	"""Tests for extract_line_from_traceback function."""

	def test_extracts_line_from_jinja_error(self):
		"""Should extract line number from Jinja2 template error traceback."""
		jinja_env = Environment()
		try:
			# This will raise UndefinedError with traceback containing template line
			render("line1\n{{ undefined.attr }}\nline3", {}, jinja_env)
		except RenderError as e:
			# The root cause should have the traceback
			root = e.__cause__
			assert root is not None
			line = extract_line_from_traceback(root)
			assert line == 2  # Error is on line 2 of template

	def test_returns_none_for_non_template_error(self):
		"""Should return None when no template frame in traceback."""
		try:
			raise ValueError("not a template error")
		except ValueError as e:
			assert extract_line_from_traceback(e) is None


class TestExtractLineNumber:
	"""Tests for extract_line_number function."""

	def test_extracts_from_lineno_attribute(self):
		"""Should extract from lineno attribute if present."""

		class FakeError(Exception):
			lineno: int = 42

		assert extract_line_number(FakeError()) == 42

	def test_extracts_from_message(self):
		"""Should extract 'line X' from exception message."""
		exc = Exception("Error on line 15 of template")
		assert extract_line_number(exc) == 15

	def test_returns_none_when_no_line_info(self):
		"""Should return None when no line info available."""
		exc = Exception("Generic error message")
		assert extract_line_number(exc) is None

	def test_falls_back_to_traceback_extraction(self):
		"""Should fall back to traceback when no lineno attr or message pattern."""
		jinja_env = Environment()
		try:
			render("line1\n{{ undefined.attr }}\nline3", {}, jinja_env)
		except RenderError as e:
			# The root cause has line info only in traceback (no lineno attr, no "line X" msg)
			root = e.__cause__
			assert root is not None
			assert not hasattr(root, "lineno") or root.lineno is None  # pyright: ignore[reportAttributeAccessIssue]
			assert "line" not in str(root).lower() or "line 2" not in str(root)
			# extract_line_number should still find it via traceback fallback
			assert extract_line_number(root) == 2


class TestExtractFilePath:
	"""Tests for extract_file_path function."""

	def test_extracts_from_render_error_context(self):
		"""Should extract path_raw from RenderError context."""
		exc = RenderError(
			message="test",
			kind="render_template",
			content="",
			context={"file_meta": {"path_raw": "/path/to/file.md"}},
			jinja_env=None,
			template=None,
		)
		assert extract_file_path(exc) == "/path/to/file.md"

	def test_extracts_from_conversion_error(self):
		"""Should parse file path from ConversionError message."""
		exc = ConversionError("error converting file '/path/to/file.md'")
		assert extract_file_path(exc) == "/path/to/file.md"

	def test_returns_none_for_other_errors(self):
		"""Should return None for unrecognized error types."""
		exc = ValueError("some error")
		assert extract_file_path(exc) is None

	def test_returns_none_for_render_error_with_none_context(self):
		"""Should return None when RenderError.context is None."""
		exc = RenderError(
			message="test",
			kind="render_template",
			content="",
			context=None,
			jinja_env=None,
			template=None,
		)
		assert extract_file_path(exc) is None

	def test_returns_none_for_render_error_missing_file_meta(self):
		"""Should return None when context lacks file_meta key."""
		exc = RenderError(
			message="test",
			kind="render_template",
			content="",
			context={"other_key": "value"},
			jinja_env=None,
			template=None,
		)
		assert extract_file_path(exc) is None


class TestGetSourceInfo:
	"""Tests for get_source_info function."""

	def test_walks_exception_chain(self):
		"""Should find file/line info from exception chain."""
		root_cause = UndefinedError("'foo' is undefined")
		root_cause.lineno = 5  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]

		middle = RenderError(
			message="render failed",
			kind="render_template",
			content="",
			context={"file_meta": {"path_raw": "/test/file.md"}},
			jinja_env=None,
			template=None,
		)
		middle.__cause__ = root_cause

		file_path, line_number = get_source_info(middle)
		assert file_path == "/test/file.md"
		assert line_number == 5

	def test_single_exception_no_chain(self):
		"""Should handle single exception without __cause__."""
		exc = RenderError(
			message="test",
			kind="render_template",
			content="",
			context={"file_meta": {"path_raw": "/file.md"}},
			jinja_env=None,
			template=None,
		)
		# No __cause__ set

		file_path, line_number = get_source_info(exc)
		assert file_path == "/file.md"
		assert line_number is None

	def test_file_in_root_line_in_wrapper(self):
		"""Should find line in wrapper and file in root cause."""

		class FakeErrorWithLine(Exception):
			lineno: int = 10

		# Root has file info via ConversionError message
		root = ConversionError("error converting file '/root/file.md'")

		# Wrapper has line info
		wrapper = FakeErrorWithLine("wrapper with line")
		wrapper.__cause__ = root

		file_path, line_number = get_source_info(wrapper)
		assert file_path == "/root/file.md"
		assert line_number == 10


class TestGetRootCauseMessage:
	"""Tests for get_root_cause_message function."""

	def test_gets_root_cause(self):
		"""Should return the root cause message with exception type for short messages."""
		root = ValueError("the real problem")
		wrapper = Exception("wrapper")
		wrapper.__cause__ = root

		assert get_root_cause_message(wrapper) == "ValueError: the real problem"

	def test_strips_common_prefixes(self):
		"""Should strip 'Error rendering template:' prefix and include type for short messages."""
		exc = Exception("Error rendering template: 'foo' is undefined")
		assert get_root_cause_message(exc) == "Exception: 'foo' is undefined"

	def test_returns_type_name_for_empty_message(self):
		"""Should return exception type name when message is empty."""
		exc = ValueError("")
		assert get_root_cause_message(exc) == "ValueError"


class TestFormatLocation:
	"""Tests for format_location function."""

	def test_with_file_and_line(self):
		"""Should format as path:line."""
		assert format_location("/path/file.md", 42) == "/path/file.md:42"

	def test_with_file_only(self):
		"""Should return just path when no line number."""
		assert format_location("/path/file.md", None) == "/path/file.md"

	def test_with_no_file(self):
		"""Should return placeholder when no file path."""
		assert format_location(None, None) == "(unknown location)"


class TestSanitizeFilename:
	"""Tests for sanitize_filename function."""

	def test_replaces_path_separators(self):
		"""Should replace / and \\ with underscores."""
		assert sanitize_filename("/path/to/file.md") == "path_to_file.md"

	def test_strips_leading_underscores(self):
		"""Should remove leading underscores."""
		assert sanitize_filename("___file.md") == "file.md"

	def test_truncates_long_names(self):
		"""Should truncate names longer than 100 chars."""
		long_name = "a" * 150
		assert len(sanitize_filename(long_name)) == 100

	def test_replaces_colons(self):
		"""Should replace colons with underscores."""
		assert sanitize_filename("C:path:file.md") == "C_path_file.md"

	def test_returns_unknown_for_empty_result(self):
		"""Should return 'unknown' when sanitization yields empty string."""
		assert sanitize_filename("///") == "unknown"


class TestCreateDumpDir:
	"""Tests for create_dump_dir function."""

	def test_creates_timestamped_directory(self, temp_test_dir: Path) -> None:
		"""Should create .pdj-sitegen/<timestamp>/ directory."""
		dump_dir = create_dump_dir(temp_test_dir)

		assert dump_dir.exists()
		assert dump_dir.parent.name == ".pdj-sitegen"
		assert dump_dir.parent.parent == temp_test_dir

		# Write a marker so the directory isn't empty
		(dump_dir / "_test_marker.txt").write_text(
			"created by test_creates_timestamped_directory"
		)


class TestDumpErrorContext:
	"""Tests for dump_error_context function."""

	def test_dumps_traceback(self, test_site_dir: Path) -> None:
		"""Should create traceback.txt file."""
		dump_dir = test_site_dir / "dump"
		dump_dir.mkdir(parents=True, exist_ok=True)

		try:
			raise ValueError("test error")
		except ValueError as e:
			tb_path = dump_error_context(e, dump_dir)

		assert tb_path.exists()
		content = tb_path.read_text()
		assert "ValueError" in content
		assert "test error" in content

	def test_dumps_context_for_render_error(self, test_site_dir: Path) -> None:
		"""Should create context.json for RenderError."""
		dump_dir = test_site_dir / "dump"
		dump_dir.mkdir(parents=True, exist_ok=True)

		exc = RenderError(
			message="test",
			kind="render_template",
			content="template content",
			context={"key": "value", "nested": {"a": 1}},
			jinja_env=None,
			template=None,
		)

		dump_error_context(exc, dump_dir)

		ctx_path = dump_dir / "context.json"
		assert ctx_path.exists()
		ctx = json.loads(ctx_path.read_text())
		assert ctx["key"] == "value"
		assert ctx["nested"]["a"] == 1

	def test_dumps_template_content(self, test_site_dir: Path) -> None:
		"""Should create template.txt for RenderError with content."""
		dump_dir = test_site_dir / "dump"
		dump_dir.mkdir(parents=True, exist_ok=True)

		exc = RenderError(
			message="test",
			kind="render_template",
			content="{{ my_template }}",
			context={},
			jinja_env=None,
			template=None,
		)

		dump_error_context(exc, dump_dir)

		tpl_path = dump_dir / "template.txt"
		assert tpl_path.exists()
		assert tpl_path.read_text() == "{{ my_template }}"

	def test_uses_file_hint_as_suffix(self, test_site_dir: Path) -> None:
		"""Should append sanitized file_hint to dump filenames."""
		dump_dir = test_site_dir / "dump"
		dump_dir.mkdir(parents=True, exist_ok=True)

		try:
			raise ValueError("test error")
		except ValueError as e:
			tb_path = dump_error_context(e, dump_dir, file_hint="/path/to/file.md")

		# File should be named traceback_path_to_file.md.txt
		assert tb_path.name == "traceback_path_to_file.md.txt"
		assert tb_path.exists()

	def test_handles_non_serializable_context(self, test_site_dir: Path) -> None:
		"""Should handle non-JSON-serializable context gracefully."""
		dump_dir = test_site_dir / "dump"
		dump_dir.mkdir(parents=True, exist_ok=True)

		# Function is not JSON serializable, but default=str handles it
		def non_serializable_func(x: Any) -> Any:
			return x

		exc = RenderError(
			message="test",
			kind="render_template",
			content="",
			context={"func": non_serializable_func, "normal": "value"},
			jinja_env=None,
			template=None,
		)

		# Should not raise, traceback should still be created
		tb_path = dump_error_context(exc, dump_dir)
		assert tb_path.exists()

		# Context file should exist (uses default=str for non-serializable)
		ctx_path = dump_dir / "context.json"
		assert ctx_path.exists()
		ctx = json.loads(ctx_path.read_text())
		assert ctx["normal"] == "value"
		assert "function" in ctx["func"]  # Lambda serialized as string repr


class TestFormatSingleError:
	"""Tests for format_single_error function."""

	def test_formats_with_location(self):
		"""Should format error with file:line location."""
		exc = RenderError(
			message="'foo' is undefined",
			kind="render_template",
			content="",
			context={"file_meta": {"path_raw": "/path/file.md"}},
			jinja_env=None,
			template=None,
		)

		result = format_single_error(exc)
		assert "/path/file.md" in result
		assert "'foo' is undefined" in result or "foo" in result


class TestFormatMultipleErrors:
	"""Tests for format_multiple_errors function."""

	def test_formats_multiple_errors(self):
		"""Should list all failed files."""
		exceptions = {
			"/path/file1.md": ValueError("error 1"),
			"/path/file2.md": ValueError("error 2"),
		}
		exc = MultipleExceptions("multiple errors", exceptions)

		result = format_multiple_errors(exc)
		assert "2 files failed" in result
		assert "/path/file1.md" in result
		assert "/path/file2.md" in result


class TestHandleBuildError:
	"""Tests for handle_build_error function."""

	def test_creates_dump_directory(self, test_site_dir: Path) -> None:
		"""Should create .pdj-sitegen dump directory."""
		exc = ValueError("test error")

		handle_build_error(exc, test_site_dir)

		pdj_dir = test_site_dir / ".pdj-sitegen"
		assert pdj_dir.exists()
		# Should have at least one timestamped subdirectory
		subdirs = list(pdj_dir.iterdir())
		assert len(subdirs) >= 1

	def test_prints_terse_message(
		self, test_site_dir: Path, capsys: pytest.CaptureFixture[str]
	) -> None:
		"""Should print terse summary to stderr."""
		exc = ValueError("test error message")

		handle_build_error(exc, test_site_dir)

		captured = capsys.readouterr()
		assert "1/1 files failed" in captured.err
		assert "Full details:" in captured.err

	def test_handles_multiple_exceptions(
		self, test_site_dir: Path, capsys: pytest.CaptureFixture[str]
	) -> None:
		"""Should handle MultipleExceptions properly."""
		exceptions = {
			"/file1.md": ValueError("error 1"),
			"/file2.md": ValueError("error 2"),
		}
		exc = MultipleExceptions("failed", exceptions, n_total=5)

		handle_build_error(exc, test_site_dir)

		captured = capsys.readouterr()
		assert "2/5 files failed" in captured.err

		# Should create dump files for each exception
		pdj_dir = test_site_dir / ".pdj-sitegen"
		dump_dir = next(pdj_dir.iterdir())
		dump_files = list(dump_dir.iterdir())
		assert len(dump_files) >= 2  # At least 2 traceback files

	def test_handles_conversion_error(
		self, test_site_dir: Path, capsys: pytest.CaptureFixture[str]
	) -> None:
		"""Should handle ConversionError with n_failed/n_total counts."""
		exc = ConversionError(
			"error converting file '/test.md'", n_failed=3, n_total=10
		)

		handle_build_error(exc, test_site_dir)

		captured = capsys.readouterr()
		assert "3/10 files failed" in captured.err
		assert "Full details:" in captured.err

		# Should create dump directory with traceback
		pdj_dir = test_site_dir / ".pdj-sitegen"
		assert pdj_dir.exists()


class TestIntegration:
	"""Integration tests using actual Jinja2 errors."""

	def test_full_error_flow(
		self, test_site_dir: Path, capsys: pytest.CaptureFixture[str]
	) -> None:
		"""Test complete error handling flow with real Jinja2 error."""
		jinja_env = Environment()

		try:
			render(
				"line 1\n{{ undefined_var.attr }}\nline 3",
				{"file_meta": {"path_raw": str(test_site_dir / "test.md")}},
				jinja_env,
			)
		except RenderError as e:
			handle_build_error(e, test_site_dir)

		captured = capsys.readouterr()

		# Should show count and link
		assert "1/1 files failed" in captured.err
		assert "Full details:" in captured.err

		# Check dump directory was created with error details
		pdj_dir = test_site_dir / ".pdj-sitegen"
		assert pdj_dir.exists()
		dump_dir = next(pdj_dir.iterdir())

		# Traceback should contain the error details
		traceback_files = list(dump_dir.glob("traceback*.txt"))
		assert len(traceback_files) >= 1
		traceback_content = traceback_files[0].read_text()
		assert "undefined" in traceback_content.lower()
		assert "test.md" in traceback_content

	def test_template_syntax_error_flow(
		self, test_site_dir: Path, capsys: pytest.CaptureFixture[str]
	) -> None:
		"""Test error handling with TemplateSyntaxError (malformed template)."""
		jinja_env = Environment()

		try:
			# Unclosed variable tag causes TemplateSyntaxError
			render(
				"line 1\n{{ unclosed\nline 3",
				{"file_meta": {"path_raw": str(test_site_dir / "syntax_error.md")}},
				jinja_env,
			)
		except RenderError as e:
			# TemplateSyntaxError should have lineno attribute
			_file_path, line_number = get_source_info(e)
			assert line_number is not None  # Should extract line from syntax error

			handle_build_error(e, test_site_dir)

		captured = capsys.readouterr()
		assert "1/1 files failed" in captured.err

		# Dump should exist
		pdj_dir = test_site_dir / ".pdj-sitegen"
		assert pdj_dir.exists()

	def test_deeply_nested_exception_chain(
		self, test_site_dir: Path, capsys: pytest.CaptureFixture[str]
	) -> None:
		"""Test 3+ level exception chain extracts info correctly."""

		class Level3Error(Exception):
			lineno: int = 42

		class Level2Error(Exception):
			pass

		# Build 3-level chain: Level1 -> Level2 -> Level3
		level3 = Level3Error("root cause")
		level2 = Level2Error("middle")
		level2.__cause__ = level3
		level1 = RenderError(
			message="top level",
			kind="render_template",
			content="",
			context={"file_meta": {"path_raw": "/deep/nested/file.md"}},
			jinja_env=None,
			template=None,
		)
		level1.__cause__ = level2

		# Should find file from level1, line from level3
		file_path, line_number = get_source_info(level1)
		assert file_path == "/deep/nested/file.md"
		assert line_number == 42

		handle_build_error(level1, test_site_dir)

		captured = capsys.readouterr()
		assert "1/1 files failed" in captured.err
