import pytest
from solute.epfl import components, epflassets
import time


"""
Attention: Discrepancys occur when testing at different positions in a multi test run! No significant difference
detected between BDMS MultiSelect component and Text.

SelectableList performance on Produktdaten page points toward implementation errors (high turnaround time).
"""


@pytest.fixture(params=[
    1000,
    2500,
    5000,
    10000,
])
def compo_count(request):
    return request.param


@pytest.fixture(params=[1, 2, 3])
def toggle(request):
    return request.param


def test_static_selectable_list_wide(toggle, page, compo_count):
    page.model = MyModel
    page.root_node = components.CardinalLayout(
        node_list=[
            components.Box(
                node_list=[
                    components.Box(
                        node_list=[
                            components.Box(
                                node_list=[
                                    components.ColLayout(
                                        node_list=[
                                            components.SelectableList(
                                                row_limit=compo_count,
                                                data_interface={'id': None, 'text': None},
                                                get_data='my_data'
                                            ),
                                            components.SelectableList(
                                                row_limit=compo_count,
                                                data_interface={'id': None, 'text': None},
                                                get_data='my_data'
                                            ),
                                            components.SelectableList(
                                                row_limit=compo_count,
                                                data_interface={'id': None, 'text': None},
                                                get_data='my_data'
                                            ),
                                            components.SelectableList(
                                                row_limit=compo_count,
                                                data_interface={'id': None, 'text': None},
                                                get_data='my_data'
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    start = time.time()
    out = page()
    end = time.time()

    print end - start, float(end-start) / compo_count / 4
    assert False


def test_static_selectable_list_high(toggle, page, compo_count):
    page.model = MyModel
    page.root_node = components.CardinalLayout(
        node_list=[
            components.Box(
                node_list=[
                    components.Box(
                        node_list=[
                            components.Box(
                                node_list=[
                                    components.ColLayout(
                                        node_list=[
                                            components.SelectableList(
                                                row_limit=compo_count * 4,
                                                data_interface={'id': None, 'text': None},
                                                get_data='my_data'
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    start = time.time()
    out = page()
    end = time.time()

    print end - start, float(end-start) / compo_count / 4
    assert False


class MyModel(epflassets.ModelBase):
    def load_my_data(self, calling_compo, row_offset=None, row_limit=None, row_data=None, *args, **kwargs):
        return [
            {'id': i, 'text': 'text compo %s' % i}
            for i in range(0, row_limit)
        ]
