# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout
from solute.epfl.components import Link
from solute.epfl.core.epflutil import has_permission_for_route


class LinkListLayout(PaginatedListLayout):
    data_interface = {'id': None,
                      'text': None,
                      'url': None}

    theme_path = {'default': PaginatedListLayout.theme_path,
                  'row': ['link_list_layout/theme']}

    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:link_list_layout/static', 'link_list_layout.js')]
    js_parts = []

    compo_state = PaginatedListLayout.compo_state

    #: Add the specific list type for the link list layout. see :attr:`ListLayout.list_type`
    list_type = PaginatedListLayout.list_type + ['link']

    links = None  #: List of dicts to be used as entries.
    event_name = None  #: Default event to be triggered on clicks.

    auto_update_children = False

    new_style_compo = True
    compo_js_name = 'LinkListLayout'
    compo_js_params = ['row_offset', 'row_limit', 'row_count', 'row_data', 'show_pagination', 'show_search',
                       'search_focus', 'infinite_scrolling', 'search_timeout', 'infinite_scroll_debounce_delay']

    def __init__(self, page, cid, links=None, event_name=None, show_search=None, height=None, **kwargs):
        """Paginated list using the PrettyListLayout based on bootstrap. Offers search bar above and pagination below
        using the EPFL theming mechanism. Links given as parameters are checked against the existing routes
        automatically showing or hiding them based on the users permissions.

        :param links: List of dicts with text and url. May contain an icon entry.
        :param event_name: The name of an event to be triggered instead of rendering normal links.
        :param height: Set the list to the given height in pixels.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        """
        super(PaginatedListLayout, self).__init__(page, cid, links=None, event_name=None, show_search=None, height=None,
                                                  **kwargs)

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
