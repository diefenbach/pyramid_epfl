# coding: utf-8

from solute.epfl.components.link.link import Link


class Popover(Link):

    exempt_params = set(['list_element', 'selection', 'double_click_event_name', 'name', 'url', 'route',
                         'btn_link', 'breadcrumb', 'new_window', 'tile', 'btn_link_color', 'event_name',
                         'stop_propagation_on_click', 'context_menu', 'layout_vertical', 'compo_col', 'label_col',
                         'label', 'label_style', 'btn_disabled', 'popover_max_width'])

    def __init__(self, page, cid,
                 text=None,
                 icon=None,
                 popover_text=None,
                 popover_trigger=None,
                 popover_position=None,
                 popover_max_width=None,
                 **extra_params):
        """Popover convenience component

        :param text: Alias for name.
        :param icon: The icon to be displayed in front of the text.
        :param breadcrumb: Display the link as a breadcrumb.
        :param popover_text: If set, click on link displays this text
        :param popover_trigger: trigger for popover text
        :param popover_position: popover position possible values: left right top bottom
        :param popover_max_width: popover max width as number
        """
        pass
