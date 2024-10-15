"`SplitMarkdownError` and `RenderError` exceptions"

import os
import argparse
import re
import shutil
from pathlib import Path
from typing import Any, Iterable, Literal, Optional, Tuple

import pypandoc
import tqdm
from jinja2 import Environment, FileSystemLoader, Template
from muutils.spinner import NoOpContextManager, Spinner, SpinnerContext

from pdj_sitegen.config import Config
from pdj_sitegen.consts import (
	FORMAT_PARSERS,
	FRONTMATTER_DELIMS,
	FRONTMATTER_REGEX,
	Format,
)



class SplitMarkdownError(Exception):
	"error while splitting markdown"

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