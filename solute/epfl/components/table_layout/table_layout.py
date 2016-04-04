# -*- coding: utf-8 -*-

from solute.epfl.components import PaginatedListLayout
from collections2.dicts import OrderedDict

import csv
from StringIO import StringIO


class TableLayout(PaginatedListLayout):

    # core internals
    template_name = 'table_layout/table_layout.html'
    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:table_layout/static',
                                              'table_layout.js'),
                                             ('solute.epfl.components:table_layout/static',
                                              'jquery.fixedheadertable.min.js'),
                                             ('solute.epfl.components:table_layout/static',
                                              'FileSaver.min.js')]
    css_name = PaginatedListLayout.css_name + \
        [("solute.epfl.components:table_layout/static", "css/table_layout.css")]
    compo_state = PaginatedListLayout.compo_state + ['column_visibility', 'orderby', 'ordertype', 'row_colors']

    # js settings
    compo_js_name = 'TableLayout'
    compo_js_params = PaginatedListLayout.compo_js_params + ['fixed_header']
    compo_js_extras = ['handle_click']

    # custom compo settings
    ROW_DEFAULT = "row-default"  #: Row color constant
    ROW_PRIMARY = "row-primary"  #: Row color constant
    ROW_SUCCESS = "row-success"  #: Row color constant
    ROW_INFO = "row-info"  #: Row color constant
    ROW_WARNING = "row-warning"  #: Row color constant
    ROW_DANGER = "row-danger"  #: Row color constant

    # custom compo attributes
    map_child_cls = {}  #: Used to map specific fields to child classes.
    fixed_header = True  #: Set to False if header should not be fixed.
    #: Can be set to a tuple where each entry contains True/False denoting the visibility of the corresponding column
    column_visibility = None
    #: Set to true to show a export-button which will automatically export the tables data as .csv-file.
    show_export = False
    orderby = None  #: An optional string denoting which column should be initially used for sorting.
    ordertype = None  #: An optional string denoting the initial sort order.
    row_colors = None  #: This is a simple row_id to row color mapping example: {1:ROW_DANGER,2:ROW_SUCCESS}

    def __init__(self, page, cid,
                 node_list=None,
                 height=None,
                 hide_list=None,
                 show_search=None,
                 show_pagination=None,
                 search_placeholder=None,
                 search_focus=None,
                 visible_pages_limit=None,
                 reset_row_offset_on_search_change=None,
                 search_focus_after_search=None,
                 search_timeout=None,
                 infinite_scroll_debounce_delay=None,
                 show_row_count=None,
                 show_page_count=None,
                 map_child_cls=None,
                 fixed_header=None,
                 column_visibility=None,
                 show_export=None,
                 orderby=None,
                 ordertype=None,
                 row_colors=None,
                 **kwargs):
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

        :param node_list: List of child components.
        :param height: Set the list to the given height in pixels.
        :param hide_list: Hide the list container but nothing else.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_placeholder: The placeholder text for the search input.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        :param visible_pages_limit: Specify the number of pages that should be visible in the pagination bar.
        :param reset_row_offset_on_search_change: Reset row_offset once the user changes the search string.
        :param search_focus_after_search: Focus the search input after a search
        :param search_timeout: The timeout in ms until the search event fires
        :param infinite_scroll_debounce_delay: The delay for scroll debounce in infinite scrolling lists
        :param map_child_cls: Used to map specific fields to child classes.
        :param show_row_count: Show the row count in the pagination bar (depends on show_pagination=True)
        :param show_page_count: Show the page count in the pagination bar (depends on show_pagination=True)
        :param fixed_header: Set to False if header should not be fixed.
        :param column_visibility: An optional tuple denoting which columns should be initially displayed or not.
                                  If set, its length has to match the length of table columns.
        :param show_export: Set to true to show a export-button which will export the table data as .csv-file.
        :param orderby: An optional string denoting which column should be initially used for sorting.
        :param ordertype: An optional string denoting the initial sort order.
        :param row_colors: This is a simple row_id to row color mapping example: {1:ROW_DANGER,2:ROW_SUCCESS}
        """
        pass

    def setup_component(self):
        PaginatedListLayout.setup_component(self)
        if (self.column_visibility is not None) and (type(self.column_visibility) is not tuple):
            raise Exception("TableLayout column_visibility attribute has to be of type tuple!")

    def default_child_cls(self, **compo_info):
        return self.map_child_cls[compo_info['compo_type']][1](**compo_info)

    def _get_data(self, *args, **kwargs):
        as_raw = kwargs.get('raw', False)
        if 'raw' in kwargs:
            del(kwargs['raw'])

        result = super(TableLayout, self)._get_data(*args, **kwargs)
        # used for exort
        if as_raw:
            return result

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
        def safe_encode(value):
            """ A value encoder: take a value of any kind and return it as encoded utf-8 string. """
            if type(value) is not str and type(value) is not unicode:
                value = str(value)  # for ints
            if type(value) is not unicode:
                value = value.decode('utf-8')
            return value.encode('utf-8')

        result = self._get_data(0, max(self.row_count, self.row_limit), self.row_data, raw=True)
        csvfile = StringIO()

        headings = getattr(self, 'headings', [])
        fieldnames = [safe_encode(heading['name']) for heading in headings
                      if heading.get('export_value', None) is not None]
        export_values = [heading['export_value'] for heading in headings
                         if heading.get('export_value', None) is not None]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for row in result:
            writer.writerow({fieldnames[i]: safe_encode(row[value]) for i, value in enumerate(export_values)})

        csvfile.seek(0)

        csvcontent = csvfile.read()
        return csvcontent.decode('utf-8')

    def handle_export_csv(self):
        # check export_max_rows setting to avoid long running exports
        if self.export_max_rows is not None and self.export_max_rows < self.row_count:
            self.return_ajax_response(
                ['msg',
                 'warning',
                 u'Es können nur maximal {max} Datensätze exportiert werden'.format(max=self.export_max_rows)]
            )
        else:
            self.return_ajax_response(['csv', self.export_csv(), 'table_data.csv'])
