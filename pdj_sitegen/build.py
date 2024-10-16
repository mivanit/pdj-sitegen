"""Build a site from markdown files using Jinja2 and Pandoc

Pipeline:

- Get all markdown files
- For each markdown file:
	- Regex frontmatter and content from the markdown file
	- Execute a template on the frontmatter, with globals_ and file metadata as context
	- Load the frontmatter into a dict
	- Execute a template on the content with frontmatter, globals_, file metadata, and all other docs as context
	- Convert the content to HTML using Pandoc
	- Execute a template on the specified or default template with the HTML content, frontmatter, globals_ and file metadata as context
- Copy the resources directory to the output directory
"""

import argparse
import datetime
import functools
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any, Callable, ContextManager, Iterable, Optional, Tuple

import pypandoc  # type: ignore[import-untyped]
import tqdm  # type: ignore[import-untyped]
from jinja2 import Environment, FileSystemLoader, Template
from muutils.json_serialize import json_serialize
from muutils.spinner import NoOpContextManager, SpinnerContext
from bs4 import BeautifulSoup  # type: ignore[import-untyped]

from pdj_sitegen.config import Config
from pdj_sitegen.consts import (
	FORMAT_PARSERS,
	FRONTMATTER_DELIMS,
	FRONTMATTER_REGEX,
	Format,
)
from pdj_sitegen.exceptions import (
	ConversionError,
	MultipleExceptions,
	RenderError,
	SplitMarkdownError,
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
		assert isinstance(frontmatter, str)
		body = match.group("body")
		assert isinstance(body, str)
		fmt = FRONTMATTER_DELIMS[delimiter]
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
	verbose: bool = True,
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

	if verbose:
		print(f"Found {len(md_files)} markdown files in '{content_dir}'")

	docs: dict[str, dict[str, Any]] = {}

	for file_path in tqdm.tqdm(
		md_files,
		desc="building document tree",
		unit="file",
		disable=not verbose,
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

		last_modified_time: float = file_path.stat().st_mtime
		file_meta: dict[str, Any] = {
			"path": file_path_str,
			"path_html": f"{file_path_str}.html",
			"path_raw": file_path.as_posix(),
			"modified_time": last_modified_time,
			"modified_time_str": datetime.datetime.fromtimestamp(
				last_modified_time
			).strftime("%Y-%m-%d %H:%M:%S"),
		}

		frontmatter_rendered: str = render(
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


def dump_intermediate(
	content: str,
	intermediates_dir: Optional[Path],
	fmt: str,
	path: str,
	subdir: str | None = None,
) -> None:
	"""Dump content to an intermediate file if intermediates_dir is specified"""
	if intermediates_dir:
		if subdir is None:
			subdir = fmt
		output_path: Path = intermediates_dir / fmt / f"{path}.{fmt}"
		output_path.parent.mkdir(parents=True, exist_ok=True)
		with open(output_path, "w", encoding="utf-8") as f:
			f.write(content)


def convert_single_markdown_file(
	path: str,
	output_root: Path,
	doc: dict[str, Any],
	docs: dict[str, dict[str, Any]],
	jinja_env: Environment,
	config: Config,
	intermediates_dir: Optional[Path] = None,
) -> None:
	frontmatter: dict = doc.get("frontmatter", {})
	assert isinstance(frontmatter, dict)
	body: str = doc.get("body", "")
	assert isinstance(body, str)
	file_meta: dict = doc.get("file_meta", {})
	assert isinstance(file_meta, dict)
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

	dump_intermediate_partial: Callable = functools.partial(
		dump_intermediate,
		intermediates_dir=intermediates_dir,
		path=file_meta["path"],
	)

	# dump frontmatter to intermediates
	dump_intermediate_partial(
		content=str(frontmatter),
		fmt="txt",
		subdir="frontmatter_txt",
	)
	dump_intermediate_partial(
		content=json.dumps(json_serialize(frontmatter)),
		fmt="json",
		subdir="frontmatter_json",
	)

	# Now, execute a template on the content with context
	# Render Markdown content with Jinja2
	rendered_md: str = render(
		content=body,
		context=context,
		jinja_env=jinja_env,
	)

	dump_intermediate_partial(content=rendered_md, fmt="md")

	# Convert Markdown to HTML using Pandoc
	pandoc_args: list[str] = process_pandoc_args(
		{
			**config.__pandoc__,
			**context["frontmatter"].get("__pandoc__", {}),
		}
	)

	html_content: str = pypandoc.convert_text(
		source=rendered_md,
		to=config.pandoc_fmt_to,
		format=config.pandoc_fmt_from,
		extra_args=pandoc_args,
	)

	dump_intermediate_partial(content=html_content, fmt="html")

	# Determine which HTML template to use
	template_name: str = frontmatter.get(
		"__template__",
		config.default_template.as_posix(),
	)

	# Render final HTML
	template: Template = jinja_env.get_template(template_name)
	final_html: str = template.render({"__content__": html_content, **context})
	if config.prettify:
		final_html = BeautifulSoup(final_html, "html.parser").prettify(
			formatter="minimal"
		)

	# Output HTML file
	output_path: Path = output_root / config.output_dir / file_meta["path_html"]
	output_path.parent.mkdir(parents=True, exist_ok=True)
	with open(output_path, "w", encoding="utf-8") as f:
		f.write(final_html)


def convert_markdown_files(
	docs: dict[str, dict[str, Any]],
	jinja_env: Environment,
	config: Config,
	output_root: Path,
	smart_rebuild: bool,
	rebuild_time: float,
	verbose: bool = True,
	intermediates_dir: Optional[Path] = None,
) -> None:
	n_files: int = len(docs)
	path: str
	doc: dict[str, Any]
	exceptions: dict[str, Exception] = dict()
	if verbose:
		print(f"Converting {n_files} markdown files to HTML...")
	for idx, (path, doc) in enumerate(docs.items()):
		path_raw: str = doc["file_meta"]["path_raw"]
		if smart_rebuild and os.path.getmtime(path_raw) <= rebuild_time:
			if verbose:
				print(f"\t({idx+1:3} / {n_files})  [unmodified]  '{path_raw}'")
		else:
			if verbose:
				print(f"\t({idx+1:3} / {n_files})  [building..]  '{path_raw}'")

			try:
				convert_single_markdown_file(
					path=path,
					output_root=output_root,
					doc=doc,
					docs=docs,
					jinja_env=jinja_env,
					config=config,
					intermediates_dir=intermediates_dir,
				)
			except Exception as e:
				exceptions[path_raw] = e
				if verbose:
					print(f"\t  Error converting '{path_raw}'!!!")
	if exceptions:
		first_key: str = next(iter(exceptions.keys()))
		if len(exceptions) == 1:
			raise ConversionError(
				f"error converting file '{first_key}'\n{exceptions[first_key]}"
			) from exceptions[first_key]
		else:
			raise MultipleExceptions(
				f"failed to convert {len(exceptions)}/{n_files} files",
				exceptions,
			) from exceptions[first_key]


def pipeline(
	config_path: Path,
	verbose: bool = True,
	smart_rebuild: bool = False,
) -> None:
	"""build the website

	# what this does:

	- change directory to the directory containing the config file
	- read the config file from the given path
	- set up a Jinja2 environment according to the config
	- build a document tree from the markdown files in the content directory
	- process the markdown files into HTML files and write them to the output directory
	"""

	# set up spinner context manager, depending on verbosity
	sp_class: type[ContextManager] = (
		functools.partial(SpinnerContext, update_interval=0.01)  # type: ignore[assignment]
		if verbose
		else NoOpContextManager
	)

	# get config path, change to the directory containing the config file
	root_dir: Path = config_path.parent
	root_dir_absolute: Path = root_dir.absolute()

	# read config and set up Jinja environment
	with sp_class(message="read config and set up jinja environment..."):  # type: ignore[call-arg]
		# Read the config file
		config: Config = Config.read(root_dir_absolute / config_path.name)

		# Set up Jinja2 environment
		jinja_env = Environment(
			loader=FileSystemLoader([root_dir_absolute / config.templates_dir]),
			**config.jinja_env_kwargs,
		)

		# figure out the last rebuild time, write the current time to the file
		rebuild_time: float
		try:
			rebuild_time = os.path.getmtime(root_dir_absolute / config.build_time_fname)
		except FileNotFoundError:
			# set it to very old time so that all files are rebuilt
			rebuild_time = -1.0

		with open(
			root_dir_absolute / config.build_time_fname, "w", encoding="utf-8"
		) as f:
			f.write(str(rebuild_time))

	# build doc tree (get .md files from `config.content_dir`, split content and frontmatter, execute templates on frontmatter)
	docs: dict[str, dict[str, Any]] = build_document_tree(
		content_dir=root_dir_absolute / config.content_dir,
		frontmatter_context={"config": config.serialize()},
		jinja_env=jinja_env,
		verbose=verbose,
	)

	# convert markdown files to HTML (execute templates with frontmatter on content, convert to HTML with Pandoc, execute template on HTML)
	convert_markdown_files(
		docs=docs,
		jinja_env=jinja_env,
		config=config,
		output_root=root_dir_absolute,
		smart_rebuild=smart_rebuild,
		rebuild_time=rebuild_time,
		verbose=verbose,
		intermediates_dir=(
			root_dir_absolute / config.intermediates_dir
			if config.intermediates_dir
			else None
		),
	)

	# copy resources dir to output dir
	with sp_class(message="Copying resources directory..."):  # type: ignore[call-arg]
		src_abs: Path = root_dir_absolute / config.content_dir / config.resources_dir
		out_abs: Path = root_dir_absolute / config.output_dir / config.resources_dir
		shutil.copytree(
			src=src_abs,
			dst=out_abs,
			dirs_exist_ok=True,
		)


def main() -> None:
	# parse args
	arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()
	arg_parser.add_argument("config_path", type=str, help="path to the config file")
	arg_parser.add_argument(
		"-q",
		"--quiet",
		action="store_true",
		help="disable verbose output",
	)
	arg_parser.add_argument(
		"-s",
		"--smart-rebuild",
		action="store_true",
		help="enable smart rebuild",
	)
	args: argparse.Namespace = arg_parser.parse_args()
	pipeline(
		config_path=Path(args.config_path),
		verbose=not args.quiet,
		smart_rebuild=args.smart_rebuild,
	)


if __name__ == "__main__":
	main()
