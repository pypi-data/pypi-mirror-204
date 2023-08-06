"""
Unitt tests for the ciqar.report.jinja_wrapper module.
"""

from __future__ import annotations
from contextlib import nullcontext, AbstractContextManager
from jinja2.environment import Environment, Template
from jinja2.exceptions import FilterArgumentError
from unittest.mock import Mock
from pathlib import Path
import pytest

from ciqar.report.jinja_wrapper import JinjaWrapper, TemplateRenderError


@pytest.mark.parametrize("template_name, raise_context", [
    ("default-mypy", nullcontext()),  # Existing template
    ("does-not-exist", pytest.raises(ValueError)),  # Non-existing template
])
def test_init(template_name: str, raise_context: AbstractContextManager) -> None:
    with raise_context:
        JinjaWrapper(template_package_name=template_name)
    assert True


def test_render_template_filenotfound():
    """
    Tests correct behaviour (exception) if the requested template is not available.
    """
    wrapper = JinjaWrapper(template_package_name="default-mypy")

    with pytest.raises(FileNotFoundError):
        wrapper.render_template(template_filename="doesntexist.html.in")

@pytest.mark.parametrize("render_side_effect, render_return_value, raise_context", [
    (  # Normal case, everything goes well
        None,
        "rendered file content",
        nullcontext()
    ),

    (  # Error during template rendering
       FilterArgumentError,
       None,
       pytest.raises(TemplateRenderError)
    ),
])
def test_render_template(
        render_side_effect: Exception | None,
        render_return_value: str,
        raise_context: AbstractContextManager
) -> None:
    """
    Tests the correct behaviour of "render_template" (except for the "template does not exist" case, see
    `test_render_template_filenotfound()` for that one).
    """
    mocked_template = Mock(spec=Template)
    mocked_template.render.side_effect = render_side_effect
    mocked_template.render.return_value = render_return_value

    wrapper = JinjaWrapper(template_package_name="default-mypy")
    wrapper._jinja_environment = Mock(spec=Environment)
    wrapper._jinja_environment.get_template.return_value = mocked_template

    with raise_context:
        rendered_file_content = wrapper.render_template(template_filename="example_file_list.html.in")
        assert render_return_value == rendered_file_content


@pytest.mark.parametrize("file_name, raise_context", [
    ("summary.html.in", nullcontext()),  # File exists
    ("notfound.css", pytest.raises(FileNotFoundError)),  # File does not exist
])
def test_get_static_file(file_name: str, raise_context: AbstractContextManager) -> None:
    src_dir = Path(__file__).parent.parent.parent.parent.joinpath("src")
    template_path = src_dir.joinpath("ciqar", "templates", "default-mypy")
    wrapper = JinjaWrapper(template_package_name="default-mypy")

    with raise_context:
        static_file_path = wrapper.get_static_file(template_filename=file_name)
        assert template_path.joinpath(file_name) == static_file_path
