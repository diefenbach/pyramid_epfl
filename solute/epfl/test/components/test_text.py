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
    page.root_node = components.Box(
        node_list=[
            components.Text(
                cid='text_with_title',
                value='test value',
                title='test title'
            ),
            components.Text(
                cid='text_label',
                value='test value',
                label='test label'
            ),
            components.Text(
                cid='text_label_tag',
                value='test value',
                label='test label',
                tag='foo',
            ),
            components.Text(
                cid='text_vertical',
                value='test value',
                layout_vertical=True,
                label='test label'
            ),
            components.Text(
                cid='text_vertical_tag',
                value='test value',
                layout_vertical=True,
                label='test label',
                tag='foo'
            ),
            components.Text(
                cid='text_verbose_tag',
                value='test value',
                verbose=True,
                tag='foo'
            ),
            components.Text(
                cid='text_verbose',
                value='test value',
                verbose=True,
            ),
        ]
    )

    page.handle_transaction()

    assert '>test value<' in page.text_with_title.render()
    assert 'title="test title"' in page.text_with_title.render()

    assert 'test value' in page.text_vertical.render()
    assert 'test value' in page.text_vertical_tag.render()
    assert 'test value' in page.text_label.render()
    assert '>test value<' in page.text_verbose.render()

    assert '<foo ' in page.text_verbose_tag.render()
    assert '</foo>' in page.text_verbose_tag.render()
    assert '<foo ' in page.text_vertical_tag.render()
    assert '</foo>' in page.text_vertical_tag.render()
    assert '<foo ' in page.text_label_tag.render()
    assert '</foo>' in page.text_label_tag.render()


def test_label(page, bool_quad):
    on, vertical = bool_quad
    label = None
    if on:
        label = 'test label'

    page.root_node = components.Text(
        value='test value',
        label=label,
        layout_vertical=vertical
    )

    page.handle_transaction()

    assert 'test value' in page.root_node.render()
    if on and vertical:
        assert '<label class="col-sm-12">test label</label>' in page.root_node.render()
    elif on:
        assert '<label class="col-sm-2 control-label">test label</label>' in page.root_node.render()
    else:
        assert '<label class="col-sm-2">test label</label>' not in page.root_node.render()
        assert '<label class="col-sm-2 control-label">test label</label>' not in page.root_node.render()


def test_tag_class(page):
    page.root_node = components.Box(
        node_list=[
            components.Text(
                cid='text_label_tag',
                value='test value',
                label='test label',
                tag='foo',
                tag_class='special-tag-class'
            ),
            components.Text(
                cid='text_vertical_tag',
                value='test value',
                layout_vertical=True,
                label='test label',
                tag='foo',
                tag_class='special-tag-class'
            ),
            components.Text(
                cid='text_verbose_tag',
                value='test value',
                verbose=True,
                tag='foo',
                tag_class='special-tag-class'
            ),
            components.Text(
                cid='text_label_tag_no_class',
                value='test value',
                label='test label',
                tag='foo',
            ),
            components.Text(
                cid='text_vertical_tag_no_class',
                value='test value',
                layout_vertical=True,
                label='test label',
                tag='foo',
            ),
            components.Text(
                cid='text_verbose_tag_no_class',
                value='test value',
                verbose=True,
                tag='foo',
            ),
        ]
    )

    page.handle_transaction()

    assert 'class="special-tag-class"' in page.text_verbose_tag.render()
    assert 'class="special-tag-class"' in page.text_vertical_tag.render()
    assert 'class="special-tag-class"' in page.text_label_tag.render()

    assert 'class="special-tag-class"' not in page.text_verbose_tag_no_class.render()
    assert 'class="special-tag-class"' not in page.text_vertical_tag_no_class.render()
    assert 'class="special-tag-class"' not in page.text_label_tag_no_class.render()
