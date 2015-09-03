import pytest
from solute.epfl import components
import re


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


@pytest.fixture(params=['center', 'west', 'east', 'north', 'south'])
def cardinal(request):
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


def test_component_separation(page, cardinal):
    default_compo = components.Text(value='some text')

    page.root_node = components.CardinalLayout(
        node_list=[
            default_compo(slot=cardinal),
            default_compo(slot=cardinal),
            default_compo(slot=cardinal),
            components.CardinalLayout(
                slot=cardinal,
                cid='fixed_layout',
                node_list=[
                    default_compo(cid='east', slot='east'),
                    default_compo(cid='west', slot='west'),
                    default_compo(cid='north', slot='north'),
                    default_compo(cid='south', slot='south'),
                    default_compo(cid='default'),
                    default_compo(cid='center', slot='center'),
                ]
            )
        ]
    )

    page.handle_transaction()
    fixed_layout = page.fixed_layout

    for c in ['center', 'east', 'west', 'north', 'south']:
        if cardinal == c:
            assert page.root_node.has_cardinal(c)
        else:
            assert not page.root_node.has_cardinal(c)

    assert fixed_layout.has_cardinal('east')
    assert fixed_layout.has_cardinal('west')
    assert fixed_layout.has_cardinal('north')
    assert fixed_layout.has_cardinal('south')
    assert fixed_layout.has_cardinal('center')

    assert ['east'] == [c.cid for c in fixed_layout.cardinal_components('east')]
    assert ['west'] == [c.cid for c in fixed_layout.cardinal_components('west')]
    assert ['north'] == [c.cid for c in fixed_layout.cardinal_components('north')]
    assert ['south'] == [c.cid for c in fixed_layout.cardinal_components('south')]

    assert ['default', 'center'] == [c.cid for c in fixed_layout.cardinal_components('center')]
