import pytest
from solute.epfl import components


def test_value_rendering(page):
    values = ['example value 1', 'another example value']
    page.root_node = components.Badge(
        value=values[0]
    )

    page.handle_transaction()

    assert values[0] in page.render()

    page.root_node.value = values[1]
    page.root_node.reset_render_cache()

    assert values[1] in page.render()
