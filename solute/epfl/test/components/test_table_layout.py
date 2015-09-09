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


def test_height(page, bool_toggle):
    height = None
    if bool_toggle:
        height = 300

    page.root_node = components.TableLayout(
        height=height
    )

    page.handle_transaction()

    if bool_toggle:
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
