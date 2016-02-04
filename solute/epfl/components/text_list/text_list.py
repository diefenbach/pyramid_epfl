# coding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout


class TextList(PaginatedListLayout):
    """
    Text List is simple list which displays text
    """

    # core internals
    theme_path = {'default': PaginatedListLayout.theme_path,
                  'row': ['text_list/theme'],
                  'container': ['text_list/theme']}
    js_name = PaginatedListLayout.js_name + [(
        'solute.epfl.components:text_list/static',
        'text_list.js')]

    # js settings
    compo_js_name = 'TextList'

    # derived attribute overrides
    default_child_cls = epflcomponentbase.ComponentBase
    data_interface = {'id': None,
                      'text': None}

    def __init__(self, page, cid,
                 node_list=None,
                 height=None,
                 hide_list=None,
                 show_search=None,
                 show_pagination=None,
                 search_placeholder=None,
                 search_focus=None,
                 visible_pages_limit=None,
                 reset_row_offset_on_search_change=None,
                 search_focus_after_search=None,
                 search_timeout=None,
                 infinite_scroll_debounce_delay=None,
                 show_row_count=None,
                 show_page_count=None,
                 data_interface=None,
                 **extra_params):
        """
        Text List is simple list which displays text
        :param node_list: List of child components.
        :param height: Set the list to the given height in pixels.
        :param hide_list: Hide the list container but nothing else.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_placeholder: The placeholder text for the search input.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        :param visible_pages_limit: Specify the number of pages that should be visible in the pagination bar.
        :param reset_row_offset_on_search_change: Reset row_offset once the user changes the search string.
        :param search_focus_after_search: Focus the search input after a search
        :param search_timeout: The timeout in ms until the search event fires
        :param infinite_scroll_debounce_delay: The delay for scroll debounce in infinite scrolling lists
        :param show_row_count: Show the row count in the pagination bar (depends on show_pagination=True)
        :param show_page_count: Show the page count in the pagination bar (depends on show_pagination=True)
        :param data_interface: data interface for child class needs id and text
        """
        pass
