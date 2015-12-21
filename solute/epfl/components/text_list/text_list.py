# coding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout


class TextList(PaginatedListLayout):
    """
    Text List is simple list which displays text
    """
    default_child_cls = epflcomponentbase.ComponentBase
    data_interface = {'id': None,
                      'text': None}

    theme_path = {'default': PaginatedListLayout.theme_path,
                  'row': ['text_list/theme'],
                  'container': ['text_list/theme']}

    compo_state = PaginatedListLayout.compo_state + ["search_text"]
    js_name = PaginatedListLayout.js_name + [(
        'solute.epfl.components:text_list/static',
        'text_list.js')]
    search_text = None  #: The search string written by the user.
    new_style_compo = True
    compo_js_name = 'TextList'

    def __init__(self, page, cid, data_interface=None, *args, **extra_params):
        """
        Text List is simple list which displays text
        :param data_interface: data interface for child class needs id and text
        """
        super(TextList, self).__init__(page, cid, data_interface=data_interface, *args, **extra_params)

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        import ipdb; ipdb.set_trace()
        if row_data is not None:
            if self.reset_row_offset_on_search_change and self.search_text != row_data.get("search"):
                # search parameter has been changed, move to the first page.
                self.row_offset = 0
            self.search_text = row_data.get("search")
        self.update_children()
        self.redraw()
