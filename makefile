# ==================================================
# configuration & variables
# ==================================================

# it assumes that the source is in a directory named the same as the package name
# this also gets passed to some other places
PACKAGE_NAME := pdj_sitegen

# for checking you are on the right branch when publishing
PUBLISH_BRANCH := main

# where to put docs
DOCS_DIR := docs

# where to put the coverage reports
# note that this will be published with the docs!
# modify the `docs` targets and `.gitignore` if you don't want that
COVERAGE_REPORTS_DIR := docs/coverage

# where the tests are, for pytest
TESTS_DIR := tests

# tests temp directory to clean up. will remove this in `make clean`
TESTS_TEMP_DIR := $(TESTS_DIR)/_temp/

# probably don't change these:
# --------------------------------------------------

# where the pyproject.toml file is. no idea why you would change this but just in case
PYPROJECT := pyproject.toml

# requirements.txt files for base package, all extras, dev, and all
REQ_BASE := .github/requirements.txt
REQ_EXTRAS := .github/requirements-extras.txt
REQ_DEV := .github/requirements-dev.txt
REQ_ALL := .github/requirements-all.txt

# local files (don't push this to git)
LOCAL_DIR := .github/local

# will print this token when publishing. make sure not to commit this file!!!
PYPI_TOKEN_FILE := $(LOCAL_DIR)/.pypi-token

# the last version that was auto-uploaded. will use this to create a commit log for version tag
# see `gen-commit-log` target
LAST_VERSION_FILE := .github/.lastversion

# base python to use. Will add `uv run` in front of this if `RUN_GLOBAL` is not set to 1
PYTHON_BASE := python

# where the commit log will be stored
COMMIT_LOG_FILE := $(LOCAL_DIR)/.commit_log

# pandoc commands (for docs)
PANDOC ?= pandoc

# version vars - extracted automatically from `pyproject.toml`, `$(LAST_VERSION_FILE)`, and $(PYTHON)
# --------------------------------------------------

# assuming your `pyproject.toml` has a line that looks like `version = "0.0.1"`, `gen-version-info` will extract this
VERSION := NULL
# `gen-version-info` will read the last version from `$(LAST_VERSION_FILE)`, or `NULL` if it doesn't exist
LAST_VERSION := NULL
# get the python version, now that we have picked the python command
PYTHON_VERSION := NULL


# ==================================================
# reading command line options
# ==================================================

# for formatting or something, we might want to run python without uv
# RUN_GLOBAL=1 to use global `PYTHON_BASE` instead of `uv run $(PYTHON_BASE)`
RUN_GLOBAL ?= 0

ifeq ($(RUN_GLOBAL),0)
	PYTHON = uv run $(PYTHON_BASE)
else
	PYTHON = $(PYTHON_BASE)
endif

# if you want different behavior for different python versions
# --------------------------------------------------
# COMPATIBILITY_MODE := $(shell $(PYTHON) -c "import sys; print(1 if sys.version_info < (3, 10) else 0)")

# options we might want to pass to pytest
# --------------------------------------------------

# base options for pytest, will be appended to if `COV` or `VERBOSE` are 1.
# user can also set this when running make to add more options
PYTEST_OPTIONS ?=

# set to `1` to run pytest with `--cov=.` to get coverage reports in a `.coverage` file
COV ?= 1
# set to `1` to run pytest with `--verbose`
VERBOSE ?= 0

ifeq ($(VERBOSE),1)
	PYTEST_OPTIONS += --verbose
endif

ifeq ($(COV),1)
    PYTEST_OPTIONS += --cov=.
endif

# ==================================================
# default target (help)
# ==================================================

# first/default target is help
.PHONY: default
default: help

# ==================================================
# getting version info
# we do this in a separate target because it takes a bit of time
# ==================================================

# gets version info from $(PYPROJECT), last version from $(LAST_VERSION_FILE), and python version
# uses just `python` for everything except getting the python version. no echo here, because this is "private"
.PHONY: gen-version-info
gen-version-info:
	@mkdir -p $(LOCAL_DIR)
	$(eval VERSION := $(shell python -c "import re; print('v'+re.search(r'^version\s*=\s*\"(.+?)\"', open('$(PYPROJECT)').read(), re.MULTILINE).group(1))") )
	$(eval LAST_VERSION := $(shell [ -f $(LAST_VERSION_FILE) ] && cat $(LAST_VERSION_FILE) || echo NULL) )
	$(eval PYTHON_VERSION := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')") )

# getting commit log since the tag specified in $(LAST_VERSION_FILE)
# will write to $(COMMIT_LOG_FILE)
# when publishing, the contents of $(COMMIT_LOG_FILE) will be used as the tag description (but can be edited during the process)
# uses just `python`. no echo here, because this is "private"
.PHONY: gen-commit-log
gen-commit-log: gen-version-info
	@if [ "$(LAST_VERSION)" = "NULL" ]; then \
		echo "!!! ERROR !!!"; \
		echo "LAST_VERSION is NULL, cant get commit log!"; \
		exit 1; \
	fi
	@mkdir -p $(LOCAL_DIR)
	@python -c "import subprocess; open('$(COMMIT_LOG_FILE)', 'w').write('\n'.join(reversed(subprocess.check_output(['git', 'log', '$(LAST_VERSION)'.strip() + '..HEAD', '--pretty=format:- %s (%h)']).decode('utf-8').strip().split('\n'))))"


# force the version info to be read, printing it out
# also force the commit log to be generated, and cat it out
.PHONY: version
version: gen-commit-log
	@echo "Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)"
	@echo "Commit log since last version from '$(COMMIT_LOG_FILE)':"
	@cat $(COMMIT_LOG_FILE)

.PHONY: version-new-check
version-new-check: version
	@echo "verifying that the new version is different from the last version"
	@if [ "$(VERSION)" = "$(LAST_VERSION)" ]; then \
		echo "!!! ERROR !!!"; \
		echo "Version $(VERSION) is the same as the last version $(LAST_VERSION), exiting!"; \
		exit 1; \
	fi


# ==================================================
# dependencies and setup
# ==================================================

.PHONY: setup
setup: dep-check
	@echo "install and update via uv"
	@echo "To activate the virtual environment, run one of:"
	@echo "  source .venv/bin/activate"
	@echo "  source .venv/Scripts/activate"

.PHONY: dep
dep:
	@echo "sync and export deps to $(REQ_BASE), $(REQ_EXTRAS), $(REQ_DEV), and $(REQ_ALL)"
	uv sync --all-extras
	uv export --no-dev --no-hashes > $(REQ_BASE)
	uv export --all-extras --no-dev --no-hashes > $(REQ_EXTRAS)
	uv export --no-hashes > $(REQ_DEV)
	uv export --all-extras --no-hashes > $(REQ_ALL)

.PHONY: dep-check
dep-check:
	@echo "checking uv.lock is good, exported requirements up to date"
	uv sync --all-extras --locked
	uv export --no-dev --no-hashes | diff - $(REQ_BASE)
	uv export --all-extras --no-dev --no-hashes | diff - $(REQ_EXTRAS)
	uv export --no-hashes | diff - $(REQ_DEV)
	uv export --all-extras --no-hashes | diff - $(REQ_ALL)


# ==================================================
# checks (formatting/linting, typing, tests)
# ==================================================

# runs ruff and pycln to format the code
.PHONY: format
format:
	@echo "format the source code"
	$(PYTHON) -m ruff format --config $(PYPROJECT) .
	$(PYTHON) -m ruff check --fix --config $(PYPROJECT) .
	$(PYTHON) -m pycln --config $(PYPROJECT) --all .

# runs ruff and pycln to check if the code is formatted correctly
.PHONY: format-check
format-check:
	@echo "check if the source code is formatted correctly"
	$(PYTHON) -m ruff check --config $(PYPROJECT) .
	$(PYTHON) -m pycln --check --config $(PYPROJECT) .

# runs type checks with mypy
# at some point, need to add back --check-untyped-defs to mypy call
# but it complains when we specify arguments by keyword where positional is fine
# not sure how to fix this
.PHONY: typing
typing: clean
	@echo "running type checks"
	$(PYTHON) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_ARGS) $(PACKAGE_NAME)/
	$(PYTHON) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_ARGS) $(TESTS_DIR)

.PHONY: test
test: clean
	@echo "running tests"
	$(PYTHON) -m pytest $(PYTEST_OPTIONS) $(TESTS_DIR)

# ~~~~~~~~~~
# added check dep
.PHONY: check
check: clean dep-check format-check test typing
	@echo "run format checks, dep checks, tests, typing checks"
# ~~~~~~~~~~

# ==================================================
# coverage & docs
# ==================================================

# generates a whole tree of documentation in html format.
# see `docs/make_docs.py` and the templates in `docs/templates/html/` for more info
.PHONY: docs-html
docs-html:
	@echo "generate html docs"
	$(PYTHON) docs/make_docs.py

# instead of a whole website, generates a single markdown file with all docs using the templates in `docs/templates/markdown/`.
# this is useful if you want to have a copy that you can grep/search, but those docs are much messier.
# docs-combined will use pandoc to convert them to other formats.
.PHONY: docs-md
docs-md:
	@echo "generate combined (single-file) docs in markdown"
	mkdir $(DOCS_DIR)/combined -p
	$(PYTHON) docs/make_docs.py --combined

# after running docs-md, this will convert the combined markdown file to other formats:
# gfm (github-flavored markdown), plain text, and html
# requires pandoc in path, pointed to by $(PANDOC)
# pdf output would be nice but requires other deps
.PHONY: docs-combined
docs-combined: docs-md
	@echo "generate combined (single-file) docs in markdown and convert to other formats"
	@echo "requires pandoc in path"
	$(PANDOC) -f markdown -t gfm $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME)_gfm.md
	$(PANDOC) -f markdown -t plain $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME).txt
	$(PANDOC) -f markdown -t html $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME).html

# generates coverage reports as html and text with `pytest-cov`, and a badge with `coverage-badge`
# if `.coverage` is not found, will run tests first
# also removes the `.gitignore` file that `coverage html` creates, since we count that as part of the docs
.PHONY: cov
cov:
	@echo "generate coverage reports"
	@if [ ! -f .coverage ]; then \
		echo ".coverage not found, running tests first..."; \
		$(MAKE) test; \
	fi
	mkdir $(COVERAGE_REPORTS_DIR) -p
	$(PYTHON) -m coverage report -m > $(COVERAGE_REPORTS_DIR)/coverage.txt
	$(PYTHON) -m coverage_badge -f -o $(COVERAGE_REPORTS_DIR)/coverage.svg
	$(PYTHON) -m coverage html --directory=$(COVERAGE_REPORTS_DIR)/html/
	rm -rf $(COVERAGE_REPORTS_DIR)/html/.gitignore

# runs the coverage report, then the docs, then the combined docs
.PHONY: docs
docs: cov docs-html docs-combined
	@echo "generate all documentation and coverage reports"

# removed all generated documentation files, but leaves the templates and the `docs/make_docs.py` script
# distinct from `make clean`
.PHONY: docs-clean
docs-clean:
	@echo "remove generated docs"
	rm -rf $(DOCS_DIR)/combined/
	rm -rf $(DOCS_DIR)/$(PACKAGE_NAME)/
	rm -rf $(COVERAGE_REPORTS_DIR)/
	rm -f $(DOCS_DIR)/$(PACKAGE_NAME).html
	rm -f $(DOCS_DIR)/index.html
	rm -f $(DOCS_DIR)/search.js


# ==================================================
# build and publish
# ==================================================

# verifies that the current branch is $(PUBLISH_BRANCH) and that git is clean
# used before publishing
.PHONY: verify-git
verify-git: 
	@echo "checking git status"
	if [ "$(shell git branch --show-current)" != $(PUBLISH_BRANCH) ]; then \
		echo "!!! ERROR !!!"; \
		echo "Git is not on the $(PUBLISH_BRANCH) branch, exiting!"; \
		exit 1; \
	fi; \
	if [ -n "$(shell git status --porcelain)" ]; then \
		echo "!!! ERROR !!!"; \
		echo "Git is not clean, exiting!"; \
		exit 1; \
	fi; \


.PHONY: build
build: 
	@echo "build the package"
	uv build

# gets the commit log, checks everything, builds, and then publishes with twine
# will ask the user to confirm the new version number (and this allows for editing the tag info)
# will also print the contents of $(PYPI_TOKEN_FILE) to the console for the user to copy and paste in when prompted by twine
.PHONY: publish
publish: gen-commit-log check build verify-git version-new-check
	@echo "run all checks, build, and then publish"

	@echo "Enter the new version number if you want to upload to pypi and create a new tag"
	@echo "Now would also be the time to edit $(COMMIT_LOG_FILE), as that will be used as the tag description"
	@read -p "Confirm: " NEW_VERSION; \
	if [ "$$NEW_VERSION" = $(VERSION) ]; then \
		echo "!!! ERROR !!!"; \
		echo "Version confirmed. Proceeding with publish."; \
	else \
		echo "Version mismatch, exiting: you gave $$NEW_VERSION but expected $(VERSION)"; \
		exit 1; \
	fi;

	@echo "pypi username: __token__"
	@echo "pypi token from '$(PYPI_TOKEN_FILE)' :"
	echo $$(cat $(PYPI_TOKEN_FILE))

	echo "Uploading!"; \
	echo $(VERSION) > $(LAST_VERSION_FILE); \
	git add $(LAST_VERSION_FILE); \
	git commit -m "Auto update to $(VERSION)"; \
	git tag -a $(VERSION) -F $(COMMIT_LOG_FILE); \
	git push origin $(VERSION); \
	twine upload dist/* --verbose

# ==================================================
# cleanup of temp files
# ==================================================

# cleans up temp files from formatter, type checking, tests, coverage
# removes all built files
# removes $(TESTS_TEMP_DIR) to remove temporary test files
# recursively removes all `__pycache__` directories and `*.pyc` or `*.pyo` files
# distinct from `make docs-clean`, which only removes generated documentation files
.PHONY: clean
clean:
	@echo "clean up temporary files"
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf $(PACKAGE_NAME).egg-info
	rm -rf $(TESTS_TEMP_DIR)
	$(PYTHON_BASE) -Bc "import pathlib; [p.unlink() for p in pathlib.Path('$(PACKAGE_NAME)').rglob('*.py[co]')]"
	$(PYTHON_BASE) -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('$(PACKAGE_NAME)').rglob('__pycache__')]"
	$(PYTHON_BASE) -Bc "import pathlib; [p.unlink() for p in pathlib.Path('$(TESTS_DIR)').rglob('*.py[co]')]"
	$(PYTHON_BASE) -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('$(TESTS_DIR)').rglob('__pycache__')]"
	$(PYTHON_BASE) -Bc "import pathlib; [p.unlink() for p in pathlib.Path('$(DOCS_DIR)').rglob('*.py[co]')]"
	$(PYTHON_BASE) -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('$(DOCS_DIR)').rglob('__pycache__')]"


# ~~~~~~~~~~
# added site-clean here
.PHONY: clean-all
clean-all: clean docs-clean site-clean
	@echo "clean up all temporary files and generated docs and generated site"
# ~~~~~~~~~~

# ==================================================
# smart help command
# ==================================================

# listing targets is from stackoverflow
# https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
# no .PHONY because this will only be run before `make help`
# it's a separate command because getting the versions takes a bit of time
help-targets:
	@echo -n "# make targets"
	@echo ":"
	@cat Makefile | sed -n '/^\.PHONY: / h; /\(^\t@*echo\|^\t:\)/ {H; x; /PHONY/ s/.PHONY: \(.*\)\n.*"\(.*\)"/    make \1\t\2/p; d; x}'| sort -k2,2 |expand -t 30

# immediately print out the help targets, and then local variables (but those take a bit longer)
.PHONY: help
help: help-targets gen-version-info
	@echo -n ""
	@echo "# makefile variables"
	@echo "    PYTHON = $(PYTHON)"
	@echo "    PYTHON_VERSION = $(PYTHON_VERSION)"
	@echo "    PACKAGE_NAME = $(PACKAGE_NAME)"
	@echo "    VERSION = $(VERSION)"
	@echo "    LAST_VERSION = $(LAST_VERSION)"
	@echo "    PYTEST_OPTIONS = $(PYTEST_OPTIONS)"


# ==================================================
# custom targets
# ==================================================
# (put them down here, or delimit with ~~~~~)

BUILD_ARGS ?=

.PHONY: site
site:
	@echo "generate site"
	$(PYTHON) -m pdj_sitegen site_src/config.yml $(BUILD_ARGS)

.PHONY: site-clean
site-clean:
	@echo "remove generated site"
	rm -rf docs/demo_site