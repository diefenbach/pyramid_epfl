import pytest
from solute.epfl import components
from solute.epfl.core.epflcomponentbase import ComponentContainerBase


@pytest.fixture(params=[0, 1, 2])
def tab_selector(request):
    return request.param


def test_visibility_settings_on_rendering(tab_selector, page):
    page.root_node = components.TabsLayout(
        node_list=[
            components.Text(value='Text value 1'),
            components.Text(value='Text value 2'),
            components.Text(value='Text value 3'),
        ]
    )

    page.handle_transaction()
    root_node = page.root_node
    root_node.handle_toggle_tab(root_node.components[tab_selector].cid)

    page.render()

    for i, compo in enumerate(root_node.components):
        if i == tab_selector:
            assert compo.is_visible()
        else:
            assert not compo.is_visible()


def test_deleting_active_tab(page):
    page.root_node = components.TabsLayout(
        node_list=[
            components.Text(value='Text value 1'),
            components.Text(value='Text value 2', cid='tab2'),
            components.Text(value='Text value 3'),
        ]
    )

    page.handle_transaction()
    root_node = page.root_node
    root_node.handle_toggle_tab(root_node.components[1].cid)

    root_node.del_component(root_node.components[1].cid)

    assert root_node.active_tab_cid == ''
