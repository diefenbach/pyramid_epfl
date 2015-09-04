import pytest
from solute.epfl import components
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_is_dirty(page, bool_toggle):
    page.root_node = components.Form(
        is_dirty=bool_toggle
    )

    page.handle_transaction()

    if bool_toggle:
        assert "dirty='1'" in page.root_node.render()
    else:
        assert "dirty='0'" in page.root_node.render()
