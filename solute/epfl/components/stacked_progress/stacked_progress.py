# * encoding: utf-8
from solute.epfl.core import epflcomponentbase


class StackedProgress(epflcomponentbase.ComponentBase):
    """
    This component display a stacked progress bar. Each progress bar has to be defined as a tuple (width, color), where
    width is a percentage width (full width is 100%)
    and color is a bootstrap progress bar class (e.g. "progress-bar-success", "progress-bar-warning progress-bar-striped"

    Use it code like this:

    .. code:: python

        progress = StackedProgress(value=[(20, "progress-bar-success"), (30, "progress-bar-warning progress-bar-striped")])

    """
    template_name = "stacked_progress/stacked_progress.html"

    compo_state = ["value"]

    value = []  #: A list if tuples defining the stacked progress bars

    def __init__(self, page, cid, value=None, **extra_params):
        """A component that display a stacked progress bar.

        :param value: The value of the progress bar
        """
        super(StackedProgress, self).__init__(page, cid, value=value, **extra_params)

