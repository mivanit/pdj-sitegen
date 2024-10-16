> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## Contents

[![PyPI](https://img.shields.io/pypi/v/pdj-sitegen)](https://pypi.org/project/pdj-sitegen/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pdj-sitegen)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/pdj-sitegen)

[![Checks](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml)
[![Checks -
docs](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml)
[![Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iOTkiIGhlaWdodD0iMjAiPg0KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iYiIgeDI9IjAiIHkyPSIxMDAlIj4NCiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+DQogICAgICAgIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1vcGFjaXR5PSIuMSIvPg0KICAgIDwvbGluZWFyR3JhZGllbnQ+DQogICAgPG1hc2sgaWQ9ImEiPg0KICAgICAgICA8cmVjdCB3aWR0aD0iOTkiIGhlaWdodD0iMjAiIHJ4PSIzIiBmaWxsPSIjZmZmIi8+DQogICAgPC9tYXNrPg0KICAgIDxnIG1hc2s9InVybCgjYSkiPg0KICAgICAgICA8cGF0aCBmaWxsPSIjNTU1IiBkPSJNMCAwaDYzdjIwSDB6Ii8+DQogICAgICAgIDxwYXRoIGZpbGw9IiNhNGE2MWQiIGQ9Ik02MyAwaDM2djIwSDYzeiIvPg0KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+DQogICAgPC9nPg0KICAgIDxnIGZpbGw9IiNmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJEZWphVnUgU2FucyxWZXJkYW5hLEdlbmV2YSxzYW5zLXNlcmlmIiBmb250LXNpemU9IjExIj4NCiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSIzMS41IiB5PSIxNCI+Y292ZXJhZ2U8L3RleHQ+DQogICAgICAgIDx0ZXh0IHg9IjgwIiB5PSIxNSIgZmlsbD0iIzAxMDEwMSIgZmlsbC1vcGFjaXR5PSIuMyI+NzklPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjc5JTwvdGV4dD4NCiAgICA8L2c+DQo8L3N2Zz4NCg==)](docs/coverage/html/)

![GitHub
commits](https://img.shields.io/github/commit-activity/t/mivanit/pdj-sitegen)
![GitHub commit
activity](https://img.shields.io/github/commit-activity/m/mivanit/pdj-sitegen)
![GitHub closed pull
requests](https://img.shields.io/github/issues-pr-closed/mivanit/pdj-sitegen)
![code size,
bytes](https://img.shields.io/github/languages/code-size/mivanit/pdj-sitegen)

# `pdj_sitegen`

***P***an***d***oc and ***J***inja ***Site*** ***Gen***erator

- docs: [`miv.name/pdj_sitegen/`](https://miv.name/pdj-sitegen/)
- demo site:
  [`miv.name/pdj_sitegen/demo_site/`](https://miv.name/pdj-sitegen/demo_site/)
- source:
  [`github.com/mivanit/pdj-sitegen`](https://github.com/mivanit/pdj-sitegen)

# Installation:

``` bash
pip install pdj-sitegen
```

you should either have [Pandoc](https://pandoc.org/) installed, or you
can run

``` bash
python -m pdj_sitegen.install_pandoc
```

which will install `pandoc` using
[`pypandoc`](https://github.com/JessicaTegner/pypandoc)

# Usage

1.  create a config file. For an example, see
    `pdj_sitegen.config.DEFAULT_CONFIG_YAML`, or print a copy of it via

``` bash
python -m pdj_sitegen.config
```

2.  adjust the config file to your needs. most importantly:

``` yaml
# directory with markdown content files and resources, relative to cwd
content_dir: content/
# directory with resources, relative to `content_dir`
resources_dir: resources/
# templates directory, relative to cwd
templates_dir: templates/
# default template file, relative to `templates_dir`
default_template: default.html.jinja2
# output directory, relative to cwd
output_dir: docs/
```

3.  populate the `content` directory with markdown files, populate
    `content/resources/` with resources (images, css, etc.), and adjust
    templates in the `templates` directory. See the demo site for usage
    examples.

4.  run the generator

``` bash
python -m pdj_sitegen your_config.yaml
```

## Submodules

- [`build`](#build)
- [`config`](#config)
- [`consts`](#consts)
- [`exceptions`](#exceptions)
- [`filters`](#filters)
- [`install_pandoc`](#install_pandoc)
- [`setup_site`](#setup_site)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/__init__.py)

# `pdj_sitegen`

[![PyPI](https://img.shields.io/pypi/v/pdj-sitegen)](https://pypi.org/project/pdj-sitegen/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pdj-sitegen)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/pdj-sitegen)

[![Checks](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml)
[![Checks -
docs](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml)
[![Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iOTkiIGhlaWdodD0iMjAiPg0KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iYiIgeDI9IjAiIHkyPSIxMDAlIj4NCiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+DQogICAgICAgIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1vcGFjaXR5PSIuMSIvPg0KICAgIDwvbGluZWFyR3JhZGllbnQ+DQogICAgPG1hc2sgaWQ9ImEiPg0KICAgICAgICA8cmVjdCB3aWR0aD0iOTkiIGhlaWdodD0iMjAiIHJ4PSIzIiBmaWxsPSIjZmZmIi8+DQogICAgPC9tYXNrPg0KICAgIDxnIG1hc2s9InVybCgjYSkiPg0KICAgICAgICA8cGF0aCBmaWxsPSIjNTU1IiBkPSJNMCAwaDYzdjIwSDB6Ii8+DQogICAgICAgIDxwYXRoIGZpbGw9IiNhNGE2MWQiIGQ9Ik02MyAwaDM2djIwSDYzeiIvPg0KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+DQogICAgPC9nPg0KICAgIDxnIGZpbGw9IiNmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJEZWphVnUgU2FucyxWZXJkYW5hLEdlbmV2YSxzYW5zLXNlcmlmIiBmb250LXNpemU9IjExIj4NCiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSIzMS41IiB5PSIxNCI+Y292ZXJhZ2U8L3RleHQ+DQogICAgICAgIDx0ZXh0IHg9IjgwIiB5PSIxNSIgZmlsbD0iIzAxMDEwMSIgZmlsbC1vcGFjaXR5PSIuMyI+NzklPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjc5JTwvdGV4dD4NCiAgICA8L2c+DQo8L3N2Zz4NCg==)](docs/coverage/html/)

![GitHub
commits](https://img.shields.io/github/commit-activity/t/mivanit/pdj-sitegen)
![GitHub commit
activity](https://img.shields.io/github/commit-activity/m/mivanit/pdj-sitegen)
![GitHub closed pull
requests](https://img.shields.io/github/issues-pr-closed/mivanit/pdj-sitegen)
![code size,
bytes](https://img.shields.io/github/languages/code-size/mivanit/pdj-sitegen)

### `pdj_sitegen`

***P***an***d***oc and ***J***inja ***Site*** ***Gen***erator

- docs: [`miv.name/pdj_sitegen/`](https://miv.name/pdj-sitegen/)
- demo site:
  [`miv.name/pdj_sitegen/demo_site/`](https://miv.name/pdj-sitegen/demo_site/)
- source:
  [`github.com/mivanit/pdj-sitegen`](https://github.com/mivanit/pdj-sitegen)

### Installation:

``` bash
pip install pdj-sitegen
```

you should either have [Pandoc](https://pandoc.org/) installed, or you
can run

``` bash
python -m <a href="pdj_sitegen/install_pandoc.html">pdj_sitegen.install_pandoc</a>
```

which will install `pandoc` using
[`pypandoc`](https://github.com/JessicaTegner/pypandoc)

### Usage

1.  create a config file. For an example, see
    `<a href="pdj_sitegen/config.html#DEFAULT_CONFIG_YAML">pdj_sitegen.config.DEFAULT_CONFIG_YAML</a>`,
    or print a copy of it via

``` bash
python -m <a href="pdj_sitegen/config.html">pdj_sitegen.config</a>
```

2.  adjust the config file to your needs. most importantly:

``` yaml
### directory with markdown content files and resources, relative to cwd
content_dir: content/
### directory with resources, relative to `content_dir`
resources_dir: resources/
### templates directory, relative to cwd
templates_dir: templates/
### default template file, relative to `templates_dir`
default_template: default.html.jinja2
### output directory, relative to cwd
output_dir: docs/
```

3.  populate the `content` directory with markdown files, populate
    `content/resources/` with resources (images, css, etc.), and adjust
    templates in the `templates` directory. See the demo site for usage
    examples.

4.  run the generator

``` bash
python -m pdj_sitegen your_config.yaml
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/__init__.py#L0-L2)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## Contents

Build a site from markdown files using Jinja2 and Pandoc

Pipeline:

- Get all markdown files
- For each markdown file: - Regex frontmatter and content from the
  markdown file - Execute a template on the frontmatter, with globals\_
  and file metadata as context - Load the frontmatter into a dict -
  Execute a template on the content with frontmatter, globals\_, file
  metadata, and all other docs as context - Convert the content to HTML
  using Pandoc - Execute a template on the specified or default template
  with the HTML content, frontmatter, globals\_ and file metadata as
  context
- Copy the resources directory to the output directory

## API Documentation

- [`split_md`](#split_md)
- [`render`](#render)
- [`build_document_tree`](#build_document_tree)
- [`process_pandoc_args`](#process_pandoc_args)
- [`dump_intermediate`](#dump_intermediate)
- [`convert_single_markdown_file`](#convert_single_markdown_file)
- [`convert_markdown_files`](#convert_markdown_files)
- [`pipeline`](#pipeline)
- [`main`](#main)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py)

# `pdj_sitegen.build`

Build a site from markdown files using Jinja2 and Pandoc

Pipeline:

- Get all markdown files
- For each markdown file: - Regex frontmatter and content from the
  markdown file - Execute a template on the frontmatter, with globals\_
  and file metadata as context - Load the frontmatter into a dict -
  Execute a template on the content with frontmatter, globals\_, file
  metadata, and all other docs as context - Convert the content to HTML
  using Pandoc - Execute a template on the specified or default template
  with the HTML content, frontmatter, globals\_ and file metadata as
  context
- Copy the resources directory to the output directory

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L0-L508)

### `def split_md`

``` python
(content: str) -> Tuple[str, str, Literal['yaml', 'json', 'toml']]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L47-L81)

parse markdown into a tuple of frontmatter, body, and frontmatter format

will use `FRONTMATTER_REGEX` to split the markdown content into
frontmatter and body. the possible delimiters are defined in
`FRONTMATTER_DELIMS`.

### Parameters:

- `content : str` markdown content to split

### Returns:

- `Tuple[str, str, Format]` tuple of frontmatter, body, and frontmatter
  format (yaml, json, toml)

### Raises:

- `SplitMarkdownError` : if the regex does not match

### `def render`

``` python
(
    content: str,
    context: dict[str, typing.Any],
    jinja_env: jinja2.environment.Environment
) -> str
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L84-L130)

render content given context and jinja2 environment. raise RenderError
if error occurs

### Parameters:

- `content : str` text content with jinja2 template syntax
- `context : dict[str, Any]` data to render into the template
- `jinja_env : Environment` jinja2 environment to use for rendering

### Returns:

- `str` rendered content

### Raises:

- `RenderError` : if an error occurs while creating or rendering the
  template

### `def build_document_tree`

``` python
(
    content_dir: pathlib.Path,
    frontmatter_context: dict[str, typing.Any],
    jinja_env: jinja2.environment.Environment,
    verbose: bool = True
) -> dict[str, dict[str, typing.Any]]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L133-L206)

given a dir of markdown files, return a dict of documents with rendered
frontmatter

documents are keyed by their path relative to `content_dir`, with suffix
removed. the dict for each document will contain:

- `frontmatter: dict[str, Any]` : rendered and parsed frontmatter for
  that document
- `body: str` : plain, unrendered markdown content for that document
- `file_meta: dict[str, Any]` : metadata about the file, including
  `"path", "path_html", "path_raw", "modified_time"`

### Parameters:

- `content_dir : Path` path to glob for markdown files
- `frontmatter_context : dict[str, Any]` context to use to render the
  frontmatter *before* parsing it into a dict
- `jinja_env : Environment` jinja2 environment to use for rendering

### Returns:

- `dict[str, dict[str, Any]]` dict of documents with rendered
  frontmatter.

### `def process_pandoc_args`

``` python
(pandoc_args: dict[str, typing.Any]) -> list[str]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L209-L240)

given args to pass to pandoc, turn them into a list of strings we can
actually pass

keys must be strings. values can be strings, bools, or iterables of
strings.

when a value is a:

- `bool` : if True, add the key to the list. if False, skip it.
- `str` : add the key and value to the list together.
- `iterable` : for each item in the iterable, add the key and item to
  the list together. (i.e. `"filters": ["filter_a", "filter_b"]` -\>
  `["--filters", "filter_a", "--filters", "filter_b"]`)

### Parameters:

- `pandoc_args : dict[str, Any]`

### Returns:

- `list[str]`

### `def dump_intermediate`

``` python
(
    content: str,
    intermediates_dir: Optional[pathlib.Path],
    fmt: str,
    path: str,
    subdir: str | None = None
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L243-L257)

Dump content to an intermediate file if intermediates_dir is specified

### `def convert_single_markdown_file`

``` python
(
    path: str,
    output_root: pathlib.Path,
    doc: dict[str, typing.Any],
    docs: dict[str, dict[str, typing.Any]],
    jinja_env: jinja2.environment.Environment,
    config: pdj_sitegen.config.Config,
    intermediates_dir: Optional[pathlib.Path] = None
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L260-L345)

### `def convert_markdown_files`

``` python
(
    docs: dict[str, dict[str, typing.Any]],
    jinja_env: jinja2.environment.Environment,
    config: pdj_sitegen.config.Config,
    output_root: pathlib.Path,
    smart_rebuild: bool,
    rebuild_time: float,
    verbose: bool = True,
    intermediates_dir: Optional[pathlib.Path] = None
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L348-L397)

### `def pipeline`

``` python
(
    config_path: pathlib.Path,
    verbose: bool = True,
    smart_rebuild: bool = False
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L400-L481)

build the website

### what this does:

- change directory to the directory containing the config file
- read the config file from the given path
- set up a Jinja2 environment according to the config
- build a document tree from the markdown files in the content directory
- process the markdown files into HTML files and write them to the
  output directory

### `def main`

``` python
() -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/build.py#L484-L505)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## Contents

define the config, and also provide CLI for printing template

## API Documentation

- [`DEFAULT_CONFIG_YAML`](#DEFAULT_CONFIG_YAML)
- [`read_data_file`](#read_data_file)
- [`emit_data_file`](#emit_data_file)
- [`save_data_file`](#save_data_file)
- [`Config`](#Config)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py)

# `pdj_sitegen.config`

define the config, and also provide CLI for printing template

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L0-L166)

- `DEFAULT_CONFIG_YAML: str = '# NOTE: the current working directory (cwd) will be set to the location of this file!\n# directory with markdown content files and resources, relative to cwd\ncontent_dir: content\n# directory with resources, relative to`content_dir`\nresources_dir: resources\n# templates directory, relative to cwd\ntemplates_dir: templates\n# default template file, relative to`templates_dir`\ndefault_template: default.html.jinja2\n# output directory, relative to cwd\noutput_dir: docs\n# intermediate files directory -- if null, then no intermediate files will be saved\nintermediates_dir: null\n# kwargs to pass to the Jinja2 environment\njinja_env_kwargs: {}\n# pandoc formats\npandoc_fmt_from: markdown+smart\npandoc_fmt_to: html\n# extra kwargs to pass to pandoc (this will be augmented with`pandoc_args`from the frontmatter of a file)\npandoc_kwargs:\n  mathjax: true\n# extra globals to pass -- this can be anything\nglobals_:\n  pdjsg_url: https://github.com/mivanit/pdj-sitegen'`

### `def read_data_file`

``` python
(
    file_path: pathlib.Path,
    fmt: Optional[Literal['yaml', 'json', 'toml']] = None
) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L35-L51)

read a file from any of json, yaml, or toml

### `def emit_data_file`

``` python
(data: dict[str, typing.Any], fmt: Literal['yaml', 'json', 'toml']) -> str
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L54-L64)

emit a file as json or yaml

### `def save_data_file`

``` python
(
    data: dict[str, typing.Any],
    file_path: pathlib.Path,
    fmt: Optional[Literal['yaml', 'json', 'toml']] = None
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L67-L76)

save a file as json or yaml

### `class Config(muutils.json_serialize.serializable_dataclass.SerializableDataclass):`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L79-L154)

configuration for the site generator

### `Config`

``` python
(
    content_dir: pathlib.Path = WindowsPath('content'),
    resources_dir: pathlib.Path = WindowsPath('resources'),
    templates_dir: pathlib.Path = WindowsPath('templates'),
    default_template: pathlib.Path = WindowsPath('default.html.jinja2'),
    intermediates_dir: Optional[pathlib.Path] = None,
    output_dir: pathlib.Path = WindowsPath('output'),
    build_time_fname: pathlib.Path = WindowsPath('.build_time'),
    jinja_env_kwargs: dict[str, typing.Any] = <factory>,
    globals_: dict[str, typing.Any] = <factory>,
    pandoc_kwargs: dict[str, typing.Any] = <factory>,
    pandoc_fmt_from: str = 'markdown+smart',
    pandoc_fmt_to: str = 'html'
)
```

- `content_dir: pathlib.Path = WindowsPath('content')`

- `resources_dir: pathlib.Path = WindowsPath('resources')`

- `templates_dir: pathlib.Path = WindowsPath('templates')`

- `default_template: pathlib.Path = WindowsPath('default.html.jinja2')`

- `intermediates_dir: Optional[pathlib.Path] = None`

- `output_dir: pathlib.Path = WindowsPath('output')`

- `build_time_fname: pathlib.Path = WindowsPath('.build_time')`

- `jinja_env_kwargs: dict[str, typing.Any]`

- `globals_: dict[str, typing.Any]`

- `pandoc_kwargs: dict[str, typing.Any]`

- `pandoc_fmt_from: str = 'markdown+smart'`

- `pandoc_fmt_to: str = 'html'`

### `def read`

``` python
(
    cls,
    config_path: pathlib.Path,
    fmt: Optional[Literal['yaml', 'json', 'toml']] = None
) -> pdj_sitegen.config.Config
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L143-L145)

### `def as_str`

``` python
(self, fmt: Literal['yaml', 'json', 'toml']) -> str
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L147-L148)

### `def save`

``` python
(
    self,
    config_path: pathlib.Path,
    fmt: Optional[Literal['yaml', 'json', 'toml']] = 'json'
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L150-L151)

### `def serialize`

``` python
(self) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L697-L753)

returns the class as a dict, implemented by using
`@serializable_dataclass` decorator

### `def load`

``` python
(cls, data: Union[dict[str, Any], ~T]) -> Type[~T]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L760-L824)

takes in an appropriately structured dict and returns an instance of the
class, implemented by using `@serializable_dataclass` decorator

### `def validate_fields_types`

``` python
(
    self: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/config.py#L303-L312)

validate the types of all the fields on a `SerializableDataclass`. calls
`SerializableDataclass__validate_field_type` for each field

### Inherited Members

- [`validate_field_type`](#Config.validate_field_type)
- [`diff`](#Config.diff)
- [`update_from_nested_dict`](#Config.update_from_nested_dict)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## Contents

type definitions, format maps and parsers, and frontmatter regex

## API Documentation

- [`Format`](#Format)
- [`FORMAT_MAP`](#FORMAT_MAP)
- [`FORMAT_PARSERS`](#FORMAT_PARSERS)
- [`FRONTMATTER_DELIMS`](#FRONTMATTER_DELIMS)
- [`FRONTMATTER_REGEX`](#FRONTMATTER_REGEX)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/consts.py)

# `pdj_sitegen.consts`

type definitions, format maps and parsers, and frontmatter regex

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/consts.py#L0-L49)

- `Format = typing.Literal['yaml', 'json', 'toml']`

- `FORMAT_MAP: dict[str, typing.Literal['yaml', 'json', 'toml']] = {'yaml': 'yaml', 'yml': 'yaml', 'YAML': 'yaml', 'YML': 'yaml', 'json': 'json', 'JSON': 'json', 'toml': 'toml', 'tml': 'toml', 'TOML': 'toml', 'TML': 'toml'}`

- `FORMAT_PARSERS: dict[typing.Literal['yaml', 'json', 'toml'], typing.Callable[[str], dict[str, typing.Any]]] = {'yaml': <function safe_load>, 'json': <function loads>, 'toml': <function loads>}`

- `FRONTMATTER_DELIMS: dict[str, typing.Literal['yaml', 'json', 'toml']] = {'---': 'yaml', ';;;': 'json', '+++': 'toml'}`

- `FRONTMATTER_REGEX: re.Pattern = re.compile('^(?P<delimiter>\\-\\-\\-|;;;|\\+\\+\\+)\\n(?P<frontmatter>.*?)\\n(?P=delimiter)\\n(?P<body>.*)', re.DOTALL)`

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## Contents

`SplitMarkdownError` and `RenderError` exceptions

## API Documentation

- [`SplitMarkdownError`](#SplitMarkdownError)
- [`ConversionError`](#ConversionError)
- [`RenderError`](#RenderError)
- [`MultipleExceptions`](#MultipleExceptions)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/exceptions.py)

# `pdj_sitegen.exceptions`

`SplitMarkdownError` and `RenderError` exceptions

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/exceptions.py#L0-L72)

### `class SplitMarkdownError(builtins.Exception):`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/exceptions.py#L8-L11)

error while splitting markdown

### Inherited Members

- [`Exception`](#SplitMarkdownError.__init__)

- [`with_traceback`](#SplitMarkdownError.with_traceback)

- [`add_note`](#SplitMarkdownError.add_note)

- [`args`](#SplitMarkdownError.args)

### `class ConversionError(builtins.Exception):`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/exceptions.py#L14-L17)

error while converting markdown

### Inherited Members

- [`Exception`](#ConversionError.__init__)

- [`with_traceback`](#ConversionError.with_traceback)

- [`add_note`](#ConversionError.add_note)

- [`args`](#ConversionError.args)

### `class RenderError(builtins.Exception):`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/exceptions.py#L20-L60)

error while rendering template

### `RenderError`

``` python
(
    message: str,
    kind: Literal['create_template', 'render_template'],
    content: str | None,
    context: dict[str, typing.Any] | None,
    jinja_env: jinja2.environment.Environment | None,
    template: jinja2.environment.Template | None
)
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/exceptions.py#L23-L38)

- `message: str`

- `kind: Literal['create_template', 'render_template']`

- `content: str | None`

- `context: dict[str, typing.Any] | None`

- `jinja_env: jinja2.environment.Environment | None`

- `template: jinja2.environment.Template | None`

### Inherited Members

- [`with_traceback`](#RenderError.with_traceback)
- [`add_note`](#RenderError.add_note)
- [`args`](#RenderError.args)

### `class MultipleExceptions(builtins.Exception):`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/exceptions.py#L63-L73)

Common base class for all non-exit exceptions.

### `MultipleExceptions`

``` python
(message: str, exceptions: dict[str, Exception])
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/exceptions.py#L64-L67)

- `message: str`

- `exceptions: dict[str, Exception]`

### Inherited Members

- [`with_traceback`](#MultipleExceptions.with_traceback)
- [`add_note`](#MultipleExceptions.add_note)
- [`args`](#MultipleExceptions.args)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## Submodules

- [`csv_code_table`](#csv_code_table)
- [`links_md2html`](#links_md2html)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/__init__.py)

# `pdj_sitegen.filters`

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## Contents

python pandoc filter replicating
[pandoc-csv2table](https://hackage.haskell.org/package/pandoc-csv2table)

By [@mivanit](mivanit.github.io)

## API Documentation

- [`ALIGN_MAP`](#ALIGN_MAP)
- [`emptyblock`](#emptyblock)
- [`Plain_factory`](#Plain_factory)
- [`table_cell_factory`](#table_cell_factory)
- [`table_row_factory`](#table_row_factory)
- [`header_factory`](#header_factory)
- [`body_factory`](#body_factory)
- [`keyvals_process`](#keyvals_process)
- [`codeblock_process`](#codeblock_process)
- [`test_filter`](#test_filter)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py)

# `pdj_sitegen.filters.csv_code_table`

python pandoc filter replicating
[pandoc-csv2table](https://hackage.haskell.org/package/pandoc-csv2table)

By [@mivanit](mivanit.github.io)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L0-L163)

- `ALIGN_MAP: dict[str, str] = {'L': 'AlignLeft', 'C': 'AlignCenter', 'R': 'AlignRight', 'D': 'AlignDefault'}`

### `def emptyblock`

``` python
() -> list
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L22-L23)

### `def Plain_factory`

``` python
(val: str) -> dict
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L26-L33)

### `def table_cell_factory`

``` python
(val: str) -> list
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L36-L43)

### `def table_row_factory`

``` python
(lst_vals: list) -> list
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L46-L47)

### `def header_factory`

``` python
(lst_vals: list) -> list
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L50-L54)

### `def body_factory`

``` python
(table_vals: list) -> list
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L57-L65)

### `def keyvals_process`

``` python
(keyvals: list[tuple[str, str]]) -> dict[str, str]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L68-L69)

### `def codeblock_process`

``` python
(key, value, format_, _)
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L72-L148)

### `def test_filter`

``` python
()
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/csv_code_table.py#L151-L159)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## API Documentation

- [`links_md2html`](#links_md2html)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/links_md2html.py)

# `pdj_sitegen.filters.links_md2html`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/links_md2html.py#L0-L24)

### `def links_md2html`

``` python
(key, value, format, meta) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/filters/links_md2html.py#L4-L21)

convert dendron links to markdown links

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## Contents

install pandoc using pypandoc

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/install_pandoc.py)

# `pdj_sitegen.install_pandoc`

install pandoc using pypandoc

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/install_pandoc.py#L0-L5)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.1

## Contents

cli for setting up a site

## API Documentation

- [`DEFAULT_CONFIG`](#DEFAULT_CONFIG)
- [`FILE_LOCATIONS`](#FILE_LOCATIONS)
- [`setup_site`](#setup_site)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/setup_site.py)

# `pdj_sitegen.setup_site`

cli for setting up a site

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/setup_site.py#L0-L46)

- `DEFAULT_CONFIG: pdj_sitegen.config.Config = Config(content_dir=WindowsPath('content'), resources_dir=WindowsPath('resources'), templates_dir=WindowsPath('templates'), default_template=WindowsPath('default.html.jinja2'), intermediates_dir=None, output_dir=WindowsPath('output'), build_time_fname=WindowsPath('.build_time'), jinja_env_kwargs={}, globals_={}, pandoc_kwargs={'mathjax': True}, pandoc_fmt_from='markdown+smart', pandoc_fmt_to='html')`

- `FILE_LOCATIONS: dict[str, pathlib.Path] = {'config.yml': WindowsPath('config.yml'), 'default.html.jinja2': WindowsPath('templates/default.html.jinja2'), 'index.md': WindowsPath('content/index.md'), 'style.css': WindowsPath('content/resources/style.css'), 'syntax.css': WindowsPath('content/resources/syntax.css')}`

### `def setup_site`

``` python
(root: pathlib.Path = WindowsPath('.')) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.1/setup_site.py#L24-L33)
