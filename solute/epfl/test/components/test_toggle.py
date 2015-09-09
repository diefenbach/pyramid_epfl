import pytest
from solute.epfl import components
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


@pytest.fixture(params=[True, False])
def bool_quad(request, bool_toggle):
    return bool_toggle, request.param


@pytest.fixture(params=[True, False])
def bool_hex(request, bool_quad):
    return bool_quad + (request.param, )


def test_enabled_text(page):
    on_text = 'some-on-text'
    off_text = 'some-off-text'

    page.root_node = components.Toggle(
        value=True,
        off_text=off_text,
        on_text=on_text,
    )

    page.handle_transaction()

    assert 'data-on-text="some-on-text"' in page.root_node.render()
    assert 'data-off-text="some-off-text"' in page.root_node.render()


def test_value(page, bool_toggle):
    page.root_node = components.Toggle(
        value=bool_toggle,
    )

    page.handle_transaction()

    if bool_toggle:
        assert 'value="True"' in page.root_node.render()
    else:
        assert 'value="False"' in page.root_node.render()
