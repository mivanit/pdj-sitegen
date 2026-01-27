"`SplitMarkdownError` and `RenderError` exceptions"

from typing import Any, Literal

from jinja2 import Environment, Template


class SplitMarkdownError(Exception):
	"error while splitting markdown"

	pass


class ConversionError(Exception):
	"error while converting markdown"

	pass


class RenderError(Exception):
	"error while rendering template"

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

	def __str__(self) -> str:
		if self.kind == "create_template":
			return (
				f"Error creating template: {self.message}\n"
				# f"{self.content = }\n"
				# f"{self.jinja_env = }"
			)
		elif self.kind == "render_template":
			return (
				f"Error rendering template: {self.message}\n"
				# f"{self.template = }\n"
				# f"{self.context = }"
			)
		else:
			return (
				f"Error: {self.message}\n" f"{self.kind = } (unknown)\n"
				# f"{self.content = }\n"
				# f"{self.context = }\n"
				# f"{self.jinja_env = }\n"
				# f"{self.template = }"
			)


class MultipleExceptions(Exception):
	def __init__(self, message: str, exceptions: dict[str, Exception]):
		super().__init__(message)
		self.message: str = message
		self.exceptions: dict[str, Exception] = exceptions

	def __str__(self) -> str:
		return (
			f"{len(self.exceptions)} exceptions occurred in: {list(self.exceptions.keys())}\n{self.message}\n"
			+ "\n".join(f"{name}: {exc}" for name, exc in self.exceptions.items())
		)
