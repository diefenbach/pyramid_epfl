import pytest
from solute.epfl import components
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_compact(page, bool_toggle):
    page.root_node = components.Checkbox(
        label='test label',
        compact=bool_toggle
    )

    page.handle_transaction()

    tree = etree.HTML(page.root_node.render())
    node = tree.xpath('//*[@epflid="root_node"]')[0]

    if bool_toggle:
        div = node.find('div')
        label = div.find('label')
        assert label is not None
        assert label.find('input') is not None
    else:
        assert node.find('label') is not None
        assert node.find('div') is not None
        assert node.find('div').find('input') is not None
