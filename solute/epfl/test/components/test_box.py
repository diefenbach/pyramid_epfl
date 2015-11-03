import pytest
from solute.epfl import components
from lxml import etree
import re


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


@pytest.fixture(params=['example value 1', 'another example value', None], scope='function')
def title_values(request):
    return request.param


@pytest.fixture()
def root_node(page, title_values):
    values = ['example value 1', 'another example value']
    page.root_node = components.Box(
        title=title_values
    )

    page.handle_transaction()

    return page.root_node


def test_title_rendering(title_values, root_node, bool_toggle):
    root_node.show_title = bool_toggle
    rendered_html = root_node.render()

    if title_values and bool_toggle:
        assert '<div class="panel-heading"' in rendered_html
        assert title_values in rendered_html
    elif title_values and not bool_toggle:
        assert '<div class="panel-heading"' not in rendered_html
        assert title_values not in rendered_html
    else:
        assert '<div class="panel-heading"' not in rendered_html


def test_remove_button(title_values, root_node, bool_toggle):
    root_node.is_removable = bool_toggle

    rendered_html = root_node.render()

    if title_values and not bool_toggle:
        assert '<a href="#" class="epfl_box_remove_button in_heading">' not in rendered_html
    elif title_values and bool_toggle:
        assert '<a href="#" class="epfl_box_remove_button in_heading">' in rendered_html
    elif not bool_toggle:
        assert '<a href="#" class="epfl_box_remove_button">' not in rendered_html
    elif bool_toggle:
        assert '<a href="#" class="epfl_box_remove_button">' in rendered_html


def test_hover_box(root_node, bool_toggle):
    root_node.hover_box = bool_toggle

    rendered_html = root_node.render()

    if bool_toggle:
        assert 'class="epfl_hover_box"' in rendered_html
    else:
        assert 'class="epfl_hover_box"' not in rendered_html


def test_box_shown(root_node, bool_toggle):
    root_node.box_shown = bool_toggle

    rendered_html = root_node.render()
    tree = etree.HTML(rendered_html)

    target_div = tree.xpath("//*[@epflid]")[0]

    if bool_toggle:
        assert 'epfl_box_border' in target_div.attrib.get('class')
    else:
        assert 'epfl_box_border' not in target_div.attrib.get('class')
        assert 'epfl_box' in target_div.attrib.get('class')


def test_auto_visibility(page):
    """Box auto visibility does not imply an empty box will be invisible but instead deals with the child components of
       said box. If all child components are invisible the box is too, if on or more child component is visible or none
       exist the box is visible.
    """

    page.root_node = components.Box(
        node_list=[
            components.Box(
                cid='empty_box'
            ),
            components.Box(
                cid='empty_box_no_auto_visibility',
                auto_visibility=False
            ),
            components.Box(
                cid='filled_box',
                node_list=[
                    components.Text(value='text 1'),
                    components.Text(value='text 2'),
                ]
            ),
            components.Box(
                cid='filled_box_no_auto_visibility',
                auto_visibility=False,
                node_list=[
                    components.Text(value='text 1'),
                    components.Text(value='text 2'),
                ]
            ),
        ]
    )

    page.handle_transaction()

    page.after_event_handling()  # Auto visibility is handled in after_event_handling

    # Initially all boxes should be visible.
    assert page.empty_box.is_visible()
    assert page.empty_box_no_auto_visibility.is_visible()
    assert page.filled_box.is_visible()
    assert page.filled_box_no_auto_visibility.is_visible()

    # Swap a single component on the filled boxes to invisible.
    page.filled_box.components[0].set_hidden()
    page.filled_box_no_auto_visibility.components[0].set_hidden()
    page.after_event_handling()

    # The boxes should still be visible.
    assert page.filled_box.is_visible()
    assert page.filled_box_no_auto_visibility.is_visible()

    # Swap the last remaining component on the filled boxes to invisible.
    page.filled_box.components[1].set_hidden()
    page.filled_box_no_auto_visibility.components[1].set_hidden()
    page.after_event_handling()

    # The auto visibility box should now be invisible, the other one not.
    assert not page.filled_box.is_visible()
    assert page.filled_box_no_auto_visibility.is_visible()

    # Add a dynamic component to the empty boxes.
    page.empty_box.add_component(components.Text(value='text 3'))
    page.empty_box_no_auto_visibility.add_component(components.Text(value='text 3'))
    page.after_event_handling()

    # The boxes should still be visible.
    assert page.empty_box.is_visible()
    assert page.empty_box_no_auto_visibility.is_visible()

    # Set the component on the previously empty boxes to invisible.
    page.empty_box.components[0].set_hidden()
    page.empty_box_no_auto_visibility.components[0].set_hidden()
    page.after_event_handling()

    # The auto visibility box should now be invisible, the other one not.
    assert not page.empty_box.is_visible()
    assert page.empty_box_no_auto_visibility.is_visible()


def test_read_only_overlay(root_node, bool_toggle):
    root_node.read_only = bool_toggle

    rendered_html = root_node.render()

    if bool_toggle:
        assert 'class="epfl-box-readonly-overlay"' in rendered_html
    else:
        assert 'class="epfl-box-readonly-overlay"' not in rendered_html
