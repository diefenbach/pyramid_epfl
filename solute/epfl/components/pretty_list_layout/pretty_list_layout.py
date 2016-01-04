# coding: utf-8

"""

"""

from solute.epfl.components import ListLayout


class PrettyListLayout(ListLayout):

    asset_spec = "solute.epfl.components:pretty_list_layout/static"
    theme_path = ListLayout.theme_path + ["pretty_list_layout/theme"]

    #: The max height of the list view. If the entries exceed the height, a scrollbar is displayed.
    height = None
    hide_list = False  #: Hides the list container but nothing else.
    #: Add the specific list type for the pretty list layout. see :attr:`ListLayout.list_type`
    list_type = ListLayout.list_type + ['pretty']

    css_name = ListLayout.css_name + \
        [("solute.epfl.components:pretty_list_layout/static", "pretty_list_layout.css")]

    new_style_compo = True
    compo_js_name = 'PrettyListLayout'

    def __init__(self, page, cid, height=None, **kwargs):
        """ContainerComponent using Bootstrap to prettify the output like a list.

        :param height: Set the list to the given height in pixels.
        """
        super(PrettyListLayout, self).__init__(page, cid, height=height, **kwargs)
