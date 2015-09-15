import pytest
from solute.epfl import components, epflassets
from solute.epfl.core import epflcomponentbase
import time
import timeit


"""
Attention: Discrepancys occur when testing at different positions in a multi test run! No significant difference
detected between BDMS MultiSelect component and Text.

SelectableList performance on Produktdaten page points toward implementation errors (high turnaround time).
"""


@pytest.fixture(params=[
    # 1000,
    2500,
    # 5000,
    # 10000,
])
def compo_count(request):
    return request.param


def test_static_container_with_base_children(page, compo_count):
    page.root_node = epflcomponentbase.ComponentContainerBase(
        node_list=[
            components.Text(
                text='text compo %s' % i
            ) for i in range(0, compo_count)
        ]
    )
    start = time.time()
    out = page()
    end = time.time()

    print end - start
    assert False


def test_static_selectable_list_wide(page):
    compo_count = 2500
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
                                                links=[
                                                    {'id': i, 'text': 'text compo %s' % i}
                                                    for i in range(0, compo_count)
                                                ]
                                            ),
                                            components.SelectableList(
                                                links=[
                                                    {'id': i, 'text': 'text compo %s' % i}
                                                    for i in range(0, compo_count)
                                                ]
                                            ),
                                            components.SelectableList(
                                                links=[
                                                    {'id': i, 'text': 'text compo %s' % i}
                                                    for i in range(0, compo_count)
                                                ]
                                            ),
                                            components.SelectableList(
                                                links=[
                                                    {'id': i, 'text': 'text compo %s' % i}
                                                    for i in range(0, compo_count)
                                                ]
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

    print end - start
    assert False


def test_static_selectable_list_high(page):
    compo_count = 5000
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
                                                links=[
                                                    {'id': i, 'text': 'text compo %s' % i}
                                                    for i in range(0, compo_count)
                                                ]
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

    print end - start
    assert False


def test_transaction_access_high(page):
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
                                                cid='selectable_list',
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

    page()

    assert False


class MyModel(epflassets.ModelBase):
    def load_my_data(self, *args, **kwargs):
        return [
            {'id': i, 'text': 'text compo %s' % i}
            for i in range(0, 10000)
        ]