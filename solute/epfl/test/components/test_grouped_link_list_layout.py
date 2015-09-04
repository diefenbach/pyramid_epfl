import pytest
from solute.epfl.core.epflcomponentbase import ComponentContainerBase
from solute.epfl import components
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_grouping(page):
    event_name = None
    if bool_toggle:
        event_name = 'test_event'

    page.root_node = ComponentContainerBase(
        node_list=[
            components.GroupedLinkListLayout(
                event_name=event_name,
                links=[
                    {
                        'id': i,
                        'text': 'text %s' % i,
                        'url': 'url_%s' % i,
                        'menu_group': '...group %s...' % (i / 10)
                    } for i in range(0, 100)
                ]
            ),
            components.GroupedLinkListLayout(
                event_name=event_name,
                links=[
                    {
                        'id': i,
                        'text': 'text %s' % i,
                        'url': 'url_%s' % i,
                        'menu_group': None
                    } for i in range(100, 200)
                ]
            ),
            components.GroupedLinkListLayout(
                cid='fucktard',
                event_name=event_name,
                use_headings=True,
                links=[
                    {
                        'id': i,
                        'text': 'text %s' % i,
                        'url': 'url_%s' % i,
                        'menu_group': ('...group %s...' % (i / 10), (3, 7))
                    } for i in range(200, 300)
                ]
            ),
            ]
    )
    page.handle_transaction()

    compo1 = page.root_node.components[0]
    compo2 = page.root_node.components[1]
    compo3 = page.root_node.components[2]

    compo1.after_event_handling()
    compo2.after_event_handling()
    compo3.after_event_handling()

    if bool_toggle:
        for c in list(compo1.components) + list(compo2.components) + list(compo3.components):
            assert c.event_name == 'test_event'
    else:
        for c in list(compo1.components) + list(compo2.components) + list(compo3.components):
            assert not hasattr(c, 'event_name') or not c.event_name

    assert compo1.links == [{'id': c.id, 'text': c.text, 'url': c.url, 'menu_group': c.menu_group}
                            for c in compo1.components]
    assert compo2.links == [{'id': c.id, 'text': c.text, 'url': c.url, 'menu_group': c.menu_group}
                            for c in compo2.components]
    assert compo3.links == [{'id': c.id, 'text': c.text, 'url': c.url, 'menu_group': c.menu_group}
                            for c in compo3.components]

    for i in range(0, 10):
        assert '...group %s...' % i in compo1.render()

    for i in range(10, 20):
        assert '<a class="list-group-item col-sm-12">' not in compo2.render()

    assert '<div class="list-group-item col-sm-12 list-group-item-info">' in compo3.render()
    for i in range(20, 30):
        assert '...<mark>grou</mark>p %s...' % i in compo3.render()
