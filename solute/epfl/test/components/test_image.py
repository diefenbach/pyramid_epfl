import pytest
from solute.epfl import components


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


@pytest.fixture(params=[True, False])
def bool_quad(request, bool_toggle):
    return request.param, bool_toggle


def test_image_path(page):
    page.root_node = components.Image(
        image_path='some_image.jpg'
    )

    page.handle_transaction()

    assert 'src="some_image.jpg"' in page.root_node.render()


def test_show_dominant_color(page, bool_toggle):
    page.root_node = components.Image(
        image_path='some_image.jpg',
        show_dominant_color=bool_toggle
    )

    page.handle_transaction()

    if bool_toggle:
        assert '<div class="epfl-img-component-dominant-color epfl-img-component-color" style="float:left; width:' \
               '100%; height: 30px;"></div>' in page.root_node.render()
    else:
        assert '<div class="epfl-img-component-dominant-color epfl-img-component-color" style="float:left; width:' \
               '100%; height: 30px;"></div>' not in page.root_node.render()


def test_show_additional_colors(page, bool_quad):
    show_dominant_color, show_additional_colors = bool_quad
    page.root_node = components.Image(
        image_path='some_image.jpg',
        show_dominant_color=show_dominant_color,
        show_additional_colors=show_additional_colors,
    )

    page.handle_transaction()

    if show_dominant_color:
        assert '<div class="epfl-img-component-dominant-color epfl-img-component-color" style="float:left; width:' \
               '100%; height: 30px;"></div>' in page.root_node.render()
        if show_additional_colors:
            assert '_palette1" class="epfl-img-component-color" ' in page.root_node.render()
            assert '_palette2" class="epfl-img-component-color" ' in page.root_node.render()
            assert '_palette3" class="epfl-img-component-color" ' in page.root_node.render()
            assert '_palette4" class="epfl-img-component-color" ' in page.root_node.render()
            assert '_palette5" class="epfl-img-component-color" ' in page.root_node.render()
            assert '_palette6" class="epfl-img-component-color" ' in page.root_node.render()
    else:
        assert '<div class="epfl-img-component-dominant-color epfl-img-component-color" style="float:left; width:' \
               '100%; height: 30px;"></div>' not in page.root_node.render()
        if show_additional_colors:
            assert '_palette1" class="epfl-img-component-color" ' not in page.root_node.render()
            assert '_palette2" class="epfl-img-component-color" ' not in page.root_node.render()
            assert '_palette3" class="epfl-img-component-color" ' not in page.root_node.render()
            assert '_palette4" class="epfl-img-component-color" ' not in page.root_node.render()
            assert '_palette5" class="epfl-img-component-color" ' not in page.root_node.render()
            assert '_palette6" class="epfl-img-component-color" ' not in page.root_node.render()


def test_padding(page, bool_toggle):
    page.root_node = components.Image(
        padding=bool_toggle
    )

    page.handle_transaction()

    if bool_toggle:
        assert 'padding: 10px;' in page.root_node.render()
    else:
        assert 'padding: 10px;' not in page.root_node.render()


def test_width(page, bool_toggle):
    width = None
    if bool_toggle:
        width = '372px'
    page.root_node = components.Image(
        width=width
    )

    page.handle_transaction()

    if bool_toggle:
        assert 'width: %s;' % width in page.root_node.render()
    else:
        assert 'width: auto;' in page.root_node.render()


def test_height(page, bool_toggle):
    height = None
    if bool_toggle:
        height = '372px'
    page.root_node = components.Image(
        height=height
    )

    page.handle_transaction()

    if bool_toggle:
        assert 'height: %s;' % height in page.root_node.render()
    else:
        assert 'height: auto;' in page.root_node.render()
