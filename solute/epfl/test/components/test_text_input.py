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


def test_value(page):
    page.root_node = components.TextInput(
        cid='text_with_title',
        value='test value',
    )

    page.handle_transaction()

    assert 'value="test value"' in page.root_node.render()
    assert 'data-initial-value="test value"' in page.root_node.render()


def test_max_length(page, bool_toggle):
    value = 'test value'
    page.root_node = components.TextInput(
        cid='text_with_title',
        value=value,
        max_length=120,
        show_count=bool_toggle
    )

    page.handle_transaction()

    assert 'maxlength="120"' in page.root_node.render()

    assert_string = '_input_count">{len}</span>/120)</div>'.format(len=len(value))
    if bool_toggle:
        assert assert_string in page.root_node.render()
    else:
        assert assert_string not in page.root_node.render()


def test_typeahead_date(page, bool_quad):
    page.root_node = components.TextInput(
        value='test value',
        typeahead=bool_quad[0],
        date=bool_quad[1],
    )

    page.handle_transaction()

    if bool_quad[0] or bool_quad[1]:
        assert 'autocomplete="off"' in page.root_node.render()
    else:
        assert 'autocomplete="off"' not in page.root_node.render()


def test_password(page, bool_toggle):
    page.root_node = components.TextInput(
        value='test value',
        password=bool_toggle,
    )

    page.handle_transaction()

    if bool_toggle:
        assert 'type="password"' in page.root_node.render()
        assert 'type="text"' not in page.root_node.render()
        assert 'value="test value"' not in page.root_node.render()
        assert 'data-initial-value="test value"' not in page.root_node.render()
        assert 'value=""' in page.root_node.render()
        assert 'data-initial-value=""' in page.root_node.render()
    else:
        assert 'type="password"' not in page.root_node.render()
        assert 'type="text"' in page.root_node.render()
        assert 'value="test value"' in page.root_node.render()
        assert 'data-initial-value="test value"' in page.root_node.render()


def test_layover_icon(page, bool_toggle):
    icon = None
    if bool_toggle:
        icon = 'some-icon'

    page.root_node = components.TextInput(
        value='test value',
        layover_icon=icon,
    )

    page.handle_transaction()

    if bool_toggle:
        assert '<i class="fa some-icon"></i>' in page.root_node.render()
    else:
        assert '<i class="fa some-icon"></i>' not in page.root_node.render()
