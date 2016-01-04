# coding: utf-8

"""

"""
from solute.epfl.core import epflcomponentbase


class Dropdown(epflcomponentbase.ComponentBase):

    asset_spec = "solute.epfl.components:dropdown/static"

    js_name = ["dropdown.js"]
    compo_state = epflcomponentbase.ComponentBase.compo_state + ['children']

    template_name = "dropdown/dropdown.html"

    small_button = True  #: Use a small button for the dropdown menu.
    caret = False  #: Show a caret indicator on the dropdown menu button.
    #: The label of the dropdown menu button. Optional, if a :attr:`menu_icon` is provided.
    menu_label = None
    #: Optional font-awesome icon to be rendered as menu_label. If both :attr:`menu_icon` and :attr:`menu_label` are
    #: provided, the icon is rendered before the label.
    menu_icon = None

    #: List of dicts of children to show in this component. Must have a key and a label item.
    children = None

    new_style_compo = True
    compo_js_name = 'Dropdown'

    def __init__(self, page, cid, children=None, small_button=None, menu_label=None, menu_icon=None, caret=None,
                 **extra_params):
        """An advanced dropdown.

        :param children: List of dicts of children to show in this component. Must have a key and a label item.
        :param small_button: Use a small button for the dropdown menu.
        :param menu_label: The label of the dropdown menu button. Optional, if a :attr:`menu_icon` is provided.
        :param menu_icon: Optional font-awesome icon to be rendered as menu_label. If both :attr:`menu_icon` and
                          :attr:`menu_label` are provided, the icon is rendered before the label.
        :param caret: Show a caret indicator on the dropdown menu button.
        """
        super(Dropdown, self).__init__(page, cid, children=children, small_button=small_button, menu_label=menu_label,
                                       menu_icon=menu_icon, caret=caret, **extra_params)
