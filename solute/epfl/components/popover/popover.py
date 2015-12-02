# coding: utf-8

from solute.epfl.components.link.link import Link


class Popover(Link):
    text = None  #: Alias for name.
    icon = None  #: The icon to be displayed in front of the text.
    popover_text = None  #: If set, click on link displays this text
    popover_trigger = "focus"  #: trigger for popover text
    popover_position = "top"  #: popover position possible values: left right top bottom
    popover_title = None  #: popover title

    def __init__(self, page, cid, text=None, icon=None, popover_text=None, popover_trigger=None, popover_position=None,
                 popover_title=None, **extra_params):
        """Popover convenience component

        :param text: Alias for name.
        :param icon: The icon to be displayed in front of the text.
        :param breadcrumb: Display the link as a breadcrumb.
        :param popover_text: If set, click on link displays this text
        :param popover_trigger: trigger for popover text
        :param popover_position: popover position possible values: left right top bottom
        :param popover_title: popover title
        """

        super(Link, self).__init__(page, cid, text=text, icon=icon, popover_text=popover_text,
                                   popover_trigger=popover_trigger, popover_position=popover_position,
                                   popover_title=popover_title, **extra_params)
