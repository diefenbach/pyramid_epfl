import pytest
from solute.epfl import components
from solute.epfl import epflassets
from solute.epfl import epflpage
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_icon(page, bool_toggle):
    page.root_node = components.RecursiveTree(
        show_children=bool_toggle,
        icon_open='icon-open-class',
        icon_close='icon-close-class',
    )

    page.handle_transaction()

    if bool_toggle:
        assert '<i class="fa fa-icon-close-class"></i>' in page.root_node.render()
        assert '<i class="fa fa-icon-open-class"></i>' not in page.root_node.render()
    else:
        assert '<i class="fa fa-icon-open-class"></i>' in page.root_node.render()
        assert '<i class="fa fa-icon-close-class"></i>' not in page.root_node.render()


def test_label(page, bool_toggle):
    label = None
    if bool_toggle:
        label = 'some label'

    page.root_node = components.RecursiveTree(
        id=1,
        label=label
    )

    page.handle_transaction()

    if bool_toggle:
        assert '<span>some label (1)</span>' in page.root_node.render()
    else:
        assert '<span>some label (1)</span>' not in page.root_node.render()


def test_handle_scroll(page):
    page.root_node = components.RecursiveTree()

    page.handle_transaction()
    page.root_node.handle_scroll(12345)

    assert page.root_node.scroll_position == 12345


def test_handle_click_icon(page):
    page.root_node = components.RecursiveTree()

    page.handle_transaction()
    old_show_children = page.root_node.show_children
    page.root_node.handle_click_icon()

    assert page.root_node.show_children is not old_show_children


def test_handle_click_label(page):
    page.root_node = components.RecursiveTree()

    page.handle_transaction()

    assert page.root_node.handle_click_label
    page.root_node.handle_click_label()


def test_recursive_generation(pyramid_req, bool_toggle):
    # For this example we need this as the default.
    components.RecursiveTree.show_children = True

    page = ExamplePage(None, pyramid_req)
    if bool_toggle:
        page = ExamplePageComplex(None, pyramid_req)

    page()

    root_node = page.root_node

    assert len(root_node.components) == 10
    for compo in root_node.components:
        assert len(compo.components) == 10


class ExampleModel(epflassets.ModelBase):
    data = [
        {'id': i, 'label': 'label %s' % i, 'icon_open': 'icon-open-%s' % i, 'icon_close': 'icon-close-%s' % i}
        for i in range(0, 30)
    ]

    def load_first(self, *args, **kwargs):
        return self.data[0:10]

    def load_second(self, *args, **kwargs):
        return self.data[10:20]

    def load_third(self, *args, **kwargs):
        return self.data[20:30]


class ExamplePage(epflpage.Page):
    model = ExampleModel

    root_node = components.RecursiveTree(
        get_data=['first', 'second', 'third'],
        data_interface=components.RecursiveTree.data_interface,
    )


class ExamplePageComplex(ExamplePage):
    root_node = components.RecursiveTree(
        get_data=['first', 'second', 'third'],
        data_interface=[
            components.RecursiveTree.data_interface,
            components.RecursiveTree.data_interface,
            components.RecursiveTree.data_interface
        ]
    )
