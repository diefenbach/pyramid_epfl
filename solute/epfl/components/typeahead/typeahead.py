from solute.epfl.components.grouped_link_list_layout.grouped_link_list_layout import GroupedLinkListLayout
from solute.epfl.validators.text import TextValidator
from solute.epfl.components.form.inputbase import FormInputBase


class TypeAhead(FormInputBase, GroupedLinkListLayout):
    search_focus = True  #: Focus on the search input field on load.
    show_search = True  #: Show the search input field.
    use_headings = True  #: Sets GroupedLinkListLayout to show headings instead of submenus.
    open_on_hover = True  #: Open the result list if the mouse is hovered over the component.
    show_open_button = True  #: Show the open button

    validators=[TextValidator()]  #: Use TextValidator as default for mandatory function

    event_name = 'select_option'  #: Default event name to be used for the form style value input.

    js_parts = []
    js_name = GroupedLinkListLayout.js_name + [('solute.epfl.components:typeahead/static', 'typeahead.js')]
    css_name = GroupedLinkListLayout.css_name + [('solute.epfl.components:typeahead/static', 'typeahead.css')]

    new_style_compo = True
    compo_js_name = 'TypeAhead'
    compo_js_params = GroupedLinkListLayout.compo_js_params + ['row_offset', 'row_limit', 'row_count', 'row_data',
                                                               'show_pagination', 'show_search', 'search_focus',
                                                               'open_on_hover', 'show_open_button']
    compo_js_extras = ['handle_click']

    theme_path = GroupedLinkListLayout.theme_path.copy()
    theme_path['before'] = ['pretty_list_layout/theme', '>paginated_list_layout/theme', '>typeahead/theme']

    #: List type extension, see :attr:`ListLayout.list_type` for details.
    list_type = GroupedLinkListLayout.list_type + ['typeahead']

    data_interface = {
        'id': None,
        'text': None
    }

    def __init__(self, page, cid, links=None, use_headings=None, event_name=None, show_search=None, height=None,
                 open_on_hover=None, **kwargs):
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

        :param links: List of dicts with text and url. May contain an icon and a menu_group entry.
        :param use_headings: Use menu_group strings as headings instead of submenus.
        :param event_name: The name of an event to be triggered instead of rendering normal links.
        :param height: Set the list to the given height in pixels.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        :param open_on_hover: Open the result list if the mouse is hovered over the component.
        """
        super(GroupedLinkListLayout, self).__init__(page, cid, links=None, use_headings=None, event_name=None,
                                                    show_search=None, height=None, open_on_hover=open_on_hover,
                                                    **kwargs)


    def init_transaction(self):
        super(FormInputBase, self).init_transaction()
        super(GroupedLinkListLayout, self).init_transaction()

        if self.value is None and self.default is not None:
            self.value = self.default

        if self.value:
            self.row_data["search"] = self.value

        if self.placeholder:
            self.search_placeholder = self.placeholder

    @property
    def hide_list(self):
        """The list container is supposed to be hidden if no entries are available.
        """
        return len(self.components) == 0

    def handle_select_option(self):
        selected_option = self.page.components[self.epfl_event_trace[0]]
        self.value = selected_option.text
        self.row_data["search"] = self.value
        self.redraw()

