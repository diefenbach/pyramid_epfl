import pytest
from solute.epfl import components, epflassets, epflpage
import time


"""
Attention: Discrepancys occur when testing at different positions in a multi test run! No significant difference
detected between BDMS MultiSelect component and Text.

SelectableList performance on Produktdaten page points toward implementation errors (high turnaround time).
"""


pytestmark = [
    pytest.mark.skipif(not pytest.config.getoption("--runslow"), reason='slow test'),
    pytest.mark.performance
]


@pytest.fixture(params=[
    1000,
    2500,
    5000,
    10000,
], scope="function")
def compo_count(request):
    return request.param


@pytest.fixture(params=[1, 2, 3])
def toggle(request):
    return request.param


@pytest.fixture(params=[True, False])
def performance_page(request, page, compo_count):
    page.model = MyModel
    if request.param:
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
    else:
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
    return page


def test_performance(performance_page, compo_count):
    # initial run to get a cache
    timings = [time.time()]
    out = performance_page()
    timings.append(time.time())

    # rerun a second time to check cached performance
    new_page = epflpage.Page(None, performance_page.request, performance_page.transaction)
    timings.append(time.time())
    out = new_page()
    timings.append(time.time())

    start, end, rerun_start, rerun_end = timings

    runtime = end - start
    rerun_time = rerun_end - rerun_start
    print ""
    print "=" * 50
    print "Tested %s components." % (compo_count * 4)
    print "=" * 50
    print "Start run: {0:.3}s ({1:.3}ms)".format(runtime, runtime/compo_count*1000)
    print "Cache run: {0:.3}s ({1:.3}ms)".format(rerun_time, rerun_time/compo_count*1000)
    print "Cache Speedup: {0:.1%}".format(runtime/rerun_time)
    print "=" * 50


class MyModel(epflassets.ModelBase):
    def load_my_data(self, calling_compo, row_offset=None, row_limit=None, row_data=None, *args, **kwargs):
        return [
            {'id': i, 'text': 'text compo %s' % i}
            for i in range(0, row_limit)
        ]
