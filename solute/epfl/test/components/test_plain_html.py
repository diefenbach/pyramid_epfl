import pytest
from solute.epfl import components
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_value(page):
    html = "<div><label>test label</label></div>"
    page.root_node = components.PlainHtml(
        value=html
    )

    page.handle_transaction()

    assert html in page.root_node.render()
