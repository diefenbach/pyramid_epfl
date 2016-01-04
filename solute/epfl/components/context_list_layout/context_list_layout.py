# * encoding: utf-8
from solute.epfl.components import PaginatedListLayout, Link


class ContextListLayout(PaginatedListLayout):
    """
    A searchable list layout with a context menu in every row.

    Its content and the context menu type is configured using get_data() the menu type than can be defined as attribute
    get_data example

    .. code-block:: python

        data = []
        for i in range(0, 100):
            data.append({'id': i, "text": "test" + str(i), 'context_menu':menu_type})

    component example

    .. code-block:: python

         components.ContextListLayout(
                            get_data=list_data,
                            menu_one=[{'name': u"Menu 1", 'event': "delete", 'type': "link"},
                                      {'name': "Rename", 'event': "rename", 'type': "link"}],
                            menu_two=[{'name': u"Menu 2", 'event': "delete", 'type': "link"},
                                      {'name': "Rename", 'event': "rename", 'type': "link"}],
                            handle_delete=None,
                            handle_rename=None
                            )


    A click on a context menu entry emits an event which have to be handled
    for example the entry

    .. code-block:: python

        {'name':"rename", 'event':"rename", 'type':"link"}

    have to be handled by

    .. code-block:: python

        def handle_rename(self, id, data):
            pass

    """

    # core settings
    theme_path = {'row': ['context_list_layout/theme'],
                  'default': ['pretty_list_layout/theme', '<paginated_list_layout/theme'],
                  'inner_container': ['pretty_list_layout/theme', '>context_list_layout/theme']
                  }
    js_name = PaginatedListLayout.js_name + [
        ("solute.epfl.components:context_list_layout/static", "context_list_layout.js")]
    css_name = PaginatedListLayout.css_name + [
        ("solute.epfl.components:context_list_layout/static", "context_list_layout.css")]

    # js settings
    new_style_compo = True
    compo_js_name = 'ContextListLayout'

    # derived attributes overrides
    default_child_cls = Link
    show_pagination = False  #: see :attr:`PaginatedListLayout.show_pagination`
    show_search = True  #: see :attr:`PaginatedListLayout.show_search`
    auto_update_children = True
    data_interface = {'id': None, 'text': None, 'context_menu': None}

    def __init__(self, page, cid,
                 node_list=None,
                 height=None,
                 show_search=None,
                 show_pagination=None,
                 search_placeholder=None,
                 search_focus=None,
                 visible_pages_limit=None,
                 reset_row_offset_on_search_change=None,
                 search_focus_after_search=None,
                 search_timeout=None,
                 infinite_scroll_debounce_delay=None,
                 get_data=None,
                 auto_update_children=None,
                 data_interface=None,
                 **kwargs):
        """ContextListLayout Component

        :param node_list: List of child components.
        :param height: Set the list to the given height in pixels.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_placeholder: The placeholder text for the search input.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        :param visible_pages_limit: Specify the number of pages that should be visible in the pagination bar.
        :param reset_row_offset_on_search_change: Reset row_offset once the user changes the search string.
        :param search_focus_after_search: Focus the search input after a search
        :param search_timeout: The timeout in ms until the search event fires
        :param infinite_scroll_debounce_delay: The delay for scroll debounce in infinite scrolling lists
        :param get_data: A get_data source that is used for this component
        :param auto_update_children: Updates are triggered every request in after_event_handling if True.
        :param data_interface: Data interface to translate the results from get_data polling.
        """
        pass

    def handle_delete(self, entry_id, data):
        pass

    def handle_rename(self, entry_id, data):
        pass

    def context_menu(self, context_menu_type):
        return getattr(self, context_menu_type)
