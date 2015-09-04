from solute.epfl.core import epflcomponentbase


class Popover(epflcomponentbase.ComponentBase):

    """
    Popover dialog (a click triggered tooltip) using bootstrap popover.
    The popover dialog is displayed when clicking a button.

    Example: http://getbootstrap.com/javascript/#popovers

    """

    template_name = "popover/popover.html"

    js_parts = epflcomponentbase.ComponentBase.js_parts + ["popover/popover.js"]
    asset_spec = "solute.epfl.components:popover/static"

    css_name = ["popover.css"]
    js_name = ["popover.js"]

    compo_config = []
    compo_state = ["disabled", "text", "title", "position", "label", "icon", "color"]

    #: Text to be displayed in the popover. Can be either a string or a list of strings.
    #: In the latter case, the strings are displayed in separate paragraphs.
    text = ""
    title = None  #: title to be displayed in the popover. If set to None, no title is displayed.
    position = "top"  #: possible positions are top, left, right, bottom
    #: An optional font-awesome icon that should be displayed on the button.
    #: Either the :attr:`icon` or the :attr:`label` have to be defined in order
    #: to yield a reasonable button.
    icon = None
    #: An optional label that should be displayed on the button.
    #: Either the :attr:`icon` or the :attr:`label` have to be defined in order
    #: to yield a reasonable button.
    label = None
    disabled = None  #: Set to true if button should be disabled.
    #: The color class to be used for the button. Possible values are: default, primary, warning, danger, success.
    color = "default"
    small_button = False  #: Set to true if a small button should be rendered.
    trigger = "focus"  #: Set how the popover is triggerd. possible values: click (default), hover, focus

    def __init__(self, page, cid,
                 label=None,
                 icon=None,
                 text=None,
                 title=None,
                 position="top",
                 color="default",
                 disabled=False,
                 small_button=False,
                 trigger=None,
                 **extra_params):
        """
        Popover Component

        :param label: An optional label that should be displayed on the button
        :param icon: An optional font-awesome icon that should be displayed on the button
        :param text: The text to display in the popover. Can be either a string or a list of strings. In the latter case, the strings are displayed in separate paragraphs
        :param title: An optional title to display in the popover
        :param position: The position of the popover (possible values are top, left, right, bottom)
        :param color: The color class to be used for the button
        :param disabled: Set to true if button should be disabled
        :param small_button: Set to true if a small button should be rendered
        :param trigger: Set how the popover is triggered. possible values: click (default), hover, focus

        """
        super(Popover, self).__init__(page, cid,
                                      label=label,
                                      icon=icon,
                                      text=text,
                                      title=title,
                                      position=position,
                                      color=color,
                                      disabled=disabled,
                                      small_button=small_button,
                                      trigger=trigger)

