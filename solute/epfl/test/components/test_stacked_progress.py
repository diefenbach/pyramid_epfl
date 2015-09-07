import pytest
from solute.epfl import components
import re
from lxml import etree


def test_value(page):
    page.root_node = components.StackedProgress(
        value=[(10, "progress-bar-one"), (30, "progress-bar-two"), (95, "progress-bar-three"), ]
    )

    page.handle_transaction()

    out = page.root_node.render()

    assert '<div class="progress-bar progress-bar-one" style="width: 10%">' in out
    assert '<div class="progress-bar progress-bar-two" style="width: 30%">' in out
    assert '<div class="progress-bar progress-bar-three" style="width: 95%">' in out
