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
import sys
from pathlib import Path
from typing import Any, Iterable, Literal, Optional, Tuple
import shutil

from jinja2 import Environment, FileSystemLoader, Template
import pypandoc
import tqdm
from muutils.spinner import SpinnerContext, Spinner, NoOpContextManager

from pdj_sitegen.config import Config
from pdj_sitegen.consts import (
	FRONTMATTER_DELIMS,
	FRONTMATTER_REGEX,
	FORMAT_PARSERS,
	Format,
)

VERBOSE: bool = True

class SplitMarkdownError(Exception):
	"error while splitting markdown"
	pass

class RenderError(Exception):
	"error while rendering template"
	
	def __init__(
			self,
			message: str,
			kind: Literal["create_template", "render_template"],
			content: str|None,
			context: dict[str, Any]|None,
			jinja_env: Environment|None,
			template: Template|None,
		) -> None:
		super().__init__(message)
		self.message: str = message
		self.kind: Literal["create_template", "render_template"] = kind
		self.content: str|None = content
		self.context: dict[str, Any]|None = context
		self.jinja_env: Environment|None = jinja_env
		self.template: Template|None = template

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

def split_md(
	content: str,
) -> Tuple[str, str, Format]:
	"""parse markdown into a tuple of frontmatter, body, and frontmatter format
	
	will use `FRONTMATTER_REGEX` to split the markdown content into frontmatter and body.
	the possible delimiters are defined in `FRONTMATTER_DELIMS`.

	# Parameters:
	 - `content : str`   
	   markdown content to split
	
	# Returns:
	 - `Tuple[str, str, Format]` 
	   tuple of frontmatter, body, and frontmatter format (yaml, json, toml)
	
	# Raises:
	 - `SplitMarkdownError` : if the regex does not match
	"""
	match: Optional[re.Match[str]] = re.match(FRONTMATTER_REGEX, content)
	frontmatter: str
	body: str
	fmt: Format
	if match:
		# if the regex matches, extract the frontmatter, body, and format
		delimiter: str = match.group("delimiter")
		frontmatter = match.group("frontmatter")
		body = match.group("body")
		fmt = FRONTMATTER_DELIMS.get(delimiter, None)
	else:
		raise SplitMarkdownError(f"No frontmatter found in content\n{content = }")

	return frontmatter, body, fmt


def render(
	content: str,
	context: dict[str, Any],
	jinja_env: Environment,
) -> str:
	"""render content given context and jinja2 environment. raise RenderError if error occurs
	
	# Parameters:
	 - `content : str`   
	   text content with jinja2 template syntax
	 - `context : dict[str, Any]`   
	   data to render into the template
	 - `jinja_env : Environment`   
	   jinja2 environment to use for rendering
	
	# Returns:
	 - `str` 
	   rendered content
	
	# Raises:
	 - `RenderError` : if an error occurs while creating or rendering the template
	"""	
	try:
		template: Template = jinja_env.from_string(content)
	except Exception as e_template:
		raise RenderError(
			"Error creating template",
			kind="create_template",
			content=content,
			context=context,
			jinja_env=jinja_env,
			template=None,
		) from e_template

	try:
		output: str = template.render(context)
	except Exception as e_render:
		raise RenderError(
			"Error rendering template",
			kind="render_template",
			content=content,
			context=context,
			jinja_env=jinja_env,
			template=template,
		) from e_render

	return output


def build_document_tree(
	content_dir: Path,
	frontmatter_context: dict[str, Any],
	jinja_env: Environment,
) -> dict[str, dict[str, Any]]:
	"""given a dir of markdown files, return a dict of documents with rendered frontmatter
	
	documents are keyed by their path relative to `content_dir`, with suffix removed.
	the dict for each document will contain:

	- `frontmatter: dict[str, Any]` : rendered and parsed frontmatter for that document
	- `body: str` : plain, unrendered markdown content for that document
	- `file_meta: dict[str, Any]` : metadata about the file, including `"path", "path_html", "path_raw", "modified_time"`

	# Parameters:
	 - `content_dir : Path`   
	   path to glob for markdown files
	 - `frontmatter_context : dict[str, Any]`   
	   context to use to render the frontmatter *before* parsing it into a dict
	 - `jinja_env : Environment`   
	   jinja2 environment to use for rendering
	
	# Returns:
	 - `dict[str, dict[str, Any]]` 
	   dict of documents with rendered frontmatter.
	"""	
	md_files: list[Path] = list(content_dir.rglob("*.md"))

	if VERBOSE:
		print(f"Found {len(md_files)} markdown files in '{content_dir}'")

	docs: dict[str, dict[str, Any]] = {}

	for file_path in tqdm.tqdm(
		md_files,
		desc="building document tree",
		unit="file",
		disable=not VERBOSE,
	):
		file_path_str: str = (
			file_path.relative_to(content_dir).as_posix().removesuffix(".md")
		)
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
	"""given args to pass to pandoc, turn them into a list of strings we can actually pass
	
	keys must be strings. values can be strings, bools, or iterables of strings.

	when a value is a:

	- `bool` : if True, add the key to the list. if False, skip it.
	- `str` : add the key and value to the list together.
	- `iterable` : for each item in the iterable, add the key and item to the list together.
		(i.e. `"filters": ["filter_a", "filter_b"]` -> `["--filters", "filter_a", "--filters", "filter_b"]`)
	
	# Parameters:
	 - `pandoc_args : dict[str, Any]`   
	
	# Returns:
	 - `list[str]` 
	"""	
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
			raise ValueError(f"Invalid type for pandoc arg: {type(v) = } {v = }")

	return args


def convert_single_markdown_file(
	path: str,
	doc: dict[str, Any],
	docs: dict[str, dict[str, Any]],
	jinja_env: Environment,
	config: Config,
) -> None:
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
			k: v for k, v in docs.items() if (k.startswith(path) and k != path)
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
	pandoc_args: list[str] = process_pandoc_args(
		{
			**config.pandoc_kwargs,
			**context["frontmatter"].get("pandoc_kwargs", {}),
		}
	)

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
		
def convert_markdown_files(
	docs: dict[str, dict[str, Any]],
	jinja_env: Environment,
	config: Config,
	smart_rebuild: bool,
	rebuild_time: float,
) -> None:
	n_files: int = len(docs)
	path: str
	doc: dict[str, Any]
	if VERBOSE:
		print(f"Converting {n_files} markdown files to HTML...")
	for idx, (path, doc) in enumerate(docs.items()):
		path_raw: str = doc["file_meta"]["path_raw"]
		path_plain: str = doc["file_meta"]["path"]
		if smart_rebuild and os.path.getmtime(path_raw) <= rebuild_time:
			if VERBOSE:
				print(f"\t({idx+1:3} / {n_files})  [unmodified]  '{path_raw}'")
		else:
			if VERBOSE:
				print(f"\t({idx+1:3} / {n_files})  [building..]  '{path_raw}'")

			convert_single_markdown_file(
				path=path,
				doc=doc,
				docs=docs,
				jinja_env=jinja_env,
				config=config,
			)


def main() -> None:
	"""build the website

	# what this does:

	- read the config file from the given path
	- set up a Jinja2 environment according to the config
	- build a document tree from the markdown files in the content directory
	- process the markdown files into HTML files and write them to the output directory
	"""	
	global VERBOSE
	import argparse
	arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()
	# args: required positional config path, boolean flags `quiet` and `smart_rebuild`
	arg_parser.add_argument("config_path", type=str, help="path to the config file")
	arg_parser.add_argument(
		"-q", "--quiet",
		action="store_true",
		help="disable verbose output",
	)
	arg_parser.add_argument(
		"-s", "--smart-rebuild",
		action="store_true",
		help="enable smart rebuild",
	)
	args: argparse.Namespace = arg_parser.parse_args()
	config_path: Path = Path(args.config_path)
	VERBOSE = not args.quiet
	smart_rebuild: bool = args.smart_rebuild

	sp_class: type[Spinner] = SpinnerContext if VERBOSE else NoOpContextManager
	with sp_class(message="reading config and setting up jinja environment..."):
		# Read the config file
		config: Config = Config.read(config_path)

		# Set up Jinja2 environment
		jinja_env = Environment(
			loader=FileSystemLoader([config.templates_dir]),
			**config.jinja_env_kwargs,
		)

		# figure out the last rebuild time, write the current time to the file
		rebuild_time: float
		try:
			rebuild_time = os.path.getmtime(config.build_time_fname)
		except FileNotFoundError:
			# set it to very old time so that all files are rebuilt
			rebuild_time = -1.0

		with open(config.build_time_fname, "w", encoding="utf-8") as f:
			f.write(str(rebuild_time))

	# build doc tree
	docs: dict[str, dict[str, Any]] = build_document_tree(
		content_dir=config.content_dir,
		frontmatter_context={"config": config.serialize()},
		jinja_env=jinja_env,
	)

	# process markdown files
	convert_markdown_files(
		docs=docs,
		jinja_env=jinja_env,
		config=config,
		smart_rebuild=smart_rebuild,
		rebuild_time=rebuild_time,
	)

	# copy resources dir
	with sp_class(message="Copying resources directory..."):
		shutil.copytree(
			config.content_dir / config.resources_dir,
			config.output_dir / config.resources_dir,
			dirs_exist_ok=True,
		)


if __name__ == "__main__":
	main()
