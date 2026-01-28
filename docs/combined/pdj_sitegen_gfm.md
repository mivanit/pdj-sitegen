> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

## Contents

[![PyPI](https://img.shields.io/pypi/v/pdj-sitegen)](https://pypi.org/project/pdj-sitegen/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pdj-sitegen)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/pdj-sitegen)

[![Checks](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml)
[![Checks -
docs](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml)
[![Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5OSIgaGVpZ2h0PSIyMCI+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImIiIHgyPSIwIiB5Mj0iMTAwJSI+CiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+CiAgICAgICAgPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLW9wYWNpdHk9Ii4xIi8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPG1hc2sgaWQ9ImEiPgogICAgICAgIDxyZWN0IHdpZHRoPSI5OSIgaGVpZ2h0PSIyMCIgcng9IjMiIGZpbGw9IiNmZmYiLz4KICAgIDwvbWFzaz4KICAgIDxnIG1hc2s9InVybCgjYSkiPgogICAgICAgIDxwYXRoIGZpbGw9IiM1NTUiIGQ9Ik0wIDBoNjN2MjBIMHoiLz4KICAgICAgICA8cGF0aCBmaWxsPSIjOTdDQTAwIiBkPSJNNjMgMGgzNnYyMEg2M3oiLz4KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+CiAgICA8L2c+CiAgICA8ZyBmaWxsPSIjZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iRGVqYVZ1IFNhbnMsVmVyZGFuYSxHZW5ldmEsc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMSI+CiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0PgogICAgICAgIDx0ZXh0IHg9IjMxLjUiIHk9IjE0Ij5jb3ZlcmFnZTwvdGV4dD4KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPjkzJTwvdGV4dD4KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjkzJTwvdGV4dD4KICAgIDwvZz4KPC9zdmc+Cg==)](docs/coverage/html/)

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

## Quick Start

Scaffold a new site with all default files:

``` bash
python -m pdj_sitegen.setup_site [directory]
```

This creates: - `config.yml` - default configuration -
`templates/default.html.jinja2` - default HTML template -
`content/index.md` - sample index page - `content/resources/style.css` -
basic stylesheet - `content/resources/syntax.css` - code syntax
highlighting

## Manual Setup

1.  create a config file. For an example, see
    `pdj_sitegen.config.DEFAULT_CONFIG_YAML`, or print a copy of it via

``` bash
python -m pdj_sitegen.config
```

2.  adjust the config file to your needs. most importantly:

``` yaml
# directory with markdown content files and resources, relative to cwd
content_dir: content
# templates directory, relative to cwd
templates_dir: templates
# default template file, relative to `templates_dir`
default_template: default.html.jinja2
# output directory, relative to cwd
output_dir: docs
```

3.  populate the `content` directory with markdown files and resources
    (images, css, etc.), and adjust templates in the `templates`
    directory. See the demo site for usage examples.

4.  run the generator

``` bash
python -m pdj_sitegen your_config.yaml
```

## CLI Arguments

``` bash
python -m pdj_sitegen your_config.yaml [-q] [-s]
```

- `-q, --quiet`: Disable verbose output
- `-s, --smart-rebuild`: Only rebuild files modified since last build
  (compares file modification times against `.build_time`)

# Configuration

## Config File Formats

pdj-sitegen supports multiple configuration file formats:

- **YAML** (`.yml`, `.yaml`) - recommended, human-friendly
- **TOML** (`.toml`) - also supported
- **JSON** (`.json`) - for programmatic generation

``` bash
python -m pdj_sitegen config.yml   # YAML
python -m pdj_sitegen config.toml  # TOML
python -m pdj_sitegen config.json  # JSON
```

## Content Mirroring

Files from `content_dir` are automatically copied to `output_dir`,
excluding markdown files (which are processed into HTML). Control this
with `copy_include` and `copy_exclude`:

``` yaml
# Default: copy everything except .md files
copy_include: []
copy_exclude:
  - "*.md"

# Also exclude temp files and .git
copy_exclude:
  - "*.md"
  - "*.tmp"
  - ".git*"

# Copy only specific file types
copy_include:
  - "*.css"
  - "*.js"
  - "*.png"
  - "*.jpg"
copy_exclude: []

# Force copy .md files too (include wins over exclude)
copy_include:
  - "*.md"
copy_exclude:
  - "*.md"
```

## Additional Options

``` yaml
# Global template variables accessible in all templates
globals_:
  site_name: "My Site"
  author: "Your Name"

# Directory to save intermediate processing files (for debugging)
intermediates_dir: null  # or "_intermediates"

# Prettify HTML output (uses BeautifulSoup)
prettify: false

# Pandoc format settings
pandoc_fmt_from: "markdown+smart"
pandoc_fmt_to: "html"

# Global Pandoc options (can be overridden per-file in frontmatter)
__pandoc__:
  mathjax: true
```

## Content Organization

pdj-sitegen supports both flat and nested content structures:

**Flat structure** (using dot notation):

    content/
      index.md
      blog.md
      blog.post-1.md
      blog.post-2.md

Outputs: `index.html`, `blog.html`, `blog.post-1.html`,
`blog.post-2.html`

**Nested structure** (using directories):

    content/
      index.md
      blog/
        index.md
        post-1.md
        post-2.md

Outputs: `index.html`, `blog/index.html`, `blog/post-1.html`,
`blog/post-2.html`

Both approaches work with `child_docs` in templates for hierarchical
navigation.

## Pandoc Filters

pdj-sitegen includes two built-in pandoc filters:

### `links_md2html`

Converts links ending in `.md` to `.html` during conversion. Enable in
frontmatter or global config:

``` yaml
__pandoc__:
  filter: links_md2html
```

### `csv_code_table`

Converts fenced code blocks with class `csv_table` to HTML tables.

In your markdown, use a fenced code block with the `csv_table` class and
options:

      ```{.csv_table header=1 aligns=LCR caption="My Table"}
      Name,Count,Status
      Alice,42,Active
      Bob,17,Pending
      ```

Options: - `header`: Number of header rows (default: 1) - `source`: Path
to external CSV file - `aligns`: Column alignments (L=left, C=center,
R=right, D=default) - `caption`: Table caption

## Template Variables

The following variables are available in templates:

| Variable                      | Description                                     | Example                  |
|-------------------------------|-------------------------------------------------|--------------------------|
| `frontmatter`                 | Full frontmatter dict from the current document | `{"title": "My Page"}`   |
| `file_meta.path`              | Relative path without extension                 | `blog/post-1`            |
| `file_meta.path_html`         | HTML output path                                | `blog/post-1.html`       |
| `file_meta.path_raw`          | Original file path                              | `content/blog/post-1.md` |
| `file_meta.modified_time`     | Unix timestamp of last modification             | `1706380800.0`           |
| `file_meta.modified_time_str` | Human-readable modification time                | `2024-01-27 12:00:00`    |
| `config`                      | Serialized site configuration                   | `{"output_dir": "docs"}` |
| `docs`                        | Dictionary of all documents in the site         | `{"index": {...}}`       |
| `child_docs`                  | Documents that are children of the current path | `{"blog/post-1": {...}}` |
| `content`                     | Rendered HTML content (in final template only)  | `<p>Hello</p>`           |

All frontmatter fields are also available directly (e.g.,
`{{ title }}`).

## Frontmatter Formats

Frontmatter can be written in YAML, JSON, or TOML:

**YAML** (recommended):

``` markdown
---
title: My Page
tags: [foo, bar]
---
```

**JSON**:

``` markdown
;;;
{"title": "My Page", "tags": ["foo", "bar"]}
;;;
```

**TOML**:

``` markdown
+++
title = "My Page"
tags = ["foo", "bar"]
+++
```

### Per-file Overrides

Override global settings in frontmatter:

``` yaml
---
title: My Page
__template__: custom.html.jinja2  # Use different template
__pandoc__:
  toc: true                        # Override pandoc options
  number-sections: true
---
```

# similar tools/resources

This project is a descendant of my old project
[pandoc-sitegen](https://github.com/mivanit/pandoc-sitegen), which was
very similar but used mustache templates instead of jinja2.

Some other similar projects:

- https://github.com/brianbuccola/brianbuccola.github.io
- https://runningcrocodile.fi/pandoc_static_site/
- http://pdsite.org/installing/
- https://github.com/locua/pandoc-python-static-site-gen
- https://github.com/lukasschwab/pandoc-blog
- https://github.com/fcanas/bake

if you end up using this script for your site and would me to list it
here, email me or submit a PR :)

## Submodules

- [`build`](#build)
- [`config`](#config)
- [`consts`](#consts)
- [`exceptions`](#exceptions)
- [`filters`](#filters)
- [`install_pandoc`](#install_pandoc)
- [`setup_site`](#setup_site)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/__init__.py)

# `pdj_sitegen`

[![PyPI](https://img.shields.io/pypi/v/pdj-sitegen)](https://pypi.org/project/pdj-sitegen/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pdj-sitegen)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/pdj-sitegen)

[![Checks](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml)
[![Checks -
docs](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml)
[![Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5OSIgaGVpZ2h0PSIyMCI+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImIiIHgyPSIwIiB5Mj0iMTAwJSI+CiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+CiAgICAgICAgPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLW9wYWNpdHk9Ii4xIi8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPG1hc2sgaWQ9ImEiPgogICAgICAgIDxyZWN0IHdpZHRoPSI5OSIgaGVpZ2h0PSIyMCIgcng9IjMiIGZpbGw9IiNmZmYiLz4KICAgIDwvbWFzaz4KICAgIDxnIG1hc2s9InVybCgjYSkiPgogICAgICAgIDxwYXRoIGZpbGw9IiM1NTUiIGQ9Ik0wIDBoNjN2MjBIMHoiLz4KICAgICAgICA8cGF0aCBmaWxsPSIjOTdDQTAwIiBkPSJNNjMgMGgzNnYyMEg2M3oiLz4KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+CiAgICA8L2c+CiAgICA8ZyBmaWxsPSIjZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iRGVqYVZ1IFNhbnMsVmVyZGFuYSxHZW5ldmEsc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMSI+CiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0PgogICAgICAgIDx0ZXh0IHg9IjMxLjUiIHk9IjE0Ij5jb3ZlcmFnZTwvdGV4dD4KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPjkzJTwvdGV4dD4KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjkzJTwvdGV4dD4KICAgIDwvZz4KPC9zdmc+Cg==)](docs/coverage/html/)

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

#### Quick Start

Scaffold a new site with all default files:

``` bash
python -m <a href="pdj_sitegen/setup_site.html">pdj_sitegen.setup_site</a> [directory]
```

This creates: - `config.yml` - default configuration -
`templates/default.html.jinja2` - default HTML template -
`content/index.md` - sample index page - `content/resources/style.css` -
basic stylesheet - `content/resources/syntax.css` - code syntax
highlighting

#### Manual Setup

1.  create a config file. For an example, see
    `<a href="pdj_sitegen/config.html#DEFAULT_CONFIG_YAML">pdj_sitegen.config.DEFAULT_CONFIG_YAML</a>`,
    or print a copy of it via

``` bash
python -m <a href="pdj_sitegen/config.html">pdj_sitegen.config</a>
```

2.  adjust the config file to your needs. most importantly:

``` yaml
### directory with markdown content files and resources, relative to cwd
content_dir: content
### templates directory, relative to cwd
templates_dir: templates
### default template file, relative to `templates_dir`
default_template: default.html.jinja2
### output directory, relative to cwd
output_dir: docs
```

3.  populate the `content` directory with markdown files and resources
    (images, css, etc.), and adjust templates in the `templates`
    directory. See the demo site for usage examples.

4.  run the generator

``` bash
python -m pdj_sitegen your_config.yaml
```

#### CLI Arguments

``` bash
python -m pdj_sitegen your_config.yaml [-q] [-s]
```

- `-q, --quiet`: Disable verbose output
- `-s, --smart-rebuild`: Only rebuild files modified since last build
  (compares file modification times against `.build_time`)

### Configuration

#### Config File Formats

pdj-sitegen supports multiple configuration file formats:

- **YAML** (`.yml`, `.yaml`) - recommended, human-friendly
- **TOML** (`.toml`) - also supported
- **JSON** (`.json`) - for programmatic generation

``` bash
python -m pdj_sitegen config.yml   # YAML
python -m pdj_sitegen config.toml  # TOML
python -m pdj_sitegen config.json  # JSON
```

#### Content Mirroring

Files from `content_dir` are automatically copied to `output_dir`,
excluding markdown files (which are processed into HTML). Control this
with `copy_include` and `copy_exclude`:

``` yaml
### Default: copy everything except .md files
copy_include: []
copy_exclude:
  - "*.md"

### Also exclude temp files and .git
copy_exclude:
  - "*.md"
  - "*.tmp"
  - ".git*"

### Copy only specific file types
copy_include:
  - "*.css"
  - "*.js"
  - "*.png"
  - "*.jpg"
copy_exclude: []

### Force copy .md files too (include wins over exclude)
copy_include:
  - "*.md"
copy_exclude:
  - "*.md"
```

#### Additional Options

``` yaml
### Global template variables accessible in all templates
globals_:
  site_name: "My Site"
  author: "Your Name"

### Directory to save intermediate processing files (for debugging)
intermediates_dir: null  # or "_intermediates"

### Prettify HTML output (uses BeautifulSoup)
prettify: false

### Pandoc format settings
pandoc_fmt_from: "markdown+smart"
pandoc_fmt_to: "html"

### Global Pandoc options (can be overridden per-file in frontmatter)
__pandoc__:
  mathjax: true
```

#### Content Organization

pdj-sitegen supports both flat and nested content structures:

**Flat structure** (using dot notation):

    content/
      index.md
      blog.md
      blog.post-1.md
      blog.post-2.md

Outputs: `index.html`, `blog.html`, `blog.post-1.html`,
`blog.post-2.html`

**Nested structure** (using directories):

    content/
      index.md
      blog/
        index.md
        post-1.md
        post-2.md

Outputs: `index.html`, `blog/index.html`, `blog/post-1.html`,
`blog/post-2.html`

Both approaches work with `child_docs` in templates for hierarchical
navigation.

#### Pandoc Filters

pdj-sitegen includes two built-in pandoc filters:

##### `links_md2html`

Converts links ending in `.md` to `.html` during conversion. Enable in
frontmatter or global config:

``` yaml
__pandoc__:
  filter: links_md2html
```

##### `csv_code_table`

Converts fenced code blocks with class `csv_table` to HTML tables.

In your markdown, use a fenced code block with the `csv_table` class and
options:

      ```{.csv_table header=1 aligns=LCR caption="My Table"}
      Name,Count,Status
      Alice,42,Active
      Bob,17,Pending
      ```

Options: - `header`: Number of header rows (default: 1) - `source`: Path
to external CSV file - `aligns`: Column alignments (L=left, C=center,
R=right, D=default) - `caption`: Table caption

#### Template Variables

The following variables are available in templates:

| Variable                      | Description                                     | Example                  |
|-------------------------------|-------------------------------------------------|--------------------------|
| `frontmatter`                 | Full frontmatter dict from the current document | `{"title": "My Page"}`   |
| `file_meta.path`              | Relative path without extension                 | `blog/post-1`            |
| `file_meta.path_html`         | HTML output path                                | `blog/post-1.html`       |
| `file_meta.path_raw`          | Original file path                              | `content/blog/post-1.md` |
| `file_meta.modified_time`     | Unix timestamp of last modification             | `1706380800.0`           |
| `file_meta.modified_time_str` | Human-readable modification time                | `2024-01-27 12:00:00`    |
| `config`                      | Serialized site configuration                   | `{"output_dir": "docs"}` |
| `docs`                        | Dictionary of all documents in the site         | `{"index": {...}}`       |
| `child_docs`                  | Documents that are children of the current path | `{"blog/post-1": {...}}` |
| `content`                     | Rendered HTML content (in final template only)  | `<p>Hello</p>`           |

All frontmatter fields are also available directly (e.g.,
`{{ title }}`).

#### Frontmatter Formats

Frontmatter can be written in YAML, JSON, or TOML:

**YAML** (recommended):

``` markdown
---
title: My Page
tags: [foo, bar]
---
```

**JSON**:

``` markdown
;;;
{"title": "My Page", "tags": ["foo", "bar"]}
;;;
```

**TOML**:

``` markdown
+++
title = "My Page"
tags = ["foo", "bar"]
+++
```

##### Per-file Overrides

Override global settings in frontmatter:

``` yaml
---
title: My Page
__template__: custom.html.jinja2  # Use different template
__pandoc__:
  toc: true                        # Override pandoc options
  number-sections: true
---
```

### similar tools/resources

This project is a descendant of my old project
[pandoc-sitegen](https://github.com/mivanit/pandoc-sitegen), which was
very similar but used mustache templates instead of jinja2.

Some other similar projects:

- https://github.com/brianbuccola/brianbuccola.github.io
- https://runningcrocodile.fi/pandoc_static_site/
- http://pdsite.org/installing/
- https://github.com/locua/pandoc-python-static-site-gen
- https://github.com/lukasschwab/pandoc-blog
- https://github.com/fcanas/bake

if you end up using this script for your site and would me to list it
here, email me or submit a PR :)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/__init__.py#L0-L2)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

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
- Copy content files to output directory (based on
  copy_include/copy_exclude patterns)

## API Documentation

- [`should_copy`](#should_copy)
- [`copy_content_files`](#copy_content_files)
- [`split_md`](#split_md)
- [`render`](#render)
- [`build_document_tree`](#build_document_tree)
- [`BUILTIN_FILTERS`](#BUILTIN_FILTERS)
- [`resolve_filter`](#resolve_filter)
- [`process_pandoc_args`](#process_pandoc_args)
- [`dump_intermediate`](#dump_intermediate)
- [`convert_single_markdown_file`](#convert_single_markdown_file)
- [`convert_markdown_files`](#convert_markdown_files)
- [`pipeline`](#pipeline)
- [`main`](#main)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py)

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
- Copy content files to output directory (based on
  copy_include/copy_exclude patterns)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L0-L624)

### `def should_copy`

``` python
(rel_path: str, include: list[str], exclude: list[str]) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L49-L77)

Determine if a file should be copied based on include/exclude patterns.

Rules: - If file matches any include pattern → copy (wins over
exclude) - If file matches any exclude pattern → don’t copy - If include
is empty → copy everything not excluded - If include is non-empty but
file doesn’t match → don’t copy

### Parameters:

- `rel_path : str` relative path of the file (POSIX format)
- `include : list[str]` glob patterns for files to include (empty means
  everything)
- `exclude : list[str]` glob patterns for files to exclude

### Returns:

- `bool` True if the file should be copied

### `def copy_content_files`

``` python
(
    content_dir: pathlib._local.Path,
    output_dir: pathlib._local.Path,
    include: list[str],
    exclude: list[str],
    verbose: bool = True
) -> int
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L80-L116)

Copy files from content_dir to output_dir based on include/exclude
patterns.

### Parameters:

- `content_dir : Path` source directory containing content files
- `output_dir : Path` destination directory for output
- `include : list[str]` glob patterns for files to include (empty means
  everything)
- `exclude : list[str]` glob patterns for files to exclude
- `verbose : bool` whether to print progress information

### Returns:

- `int` number of files copied

### `def split_md`

``` python
(content: str) -> tuple[str, str, typing.Literal['yaml', 'json', 'toml']]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L119-L155)

parse markdown into a tuple of frontmatter, body, and frontmatter format

will use `FRONTMATTER_REGEX` to split the markdown content into
frontmatter and body. the possible delimiters are defined in
`FRONTMATTER_DELIMS`.

### Parameters:

- `content : str` markdown content to split

### Returns:

- `tuple[str, str, Format]` tuple of frontmatter, body, and frontmatter
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
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L158-L204)

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
    content_dir: pathlib._local.Path,
    frontmatter_context: dict[str, typing.Any],
    jinja_env: jinja2.environment.Environment,
    verbose: bool = True
) -> dict[str, dict[str, typing.Any]]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L207-L280)

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

- `BUILTIN_FILTERS: dict[str, str] = {'csv_code_table': 'pdj-csv-code-table', 'links_md2html': 'pdj-links-md2html', 'pdj_sitegen.filters.csv_code_table': 'pdj-csv-code-table', 'pdj_sitegen.filters.links_md2html': 'pdj-links-md2html'}`

### `def resolve_filter`

``` python
(filter_name: str) -> str
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L294-L300)

Resolve a filter name to an executable.

Built-in filters are mapped to their entry points. External filters are
passed through unchanged.

### `def process_pandoc_args`

``` python
(pandoc_args: dict[str, typing.Any]) -> list[str]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L303-L338)

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
    intermediates_dir: pathlib._local.Path | None,
    fmt: str,
    path: str,
    subdir: str | None = None
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L341-L355)

Dump content to an intermediate file if intermediates_dir is specified

### `def convert_single_markdown_file`

``` python
(
    path: str,
    output_root: pathlib._local.Path,
    doc: dict[str, typing.Any],
    docs: dict[str, dict[str, typing.Any]],
    jinja_env: jinja2.environment.Environment,
    config: pdj_sitegen.config.Config,
    intermediates_dir: pathlib._local.Path | None = None
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L358-L450)

### `def convert_markdown_files`

``` python
(
    docs: dict[str, dict[str, typing.Any]],
    jinja_env: jinja2.environment.Environment,
    config: pdj_sitegen.config.Config,
    output_root: pathlib._local.Path,
    smart_rebuild: bool,
    rebuild_time: float,
    verbose: bool = True,
    intermediates_dir: pathlib._local.Path | None = None
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L453-L504)

### `def pipeline`

``` python
(
    config_path: pathlib._local.Path,
    verbose: bool = True,
    smart_rebuild: bool = False
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L507-L588)

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
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/build.py#L591-L621)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

## Contents

define the config, and also provide CLI for printing template

## API Documentation

- [`DEFAULT_CONFIG_YAML`](#DEFAULT_CONFIG_YAML)
- [`DEFAULT_CONFIG_TOML`](#DEFAULT_CONFIG_TOML)
- [`read_data_file`](#read_data_file)
- [`emit_data_file`](#emit_data_file)
- [`save_data_file`](#save_data_file)
- [`Config`](#Config)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py)

# `pdj_sitegen.config`

define the config, and also provide CLI for printing template

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L0-L168)

- `DEFAULT_CONFIG_YAML: str = '# NOTE: the current working directory (cwd) will be set to the location of this file!\n# directory with markdown content files and resources, relative to cwd\ncontent_dir: content\n# templates directory, relative to cwd\ntemplates_dir: templates\n# default template file, relative to`templates_dir`\ndefault_template: default.html.jinja2\n# output directory, relative to cwd\noutput_dir: output\n# intermediate files directory -- if set, intermediate files will be saved there\n# intermediates_dir: intermediates\n\n# Content mirroring: files from content_dir are copied to output_dir\n# copy_include: glob patterns to include (empty list = everything)\n# copy_exclude: glob patterns to exclude\n# If a file matches BOTH include and exclude, include wins (explicit include overrides exclude)\ncopy_include: []\ncopy_exclude:\n  - "*.md"  # markdown files are processed into HTML, not copied raw\n# kwargs to pass to the Jinja2 environment\njinja_env_kwargs: {}\n# whether to prettify with bs4\nprettify: false\n# pandoc formats\npandoc_fmt_from: markdown+smart\npandoc_fmt_to: html\n# extra kwargs to pass to pandoc (this will be augmented with`**pandoc**`from the frontmatter of a file)\n__pandoc__:\n  mathjax: true\n# extra globals to pass -- this can be anything\nglobals_:\n  pdjsg_url: https://github.com/mivanit/pdj-sitegen'`

- `DEFAULT_CONFIG_TOML: str = '# NOTE: the current working directory (cwd) will be set to the location of this file!\n\n# directory with markdown content files and resources, relative to cwd\ncontent_dir = "content"\n# templates directory, relative to cwd\ntemplates_dir = "templates"\n# default template file, relative to`templates_dir`\ndefault_template = "default.html.jinja2"\n# output directory, relative to cwd\noutput_dir = "output"\n# intermediate files directory -- if null, then no intermediate files will be saved\n# intermediates_dir = "intermediates"\n\n# Content mirroring: files from content_dir are copied to output_dir\n# copy_include: glob patterns to include (empty list = everything)\n# copy_exclude: glob patterns to exclude\n# If a file matches BOTH include and exclude, include wins (explicit include overrides exclude)\ncopy_include = []\ncopy_exclude = ["*.md"]  # markdown files are processed into HTML, not copied raw\n\n# whether to prettify with bs4\nprettify = false\n\n# pandoc formats\npandoc_fmt_from = "markdown+smart"\npandoc_fmt_to = "html"\n\n# extra kwargs to pass to pandoc (this will be augmented with`**pandoc**`from the frontmatter of a file)\n[__pandoc__]\nmathjax = true\n\n# kwargs to pass to the Jinja2 environment\n[jinja_env_kwargs]\n\n# extra globals to pass -- this can be anything\n[globals_]\npdjsg_url = "https://github.com/mivanit/pdj-sitegen"\n'`

### `def read_data_file`

``` python
(
    file_path: pathlib._local.Path,
    fmt: Optional[Literal['yaml', 'json', 'toml']] = None
) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L28-L49)

read a file from any of json, yaml, or toml

### `def emit_data_file`

``` python
(data: dict[str, typing.Any], fmt: Literal['yaml', 'json', 'toml']) -> str
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L52-L62)

emit a file as json or yaml

### `def save_data_file`

``` python
(
    data: dict[str, typing.Any],
    file_path: pathlib._local.Path,
    fmt: Optional[Literal['yaml', 'json', 'toml']] = None
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L65-L79)

save a file as json or yaml

### `class Config:`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L92-L157)

configuration for the site generator

### `Config`

``` python
(
    content_dir: pathlib._local.Path = <factory>,
    templates_dir: pathlib._local.Path = <factory>,
    default_template: pathlib._local.Path = <factory>,
    intermediates_dir: pathlib._local.Path | None = None,
    output_dir: pathlib._local.Path = <factory>,
    build_time_fname: pathlib._local.Path = <factory>,
    jinja_env_kwargs: dict[str, typing.Any] = <factory>,
    globals_: dict[str, typing.Any] = <factory>,
    prettify: bool = False,
    copy_include: list[str] = <factory>,
    copy_exclude: list[str] = <factory>,
    __pandoc__: dict[str, typing.Any] = <factory>,
    pandoc_fmt_from: str = 'markdown+smart',
    pandoc_fmt_to: str = 'html'
)
```

- `content_dir: pathlib._local.Path`

- `templates_dir: pathlib._local.Path`

- `default_template: pathlib._local.Path`

- `intermediates_dir: pathlib._local.Path | None = None`

- `output_dir: pathlib._local.Path`

- `build_time_fname: pathlib._local.Path`

- `jinja_env_kwargs: dict[str, typing.Any]`

- `globals_: dict[str, typing.Any]`

- `prettify: bool = False`

- `copy_include: list[str]`

- `copy_exclude: list[str]`

- `pandoc_fmt_from: str = 'markdown+smart'`

- `pandoc_fmt_to: str = 'html'`

### `def load`

``` python
(cls, data: dict[str, typing.Any]) -> pdj_sitegen.config.Config
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L123-L134)

Load Config from a dictionary.

### `def serialize`

``` python
(self) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L136-L147)

Serialize Config to a dictionary.

### `def read`

``` python
(
    cls,
    config_path: pathlib._local.Path,
    fmt: Optional[Literal['yaml', 'json', 'toml']] = None
) -> pdj_sitegen.config.Config
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L149-L151)

### `def as_str`

``` python
(self, fmt: Literal['yaml', 'json', 'toml']) -> str
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L153-L154)

### `def save`

``` python
(
    self,
    config_path: pathlib._local.Path,
    fmt: Optional[Literal['yaml', 'json', 'toml']] = 'json'
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/config.py#L156-L157)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

## Contents

type definitions, format maps and parsers, and frontmatter regex

## API Documentation

- [`Format`](#Format)
- [`FORMAT_MAP`](#FORMAT_MAP)
- [`FORMAT_PARSERS`](#FORMAT_PARSERS)
- [`FRONTMATTER_DELIMS`](#FRONTMATTER_DELIMS)
- [`FRONTMATTER_REGEX`](#FRONTMATTER_REGEX)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/consts.py)

# `pdj_sitegen.consts`

type definitions, format maps and parsers, and frontmatter regex

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/consts.py#L0-L44)

- `Format = typing.Literal['yaml', 'json', 'toml']`

- `FORMAT_MAP: dict[str, typing.Literal['yaml', 'json', 'toml']] = {'yaml': 'yaml', 'yml': 'yaml', 'YAML': 'yaml', 'YML': 'yaml', 'json': 'json', 'JSON': 'json', 'toml': 'toml', 'tml': 'toml', 'TOML': 'toml', 'TML': 'toml'}`

- `FORMAT_PARSERS: dict[typing.Literal['yaml', 'json', 'toml'], typing.Callable[[str], dict[str, typing.Any]]] = {'yaml': <function safe_load>, 'json': <function loads>, 'toml': <function loads>}`

- `FRONTMATTER_DELIMS: dict[str, typing.Literal['yaml', 'json', 'toml']] = {'---': 'yaml', ';;;': 'json', '+++': 'toml'}`

- `FRONTMATTER_REGEX: re.Pattern[str] = re.compile('^(?P<delimiter>\\-\\-\\-|;;;|\\+\\+\\+)\\n(?P<frontmatter>.*?)\\n(?P=delimiter)\\n(?P<body>.*)', re.DOTALL)`

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

## Contents

`SplitMarkdownError` and `RenderError` exceptions

## API Documentation

- [`SplitMarkdownError`](#SplitMarkdownError)
- [`ConversionError`](#ConversionError)
- [`RenderError`](#RenderError)
- [`MultipleExceptions`](#MultipleExceptions)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/exceptions.py)

# `pdj_sitegen.exceptions`

`SplitMarkdownError` and `RenderError` exceptions

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/exceptions.py#L0-L73)

### `class SplitMarkdownError(builtins.Exception):`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/exceptions.py#L8-L11)

error while splitting markdown

### Inherited Members

- [`Exception`](#SplitMarkdownError.__init__)

- [`with_traceback`](#SplitMarkdownError.with_traceback)

- [`add_note`](#SplitMarkdownError.add_note)

- [`args`](#SplitMarkdownError.args)

### `class ConversionError(builtins.Exception):`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/exceptions.py#L14-L17)

error while converting markdown

### Inherited Members

- [`Exception`](#ConversionError.__init__)

- [`with_traceback`](#ConversionError.with_traceback)

- [`add_note`](#ConversionError.add_note)

- [`args`](#ConversionError.args)

### `class RenderError(builtins.Exception):`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/exceptions.py#L20-L61)

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
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/exceptions.py#L23-L38)

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
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/exceptions.py#L64-L74)

Common base class for all non-exit exceptions.

### `MultipleExceptions`

``` python
(message: str, exceptions: dict[str, Exception])
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/exceptions.py#L65-L68)

- `message: str`

- `exceptions: dict[str, Exception]`

### Inherited Members

- [`with_traceback`](#MultipleExceptions.with_traceback)
- [`add_note`](#MultipleExceptions.add_note)
- [`args`](#MultipleExceptions.args)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

## Submodules

- [`csv_code_table`](#csv_code_table)
- [`links_md2html`](#links_md2html)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/__init__.py)

# `pdj_sitegen.filters`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/__init__.py#L0-L0)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

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
- [`main`](#main)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py)

# `pdj_sitegen.filters.csv_code_table`

python pandoc filter replicating
[pandoc-csv2table](https://hackage.haskell.org/package/pandoc-csv2table)

By [@mivanit](mivanit.github.io)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L0-L195)

- `ALIGN_MAP: dict[str, str] = {'L': 'AlignLeft', 'C': 'AlignCenter', 'R': 'AlignRight', 'D': 'AlignDefault'}`

### `def emptyblock`

``` python
() -> list[typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L23-L24)

### `def Plain_factory`

``` python
(val: str) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L27-L34)

### `def table_cell_factory`

``` python
(val: str) -> list[typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L37-L44)

### `def table_row_factory`

``` python
(lst_vals: list[str]) -> list[typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L47-L48)

### `def header_factory`

``` python
(lst_vals: list[str]) -> list[typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L51-L55)

### `def body_factory`

``` python
(table_vals: list[list[str]]) -> list[typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L58-L66)

### `def keyvals_process`

``` python
(keyvals: list[tuple[str, str]]) -> dict[str, str]
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L69-L70)

### `def codeblock_process`

``` python
(
    key: str,
    value: Any,
    format_: str,
    _: Any
) -> dict[str, typing.Any] | None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L73-L175)

### `def test_filter`

``` python
() -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L178-L187)

### `def main`

``` python
() -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/csv_code_table.py#L190-L191)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

## API Documentation

- [`links_md2html`](#links_md2html)
- [`main`](#main)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/links_md2html.py)

# `pdj_sitegen.filters.links_md2html`

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/links_md2html.py#L0-L27)

### `def links_md2html`

``` python
(key: str, value: Any, format: str, meta: Any) -> typing.Any | None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/links_md2html.py#L6-L20)

convert .md links to .html links

### `def main`

``` python
() -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/filters/links_md2html.py#L23-L24)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

## Contents

install pandoc using pypandoc

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/install_pandoc.py)

# `pdj_sitegen.install_pandoc`

install pandoc using pypandoc

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/install_pandoc.py#L0-L5)

> docs for [`pdj_sitegen`](https://github.com/mivanit/pdj-sitegen)
> v0.0.3

## Contents

CLI for scaffolding a new pdj-sitegen site.

Creates default configuration, templates, and content files to get
started quickly. Run with `python -m pdj_sitegen.setup_site [directory]`
to scaffold a new site.

## API Documentation

- [`DEFAULT_CONFIG`](#DEFAULT_CONFIG)
- [`RESOURCES_DIR`](#RESOURCES_DIR)
- [`FILE_LOCATIONS`](#FILE_LOCATIONS)
- [`setup_site`](#setup_site)
- [`main`](#main)

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/setup_site.py)

# `pdj_sitegen.setup_site`

CLI for scaffolding a new pdj-sitegen site.

Creates default configuration, templates, and content files to get
started quickly. Run with
`python -m <a href="">pdj_sitegen.setup_site</a> [directory]` to
scaffold a new site.

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/setup_site.py#L0-L86)

- `DEFAULT_CONFIG: pdj_sitegen.config.Config = Config(content_dir=PosixPath('content'), templates_dir=PosixPath('templates'), default_template=PosixPath('default.html.jinja2'), intermediates_dir=None, output_dir=PosixPath('output'), build_time_fname=PosixPath('.build_time'), jinja_env_kwargs={}, globals_={}, prettify=False, copy_include=[], copy_exclude=['*.md'], __pandoc__={'mathjax': True}, pandoc_fmt_from='markdown+smart', pandoc_fmt_to='html')`

- `RESOURCES_DIR: pathlib._local.Path = PosixPath('resources')`

- `FILE_LOCATIONS: dict[str, pathlib._local.Path] = {'config.yml': PosixPath('config.yml'), 'default.html.jinja2': PosixPath('templates/default.html.jinja2'), 'index.md': PosixPath('content/index.md'), 'style.css': PosixPath('content/resources/style.css'), 'syntax.css': PosixPath('content/resources/syntax.css')}`

### `def setup_site`

``` python
(root: pathlib._local.Path = PosixPath('.')) -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/setup_site.py#L30-L58)

Scaffold a new pdj-sitegen site with default files.

Copies bundled template files from the package to the specified root
directory, creating the necessary directory structure.

### Parameters:

- `root : Path` Root directory to create site files in. Defaults to
  current directory.

### Creates:

- `config.yml` - default site configuration
- `templates/default.html.jinja2` - default HTML template
- `content/index.md` - sample index page
- `content/resources/style.css` - basic stylesheet
- `content/resources/syntax.css` - code syntax highlighting

### `def main`

``` python
() -> None
```

[View Source on
GitHub](https://github.com/mivanit/pdj-sitegen/blob/0.0.3/setup_site.py#L61-L83)

CLI entry point for setup_site.
