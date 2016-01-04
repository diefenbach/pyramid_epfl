# coding: utf-8
from solute.epfl.core import epflcomponentbase


class Progress(epflcomponentbase.ComponentBase):
    """
    This component display a progress bar.

    Use it code like this:

    .. code:: python

        progress = Progress(min=0, max=100, value=70)

   """

    # core internals
    template_name = "progress/progress.html"
    compo_state = ["value", "min", "max", "color"]

    # custom compo attributes
    value = 0  #: The value of the progress bar
    min = 0  #: The min value of the progress bar
    max = 100  #: The max value of the progress bar
    color = "default"  #: color of the progress bar (can be "default", "info", "warning", "danger", "success"
    hide_value_label = False  #: Set to True if value label should not be printed

    def __init__(self, page, cid,
                 value=None,
                 min=None,
                 max=None,
                 color=None,
                 hide_value_label=None,
                 **extra_params):
        """A component that display a progress bar.

        :param value: The value of the progress bar
        :param min: The min value of the progress bar
        :param max: The max value of the progress bar
        :param color: The color of the progress bar
        :param hide_value_label: Set to True if value label should not be printed
        """
        pass
