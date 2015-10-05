from solute.epfl.components import PaginatedListLayout
from collections2.dicts import OrderedDict


class TableLayout(PaginatedListLayout):
    js_parts = []
    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:table_layout/static',
                                              'table_layout.js'),
                                             ('solute.epfl.components:table_layout/static',
                                              'jquery.fixedheadertable.min.js')]
    css_name = PaginatedListLayout.css_name + \
        [("solute.epfl.components:table_layout/static", "css/table_layout.css")]

    template_name = 'table_layout/table_layout.html'

    compo_state = PaginatedListLayout.compo_state + ['column_visibility', 'orderby', 'ordertype', 'row_colors']

    #: Used to map specific fields to child classes.
    map_child_cls = {}
    fixed_header = True  #: Set to False if header should not be fixed.
    #: Can be set to a tuple where each entry contains True/False denoting the visibility of the corresponding column
    column_visibility = None

    orderby = None  #: An optional string denoting which column should be initially used for sorting.
    ordertype = None  #: An optional string denoting the initial sort order.

    row_colors = None  #: This is a simple row_id to row color mapping example: {1:ROW_DANGER,2:ROW_SUCCESS}

    ROW_DEFAULT = "row-default"  #: Row color constant
    ROW_PRIMARY = "row-primary"  #: Row color constant
    ROW_SUCCESS = "row-success"  #: Row color constant
    ROW_INFO = "row-info"  #: Row color constant
    ROW_WARNING = "row-warning"  #: Row color constant
    ROW_DANGER = "row-danger"  #: Row color constant

    new_style_compo = True
    compo_js_name = 'TableLayout'
    compo_js_params = ['row_offset', 'row_limit', 'row_count', 'row_data',
                       'show_pagination', 'show_search', 'search_focus', 'fixed_header']
    compo_js_extras = ['handle_click']

    def __init__(self, page, cid, show_search=None, height=None, column_visibility=None, orderby=None, ordertype=None,
                 row_colors=None, **kwargs):
        """Table based on a paginated list. Offers searchbar above and pagination below using the EPFL theming
        mechanism.

        components.TableLayout(
            get_data='objects',
            show_search=False,
            headings=[
                {'title': 'Name'},
                {'title': 'Wert', 'name': 'value', 'sortable': True},
                {'title': 'Einheit', 'toggle_visibility_supported': True },
            ],
            map_child_cls=[
                ('name', components.Text, {'value': 'name'}),
                ('value', components.Text, {'value': 'value'}),
                ('unit', components.Text, {'value': 'unit'}),
            ],
            data_interface={
                'id': None,
                'name': None,
                'value': None,
                'unit': None,
            }
        )

        :param height: Set the table to the given height in pixels.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        :param column_visibility: An optional tuple denoting which columns should be initially displayed or not.
                                  If set, its length has to match the length of table columns.
        :param orderby: An optional string denoting which column should be initially used for sorting.
        :param ordertype: An optional string denoting the initial sort order.
        :param row_colors: This is a simple row_id to row color mapping example: {1:ROW_DANGER,2:ROW_SUCCESS}
        """
        super(PaginatedListLayout, self).__init__(
            page, cid, show_search=None, height=height, column_visibility=column_visibility, row_colors=row_colors,
            orderby=orderby, ordertype=ordertype, **kwargs)

    def setup_component(self):
        PaginatedListLayout.setup_component(self)
        if (self.column_visibility is not None) and (type(self.column_visibility) is not tuple):
            raise Exception("TableLayout column_visibility attribute has to be of type tuple!")

    def default_child_cls(self, **compo_info):
        return self.map_child_cls[compo_info['compo_type']][1](**compo_info)

    def _get_data(self, *args, **kwargs):
        result = super(TableLayout, self)._get_data(*args, **kwargs)
        out = []
        child_maps = list(enumerate(self.map_child_cls))
        for row in result:
            for i, child_map in child_maps:
                if len(child_map) == 3:
                    key, cls, interface = child_map
                else:
                    key, cls = child_map
                    interface = {}

                data = {'row': row,
                        'key': key,
                        'compo_type': i,
                        'id': "%s_%s" % (row['id'], i)}

                for key, value in interface.items():
                    data[key] = row[value]

                out.append(data)

        return out

    @property
    def slotted_components(self):
        slotted_components = OrderedDict()
        for compo in self.components:
            slotted_components.setdefault(compo.row['id'], []).append(compo)
        return slotted_components

    def handle_show_column(self, column_index):
        col_visibility = self.column_visibility
        if col_visibility is None and not hasattr(self, 'headings'):
            return
        if col_visibility is None:
            col_visibility = tuple([True for x in range(0, len(self.headings))])
        col_visibility = col_visibility[:column_index] + (True,) + col_visibility[column_index + 1:]
        self.column_visibility = col_visibility
        self.redraw()

    def handle_hide_column(self, column_index):
        col_visibility = self.column_visibility
        if col_visibility is None and not hasattr(self, 'headings'):
            return
        if col_visibility is None:
            col_visibility = tuple([True for x in range(0, len(self.headings))])
        col_visibility = col_visibility[:column_index] + \
            (False,) + col_visibility[column_index + 1:]
        self.column_visibility = col_visibility
        self.redraw()

    def handle_adjust_sorting(self, column_index):
        if self.orderby == self.headings[column_index]['name']:
            # Change sorting
            if self.ordertype == 'asc':
                self.ordertype = 'desc'
            else:
                self.ordertype = 'asc'
        else:
            self.orderby = self.headings[column_index]['name']
            self.ordertype = 'asc'
        self.row_data.update({'orderby': self.orderby})
        self.row_data.update({'ordertype': self.ordertype})
        self.redraw()

    def export_csv(self):
        csv_string = ''
        result = super(TableLayout, self)._get_data(0, self.row_count, self.row_data, {})
        for key in result[0].keys():
            csv_string = '%s%s;' % (csv_string, key)
        csv_string = '%s\n' % csv_string
        for row in result:
            for value in row.values():
                csv_string = '%s%s;' % (csv_string, value)
            csv_string = '%s\n' % csv_string
        return csv_string

    def handle_export_csv(self):
        csv = self.export_csv()
        self.return_ajax_response([csv, 'table_data.csv'])
