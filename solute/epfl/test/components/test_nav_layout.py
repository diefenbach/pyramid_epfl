import pytest
from solute.epfl import components


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


@pytest.fixture(params=[True, False])
def bool_quad(request, bool_toggle):
    return request.param, bool_toggle


def test_img(page, bool_toggle):
    img = None
    if bool_toggle:
        img = 'some_image.jpg'
    page.root_node = components.NavLayout(
        img=img
    )

    page.handle_transaction()

    if bool_toggle:
        assert '<img src="%s" class="pull-left" />' % img in page.root_node.render()
    else:
        assert '<img src="' not in page.root_node.render()
        assert '" class="pull-left" />' not in page.root_node.render()


def test_title(page, bool_toggle):
    title = None
    if bool_toggle:
        title = 'some title'
    page.root_node = components.NavLayout(
        title=title
    )

    page.handle_transaction()

    if bool_toggle:
        assert title in page.root_node.render()
    else:
        assert '<a class="navbar-brand" href="/">' not in page.root_node.render()


def test_title_img(page, bool_quad):
    img = None
    if bool_quad[0]:
        img = 'some_image.jpg'
    title = None
    if bool_quad[1]:
        title = 'some title'

    page.root_node = components.NavLayout(
        title=title,
        img=img
    )

    page.handle_transaction()

    if bool_quad[0] and bool_quad[1]:
        assert '<img src="{img}" alt="{title}" class="pull-left" />'.format(img=img, title=title) \
               in page.root_node.render()
    elif bool_quad[0]:
        assert '<img src="%s" class="pull-left" />' % img in page.root_node.render()
    elif bool_quad[1]:
        assert title in page.root_node.render()
    else:
        assert '<a class="navbar-brand" href="/">' not in page.root_node.render()
