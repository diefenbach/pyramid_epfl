# coding: utf-8

"""

"""

from solute.epfl.components import Box


class ModalBox(Box):
    """
    A box that is displayed as a modal component, rendered as a layover on the page.

    You can use this component in two ways: Creating it directly when you need it (preferred),
    or create it initially and set it to visible if needed (not recommended, since use of visible() should
    be avoided).

    For the first, recommended way, create the modal box as follows:

    .. code:: python

        self.add_component(
            ModalBox(
                cid = "my_modal_box",
                node_list = [
                    Text(value="A modal box")
                ]
            )
        )

    The component is deleted when the user closes it.

    If you want to create a box that is not deleted on dismissal, but hidden only, create it as follows:

    .. code:: python

        self.add_component(
            ModalBox(
                cid = "my_modal_box",
                visible = False,
                hover_box_remove_on_close = False,
                node_list = [
                    Text(value="A modal box")
                ]
            )
        )
        self.page.components["my_modal_box"].open()

    In this case, the box is not deleted on dismissal, but the handle_hide() event is triggered.

    """

    # derived attribute overrides
    hover_box = True  #: see :attr:`Box.hover_box`
    auto_visibility = False  #: see :attr:`Box.hover_box`
    is_removable = True  #: see :attr:`Box.hover_box`
    hover_box_remove_on_close = True  #: see :attr:`Box.hover_box`
    hover_box_close_on_outside_click = True  #: see :attr:`Box.hover_box`

    # custom compo attributes

    #: Used to specify the width of the modal. The width is given in percentage of the full page width.
    hover_box_width = 50

    def __init__(self, page, cid,
                 title=None,
                 auto_visibility=None,
                 hover_box=None,
                 hover_box_remove_on_close=None,
                 hover_box_close_on_outside_click=None,
                 box_shown=None,
                 show_title=None,
                 is_removable=None,
                 is_refreshable=None,
                 read_only=None,
                 hover_box_width=None,
                 **extra_params):
        """
        A box that is displayed as a modal box as an overlay in the center of the screen.

        :param title: The title of the box will be shown on top of the container in its headbar.
        :param auto_visibility: Defaulting to true any component with this set to true will be only visible if it
         contains visible child components.
        :param hover_box: If set to true the box will be hovering in the center of the screen with everything else being
         forced into the background by a transparent gray overlay.
        :param hover_box_remove_on_close: Defaulting to true any hover box will be removed when clicking the X, else it
         will be set hidden.
        :param hover_box_close_on_outside_click: Defaulting to true any hover box will be closed when clicking outside
         of the box.
        :param box_shown: Defaulting to true the border around the box will only be visible if this is true.
        :param show_title: Defaulting to true the title will only be shown if this is true.
        :param is_removable: Defaulting to false the box will only show its removal button if this is true.
        :param is_refreshable: Defaulting to false the box will only show its refresh button if this is true.
        :param read_only: If readonly is true an overly will be shown over the whole container and prevent inputs
        :param hover_box_width: The width of the modal box given in percentage of the full page width
        """
        pass

    def open(self):
        """
        Open and display the modal box.
        """
        self.set_visible()
        self.redraw()
