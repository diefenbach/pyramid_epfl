from solute.epfl.components.link.link import Link


class Popover(Link):
    """
    Popover dialog (a click triggered tooltip) using bootstrap popover.
    The popover dialog is displayed when clicking a button.

    Example: http://getbootstrap.com/javascript/#popovers

    """
    compo_state = Link.compo_state + ["title", "position", "color", "small_button", "trigger"]

    title = None  #: title to be displayed in the popover. If set to None, no title is displayed.
    position = "top"  #: possible positions are top, left, right, bottom
    small_button = False  #: Set to true if a small button should be rendered.
    trigger = "focus"  #: Set how the popover is triggerd. possible values: click (default), hover, focus
    #: The color class to be used for the button. Possible values are: default, primary, warning, danger, success.
    color = "default"

    def __init__(self, page, cid,
                 icon=None,
                 text=None,
                 title=None,
                 position="top",
                 color="default",
                 small_button=False,
                 trigger=None,
                 **extra_params):
        """
        Popover Component

        :param icon: An optional font-awesome icon that should be displayed on the button
        :param text: The text to display in the popover. Can be either a string or a list of strings. In the latter case, the strings are displayed in separate paragraphs
        :param title: An optional title to display in the popover
        :param position: The position of the popover (possible values are top, left, right, bottom)
        :param color: The color class to be used for the button
        :param small_button: Set to true if a small button should be rendered
        :param trigger: Set how the popover is triggered. possible values: click (default), hover, focus

        """
        super(Popover, self).__init__(page, cid,
                                      icon=icon,
                                      text=text,
                                      title=title,
                                      position=position,
                                      color=color,
                                      trigger=trigger)

    def init_transaction(self):
        super(Popover, self).init_transaction()
        if self.icon is not None:
            if self.icon.startswith("fa-"):
                raise DeprecationWarning("icon starting with fa- is deprecated")

        self.btn_link = self.small_button
        self.popover_position = self.position
        self.popover_title = self.title
        self.popover_trigger = self.trigger
        self.btn_link_color = self.color
