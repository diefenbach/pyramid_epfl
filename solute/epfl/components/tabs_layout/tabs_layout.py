from solute.epfl.core import epflcomponentbase


class TabsLayout(epflcomponentbase.ComponentContainerBase):

    # core internals
    template_name = "tabs_layout/tabs_layout.html"
    asset_spec = "solute.epfl.components:tabs_layout/static"
    compo_state = ["active_tab_cid"]
    js_name = ["tabs_layout.js"]

    # js settings
    new_style_compo = True
    compo_js_name = 'TabsLayout'

    # custom compo attributes
    active_tab_cid = ""  #: CID of the currently active tab.

    def __init__(self, page, cid,
                 node_list=None,
                 active_tab_cid=None,
                 **extra_params):
        """A Layouting component displaying its children inside separate tabs.

        :param node_list: List of child components.
        :param active_tab_cid: CID of the currently active tab.
        """
        pass

    def render(self, target='main'):
        """Just before the normal rendering the visibility of all child components needs to be updated.
        """
        for i, compo in enumerate(self.components):
            if self.is_active_tab(i + 1, compo):
                compo.set_visible()
            else:
                compo.set_hidden()

        return super(TabsLayout, self).render(target=target)

    def handle_toggle_tab(self, selected_compo_cid):
        if self.active_tab_cid != selected_compo_cid:
            self.redraw()
        self.active_tab_cid = selected_compo_cid
        self.add_js_response("$('#%s_tabmenuentry').tab('show');" % self.active_tab_cid)

    def del_component(self, cid, slot=None):
        # In case the deleted component was the active tab the active_tab_cid attribute is reset to an empty string.
        if cid == self.active_tab_cid:
            self.active_tab_cid = ''
        super(TabsLayout, self).del_component(cid, slot)

    def is_active_tab(self, loop, compo_obj):
        """Check whether the component is the currently active tab or the first tab if no cid has been set as active.
        """
        if type(loop) is not int:
            loop = loop.index
        return (self.active_tab_cid == "" and loop == 1) or (self.active_tab_cid == compo_obj.cid)
