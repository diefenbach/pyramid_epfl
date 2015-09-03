import pytest
from solute.epfl import components
import re
from lxml import etree


def test_render_number_of_shown_pages(page):

    compo = components.Text(value='some text')
    row_offset = 0
    row_limit = 20
    row_count = 500
    paginated_node_list = []
    for i in range(0, row_limit):
        paginated_node_list.append(compo)

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
            continue # prev first
        if i == 1:
            continue # prev
        if i<11:
            # pages 1 - 9
            assert "<span>%s</span>" % (i-1) in etree.tostring(elem)


