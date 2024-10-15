"""Build a site from markdown files using Jinja2 and Pandoc

Pipeline:

- Get all markdown files
- For each markdown file:
    - Regex frontmatter and content from the markdown file
    - Execute a template on the frontmatter, with globals_ and file metadata as context
    - Load the frontmatter into a dict
    - Execute a template on the content with frontmatter, globals_ and file metadata as context
    - Convert the content to HTML using Pandoc
    - Execute a template on the specified or default template with the HTML content, frontmatter, globals_ and file metadata as context
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Tuple

import yaml
from jinja2 import Environment, FileSystemLoader, Template
from muutils.dictmagic import kwargs_to_nested_dict, update_with_nested_dict
import pypandoc

from pdj_sitegen.config import Config
from pdj_sitegen.consts import FRONTMATTER_DELIMS, FRONTMATTER_REGEX, FORMAT_PARSERS, Format #, StructureFormat


class RenderError(Exception):
	pass

def split_md(
		content: str,
	) -> Tuple[str, str, Format]:
	"parse markdown into a tuple of frontmatter, body, and frontmatter format"
	match: Optional[re.Match[str]] = re.match(FRONTMATTER_REGEX, content)
	frontmatter: str
	body: str
	fmt: Format
	if match:
		# if the regex matches, extract the frontmatter, body, and format
		delimiter: str = match.group("delimiter")
		frontmatter = match.group("frontmatter")
		body = match.group("body")
		fmt = FRONTMATTER_DELIMS.get(
			delimiter, None
		)
	else:
		raise Exception("No frontmatter found in content.")

	return frontmatter, body, fmt

def render(
	content: str,
	context: dict[str, Any],
	jinja_env: Environment,
) -> str:
	try:
		template: Template = jinja_env.from_string(content)
	except Exception as e_template:
		raise RenderError(f"Error creating template: {e_template}\n{content = }\n{jinja_env = }") from e_template

	try:
		output: str = template.render(context)
	except Exception as e_render:
		raise RenderError(f"Error rendering template: {e_render}\n{template = }\n{context = }") from e_render

	return output

def build_document_tree(
	content_dir: Path,
	frontmatter_context: dict[str, Any],
	jinja_env: Environment,
) -> dict[str, dict[str, Any]]:
	"given a dir of markdown files, return a dict of documents with rendered frontmatter"
	md_files: list[Path] = list(content_dir.rglob("*.md"))

	docs: dict[str, dict[str, Any]] = {}

	for file_path in md_files:
		file_path_str: str = file_path.relative_to(content_dir).as_posix().removesuffix(".md")
		with open(file_path, "r", encoding="utf-8") as f:
			content: str = f.read()
		frontmatter_raw: str
		body: str
		fmt: Format
		frontmatter_raw, body, fmt = split_md(content)
		
		file_meta: dict[str, Any] = {
			"path": file_path_str,
			"path_html": f"{file_path_str}.html",
			"path_raw": file_path.as_posix(),
			"modified_time": os.path.getmtime(file_path),
		}
		
		frontmatter_rendered: dict[str, Any] = render(
			content=frontmatter_raw,
			context={**frontmatter_context, "file_meta": file_meta},
			jinja_env=jinja_env,
		)
		frontmatter: dict[str, Any] = FORMAT_PARSERS[fmt](frontmatter_rendered)

		docs[file_path_str] = {
			"frontmatter": frontmatter,
			"body": body,
			"file_meta": file_meta,
		}
	return docs


def process_pandoc_args(pandoc_args: dict[str, Any]) -> list[str]:
	args: list[str] = list()
	for k, v in pandoc_args.items():
		if isinstance(v, bool):
			if v:
				args.append(f"--{k}")
		elif isinstance(v, str):
			args.extend([f"--{k}", v])
		elif isinstance(v, Iterable):
			for x in v:
				args.extend([f"--{k}", x])
		else:
			args.extend([f"--{k}", v])

	return args

def process_markdown_files(
	docs: dict[str, dict[str, Any]],
	jinja_env: Environment,
	config: Config,
) -> None:
	path: str
	doc: dict[str, Any]
	for path, doc in docs.items():
		frontmatter: dict = doc.get("frontmatter", {})
		body: dict = doc.get("body", "")
		file_meta: str = doc.get("file_meta", {})
		context: dict[str, Any] = {
			**frontmatter,
			"frontmatter": frontmatter,
			"file_meta": file_meta,
			"config": config.serialize(),
			"docs": docs,
			"child_docs": {
				k: v
				for k, v in docs.items()
				if (k.startswith(path) and k != path)
			},
		}

		# Now, execute a template on the content with context
		# Render Markdown content with Jinja2
		rendered_md: str = render(
			content=body,
			context=context,
			jinja_env=jinja_env,
		)

		# Convert Markdown to HTML using Pandoc
		pandoc_args: list[str] = process_pandoc_args({
			**config.pandoc_kwargs,
			**context["frontmatter"].get("pandoc_kwargs", {}),
		})

		html_content: str = pypandoc.convert_text(
			source=rendered_md,
			to=config.pandoc_fmt_to,
			format=config.pandoc_fmt_from,
			extra_args=pandoc_args,
		)

		# Determine which HTML template to use
		template_name: str = frontmatter.get(
			"__template__",
			config.default_template.as_posix(),
		)

		# Render final HTML
		template: Template = jinja_env.get_template(template_name)
		final_html: str = template.render({"__content__": html_content, **context})

		# Output HTML file
		output_path: Path = config.output_dir / file_meta["path_html"]
		output_path.parent.mkdir(parents=True, exist_ok=True)
		with open(output_path, "w", encoding="utf-8") as f:
			f.write(final_html)


def main() -> None:
	if len(sys.argv) == 1:
		config_path = Path(sys.argv[1])
	else:
		raise Exception("No config file provided.")

	# Read the config file
	config: Config = Config.read(config_path)

	# Set up Jinja2 environment
	jinja_env = Environment(
		loader=FileSystemLoader([config.templates_dir]),
		**config.jinja_env_kwargs,
	)

	docs: dict[str, dict[str, Any]] = build_document_tree(
		content_dir=config.content_dir,
		frontmatter_context={"config" : config.serialize()},
		jinja_env=jinja_env,
	)


	process_markdown_files(
		docs=docs,
		jinja_env=jinja_env,
		config=config,
	)


if __name__ == "__main__":
	main()
