import pytest
from solute.epfl import components
from solute.epfl.core.epflcomponentbase import ComponentContainerBase

from link_asserts import assert_href_is, assert_with_a_twist, assert_breadcrumb, assert_list_element

@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param

@pytest.fixture(params=[
    # event_name, route, url
    (None, None, None),
    ('some_event', None, None),
    ('some_event', 'some_route', None),
    ('some_event', 'some_route', 'some_url'),
    (None, '/test_link_route', None),
    (None, '/test_link_route', 'some_url'),
    (None, None, 'some_url'),
])
def link_param_url(request):
    return request.param + ('some text', None)


def test_name_generation(page):
    test_name = '[[{{test_name}}]]'
    test_text = '[[{{test_text}}]]'

    page.root_node = components.Link(
        url='/foobar'
    )
    page.handle_transaction()
    compo = page.root_node

    assert 'None' in compo.render(), 'text and name are not set, but "None" is missing in the rendered html.'
    compo.render_cache = None

    compo.text = test_text
    assert test_text in compo.render(), 'text set to "{text}" but is missing in the rendered html.'.format(
        text=test_text
    )
    compo.render_cache = None

    compo.text = test_text
    compo.name = test_name
    assert test_name in compo.render(), 'name set to "{name}" but is missing in the rendered html.'.format(
        text=test_text,
        name=test_name,
    )
    assert test_text not in compo.render(), 'name set to "{name}" but text "{text}" is in the rendered html.'.format(
        text=test_text,
        name=test_name,
    )
    compo.render_cache = None

    compo.text = None
    compo.name = test_name
    assert test_name in compo.render(), 'name set to "{name}" but is missing in the rendered html.'.format(
        text=test_text,
        name=test_name,
    )
    assert 'None' not in compo.render(), 'name set to "{name}" but "None" is in the rendered html.'.format(
        text=test_text,
        name=test_name,
    )
    compo.render_cache = None


def test_url_generation(link_param_url, page, config):
    config.add_route('/test_link_route', pattern='/test_link_route')
    event_name, route, url, text, name = link_param_url

    page.root_node = components.Link(
        url=url,
        route=route,
        name=name,
        text=text,
        event_name=event_name,
    )
    page.handle_transaction()

    params = dict(
        _url=page.root_node._url,
        url=url,
        route=route,
        name=name,
        text=text,
        event_name=event_name,
    )

    compo = page.root_node

    if event_name:
        assert compo._url is None, 'event_name is set to {event_name} but _url is {_url}.'.format(**params)
        assert_href_is('event_name', params, compo, None)
    elif route:
        assert compo._url == route, 'route is set to {route} but _url is {_url}.'.format(**params)
        assert_href_is('route', params, compo, route)
    elif url:
        assert compo._url == url, 'url is set to {url} but _url is {_url}.'.format(**params)
        assert_href_is('url', params, compo, url)


def test_url_generation_with_dynamic_route(page, config):
    route = 'test_link_route_parametrized'
    config.add_route(route, pattern='/test_link_route/{param}')

    page.root_node = components.Link(
        text='foobar',
        route=route
    )
    page.handle_transaction()

    assert_href_is('route', {'route': route}, page.root_node, None)
    page.request.matchdict['param'] = '1234'
    assert_href_is('route', {'route': route}, page.root_node, '/test_link_route/1234')


def test_url_generation_with_dynamic_url(page):
    url = 'some_url/{with_a_twist}'
    page.root_node = components.Link(
        text='foobar',
        url=url
    )
    page.handle_transaction()

    assert_href_is('url', {'url': url}, page.root_node, None)
    twisted_url = assert_with_a_twist('url', page, url)
    assert_href_is('url', {'url': twisted_url}, page.root_node, twisted_url)


def test_icon(page):
    page.root_node = components.Link(
        text='foobar',
        icon='home'
    )
    page.handle_transaction()

    compo = page.root_node

    assert '<i class="fa fa-{icon}"></i>'.format(icon='home') in compo.render(), \
        'icon set to "home" but i tag is missing or malformed in html.'


def test_breadcrumb(page):
    page.root_node = ComponentContainerBase(
        node_list=[
            components.Link(
                cid='first_link',
                text='foobar',
                breadcrumb=True
            )])
    page.handle_transaction()

    root = page.root_node
    compo = page.first_link

    assert compo.is_first(), 'Link is first in container but is_first() is False.'
    assert_breadcrumb(compo)

    root.add_component(components.Link(
        cid='second_link',
        text='foobar',
        breadcrumb=True
    ))
    assert compo.is_first(), 'Link is first in container but is_first() is False.'
    assert_breadcrumb(compo)

    root.add_component(
        components.Link(
            cid='third_link',
            slot='foobar',
            text='foobar',
            breadcrumb=True
        ),
        position=0)

    assert compo.is_first(), 'Link is first in container but is_first() is False.'
    assert_breadcrumb(compo)

    root.add_component(components.Link(
        text='foobar',
        breadcrumb=True
    ), position=0)
    assert not compo.is_first(), 'Link is not first in container but is_first() is True.'
    assert_breadcrumb(compo)


def test_tile(page):
    page.root_node = components.Link(
        text='foobar',
        tile=True
    )
    page.handle_transaction()

    compo = page.root_node

    assert 'class="tile-link"' in compo.render(), 'tile set to True but class is missing or malformed in html.'


def test_list_element(page, route):
    page.root_node = components.Link(
        url='/foobar',
        text='foobar',
        list_element=True
    )
    page.handle_transaction()

    compo = page.root_node

    route.path = None
    assert not compo.is_current_url(), 'route.path is not equal to _url but is_current_url returns True.'
    assert_list_element(compo)

    route.path = compo._url
    assert compo.is_current_url(), 'route.path is equal to _url but is_current_url returns False.'
    assert_list_element(compo)


def test_selection(page):
    page.root_node = components.Link(
        url='/foobar',
        text='foobar',
    )
    page.handle_transaction()

    compo = page.root_node

    for selection, result in [
        ((0, 10), '<mark>foobar</mark>'),
        ((0, 3), '<mark>foo</mark>bar'),
        ((2, 4), 'fo<mark>ob</mark>ar'),
        ((2, 10), 'fo<mark>obar</mark>'), ]:

        compo.selection = selection
        assert result in compo.render(), \
            'selection set around foobar, but mark tag is missing or malformed in html.'
        compo.render_cache = None


def test_new_window(page):
    page.root_node = components.Link(
        text='foobar',
        new_window=True,
        tile=True
    )
    page.handle_transaction()

    compo = page.root_node

    assert 'target="_blank"' in compo.render(), 'new_window set to True but target="_blank" is missing or malformed in html.'


def test_context_menu(page, bool_toggle):
    page.root_node = components.Link(
        text='foobar'
    )

    page.handle_transaction()
    compo = page.root_node

    if bool_toggle:
        compo.context_menu = [{'name': u"Delete", 'event': "delete", 'type': "link"},
                              {'name': "Rename", 'event': "rename", 'type': "link"}]
    else:
        compo.context_menu = None

    rendered_html = compo.render()

    if bool_toggle:
        assert 'epfl-context-menu-btn' in rendered_html, "Could not find context menu button"
        assert 'context-dropdown-menu' in rendered_html, "Could not find context menu"
        assert 'data-event="delete"' in rendered_html, "Could not find context menu entry delete"
        assert 'data-event="rename"' in rendered_html, "Could not find context menu entry rename"
    else:
        assert 'epfl-context-menu-btn' not in rendered_html, "Find context menu button where no was expected"
        assert 'context-dropdown-menu' not in rendered_html, "Find context menu where no was expected"
        assert 'data-event="delete"' not in rendered_html, "Find context menu entry delete where no was expected"
        assert 'data-event="rename"' not in rendered_html, "Fnd context menu entry rename where no was expected"
