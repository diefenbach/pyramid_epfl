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


def test_enabled_icon(page, bool_hex):
    enabled_icon = None
    if bool_hex[0]:
        enabled_icon = 'enabled-icon'
    enabled_icon_color = None
    if bool_hex[1]:
        enabled_icon_color = 'primary'
    enabled_icon_size = None
    if bool_hex[2]:
        enabled_icon_size = '2x'

    page.root_node = components.SimpleToggle(
        value=True,
        enabled_icon=enabled_icon,
        enabled_icon_color=enabled_icon_color,
        enabled_icon_size=enabled_icon_size,
        )

    page.handle_transaction()

    out = page.root_node.render()

    enabled_icon_pattern = re.compile('class="[^"]*fa-enabled-icon[^"]*"', re.MULTILINE)
    enabled_icon_color_pattern = re.compile('class="[^"]*text-primary[^"]*"', re.MULTILINE)
    enabled_icon_size_pattern = re.compile('class="[^"]*fa-2x[^"]*"', re.MULTILINE)

    if bool_hex[0]:
        assert enabled_icon_pattern.search(out)
    else:
        assert not enabled_icon_pattern.search(out)

    if bool_hex[1]:
        assert enabled_icon_color_pattern.search(out)
    else:
        assert not enabled_icon_color_pattern.search(out)

    if bool_hex[2]:
        assert enabled_icon_size_pattern.search(out)
    else:
        assert not enabled_icon_size_pattern.search(out)


def test_disabled_icon(page, bool_hex):
    disabled_icon = None
    if bool_hex[0]:
        disabled_icon = 'disabled-icon'
    disabled_icon_color = None
    if bool_hex[1]:
        disabled_icon_color = 'primary'
    disabled_icon_size = None
    if bool_hex[2]:
        disabled_icon_size = '2x'

    page.root_node = components.SimpleToggle(
        value=False,
        disabled_icon=disabled_icon,
        disabled_icon_color=disabled_icon_color,
        disabled_icon_size=disabled_icon_size,
        )

    page.handle_transaction()

    out = page.root_node.render()

    disabled_icon_pattern = re.compile('class="[^"]*fa-disabled-icon[^"]*"', re.MULTILINE)
    disabled_icon_color_pattern = re.compile('class="[^"]*text-primary[^"]*"', re.MULTILINE)
    disabled_icon_size_pattern = re.compile('class="[^"]*fa-2x[^"]*"', re.MULTILINE)

    if bool_hex[0]:
        assert disabled_icon_pattern.search(out)
    else:
        assert not disabled_icon_pattern.search(out)

    if bool_hex[1]:
        assert disabled_icon_color_pattern.search(out)
    else:
        assert not disabled_icon_color_pattern.search(out)

    if bool_hex[2]:
        assert disabled_icon_size_pattern.search(out)
    else:
        assert not disabled_icon_size_pattern.search(out)
