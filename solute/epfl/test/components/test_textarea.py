# * encoding: utf-8

import pytest
from solute.epfl import components


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_max_length(page, bool_toggle):
    value = 'test value'
    page.root_node = components.Textarea(
        cid='text_with_title',
        value=value,
        max_length=120,
        show_count=bool_toggle
    )

    page.handle_transaction()

    assert 'maxlength="120"' in page.root_node.render()

    assert_string = '_input_count">{len}</span>/120)</div>'.format(len=len(value))
    if bool_toggle:
        assert assert_string in page.root_node.render()
    else:
        assert assert_string not in page.root_node.render()
