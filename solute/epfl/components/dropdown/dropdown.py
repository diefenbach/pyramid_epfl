# coding: utf-8
from solute.epfl.core import epflcomponentbase


class Dropdown(epflcomponentbase.ComponentBase):

    # core internals
    template_name = "dropdown/dropdown.html"
    asset_spec = "solute.epfl.components:dropdown/static"
    js_name = ["dropdown.js"]
    compo_state = epflcomponentbase.ComponentBase.compo_state + ['children']

    # js settings
    new_style_compo = True
    compo_js_name = 'Dropdown'

    # custom compo attributes
    small_button = True  #: Use a small button for the dropdown menu.
    caret = False  #: Show a caret indicator on the dropdown menu button.
    #: The label of the dropdown menu button. Optional, if a :attr:`menu_icon` is provided.
    menu_label = None
    #: Optional font-awesome icon to be rendered as menu_label. If both :attr:`menu_icon` and :attr:`menu_label` are
    #: provided, the icon is rendered before the label.
    menu_icon = None

    #: List of dicts of children to show in this component. Must have a key and a label item.
    children = None

    def __init__(self, page, cid,
                 small_button=None,
                 caret=None,
                 menu_label=None,
                 menu_icon=None,
                 children=None,
                 **extra_params):
        """An advanced dropdown.

        :param small_button: Use a small button for the dropdown menu.
        :param menu_label: The label of the dropdown menu button. Optional, if a :attr:`menu_icon` is provided.
        :param menu_icon: Optional font-awesome icon to be rendered as menu_label. If both :attr:`menu_icon` and
                          :attr:`menu_label` are provided, the icon is rendered before the label.
        :param caret: Show a caret indicator on the dropdown menu button.
        :param children: List of dicts of children to show in this component. Must have a key and a label item.
        """
        pass
