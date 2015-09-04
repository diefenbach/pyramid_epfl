import pytest
from solute.epfl import components


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_type(page, bool_toggle):
    _type = None
    if bool_toggle:
        _type = 'hr'
    page.root_node = components.Placeholder(
        type=_type
    )

    page.handle_transaction()

    if bool_toggle:
        assert '<hr epflid="' in page.render()
        assert '<br epflid="' not in page.render()
    else:
        assert '<hr epflid="' not in page.render()
        assert '<br epflid="' in page.render()
