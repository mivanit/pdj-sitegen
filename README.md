[![PyPI](https://img.shields.io/pypi/v/pdj-sitegen)](https://pypi.org/project/pdj-sitegen/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pdj-sitegen)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/pdj-sitegen)

[![Checks](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/checks.yml)
[![Checks - docs](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/pdj-sitegen/actions/workflows/make-docs.yml)
[![Coverage](docs/coverage/coverage.svg)](docs/coverage/html/)

![GitHub commits](https://img.shields.io/github/commit-activity/t/mivanit/pdj-sitegen)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/mivanit/pdj-sitegen)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/mivanit/pdj-sitegen)
![code size, bytes](https://img.shields.io/github/languages/code-size/mivanit/pdj-sitegen)

# `pdj_sitegen`

**_P_**an**_d_**oc and **_J_**inja **_Site_** **_Gen_**erator

- docs: [`miv.name/pdj_sitegen/`](https://miv.name/pdj-sitegen/)
- demo site: [`miv.name/pdj_sitegen/demo_site/`](https://miv.name/pdj-sitegen/demo_site/)
- source: [`github.com/mivanit/pdj-sitegen`](https://github.com/mivanit/pdj-sitegen)

# Installation:

```bash
pip install pdj-sitegen
```

you should either have [Pandoc](https://pandoc.org/) installed, or you can run
```bash
python -m pdj_sitegen.install_pandoc
```
which will install `pandoc` using [`pypandoc`](https://github.com/JessicaTegner/pypandoc)

# Usage

## Quick Start

Scaffold a new site with all default files:
```bash
python -m pdj_sitegen.setup_site [directory]
```

This creates:
- `config.yml` - default configuration
- `templates/default.html.jinja2` - default HTML template
- `content/index.md` - sample index page
- `content/resources/style.css` - basic stylesheet
- `content/resources/syntax.css` - code syntax highlighting

## Manual Setup

1. create a config file. For an example, see `pdj_sitegen.config.DEFAULT_CONFIG_YAML`, or print a copy of it via
```bash
python -m pdj_sitegen.config
```

2. adjust the config file to your needs. most importantly:
```yaml
# directory with markdown content files and resources, relative to cwd
content_dir: content
# templates directory, relative to cwd
templates_dir: templates
# default template file, relative to `templates_dir`
default_template: default.html.jinja2
# output directory, relative to cwd
output_dir: docs
```

3. populate the `content` directory with markdown files and resources (images, css, etc.), and adjust templates in the `templates` directory. See the demo site for usage examples.

4. run the generator
```bash
python -m pdj_sitegen your_config.yaml
```

## CLI Arguments

```bash
python -m pdj_sitegen your_config.yaml [-q] [-s]
```

- `-q, --quiet`: Disable verbose output
- `-s, --smart-rebuild`: Only rebuild files modified since last build (compares file modification times against `.build_time`)

# Configuration

## Config File Formats

pdj-sitegen supports multiple configuration file formats:

- **YAML** (`.yml`, `.yaml`) - recommended, human-friendly
- **TOML** (`.toml`) - also supported
- **JSON** (`.json`) - for programmatic generation

```bash
python -m pdj_sitegen config.yml   # YAML
python -m pdj_sitegen config.toml  # TOML
python -m pdj_sitegen config.json  # JSON
```

## Content Mirroring

Files from `content_dir` are automatically copied to `output_dir`, excluding markdown files (which are processed into HTML). Control this with `copy_include` and `copy_exclude`:

```yaml
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

```yaml
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
```
content/
  index.md
  blog.md
  blog.post-1.md
  blog.post-2.md
```
Outputs: `index.html`, `blog.html`, `blog.post-1.html`, `blog.post-2.html`

**Nested structure** (using directories):
```
content/
  index.md
  blog/
    index.md
    post-1.md
    post-2.md
```
Outputs: `index.html`, `blog/index.html`, `blog/post-1.html`, `blog/post-2.html`

Both approaches work with `child_docs_dotlist` (path prefix matching) and `child_docs_folder` (same directory) in templates for hierarchical navigation.

## Pandoc Filters

pdj-sitegen includes two built-in pandoc filters:

### `links_md2html`

Converts links ending in `.md` to `.html` during conversion. Enable in frontmatter or global config:

```yaml
__pandoc__:
  filter: links_md2html
```

### `csv_code_table`

Converts fenced code blocks with class `csv_table` to HTML tables.

In your markdown, use a fenced code block with the `csv_table` class and options:

```
'''{.csv_table header=1 aligns=LCR caption="My Table"}
Name,Count,Status
Alice,42,Active
Bob,17,Pending
'''
```

> NOTE: in the above, use backticks (`) instead of single quotes (') for the fenced code block; single quotes are used here to avoid rendering issues.


Options:

- `header`: Number of header rows (default: 1)
- `source`: Path to external CSV file
- `aligns`: Column alignments (L=left, C=center, R=right, D=default)
- `caption`: Table caption

## Template Variables

The following variables are available in templates:

| Variable                      | Description                                           | Example                    |
| ----------------------------- | ----------------------------------------------------- | -------------------------- |
| `frontmatter`                 | Full frontmatter dict from the current document       | `{"title": "My Page"}`     |
| `file_meta.path`              | Relative path without extension                       | `blog/post-1`              |
| `file_meta.path_html`         | HTML output path                                      | `blog/post-1.html`         |
| `file_meta.path_raw`          | Original file path                                    | `content/blog/post-1.md`   |
| `file_meta.path_to_root`      | Relative path prefix to site root (no trailing slash) | `.` or `..` or `../..`     |
| `file_meta.modified_time`     | Unix timestamp of last modification                   | `1706380800.0`             |
| `file_meta.modified_time_str` | Human-readable modification time                      | `2024-01-27 12:00:00`      |
| `config`                      | Serialized site configuration                         | `{"output_dir": "docs"}`   |
| `docs`                        | Dictionary of all documents in the site               | `{"index": {...}}`         |
| `child_docs_dotlist`          | Documents matching by path prefix                     | `{"blog.post-1": {...}}`   |
| `child_docs_folder`           | Documents in the same directory                       | `{"about": {...}}`         |
| `dir_files`                   | List of all filenames in the directory                | `["index.md", "about.md"]` |
| `dir_subdirs`                 | List of subdirectory names                            | `["images", "posts"]`      |
| `dir_contents_recursive`      | List of all files recursively (relative paths)        | `["images/logo.png"]`      |
| `content`                     | Rendered HTML content (in final template only)        | `<p>Hello</p>`             |

All frontmatter fields are also available directly (e.g., `{{ title }}`).

## Frontmatter Formats

Frontmatter can be written in YAML, JSON, or TOML:

**YAML** (recommended):
```markdown
---
title: My Page
tags: [foo, bar]
---
```

**JSON**:
```markdown
;;;
{"title": "My Page", "tags": ["foo", "bar"]}
;;;
```

**TOML**:
```markdown
+++
title = "My Page"
tags = ["foo", "bar"]
+++
```

### Per-file Overrides

Override global settings in frontmatter:

```yaml
---
title: My Page
__template__: custom.html.jinja2  # Use different template
__pandoc__:
  toc: true                        # Override pandoc options
  number-sections: true
---
```

# similar tools/resources

This project is a descendant of my old project [pandoc-sitegen](https://github.com/mivanit/pandoc-sitegen), which was very similar but used mustache templates instead of jinja2.

Some other similar projects:

- https://github.com/brianbuccola/brianbuccola.github.io
- https://runningcrocodile.fi/pandoc_static_site/
- http://pdsite.org/installing/
- https://github.com/locua/pandoc-python-static-site-gen
- https://github.com/lukasschwab/pandoc-blog
- https://github.com/fcanas/bake

if you end up using this script for your site and would me to list it here, email me or submit a PR :)

