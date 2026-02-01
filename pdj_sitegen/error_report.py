"""Error reporting utilities for terse, actionable error messages.

Handles formatting of build errors with:
- File paths and line numbers
- Terse terminal output
- Verbose context dumped to .pdj-sitegen/<timestamp>/ directory
"""

import datetime
import json
import re
import sys
import traceback
from pathlib import Path
from typing import Any

from pdj_sitegen.exceptions import ConversionError, MultipleExceptions, RenderError


def extract_line_from_traceback(exc: BaseException) -> int | None:
	"""Extract template line number from exception traceback.

	Jinja2 rewrites tracebacks to show template lines like:
	  File "<template>", line 6, in top-level template code
	"""
	tb = exc.__traceback__
	while tb is not None:
		frame = tb.tb_frame
		# Check for Jinja2 template frames
		if frame.f_code.co_filename == "<template>":
			return tb.tb_lineno
		tb = tb.tb_next
	return None


def extract_line_number(exc: BaseException) -> int | None:
	"""Extract line number from Jinja2 exception.

	Tries multiple methods:
	1. lineno attribute (TemplateSyntaxError)
	2. Parse 'line X' from message
	3. Extract from traceback template frames
	"""
	# Check for lineno attribute (TemplateSyntaxError has this)
	if hasattr(exc, "lineno") and exc.lineno is not None:
		return int(exc.lineno)

	# Parse from message like "line 6" or "(line 6)"
	msg = str(exc)
	match = re.search(r"line (\d+)", msg, re.IGNORECASE)
	if match:
		return int(match.group(1))

	# Try extracting from traceback
	line = extract_line_from_traceback(exc)
	if line is not None:
		return line

	return None


def extract_file_path(exc: BaseException) -> str | None:
	"""Extract source file path from exception.

	Checks RenderError.context for file_meta, or ConversionError message.
	"""
	if isinstance(exc, RenderError) and exc.context:
		file_meta = exc.context.get("file_meta", {})
		return file_meta.get("path_raw")

	if isinstance(exc, ConversionError):
		# Parse from message like "error converting file '/path/to/file.md'"
		msg = str(exc)
		match = re.search(r"file ['\"]([^'\"]+)['\"]", msg)
		if match:
			return match.group(1)

	return None


def get_source_info(exc: BaseException) -> tuple[str | None, int | None]:
	"""Extract (file_path, line_number) from exception chain.

	Walks the __cause__ chain to find file and line info.
	"""
	file_path: str | None = None
	line_number: int | None = None

	# Walk the exception chain
	current: BaseException | None = exc
	while current is not None:
		if file_path is None:
			file_path = extract_file_path(current)

		if line_number is None:
			line_number = extract_line_number(current)

		# If we have both, we're done
		if file_path is not None and line_number is not None:
			break

		current = current.__cause__

	return file_path, line_number


def get_root_cause_message(exc: BaseException) -> str:
	"""Get the most specific error message from exception chain."""
	# Walk to the root cause
	current: BaseException | None = exc
	root: BaseException = exc
	while current is not None:
		root = current
		current = current.__cause__

	# Get exception type name
	exc_type = type(root).__name__

	# Get a clean message
	msg = str(root)
	# Remove common prefixes
	for prefix in ["Error rendering template:", "Error creating template:"]:
		if msg.startswith(prefix):
			msg = msg[len(prefix) :].strip()
			break

	if not msg:
		return exc_type

	# For short/cryptic messages, prepend the exception type
	if len(msg) < 30 or "'" not in msg:
		return f"{exc_type}: {msg}"

	return msg


def extract_source_line(exc: BaseException, line_number: int | None) -> str | None:
	"""Extract the source line that caused the error."""
	if line_number is None:
		return None

	# Walk chain to find RenderError with content
	current: BaseException | None = exc
	while current is not None:
		if isinstance(current, RenderError) and current.content:
			lines = current.content.splitlines()
			if 1 <= line_number <= len(lines):
				return lines[line_number - 1]
		current = current.__cause__

	return None


def format_location(file_path: str | None, line_number: int | None) -> str:
	"""Format file:line location string."""
	if file_path is None:
		return "(unknown location)"

	if line_number is not None:
		return f"{file_path}:{line_number}"
	return file_path


def format_single_error(exc: BaseException) -> str:
	"""Format a single exception tersely."""
	file_path, line_number = get_source_info(exc)
	root_msg = get_root_cause_message(exc)
	location = format_location(file_path, line_number)
	source_line = extract_source_line(exc, line_number)

	lines = [f"on {location}:"]
	if source_line is not None:
		lines.append(f"  {source_line.strip()}")
	lines.append(root_msg)

	return "\n".join(lines)


def format_multiple_errors(exc: MultipleExceptions) -> str:
	"""Format MultipleExceptions tersely."""
	lines = [f"{len(exc.exceptions)} files failed to convert:\n"]

	for idx, (path, sub_exc) in enumerate(exc.exceptions.items(), 1):
		_, line_number = get_source_info(sub_exc)
		root_msg = get_root_cause_message(sub_exc)
		location = format_location(path, line_number)
		source_line = extract_source_line(sub_exc, line_number)

		lines.append(f"  {idx}. on {location}:")
		if source_line is not None:
			lines.append(f"       {source_line.strip()}")
		lines.append(f"     {root_msg}\n")

	return "\n".join(lines)


def create_dump_dir(root_dir: Path) -> Path:
	"""Create .pdj-sitegen/<timestamp>/ directory."""
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	dump_dir = root_dir / ".pdj-sitegen" / timestamp
	dump_dir.mkdir(parents=True, exist_ok=True)
	return dump_dir


def sanitize_filename(path: str) -> str:
	"""Convert a file path to a safe filename."""
	# Replace path separators and other problematic chars
	safe = path.replace("/", "_").replace("\\", "_").replace(":", "_")
	# Remove leading underscores
	safe = safe.lstrip("_")
	# Truncate if too long
	if len(safe) > 100:
		safe = safe[:100]
	return safe or "unknown"


def dump_error_context(
	exc: BaseException,
	dump_dir: Path,
	file_hint: str | None = None,
) -> Path:
	"""Dump verbose error context to files.

	Creates:
	- traceback.txt - full Python traceback
	- context.json - RenderError context (if available)
	- template.txt - template content (if available)

	Returns path to the main error file.
	"""
	suffix = f"_{sanitize_filename(file_hint)}" if file_hint else ""

	# Dump full traceback
	tb_path = dump_dir / f"traceback{suffix}.txt"
	with open(tb_path, "w") as f:
		f.write("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))

	# Dump context if RenderError
	if isinstance(exc, RenderError) and exc.context:
		ctx_path = dump_dir / f"context{suffix}.json"
		try:
			# Use default=str to handle non-serializable objects
			with open(ctx_path, "w") as f:
				json.dump(exc.context, f, indent=2, default=str)
		except Exception:
			pass  # Best effort

	# Dump template content if available
	if isinstance(exc, RenderError) and exc.content:
		tpl_path = dump_dir / f"template{suffix}.txt"
		with open(tpl_path, "w") as f:
			f.write(exc.content)

	return tb_path


def handle_build_error(exc: BaseException, root_dir: Path) -> None:
	"""Handle a build error: print terse message, dump context, exit.

	This is the main entry point for error handling.
	"""
	# Create dump directory
	dump_dir = create_dump_dir(root_dir)

	# Get counts and dump context
	if isinstance(exc, MultipleExceptions):
		n_failed = exc.n_failed
		n_total = exc.n_total
		# Dump each sub-exception
		for path, sub_exc in exc.exceptions.items():
			dump_error_context(sub_exc, dump_dir, file_hint=path)
	elif isinstance(exc, ConversionError):
		n_failed = exc.n_failed
		n_total = exc.n_total
		file_path, _ = get_source_info(exc)
		dump_error_context(exc, dump_dir, file_hint=file_path)
	else:
		n_failed = 1
		n_total = 1
		file_path, _ = get_source_info(exc)
		dump_error_context(exc, dump_dir, file_hint=file_path)

	# Print detailed error info
	if isinstance(exc, MultipleExceptions):
		print(format_multiple_errors(exc), file=sys.stderr)
	else:
		print(format_single_error(exc), file=sys.stderr)

	# Print summary in red
	print(f"\n\033[91m{n_failed}/{n_total} files failed to convert\033[0m", file=sys.stderr)
	print(f"  Full details: {dump_dir}/", file=sys.stderr)
