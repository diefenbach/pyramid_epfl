# coding: utf-8
from solute.epfl.core.epflcomponentbase import ComponentBase


class Link(ComponentBase):

    # core internals
    template_name = "link/link.html"
    asset_spec = "solute.epfl.components:link/static"
    js_name = ["link.js", "jquery.tooltipster.min.js"]
    css_name = ["link.css", "tooltipster.css", "tooltipster-shadow.css"]
    compo_state = ["url", "route", "text", "icon", "name", "active", "context_menu", "popover_text", "popover_trigger"]

    # js settings
    compo_js_auto_parts = True
    compo_js_params = ['event_name', 'double_click_event_name', 'shift_click_event_name', 'stop_propagation_on_click',
                       'popover_text', 'popover_position', 'popover_trigger']
    compo_js_name = 'Link'
    compo_js_extras = ['handle_click', 'handle_double_click', 'handle_shift_click']

    # custom compo attributes
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
    #: Name of an event to be triggered on double click, prevents url and route from taking effect.
    double_click_event_name = None
    #: Name of an event to be triggered on shift click, prevents url and route from taking effect.
    shift_click_event_name = None
    btn_link = False  #: Set to true if link should be displayed as a button.
    btn_link_color = "default"  #: the color of the link button possible values: bootstrap colors: primary default etc.
    new_window = False  #: Set to true if link should be opened in new window or tab
    popover_text = None  #: If set, click on link displays this text
    popover_trigger = "hover"  #: trigger for popover text
    popover_position = "top"  #: popover position possible values: left right top bottom
    active = False  #: Sets the active class in html
    stop_propagation_on_click = False  #: Set to true if click event should not be propagated to parent components
    #: Set to context menu list of dicts or to string
    #: list of dicts example: [{'name': u"Delete", 'event': "delete", 'type': "link"},
    #: {'name': "Rename", 'event': "rename", 'type': "link", 'disabled': True}]
    #: if string is set link component calls container compos context_menu function with context_menu as parameter
    context_menu = None

    def __init__(self, page, cid,
                 url=None,
                 route=None,
                 name=None,
                 text=None,
                 icon=None,
                 breadcrumb=None,
                 tile=None,
                 list_element=None,
                 btn_link=None,
                 new_window=None,
                 event_name=None,
                 double_click_event_name=None,
                 selection=None,
                 stop_propagation_on_click=None,
                 popover_text=None,
                 context_menu=None,
                 popover_trigger=None,
                 popover_position=None,
                 btn_link_color=None,
                 **extra_params):
        """Simple Link component.

        Usage:
        .. code-block:: python

            Link(
                name="billiger.de",
                url="http://www.billiger.de"
            )

        :param url: The url this link points to. Used as src attribute of the A-Tag. If present route will be ignored.
        :param route: The route this link points to. Used to look up the url for the src attribute of the A-Tag.
        :param name: The name displayed for this component.
        :param text: Alias for name.
        :param icon: The icon to be displayed in front of the text.
        :param breadcrumb: Display the link as a breadcrumb.
        :param tile: Display the link as a rectangular tile.
        :param list_element: Display the link as a bootstrap style list element.
        :param btn_link: Display the link as a bootstrap style button.
        :param new_window: Open link in new window or tab
        :param event_name: Name of an event to be triggered on click, prevents url and route from taking effect.
        :param double_click_event_name: Name of an event to be triggered on double click, prevents url and route from
                                        taking effect.
        :param selection: Tuple of integers: (selection_start, selection_end). MARK-Tag will be applied there.
        :param stop_propagation_on_click: Set to true if click event should not be propagated to parent components
        :param popover_text: If set, click on link displays this text
        :param popover_trigger: trigger for popover text
        :param context_menu: Set to context menu list of dicts or to string
        :param popover_position: popover position possible values: left right top bottom
        :param btn_link_color: the color of the link button possible values: bootstrap colors: primary default etc ...
        list of dicts example: [{'name': u"Delete", 'event': "delete", 'type': "link"},{'name': "Rename",
                               'event': "rename", 'type': "link"}]
        if string is set link component calls container compos context_menu function with context_menu as parameter
        """
        pass

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
        # check for legacy menu
        if hasattr(self, "menu"):
            if self.menu:
                return self.menu
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
