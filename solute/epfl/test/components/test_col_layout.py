import pytest
from solute.epfl import components
import re


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


@pytest.fixture(params=['center', 'west', 'east', 'north', 'south'])
def cardinal(request):
    return request.param


def test_vertical_centered(page, bool_toggle):
    page.root_node = components.ColLayout(
        vertical_center=bool_toggle,
    )
    page.handle_transaction()

    if bool_toggle:
        assert page.root_node.render().startswith('<div class="row vertical-align"')
    else:
        assert page.root_node.render().startswith('<div class="row"')


def test_css_cls(page):
    page.root_node = components.ColLayout(
        css_cls='some-css-class',
    )
    page.handle_transaction()

    assert page.root_node.render().startswith('<div class="row some-css-class"')


def test_col_width_assignment(page, bool_toggle):
    align = None
    if bool_toggle:
        align = 'centered'
    compo = components.Text(value='some text')

    page.root_node = components.ColLayout(
        node_list=[
            compo(cols=2, col_class='first-addition', align=align),
            compo(cols=4, col_class='second-addition', align=align),
            compo(cols=6, col_class='third-addition', align=align),
            compo(cols=2, col_class='fourth-addition', align=align),
            compo(cols=4, col_class='fifth-addition', align=align),
            compo(cols=6, col_class='sixth-addition', align=align),
        ]
    )

    page.handle_transaction()

    assert 'col-first-addition-2' in page.root_node.render()
    assert 'col-second-addition-4' in page.root_node.render()
    assert 'col-third-addition-6' in page.root_node.render()
    assert 'col-fourth-addition-2' in page.root_node.render()
    assert 'col-fifth-addition-4' in page.root_node.render()
    assert 'col-sixth-addition-6' in page.root_node.render()

    if bool_toggle:
        assert 'col-first-addition-2 text-centered' in page.root_node.render()
        assert 'col-second-addition-4 text-centered' in page.root_node.render()
        assert 'col-third-addition-6 text-centered' in page.root_node.render()
        assert 'col-fourth-addition-2 text-centered' in page.root_node.render()
        assert 'col-fifth-addition-4 text-centered' in page.root_node.render()
        assert 'col-sixth-addition-6 text-centered' in page.root_node.render()
    else:
        assert 'col-first-addition-2 text-centered' not in page.root_node.render()
        assert 'col-second-addition-4 text-centered' not in page.root_node.render()
        assert 'col-third-addition-6 text-centered' not in page.root_node.render()
        assert 'col-fourth-addition-2 text-centered' not in page.root_node.render()
        assert 'col-fifth-addition-4 text-centered' not in page.root_node.render()
        assert 'col-sixth-addition-6 text-centered' not in page.root_node.render()
