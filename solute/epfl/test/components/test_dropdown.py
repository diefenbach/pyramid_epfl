import pytest
from solute.epfl import components
import re


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


@pytest.fixture(params=['center', 'west', 'east', 'north', 'south'])
def cardinal(request):
    return request.param


def test_vertical_centered(page, bool_toggle):
    page.root_node = components.Dropdown(
        small_button=bool_toggle,
    )
    page.handle_transaction()

    if bool_toggle:
        assert '"btn btn-default btn-xs dropdown-toggle"' in page.root_node.render()
    else:
        assert '"btn btn-default dropdown-toggle"' in page.root_node.render()


def test_caret(page, bool_toggle):
    page.root_node = components.Dropdown(
        caret=bool_toggle,
    )
    page.handle_transaction()

    if bool_toggle:
        assert " <span class='caret'></span>" in page.root_node.render()
    else:
        assert " <span class='caret'></span>" not in page.root_node.render()


def test_menu_icon(page, bool_toggle):
    menu_icon = None
    if bool_toggle:
        menu_icon = 'fa-times'
    page.root_node = components.Dropdown(
        menu_icon=menu_icon,
    )
    page.handle_transaction()

    if bool_toggle:
        assert '<i class="fa fa-times"></i>' in page.root_node.render()
    else:
        assert '<i class="fa fa-times"></i>' not in page.root_node.render()


def test_menu_label(page, bool_toggle):
    menu_label = None
    if bool_toggle:
        menu_label = 'some label'
    page.root_node = components.Dropdown(
        menu_label=menu_label,
    )
    page.handle_transaction()

    if bool_toggle:
        assert 'some label' in page.root_node.render()
    else:
        assert 'some label' not in page.root_node.render()


def test_children(page):
    page.root_node = components.Dropdown(
        children=[
            {'key': 'first key', 'label': 'first label'},
            {'key': 'second key', 'label': 'second label'},
            {'key': 'third key', 'label': 'third label'},
        ]
    )
    page.handle_transaction()

    assert '"first key"' in page.root_node.render()
    assert '>first label<' in page.root_node.render()

    assert '"second key"' in page.root_node.render()
    assert '>second label<' in page.root_node.render()

    assert '"third key"' in page.root_node.render()
    assert '>third label<' in page.root_node.render()
