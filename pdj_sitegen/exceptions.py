"""Exception classes for pdj-sitegen.

This module defines custom exceptions for the build pipeline:

- `SplitMarkdownError`: Raised when markdown cannot be split into frontmatter and body
- `ConversionError`: Raised when markdown to HTML conversion fails
- `RenderError`: Raised when Jinja2 template rendering fails
- `MultipleExceptions`: Aggregates multiple errors from batch processing
"""

from collections.abc import Mapping
from typing import Any, Literal

from jinja2 import Environment, Template


class SplitMarkdownError(Exception):
	"""Raised when markdown content cannot be split into frontmatter and body.

	This typically occurs when:
	- The frontmatter delimiters (---, ;;;, +++) are missing or malformed
	- The content does not match the expected frontmatter regex pattern
	- The frontmatter section cannot be parsed (invalid YAML/JSON/TOML)
	"""

	pass


class ConflictingIndexError(Exception):
	"""Raised when both index.md and _index.md exist in the same directory.

	When normalize_index_names is enabled, both files would produce the same
	output (index.html), so this is an error. The user must remove one.

	# Attributes:
	 - `directory : str` - the directory containing conflicting index files
	 - `files : list[str]` - list of conflicting file names
	"""

	def __init__(self, directory: str, files: list[str]) -> None:
		self.directory: str = directory
		self.files: list[str] = files
		message = (
			f"Conflicting index files in '{directory}': "
			f"{', '.join(repr(f) for f in files)}. "
			f"Remove one or set normalize_index_names: false"
		)
		super().__init__(message)


class ConversionError(Exception):
	"""Raised when markdown to HTML conversion fails.

	This exception captures details about the conversion failure including
	counts of failed vs total files for batch operations.

	# Attributes:
	 - `message : str` - description of what went wrong
	 - `n_failed : int` - number of files that failed to convert
	 - `n_total : int` - total number of files in the batch
	"""

	def __init__(
		self,
		message: str,
		n_failed: int = 1,
		n_total: int = 1,
	) -> None:
		super().__init__(message)
		self.message: str = message
		self.n_failed: int = n_failed
		self.n_total: int = n_total


class RenderError(Exception):
	"""Raised when Jinja2 template rendering fails.

	Captures context about the failure to aid debugging, including the
	template content, rendering context, and Jinja environment.

	# Attributes:
	 - `message : str` - description of what went wrong
	 - `kind : Literal["create_template", "render_template"]` - phase where error occurred
	 - `content : str | None` - the template source that failed
	 - `context : dict[str, Any] | None` - the context dict passed to render()
	 - `jinja_env : Environment | None` - the Jinja2 environment used
	 - `template : Template | None` - the compiled template (if creation succeeded)
	"""

	def __init__(
		self,
		message: str,
		kind: Literal["create_template", "render_template"],
		content: str | None,
		context: dict[str, Any] | None,
		jinja_env: Environment | None,
		template: Template | None,
	) -> None:
		super().__init__(message)
		self.message: str = message
		self.kind: Literal["create_template", "render_template"] = kind
		self.content: str | None = content
		self.context: dict[str, Any] | None = context
		self.jinja_env: Environment | None = jinja_env
		self.template: Template | None = template

	def __str__(self) -> str:  # pyright: ignore[reportImplicitOverride]
		if self.kind == "create_template":
			return (
				f"Error creating template: {self.message}\n"
				f"{self.content = }\n"
				f"{self.jinja_env = }"
			)
		elif self.kind == "render_template":
			return (
				f"Error rendering template: {self.message}\n"
				f"{self.template = }\n"
				f"{self.context = }"
			)
		else:
			return (
				f"Error: {self.message}\n"
				f"{self.kind = } (unknown)\n"
				f"{self.content = }\n"
				f"{self.context = }\n"
				f"{self.jinja_env = }\n"
				f"{self.template = }"
			)


class MultipleExceptions(Exception):
	"""Exception aggregating multiple errors that occurred during batch processing.

	Used when processing multiple files and collecting errors rather than
	failing on the first error. Stores individual exceptions keyed by
	their source (typically file path).

	# Attributes:
	 - `message : str` - summary message describing the failure
	 - `exceptions : dict[str, Exception]` - dictionary mapping source identifiers to exceptions
	 - `n_failed : int` - number of failures (computed from len(exceptions))
	 - `n_total : int` - total number of items that were processed
	"""

	def __init__(
		self,
		message: str,
		exceptions: Mapping[str, Exception],
		n_total: int = 0,
	) -> None:
		super().__init__(message)
		self.message: str = message
		self.exceptions: dict[str, Exception] = dict(exceptions)
		self.n_failed: int = len(exceptions)
		self.n_total: int = n_total if n_total > 0 else len(exceptions)

	def __str__(self) -> str:  # pyright: ignore[reportImplicitOverride]
		return (
			f"{len(self.exceptions)} exceptions occurred in: {list(self.exceptions.keys())}\n{self.message}\n"
			+ "\n".join(f"{name}: {exc}" for name, exc in self.exceptions.items())
		)
