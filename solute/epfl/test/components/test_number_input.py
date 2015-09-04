import pytest
from solute.epfl import components
import re
from lxml import etree


@pytest.fixture(params=[True, False])
def bool_toggle(request):
    return request.param


def test_min_value(page, bool_toggle):
    min_value = None
    if bool_toggle:
        min_value = 1111

    page.root_node = components.NumberInput(
        min_value=min_value
    )

    page.handle_transaction()

    if bool_toggle:
        assert 'min="1111"' in page.root_node.render()
    else:
        assert 'min="' not in page.root_node.render()


def test_max_value(page, bool_toggle):
    max_value = None
    if bool_toggle:
        max_value = 1111

    page.root_node = components.NumberInput(
        max_value=max_value
    )

    page.handle_transaction()

    if bool_toggle:
        assert 'max="1111"' in page.root_node.render()
    else:
        assert 'max="' not in page.root_node.render()


def test_patterns(page, bool_toggle):
    override_pattern = None
    if bool_toggle:
        override_pattern = 'override pattern'
    page.root_node = components.Box(
        node_list=[
            components.NumberInput(
                input_pattern=override_pattern,
                cid='number_input',
                validation_type='number'
            ),
            components.NumberInput(
                input_pattern=override_pattern,
                cid='float_input',
                validation_type='float'
            ),
            components.NumberInput(
                input_pattern=override_pattern,
                cid='default_input',
                validation_type='default'
            ),
            ]
    )

    page.handle_transaction()

    if bool_toggle:
        for compo in page.root_node.components:
            assert 'pattern="override pattern"' in compo.render()
            assert 'pattern="\d*"' not in compo.render()
            assert 'pattern="[0-9]+([\.|,][0-9]{1,2})?"' not in compo.render()
            assert 'pattern="[0-9]+([\.|,][0-9]+)?"' not in compo.render()
    else:
        assert 'pattern="\d*"' in page.number_input.render()
        assert 'pattern="\d*"' not in page.float_input.render()
        assert 'pattern="\d*"' not in page.default_input.render()

        assert 'pattern="[0-9]+([\.|,][0-9]{1,2})?"' in page.float_input.render()
        assert 'pattern="[0-9]+([\.|,][0-9]{1,2})?"' not in page.number_input.render()
        assert 'pattern="[0-9]+([\.|,][0-9]{1,2})?"' not in page.default_input.render()

        assert 'pattern="[0-9]+([\.|,][0-9]+)?"' in page.default_input.render()
        assert 'pattern="[0-9]+([\.|,][0-9]+)?"' not in page.float_input.render()
        assert 'pattern="[0-9]+([\.|,][0-9]+)?"' not in page.number_input.render()
