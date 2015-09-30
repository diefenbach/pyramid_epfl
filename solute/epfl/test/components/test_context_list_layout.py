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
    page.handle_transaction()

    root = page.root_node

    assert 'data-event="menu_one"' and 'data-event="menu_two"' in root.render()
