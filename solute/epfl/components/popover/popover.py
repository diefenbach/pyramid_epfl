# coding: utf-8

from solute.epfl.components.link.link import Link


class Popover(Link):
    def __init__(self, page, cid, text=None, icon=None, popover_text=None, popover_trigger=None, popover_position=None,
                 **extra_params):
        """Popover convenience component

        :param text: Alias for name.
        :param icon: The icon to be displayed in front of the text.
        :param breadcrumb: Display the link as a breadcrumb.
        :param popover_text: If set, click on link displays this text
        :param popover_trigger: trigger for popover text
        :param popover_position: popover position possible values: left right top bottom
        """

        super(Link, self).__init__(page, cid, text=text, icon=icon, popover_text=popover_text,
                                   popover_trigger=popover_trigger, popover_position=popover_position, **extra_params)
