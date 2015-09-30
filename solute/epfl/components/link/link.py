# coding: utf-8


from solute.epfl.core.epflcomponentbase import ComponentBase


class Link(ComponentBase):
    asset_spec = "solute.epfl.components:link/static"
    template_name = "link/link.html"
    js_name = ["link.js"]
    css_name = ["link.css"]

    compo_state = ["url", "route", "text", "icon", "name", "active"]

    url = None  #: The url this link points to. Used for the src attribute of the A-Tag.
    route = None  #: The route this link points to. Used to look up the url for the src attribute of the A-Tag.
    name = None  #: The name displayed for this link.
    text = None  #: Alias for name.
    icon = None  #: The icon to be displayed in front of the text.
    breadcrumb = False  #: Display the link as a breadcrumb.
    tile = False  #: Display the link as a rectangular tile.
    list_element = False  #: Display the link as a bootstrap style list element.
    selection = None  #: Tuple of integers: (selection_start, selection_end). MARK-Tag will be applied there.
    event_name = None  #: Name of an event to be triggered on click, prevents url and route from taking effect.
    double_click_event_name = None  #: Name of an event to be triggered on double click, prevents url and route from taking effect.
    btn_link = False  #: Set to true if link should be displayed as a button.
    new_window = False  #: Set to true if link should be opened in new window or tab
    active = False  #: Sets the active class in html
    stop_propagration_on_click = False  #: Set to true if click event should not be propagated to parent components
    #: Set to context menu list of dicts or to string
    #: list of dicts example: [{'name': u"Delete", 'event': "delete", 'type': "link"},{'name': "Rename", 'event': "rename", 'type': "link"}]
    #: if string is set link component calls container compos context_menu function with context_menu as parameter
    context_menu = None

    new_style_compo = True
    compo_js_params = ['event_name', 'double_click_event_name', 'stop_propagration_on_click']
    compo_js_name = 'Link'
    compo_js_extras = ['handle_click', 'handle_double_click']

    def __init__(self, page, cid, url=None, route=None, name=None, text=None, icon=None, breadcrumb=None, tile=None,
                 list_element=None, btn_link=None, new_window=None, event_name=None,double_click_event_name=None,
                 selection=None, stop_propagration_on_click=None,context_menu=None, **extra_params):
        """Simple Link component.

        Usage:
        .. code-block:: python

            Link(
                name="billiger.de",
                url="http://www.billiger.de"
            )

        :param url: The url this link points to. Used as src attribute of the A-Tag. If present route will be ignored.
        :param route: The route this link points to. Used to look up the url for the src attribute of the A-Tag.
        :param name: The name displayed for this link.
        :param text: Alias for name.
        :param icon: The icon to be displayed in front of the text.
        :param breadcrumb: Display the link as a breadcrumb.
        :param tile: Display the link as a rectangular tile.
        :param list_element: Display the link as a bootstrap style list element.
        :param btn_link: Display the link as a bootstrap style button.
        :param new_window: Open link in new window or tab
        :param event_name: Name of an event to be triggered on click, prevents url and route from taking effect.
        :param double_click_event_name: Name of an event to be triggered on double click, prevents url and route from taking effect.
        :param selection: Tuple of integers: (selection_start, selection_end). MARK-Tag will be applied there.
        :param stop_propagration_on_click: Set to true if click event should not be propagated to parent components
        :param context_menu: Set to context menu list of dicts or to string
        list of dicts example: [{'name': u"Delete", 'event': "delete", 'type': "link"},{'name': "Rename", 'event': "rename", 'type': "link"}]
        if string is set link component calls container compos context_menu function with context_menu as parameter
        """
        super(Link, self).__init__(page, cid, url=url, route=route, name=name, text=text, icon=icon,
                                   breadcrumb=breadcrumb, tile=tile, list_element=list_element,
                                   btn_link=btn_link, new_window=new_window, event_name=event_name,
                                   double_click_event_name=double_click_event_name,
                                   selection=selection,
                                   stop_propagration_on_click=stop_propagration_on_click,context_menu=context_menu,
                                   **extra_params)

    @property
    def _url(self):
        if self.event_name:
            return

        if self.route is None and self.url is None:
            return

        try:
            return self.page.get_route_path(self.route)
        except KeyError:
            pass

        try:
            return self.page.get_route_path(self.route, **self.page.request.matchdict)
        except KeyError:
            pass

        if self.url is None:
            return

        try:
            return self.url.format()
        except KeyError:
            pass

        try:
            return self.url.format(**self.page.request.matchdict)
        except KeyError:
            return None

    def get_context_menu(self):
        """ returns a context menu dict, if context_menu is a string ask container compo for context menu dict
        """
        if self.context_menu is None:
            return None
        elif type(self.context_menu) == list:
            return self.context_menu
        elif type(self.context_menu) == str:
            return self.container_compo.context_menu(self.context_menu)

    def is_first(self):
        """Returns True if the Link is the first component in this slot.
        """
        if not self.container_compo:
            return True
        siblings = self.container_compo.components
        position = siblings.index(self)
        if position == 0:
            return True

        for i in range(0, position):
            if siblings[i].slot == self.slot:
                return False

        return True

    def is_current_url(self):
        return self.page.request.matched_route.path == self._url
