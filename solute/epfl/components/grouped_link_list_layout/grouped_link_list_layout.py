# coding: utf-8
from solute.epfl.components import LinkListLayout


class GroupedLinkListLayout(LinkListLayout):

    # core internals
    template_name = "grouped_link_list_layout/grouped_link_list_layout.html"
    css_name = LinkListLayout.css_name + [('solute.epfl.components:grouped_link_list_layout/static',
                                           'grouped_link_list_layout.css')]

    # derived attribute overrides
    data_interface = {'id': None,
                      'text': None,
                      'url': None,
                      'menu_group': None}

    # custom compo attributes
    use_headings = False  #: Use menu_group strings as headings instead of submenus.
    #: Add the specific list type for the grouped list layout. see :attr:`ListLayout.list_type`
    list_type = LinkListLayout.list_type + ['grouped']

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
                 use_headings=None,
                 **kwargs):
        """Paginated list using the PrettyListLayout based on bootstrap. Offers search bar above and pagination below
        using the EPFL theming mechanism. Links given as parameters are checked against the existing routes
        automatically showing or hiding them based on the users permissions. Entries can be grouped in submenus or below
        a common heading given in the menu_group entry.

        The format of menu_group entries can either be string or tuple. The later being used to allow selection of text
        to be marked with the html MARK-Tag. The tuple should look like this: ("group name", (sel_start, sel_end)) with
        sel_start and sel_end being integers used to slice the string "group name".

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
        :param use_headings: Use menu_group strings as headings instead of submenus.
        """
        pass

    @property
    def groups(self):
        groups = []

        def is_selection_group(target):
            return type(target) is tuple and len(target) == 2 and type(target[1]) is tuple and len(target[1]) == 2 \
                and type(target[1][0]) is int and type(target[1][1]) is int

        for compo in self.components:
            if getattr(compo, 'menu_group', None):
                menu_group = compo.menu_group

                # Special handling for selection groups or str/unicode menu_groups.
                if is_selection_group(menu_group) or type(menu_group) in [str, unicode]:
                    menu_group = (menu_group, )

                # Local shadow variable in order to recursively overwrite it without losing reference.
                _groups = groups

                # Detect best candidate for positioning the current compo.
                for name in menu_group:
                    selection = None
                    if type(name) is tuple and is_selection_group(name):
                        name, selection = name

                    for group in _groups:
                        if group.get('name') == name:
                            _groups = group.setdefault('components', [])
                            group.setdefault('icon', getattr(compo, 'icon', None))
                            break
                    else:
                        group = None

                    # If no group has been found or if it doesn't match the target name we need to create it.
                    if not group or group.get('name') != name:
                        _groups.append({
                            'type': 'group',
                            'name': name,
                            'icon': getattr(compo, 'icon', None),
                            'components': [],
                        })
                        if selection:
                            _groups[-1]['selection'] = selection
                        _groups = _groups[-1]['components']

                _groups.append({
                    'type': 'entry',
                    'component': compo,
                })
            else:
                groups.append({
                    'component': compo,
                    'type': 'entry',
                })

        return groups
