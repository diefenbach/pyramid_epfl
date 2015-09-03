import pytest
from solute.epfl.core.epflcomponentbase import ComponentContainerBase
from solute.epfl import components
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_link_generation(page, bool_toggle):
    event_name = None
    if bool_toggle:
        event_name = 'test_event'

    page.root_node = components.LinkListLayout(
        event_name=event_name,
        links=[
            {'id': i, 'name': 'link %s' % i} for i in range(0, 100)
        ]
    )
    page.handle_transaction()
    page.root_node.after_event_handling()

    if bool_toggle:
        for c in page.root_node.components:
            assert c.event_name == 'test_event'
    else:
        for c in page.root_node.components:
            assert not hasattr(c, 'event_name') or not c.event_name

    assert page.root_node.links == [{'id': c.id, 'name': c.name} for c in page.root_node.components]
