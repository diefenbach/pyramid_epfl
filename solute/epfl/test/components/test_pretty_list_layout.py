import pytest
from solute.epfl import components
import re


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


@pytest.fixture(params=[True, False])
def bool_quad(request, bool_toggle):
    return request.param, bool_toggle


@pytest.fixture(params=['center', 'west', 'east', 'north', 'south'])
def cardinal(request):
    return request.param


def test_height_and_hidden(page, bool_quad):
    height_toggle, visible_toggle = bool_quad
    height = None
    if height_toggle:
        height = 300

    page.root_node = components.PrettyListLayout(
        height=height,
        hide_list=visible_toggle
    )

    page.handle_transaction()

    if height_toggle:
        assert 'height: 300px;' in page.root_node.render()
    else:
        assert 'height: 300px;' not in page.root_node.render()

    if visible_toggle:
        assert 'display: none;' in page.root_node.render()
    else:
        assert 'display: none;' not in page.root_node.render()
