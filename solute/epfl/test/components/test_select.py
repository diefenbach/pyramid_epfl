import pytest
from solute.epfl import components
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_options(page):
    page.root_node = components.Select(
        options=[
            "plain text option",
            ("tuple_option", "tuple option"),
            {"value": "dict_option", "visual": "dict option"},
            {"id": "dict_id_option", "value": "invisible_field", "visual": "dict id option"}
        ]
    )

    page.handle_transaction()

    assert "plain text option" in page.root_node.render()
    assert "tuple option" in page.root_node.render()
    assert "dict option" in page.root_node.render()
    assert "dict id option" in page.root_node.render()

    assert 'value="plain text option"' in page.root_node.render()
    assert 'value="tuple_option"' in page.root_node.render()
    assert 'value="dict_option"' in page.root_node.render()
    assert 'value="dict_id_option"' in page.root_node.render()

    assert 'selected="selected"' not in page.root_node.render()

    for option in ["plain text option", "tuple_option", "dict_option", "dict_id_option"]:
        page.root_node.value = option
        page.root_node.reset_render_cache()

        pattern = re.compile('<[^>]*value="' + option + '"[^>]*selected="selected"[^>]*>', re.MULTILINE)
        assert pattern.search(page.root_node.render())
