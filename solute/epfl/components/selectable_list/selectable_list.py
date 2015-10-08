# coding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import LinkListLayout


class SelectableList(LinkListLayout):
    """
    Selectable List is a MultiSelect Component, multiple values can be selected
    """
    js_name = LinkListLayout.js_name + [('solute.epfl.components:selectable_list/static', 'selectable_list.js')]
    data_interface = {'id': None, 'text': None}

    compo_state = LinkListLayout.compo_state + ["search_text", "selected_ids", "last_selected_index"]

    #: List type extension, see :attr:`ListLayout.list_type` for details.
    list_type = LinkListLayout.list_type + ['selectable']

    search_text = None  #: search text for custom search text handling

    scroll_pos = None  #: Scrollbar position this is used to jump back to the last scroll pos after redraw
    last_selected_index = None  #: The index of the element last selected.

    selected_ids = set()  #: a set with selected component ids

    compo_js_name = 'SelectableList'

    def __init__(self, page, cid, data_interface=None, *args, **extra_params):
        """
        Selectable List is a MultiSelect Component, multiple values can be selected
        :param data_interface: data interface for child class needs id and text
        """
        super(SelectableList, self).__init__(page, cid, data_interface=data_interface, *args, **extra_params)

    @staticmethod
    def default_child_cls(*args, **kwargs):
        kwargs["event_name"] = "select"
        kwargs["double_click_event_name"] = "double_click"
        kwargs["shift_click_event_name"] = "shift_click"
        return LinkListLayout.default_child_cls(*args, **kwargs)

    def handle_select(self, selected_id=None, cid=None):
        if selected_id:
            for compo in self.components:
                if compo.id == selected_id:
                    compo.active = not compo.active
                    if compo.active:
                        self.selected_ids.add(compo.id)
                        self.last_selected_index = compo.position + self.row_offset
                    else:
                        self.selected_ids.remove(compo.id)
                    return
        if cid is None:
            cid = self.epfl_event_trace[0]
        compo = self.page.components[cid]
        compo.active = not compo.active
        if compo.active:
            self.selected_ids.add(compo.id)
            self.last_selected_index = compo.position + self.row_offset
        else:
            try:
                self.selected_ids.remove(compo.id)
            except KeyError:
                pass
        compo.redraw()

    def handle_double_click(self):
        # Overwrite me for doubleclick handling
        pass

    def handle_shift_click(self):
        if not self.last_selected_index:
            return self.handle_select()
        compo = self.page.components[self.epfl_event_trace[0]]
        current_index = compo.position + self.row_offset
        min_index = min(current_index, self.last_selected_index)
        max_index = max(current_index + 1, self.last_selected_index)
        old_row_settings = self.row_limit, self.row_offset

        self.row_offset = min_index
        self.row_limit = max_index - min_index
        self.update_children()

        for compo in self.components:
            if not compo.active:
                self.handle_select(cid=compo.cid)

        self.row_limit, self.row_offset = old_row_settings
        self.update_children(force=True)

    def get_selected(self):
        """
        This method returns a list of selected components.
        Caution: This method is only available for compatibility reasons. It should be
        considered deprecated and will probably be removed soon.
        The reason for this is that the list of selected components does not contain selected
        entries that are currently not visible in the component (for example, due to pagination)
        get_selected_ids(self) should be used for this.

        :return: a list with selected components
        """
        return [compo for compo in self.components if compo.active]

    def get_selected_ids(self):
        """
        This method returns a set of selected component ids. Compared to get_selected(self),
        this method also returns entries that have been selected but are currently not visible
        (for example, due to pagination).

        :return: a set with selected component ids.
        """
        return self.selected_ids

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        super(SelectableList, self).handle_set_row(row_offset, row_limit, row_data)
        if row_data is not None:
            if self.reset_row_offset_on_search_change and self.search_text != row_data.get("search"):
                # search parameter has been changed, move to the first page.
                self.row_offset = 0
            self.search_text = row_data.get("search")
        self.update_children()
        self.redraw()

    def update_children(self, force=False):
        result = super(SelectableList, self).update_children(force=force)
        for compo in self.components:
            if compo.id in self.selected_ids:
                compo.active = True
        return result
