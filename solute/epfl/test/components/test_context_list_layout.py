# * encoding: utf-8
from solute.epfl import components


def test_context_menu_from_parent(page):
    def list_data(calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
        return [{"id": 1, "text": "first_link", "context_menu": "menu_one"},
                {"id": 2, "text": "second_link", "context_menu": "menu_two"}]

    page.root_node = components.ContextListLayout(
        menu_one=[{'name': u"menu_one", 'event': "menu_one", 'type': "link"}],
        menu_two=[{'name': u"menu_two", 'event': "menu_two", 'type': "link"}],
        get_data=list_data
    )

    context_menu_html = ['epfl-context-menu-btn', 'context-dropdown-menu', 'data-event="menu_one"',
                         'data-event="menu_two"']

    page.handle_transaction()

    compo = page.root_node
    assert all(
        str in compo.render() for str in context_menu_html), "Could not find context menu or context menu is invalid"

    compo.render_cache = None
    for child in compo.components:
        child.render_cache = None

    compo.menu_one = None
    compo.menu_two = None

    assert not any(str in compo.render() for str in context_menu_html),  "Found context menu where no menu was expected"
