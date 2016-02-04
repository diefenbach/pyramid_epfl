# coding: utf-8

"""

"""

from solute.epfl.components import LinkListLayout


class HoverLinkListLayout(LinkListLayout):

    # core internals
    theme_path = {'default': LinkListLayout.theme_path['default'],
                  'row': ['hover_link_list_layout/theme']}
    js_name = LinkListLayout.js_name + [('solute.epfl.components:hover_link_list_layout/static',
                                         'hover_link_list_layout.js')]

    # js settings
    compo_js_auto_parts = True
    compo_js_name = 'HoverLinkListLayout'

    # derived attribute overrides
    data_interface = {
        'id': None,
        'text': None,
        'src': None,
        'url': None
    }

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
                 links=None,
                 event_name=None,
                 **kwargs):
        """Paginated list using the PrettyListLayout based on bootstrap. Offers search bar above and pagination below
        using the EPFL theming mechanism. Links given as parameters are checked against the existing routes
        automatically showing or hiding them based on the users permissions.

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
        :param links: List of dicts with text and url. May contain an icon entry.
        :param event_name: The name of an event to be triggered instead of rendering normal links.
        """
        pass
