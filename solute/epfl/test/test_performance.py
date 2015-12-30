import pytest
from solute.epfl import components, epflassets, epflpage
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


@pytest.mark.skipif('"--slowtests" not in sys.argv')
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
                                                skip_child_access=True,
                                                row_limit=compo_count,
                                                data_interface={'id': None, 'text': None},
                                                get_data='my_data'
                                            ),
                                            components.SelectableList(
                                                skip_child_access=True,
                                                row_limit=compo_count,
                                                data_interface={'id': None, 'text': None},
                                                get_data='my_data'
                                            ),
                                            components.SelectableList(
                                                skip_child_access=True,
                                                row_limit=compo_count,
                                                data_interface={'id': None, 'text': None},
                                                get_data='my_data'
                                            ),
                                            components.SelectableList(
                                                skip_child_access=True,
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

    # rerun a second time to also check cache performance
    new_page = epflpage.Page(None, page.request, page.transaction)
    rerun_start = time.time()
    out = new_page()
    rerun_end = time.time()

    print_output(compo_count, end, start, rerun_end, rerun_start)


@pytest.mark.skipif('"--slowtests" not in sys.argv')
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
                                                skip_child_access=True,
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
    # rerun a second time to also check cache performance
    new_page = epflpage.Page(None, page.request, page.transaction)
    rerun_start = time.time()
    out = new_page()
    rerun_end = time.time()

    print_output(compo_count, end, start, rerun_end, rerun_start)


def print_output(compo_count, end, start, rerun_end, rerun_start):
    runtime = end - start
    reruntime = rerun_end - rerun_start
    print ""
    print "=" * 50
    print "Tested %s components." % (compo_count * 4)
    print "=" * 50
    print "Clean run: {0:.3}s ({1:.3}ms)".format(runtime, runtime/compo_count*1000)
    print "Cache run: {0:.3}s ({1:.3}ms)".format(reruntime, reruntime/compo_count*1000)
    print "Speedup: {0:.1%}".format(runtime/reruntime)
    print "=" * 50


class MyModel(epflassets.ModelBase):
    def load_my_data(self, calling_compo, row_offset=None, row_limit=None, row_data=None, *args, **kwargs):
        return [
            {'id': i, 'text': 'text compo %s' % i}
            for i in range(0, row_limit)
        ]
