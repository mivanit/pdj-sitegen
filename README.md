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

Both approaches work with `child_docs` in templates for hierarchical navigation.

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

