# * encoding: utf-8
import pytest
from solute.epfl import components


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_context_menu_from_parent(page, bool_toggle):
    def list_data(calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
        if bool_toggle:
            return [{"id": 1, "text": "first_link", "context_menu": "menu_one"},
                    {"id": 2, "text": "second_link", "context_menu": "menu_two"}]
        else:
            return [{"id": 1, "text": "first_link", "context_menu": None},
                    {"id": 2, "text": "second_link", "context_menu": None}]

    page.root_node = components.ContextListLayout(
        get_data=list_data
    )

    page.handle_transaction()
    compo = page.root_node

    if bool_toggle:
        compo.menu_one = [{'name': u"menu_one", 'event': "menu_one", 'type': "link"}]
        compo.menu_two = [{'name': u"menu_two", 'event': "menu_two", 'type': "link"}]
    else:
        compo.menu_one = None
        compo.menu_two = None

    rendered_html = compo.render()

    if bool_toggle:
        assert 'epfl-context-menu-btn' in rendered_html, "Could not find context menu button"
        assert 'context-dropdown-menu' in rendered_html, "Could not find context menu"
        assert 'data-event="menu_one"' in rendered_html, "Could not find context menu entry menu_one"
        assert 'data-event="menu_two"' in rendered_html, "Could not find context menu entry menu_two"
    else:
        assert 'epfl-context-menu-btn' not in rendered_html, "Find context menu button where no was expected"
        assert 'context-dropdown-menu' not in rendered_html, "Find context menu where no was expected"
        assert 'data-event="menu_one"' not in rendered_html, "Find context menu entry menu_one where no was expected"
        assert 'data-event="menu_two"' not in rendered_html, "Fnd context menu entry menu_two where no was expected"
