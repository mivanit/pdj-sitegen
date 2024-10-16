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

3. populate the `content` directory with markdown files, populate `content/resources/` with resources (images, css, etc.), and adjust templates in the `templates` directory. See the demo site for usage examples.

4. run the generator
```bash
python -m pdj_sitegen your_config.yaml
```