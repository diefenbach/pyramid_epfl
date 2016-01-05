# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout
from solute.epfl.components import Link
from solute.epfl.core.epflutil import has_permission_for_route


class LinkListLayout(PaginatedListLayout):

    # core internals
    theme_path = {'default': PaginatedListLayout.theme_path,
                  'row': ['link_list_layout/theme']}

    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:link_list_layout/static', 'link_list_layout.js')]
    compo_state = PaginatedListLayout.compo_state

    # js settings
    compo_js_auto_parts = True
    compo_js_name = 'LinkListLayout'
    compo_js_params = ['row_offset', 'row_limit', 'row_count', 'row_data', 'show_pagination', 'show_search',
                       'search_focus']

    # derived attribute overrides
    data_interface = {'id': None,
                      'text': None,
                      'url': None}
    auto_update_children = False
    #: Add the specific list type for the link list layout. see :attr:`ListLayout.list_type`
    list_type = PaginatedListLayout.list_type + ['link']

    # custom compo attributes
    links = None  #: List of dicts to be used as entries.
    event_name = None  #: Default event to be triggered on clicks.

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
        :param links: List of dicts with text and url. May contain an icon entry.
        :param event_name: The name of an event to be triggered instead of rendering normal links.
        """
        pass

    def get_data(self, row_offset=None, row_limit=None, row_data=None):
        links = []
        if self.links is None:
            self.links = []
        highest_rank = 0
        for i, link in enumerate(self.links):
            if not has_permission_for_route(self.request, link.get('route', link.get('url'))):
                continue

            links.append({'id': i})
            links[-1].update(link)

            if self.event_name:
                links[-1]['event_name'] = self.event_name
            highest_rank = max(highest_rank, links[-1].get('rank') or 0)

        links.sort(key=lambda x: highest_rank + 1 if x.get('rank') is None else x.get('rank'))

        return links

    @classmethod
    def default_child_cls(cls, *args, **kwargs):
        kwargs['list_element'] = True
        if cls.event_name:
            kwargs['event_name'] = cls.event_name
        return Link(*args, **kwargs)

    def is_current_url(self, url):
        return self.page.request.matched_route.path == url
