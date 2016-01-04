from solute.epfl.components.grouped_link_list_layout.grouped_link_list_layout import GroupedLinkListLayout
from solute.epfl.validators.text import TextValidator


class TypeAhead(GroupedLinkListLayout):

    # core internals
    compo_state = GroupedLinkListLayout.compo_state + ["selected_id", "label"]
    js_name = GroupedLinkListLayout.js_name + [('solute.epfl.components:typeahead/static', 'typeahead.js')]
    css_name = GroupedLinkListLayout.css_name + [('solute.epfl.components:typeahead/static', 'typeahead.css')]
    theme_path = GroupedLinkListLayout.theme_path.copy()
    theme_path['before'] = ['pretty_list_layout/theme', '>paginated_list_layout/theme', '>typeahead/theme']
    theme_path['inner_container'] = ['typeahead/theme']

    # js settings
    compo_js_name = 'TypeAhead'
    compo_js_params = GroupedLinkListLayout.compo_js_params + ['row_offset', 'row_limit', 'row_count', 'row_data',
                                                               'show_pagination', 'show_search', 'search_focus',
                                                               'open_on_hover', 'hide_list', 'search_timeout']
    compo_js_extras = ['handle_click']

    # derived attribute overrides
    validators = [TextValidator()]  #: Use TextValidator as default for mandatory function
    search_focus = False  #: Focus on the search input field on load.
    show_search = True  #: Show the search input field.
    use_headings = True  #: Sets GroupedLinkListLayout to show headings instead of submenus.
    event_name = 'select_option'  #: Default event name to be used for the form style value input.
    default = None  #: Default value that may be pre-set or pre-selected
    #: List type extension, see :attr:`ListLayout.list_type` for details.
    list_type = GroupedLinkListLayout.list_type + ['typeahead']
    data_interface = {
        'id': None,
        'text': None
    }

    # custom compo attribtes
    open_on_hover = True  #: Open the result list if the mouse is hovered over the component.
    force_hide_list = False  #: Force the dropdown list to hide
    mandatory = False  #: Set to true if value has to be provided for this element in order to yield a valid form
    label = None  #: Optional label describing the input field.
    placeholder = None  #: Placeholder text that can be displayed if supported by the input.
    compo_col = 12  #: col width of the component
    label_col = 2  #: label col width, input col is compo_col - label_col
    selected_id = None  #: Id param of selected option

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
                 links=None,
                 event_name=None,
                 use_headings=None,
                 default=None,
                 open_on_hover=None,
                 force_hide_list=None,
                 mandatory=None,
                 label=None,
                 placeholder=None,
                 compo_col=None,
                 label_col=None,
                 selected_id=None,
                 **kwargs):
        """TypeAhead component that offers grouping of entries under a common heading. Offers search bar above and
        pagination below using the EPFL theming mechanism. Links given as parameters are checked against the existing
        routes automatically showing or hiding them based on the users permissions. Entries can be grouped below a
        common heading given in the menu_group entry.

        .. code-block:: python

            components.TypeAhead(
                event_name='selected_category',
                links=[
                    {'text': 'foo0', 'url': '#foo', 'menu_group': 'bar'},
                    {'text': 'foo1', 'url': '#foo', 'menu_group': 'bar'},
                    {'text': 'foo2', 'url': '#foo', 'menu_group': 'bar2'},
                    {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                    {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                    {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                    {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                ]
            )

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
        :param links: List of dicts with text and url. May contain an icon entry.
        :param event_name: The name of an event to be triggered instead of rendering normal links.
        :param use_headings: Use menu_group strings as headings instead of submenus.
        :param default: Default value that may be pre-set or pre-selected
        :param open_on_hover: Open the result list if the mouse is hovered over the component.
        :param force_hide_list: Force the dropdown list to hide
        :param mandatory: Set to true if value has to be provided for this element in order to yield a valid form
        :param label: Optional label describing the input field.
        :param placeholder: Placeholder text that can be displayed if supported by the input.
        :param compo_col: col width of the component
        :param label_col: label col width, input col is compo_col - label_col
        :param selected_id: Id param of selected option
        """
        pass

    def init_transaction(self):
        super(GroupedLinkListLayout, self).init_transaction()
        if self.placeholder:
            self.search_placeholder = self.placeholder

    @property
    def hide_list(self):
        """The list container is supposed to be hidden if no entries are available.
        """
        return len(self.components) == 0 or self.force_hide_list

    def handle_select_option(self):
        selected_option = self.page.components[self.epfl_event_trace[0]]
        self.value = selected_option.text
        self.selected_id = selected_option.id
        self.row_data["search"] = self.value
        self.redraw()

    def set_state_attr(self, key, value):
        super(GroupedLinkListLayout,self).set_state_attr(key=key,value=value)
        if key == "value":
            if value is not None:
                self.row_data["search"] = value

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        super(GroupedLinkListLayout,self).handle_set_row(row_offset=row_offset,row_limit=row_limit,row_data=row_data)
        self.value = None # if something in search changed set the value to None
        self.selected_id = None
