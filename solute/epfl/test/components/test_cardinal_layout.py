import pytest
from solute.epfl import components
import re


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_constrained(page, bool_toggle):
    page.root_node = components.CardinalLayout(
        constrained=bool_toggle,
        node_list=[
            components.CardinalLayout(cid="unconstrained", constrained=False),
            components.CardinalLayout(cid="constrained", constrained=True),
        ]
    )

    page.handle_transaction()

    out = str(page.root_node.render())
    unconstrained = str(page.unconstrained.render())
    constrained = str(page.constrained.render())

    assert unconstrained.startswith('<div class="col-sm-12"')
    assert constrained.startswith('<div class="col-sm-12"')

    if bool_toggle:
        assert out.startswith('<div class="container"')
    else:
        assert out.startswith('<div class="container-fluid"')
