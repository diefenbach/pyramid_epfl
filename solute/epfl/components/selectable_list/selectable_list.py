# coding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import LinkListLayout


class SelectableList(LinkListLayout):
    """
    Selectable List is a MultiSelect Component, multiple values can be selected
    """
    data_interface = {'id': None, 'text': None}

    compo_state = LinkListLayout.compo_state + ["search_text"]

    #: List type extension, see :attr:`ListLayout.list_type` for details.
    list_type = LinkListLayout.list_type + ['selectable']
    event_name = 'select'  #: Default event to be triggered on clicks.

    search_text = None  #: search text for custom search text handling

    scroll_pos = None  #: Scrollbar position this is used to jump back to the last scroll pos after redraw

    def __init__(self, page, cid, data_interface=None, *args, **extra_params):
        """
        Selectable List is a MultiSelect Component, multiple values can be selected
        :param data_interface: data interface for child class needs id and text
        """
        super(SelectableList, self).__init__(page, cid, data_interface=data_interface, *args, **extra_params)

    @staticmethod
    def default_child_cls(*args, **kwargs):
        kwargs["double_click_event_name"] = "double_click"
        return LinkListLayout.default_child_cls(*args, **kwargs)

    def handle_select(self):
        cid = getattr(self.page, self.epfl_event_trace[0]).cid
        self.page.components[cid].active = not self.page.components[cid].active
        self.page.components[cid].redraw()

    def handle_double_click(self):
        # Overwrite me for doubleclick handling
        pass

    def get_selected(self):
        """
        :return: a list with selected compontents
        """
        return [compo for compo in self.components if compo.active]

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        super(SelectableList, self).handle_set_row(row_offset, row_limit, row_data)
        if row_data is not None:
            self.search_text = row_data.get("search")
        self.update_children()
        self.redraw()
