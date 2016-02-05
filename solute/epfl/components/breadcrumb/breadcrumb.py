# coding: utf-8

from solute.epfl.components.link.link import Link


class Breadcrumb(Link):

    # core internals
    template_name = "breadcrumb/breadcrumb.html"

    exempt_params = set(['list_element', 'selection', 'double_click_event_name', 'context_menu',
                         'popover_position', 'event_name', 'text', 'btn_link', 'breadcrumb', 'new_window',
                         'popover_trigger', 'tile', 'btn_link_color', 'popover_text', 'stop_propagation_on_click',
                         'layout_vertical', 'compo_col', 'label_col', 'label', 'label_style', 'btn_disabled'])

    # custom compo attributes
    breadcrumb = True  #: The link is used as a breadcrumb per default.
    slot = 'left'

    def __init__(self, page, cid,
                 url=None,
                 route=None,
                 name=None,
                 icon=None,
                 **extra_params):
        """Convenience component that can be used for creating breadcrumbs.

        Usage:
        .. code-block:: python

            self.page.breadcrumbs.add_component(
                components.Breadcrump(
                    name='Home',
                    url='/',
                    slot='left'
                )
            )

        :param url: The url this link points to. Used as src attribute of the A-Tag. If present route will be ignored.
        :param route: The route this link points to. Used to look up the url for the src attribute of the A-Tag.
        :param name: The name displayed for this component.
        :param icon: The icon to be displayed in front of the text.
        """
        pass
