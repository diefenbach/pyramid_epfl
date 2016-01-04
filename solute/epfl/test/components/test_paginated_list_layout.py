import pytest
from solute.epfl.core.epflcomponentbase import ComponentContainerBase
from solute.epfl import components
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_render_number_of_shown_pages(page):
    row_offset = 0
    row_limit = 20
    row_count = 500
    paginated_node_list = []
    for i in range(0, row_limit):
        paginated_node_list.append(components.Text(value='some text'))

    page.root_node = components.PaginatedListLayout(
        show_pagination=True,
        visible_pages_limit=9,
        row_offset=row_offset,
        row_limit=row_limit,
        row_count=row_count,
        node_list=paginated_node_list
    )
    page.handle_transaction()

    compo = page.root_node
    compo_html = compo.render()
    # lxml has problems with these html characters
    entities_to_replace = [
        (u'laquo', 'amp'),
        (u'raquo', 'amp')
    ]
    for before, after in entities_to_replace:
        compo_html = compo_html.replace(before, after)

    compo_html = etree.fromstring(compo_html)
    pagination_bar = compo_html.find(".//ul[@class='pagination-sm pagination']")
    li_tags = pagination_bar.findall("li")
    assert len(li_tags) == 13
    for i, elem in enumerate(li_tags):
        if i == 0:
            continue  # prev first
        if i == 1:
            continue  # prev
        if i < 11:
            # pages 1 - 9
            assert "<span>%s</span>" % (i - 1) in etree.tostring(elem)


def test_show_search(page, bool_toggle):
    page.root_node = ComponentContainerBase(
        node_list=[
            components.PaginatedListLayout(
                cid='placeholder',
                search_placeholder='a search placeholder',
                show_search=bool_toggle
            ),
            components.PaginatedListLayout(
                cid='no_placeholder',
                show_search=bool_toggle
            ),
        ]
    )

    page.handle_transaction()

    if bool_toggle:
        assert '<input class="form-control epfl-search-input"' in page.placeholder.render()
        assert '<input class="form-control epfl-search-input"' in page.no_placeholder.render()
        assert 'placeholder="a search placeholder"' in page.placeholder.render()
        assert 'placeholder="Search..."' in page.no_placeholder.render()
    else:
        assert '<input class="form-control epfl-search-input"' not in page.placeholder.render()
        assert '<input class="form-control epfl-search-input"' not in page.no_placeholder.render()
        assert 'placeholder="a search placeholder"' not in page.placeholder.render()
        assert 'placeholder="Search..."' not in page.no_placeholder.render()


def test_show_pagination(page, bool_toggle):
    page.root_node = components.PaginatedListLayout(
        cid='placeholder',
        show_pagination=bool_toggle
    )

    page.handle_transaction()

    page.root_node.row_count = 1000

    if bool_toggle:
        assert '<ul class="pagination-sm pagination"' in page.root_node.render()
    else:
        assert '<ul class="pagination-sm pagination"' not in page.root_node.render()
