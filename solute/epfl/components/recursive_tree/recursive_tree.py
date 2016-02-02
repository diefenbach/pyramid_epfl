from solute.epfl.core import epflcomponentbase


class RecursiveTree(epflcomponentbase.ComponentContainerBase):

    # core internals
    asset_spec = 'solute.epfl.components:recursive_tree/static'
    theme_path = ['recursive_tree/theme']
    js_name = ['recursive_tree.js']
    css_name = ['recursive_tree.css']
    compo_state = epflcomponentbase.ComponentContainerBase.compo_state + [
        'icon_open', 'icon_close', 'label', 'get_data', 'show_children', 'data_interface', 'scroll_position',
        'default_child_cls', 'show_id'
    ]

    # js settings
    compo_js_auto_parts = True
    compo_js_params = ['scroll_position']
    compo_js_name = 'RecursiveTree'

    # derived attribute overrides
    data_interface = {'id': None, 'label': None, 'icon_open': None, 'icon_close': None}

    # custom compo attributes
    icon_open = None  #: Icon displayed when children are shown.
    icon_close = None  #: Icon displayed when children are hidden.
    label = None  #: Text to be shown as label of this node.
    #: Normally set by the get_data/update_children mechanism this is present to make a safe None check against it.
    id = None
    show_children = False  #: Toggle whether the child components are currently visible or not.
    scroll_position = None  #: Position in pixels the component will scroll to on loading.
    show_id = False  #: show the id in tree leaf

    def __init__(self, page, cid,
                 node_list=None,
                 data_interface=None,
                 get_data=None,
                 default_child_cls=None,
                 icon_open=None,
                 icon_close=None,
                 label=None,
                 id=None,
                 show_children=None,
                 scroll_position=None,
                 show_id=None,
                 **kwargs):
        """Simple tree component.

        :param node_list: List of child components.
        :param data_interface: Data interface to translate the results from get_data polling. If a list is given it will
                               be used for the according levels given in the get_data list. Else this is used on all
                               children.
        :param get_data: List of get_data sources. First entry is used for first level, second for second, and so on.
        :param default_child_cls: Default component to be used to initialize children.
        :param icon_open: Icon displayed when children are shown.
        :param icon_close: Icon displayed when children are hidden.
        :param label: Text to be shown as label of this node.
        :param id: Normally set by the get_data/update_children mechanism this is present to make a safe None check
                   against it.
        :param show_children: Load and show any potential children that would be returned by polling get_data.
        :param scroll_position: Position in pixels the component will scroll to on loading.
        :param show_id: show the id in tree leaf
        """
        pass

    def init_struct(self):
        if self.default_child_cls is None:
            self.default_child_cls = self.__unbound_component__(cid=None)
        if type(self.get_data) is list:
            data = self.get_data[:]
            self.get_data = data.pop(0)
            if len(data) > 0:
                if type(self.data_interface) is list:
                    data_interface = self.data_interface[:]
                    self.data_interface = data_interface.pop(0)
                    if len(data_interface) == 1:
                        data_interface = data_interface[0]
                    self.default_child_cls = self.default_child_cls(get_data=data, data_interface=data_interface)
                else:
                    self.default_child_cls = self.default_child_cls(get_data=data)

    def handle_click_label(self):
        pass

    def handle_click_icon(self):
        self.show_children = not self.show_children

    def _get_data(self, *args, **kwargs):
        if self.show_children:
            return super(RecursiveTree, self)._get_data(*args, **kwargs)
        return []

    def handle_scroll(self,scroll_pos):
        self.scroll_position = scroll_pos
