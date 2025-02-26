import pytest
from jinja2 import Environment

from pdj_sitegen.build import RenderError, SplitMarkdownError, render, split_md


def test_split_md_error():
	with pytest.raises(SplitMarkdownError):
		split_md("This is content without frontmatter")


def test_render_create_template_error():
	jinja_env = Environment()
	with pytest.raises(RenderError) as exc_info:
		render("{{ unclosed_tag", {}, jinja_env)
	assert exc_info.value.kind == "create_template"


def test_render_render_template_error():
	jinja_env = Environment()
	render("{{ undefined_variable }}", {}, jinja_env)


def test_render_error_str():
	jinja_env = Environment()
	try:
		render("{{ unclosed_tag", {}, jinja_env)
	except RenderError as e:
		assert "Error creating template" in str(e)

	try:
		render("{{ undefined_variable }}", {}, jinja_env)
	except RenderError as e:
		assert "Error rendering template" in str(e)
