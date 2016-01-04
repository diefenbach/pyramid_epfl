# coding: utf-8
from solute.epfl.components import ListLayout


class PrettyListLayout(ListLayout):

    # core internals
    asset_spec = "solute.epfl.components:pretty_list_layout/static"
    theme_path = ListLayout.theme_path + ["pretty_list_layout/theme"]
    css_name = ListLayout.css_name + \
        [("solute.epfl.components:pretty_list_layout/static", "pretty_list_layout.css")]

    # custom compo attributes

    #: The max height of the list view. If the entries exceed the height, a scrollbar is displayed.
    height = None
    hide_list = False  #: Hides the list container but nothing else.

    # derived attribute overrides

    #: Add the specific list type for the pretty list layout. see :attr:`ListLayout.list_type`
    list_type = ListLayout.list_type + ['pretty']

    def __init__(self, page, cid,
                 node_list=None,
                 height=None,
                 **extra_params):
        """ContainerComponent using Bootstrap to prettify the output like a list.

        :param node_list: List of child components.
        :param height: Set the list to the given height in pixels.
        :param hide_list: Hide the list container but nothing else.
        """
        pass
