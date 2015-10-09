import pytest
from solute.epfl import components
import re
from lxml import etree
from solute.epfl import epflassets


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


@pytest.fixture(params=[True, False])
def bool_quad(request, bool_toggle):
    return bool_toggle, request.param


@pytest.fixture(params=[True, False])
def bool_hex(request, bool_quad):
    return bool_quad + (request.param, )


def test_title(page, bool_toggle):
    title = None
    if bool_toggle:
        title = 'test title'

    page.root_node = components.TableLayout(
        title=title
    )

    page.handle_transaction()

    if bool_toggle:
        assert '<div class="panel-heading">test title</div>' in page.root_node.render()
    else:
        assert '<div class="panel-heading">test title</div>' not in page.root_node.render()


def test_height(page, bool_quad):
    height = None
    if bool_quad[0]:
        height = 300

    page.root_node = components.TableLayout(
        height=height
    )

    page.handle_transaction()

    if bool_quad[0]:
        page.root_node.row_count = 10
        if bool_quad[1]:
            page.root_node.row_limit = 15
        else:
            page.root_node.row_limit = 5

    if bool_quad[0] and bool_quad[1]:
        assert 'style="height: 300px;"' in page.root_node.render()
        assert 'style="height: 220px;"' not in page.root_node.render()
    elif bool_quad[0] and not bool_quad[1]:
        assert 'style="height: 300px;"' in page.root_node.render()
        assert 'style="height: 220px;"' in page.root_node.render()
    else:
        assert 'style="height: 300px;"' not in page.root_node.render()
        assert 'style="height: 220px;"' not in page.root_node.render()


def test_style(page, bool_toggle):
    style = None
    if bool_toggle:
        style = 'some: style; addons: yay; '

    page.root_node = components.TableLayout(
        style=style
    )

    page.handle_transaction()

    if bool_toggle:
        assert 'style="some: style; addons: yay; "' in page.root_node.render()
    else:
        assert 'style="some: style; addons: yay; "' not in page.root_node.render()


def test_generation(page):
    page.model = ExampleModel
    page.setup_model()

    page.root_node = components.TableLayout(
        get_data='entries',
        data_interface={
            'id': None,
            'col1': None,
            'col2': None,
            'col3': None,
        },
        map_child_cls=[
            ('col1', components.Text, {'value': 'col1'}),
            ('col2', components.Text, {'value': 'col2'}),
            ('col3', components.Text, {'value': 'col3'}),
        ],
    )

    page.handle_transaction()
    root_node = page.root_node

    assert len(root_node.components) == 30 * 3  # 3 columns for 30 rows.

    root_node.render()


def test_column_visibility_exception(page):
    page.model = ExampleModel
    page.setup_model()

    page.root_node = components.TableLayout(
        column_visibility='foobar',
        get_data='entries',
        data_interface={
            'id': None,
            'col1': None,
            'col2': None,
            'col3': None,
        },
        map_child_cls=[
            ('col1', components.Text, {'value': 'col1'}),
            ('col2', components.Text, {'value': 'col2'}),
            ('col3', components.Text, {'value': 'col3'}),
            ('value', components.Text),
        ],
    )

    try:
        page.handle_transaction()
        raised = False
    except Exception as e:
        assert e.message == "TableLayout column_visibility attribute has to be of type tuple!"
        raised = True

    assert raised


class ExampleModel(epflassets.ModelBase):
    data = [
        {'id': i, 'col1': 'col1 %s' % i, 'col2': 'col2 %s' % i, 'col3': 'col3 %s' % i, 'value': 'value %s' % i, }
        for i in range(0, 30)
    ]

    def load_entries(self, *args, **kwargs):
        return self.data


def test_handle_adjust_sorting(page, bool_quad):
    page.model = ExampleModel
    page.setup_model()

    page.root_node = components.TableLayout(
        get_data='entries',
        headings=[
            {'title': 'field 1', 'name': 'col1'},
            {'title': 'field 2', 'name': 'value', 'sortable': True},
            {'title': 'field 3', 'toggle_visibility_supported': True},
            {'title': 'field 4', 'toggle_visibility_supported': True},
        ],
        data_interface={
            'id': None,
            'col1': None,
            'col2': None,
            'col3': None,
        },
        map_child_cls=[
            ('col1', components.Text, {'value': 'col1'}),
            ('col2', components.Text, {'value': 'col2'}),
            ('col3', components.Text, {'value': 'col3'}),
        ],
    )

    page.handle_transaction()

    if bool_quad[0]:
        page.root_node.orderby = page.root_node.headings[1]['name']
        if bool_quad[1]:
            page.root_node.ordertype = 'asc'
    else:
        page.root_node.orderby = page.root_node.headings[0]['name']

    page.root_node.handle_adjust_sorting(1)

    if bool_quad[0] and bool_quad[1]:
        assert page.root_node.orderby == 'value'
        assert page.root_node.ordertype == 'desc'
    elif bool_quad[0] and not bool_quad[1]:
        assert page.root_node.orderby == 'value'
        assert page.root_node.ordertype == 'asc'
    else:
        assert page.root_node.orderby == 'value'
        assert page.root_node.ordertype == 'asc'


def test_handle_show_hide_column(page, bool_hex):
    bool_quad = bool_hex[:2]
    page.model = ExampleModel
    page.setup_model()

    page.root_node = components.TableLayout(
        get_data='entries',
        data_interface={
            'id': None,
            'col1': None,
            'col2': None,
            'col3': None,
        },
        map_child_cls=[
            ('col1', components.Text, {'value': 'col1'}),
            ('col2', components.Text, {'value': 'col2'}),
            ('col3', components.Text, {'value': 'col3'}),
        ],
    )
    if bool_quad[0]:
        page.root_node = components.TableLayout(
            headings=[
                {'title': 'field 1', 'name': 'col1'},
                {'title': 'field 2', 'name': 'value', 'sortable': True},
                {'title': 'field 3', 'toggle_visibility_supported': True},
                {'title': 'field 4', 'toggle_visibility_supported': True},
            ],
            get_data='entries',
            data_interface={
                'id': None,
                'col1': None,
                'col2': None,
                'col3': None,
            },
            map_child_cls=[
                ('col1', components.Text, {'value': 'col1'}),
                ('col2', components.Text, {'value': 'col2'}),
                ('col3', components.Text, {'value': 'col3'}),
            ],
        )

    page.handle_transaction()

    table = page.root_node

    if bool_hex[2]:
        table.handle_hide_column(2)
    else:
        table.handle_show_column(2)
        table.handle_hide_column(2)

    if not bool_quad[0]:
        assert table.column_visibility is None
        return

    assert table.column_visibility == (True, True, False, True, )
    table.handle_hide_column(3)
    assert table.column_visibility == (True, True, False, False, )
    table.handle_hide_column(3)
    assert table.column_visibility == (True, True, False, False, )
    table.handle_show_column(3)
    assert table.column_visibility == (True, True, False, True, )
    table.handle_show_column(2)
    assert table.column_visibility == (True, True, True, True, )


def test_parsing_order(page):
    page.model = ExampleModel
    page.setup_model()

    page.root_node = components.TableLayout(
        get_data='entries',
        data_interface={
            'id': None,
            'col1': None,
            'col2': None,
            'col3': None,
        },
        map_child_cls=[
            ('col1', components.Text, {'value': 'col1'}),
            ('col2', components.Text, {'value': 'col2'}),
            ('col3', components.Text, {'value': 'col3'}),
        ],
    )

    page.handle_transaction()
    root_node = page.root_node

    assert len(root_node.components) == 30 * 3  # 3 columns for 30 rows.

    out = root_node.render()

    old_data_id, old_sub_id = -1, -1
    for compo in root_node.components:
        data_id, sub_id = compo.id.split('_')
        data_id, sub_id = int(data_id), int(sub_id)
        assert (data_id >= old_data_id and sub_id > old_sub_id) or data_id > old_data_id
        old_data_id, old_sub_id = data_id, sub_id


class CSVExampleModel(epflassets.ModelBase):
    data = [
        {'id': i, 'col1': 'col1 %s' % i, 'col2': 'col2 %s' % i, 'col3': 'col3 %s' % i, 'value': 'value %s' % i, }
        for i in range(0, 5)
    ]

    def load_entries(self, *args, **kwargs):
        return self.data


def test_csv_export_with_headings(page):
    page.model = CSVExampleModel
    page.setup_model()

    page.root_node = components.TableLayout(
        headings=[
            {'title': 'field 1', 'name': 'col1'},
            {'title': 'field 2', 'name': 'value', 'sortable': True},
            {'title': 'field 3', 'toggle_visibility_supported': True},
            {'title': 'field 4', 'toggle_visibility_supported': True},
        ],
        get_data='entries',
        data_interface={
            'id': None,
            'col1': None,
            'col2': None,
            'col3': None,
        },
        map_child_cls=[
            ('col1', components.Text, {'value': 'col1'}),
            ('col2', components.Text, {'value': 'col2'}),
            ('col3', components.Text, {'value': 'col3'}),
        ],
    )

    page.handle_transaction()
    root_node = page.root_node
    csv = 'field 1;field 2;field 3;field 4\ncol1 0;col2 0;col3 0\ncol1 1;col2 1;col3 1\ncol1 2;col2 2;col3 2\n' \
          'col1 3;col2 3;col3 3\ncol1 4;col2 4;col3 4'
    assert csv == root_node.export_csv()


def test_export_button(page, bool_toggle):
    page.model = CSVExampleModel
    page.setup_model()

    page.root_node = components.TableLayout(
        headings=[
            {'title': 'field 1', 'name': 'col1'},
            {'title': 'field 2', 'name': 'value', 'sortable': True},
            {'title': 'field 3', 'toggle_visibility_supported': True},
            {'title': 'field 4', 'toggle_visibility_supported': True},
        ],
        get_data='entries',
        data_interface={
            'id': None,
            'col1': None,
            'col2': None,
            'col3': None,
        },
        map_child_cls=[
            ('col1', components.Text, {'value': 'col1'}),
            ('col2', components.Text, {'value': 'col2'}),
            ('col3', components.Text, {'value': 'col3'}),
        ],
    )

    page.handle_transaction()
    root_node = page.root_node
    root_node.show_export = bool_toggle

    rendered_html = root_node.render()

    if not bool_toggle:
        assert '<div class="epfl-table-layout-export">' not in rendered_html
        assert '<i class="fa fa-download"></i> Export' not in rendered_html
    elif bool_toggle:
        assert '<div class="epfl-table-layout-export">' in rendered_html
        assert '<i class="fa fa-download"></i> Export' in rendered_html
