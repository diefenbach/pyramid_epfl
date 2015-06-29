import time

from solute.epfl.core.epfltransaction import Transaction
from collections2.dicts import OrderedDict


def test_basic_component_operations(pyramid_req):
    transaction = Transaction(pyramid_req)

    result1 = OrderedDict([('root_node', {'cid': 'root_node'})])
    result2 = OrderedDict([('root_node',
                            {'cid': 'root_node',
                             'compo_struct': OrderedDict([('child_node',
                                                           {'ccid': 'root_node',
                                                            'cid': 'child_node'})])})])
    result3 = OrderedDict([('root_node',
                            {'cid': 'root_node',
                             'compo_struct': OrderedDict([('child_node',
                                                           {'ccid': 'root_node',
                                                            'cid': 'child_node',
                                                            'compo_struct': OrderedDict([('child_node2',
                                                                                          {'ccid': 'child_node',
                                                                                           'cid': 'child_node2'})])})])})])

    transaction.set_component('root_node',
        {})
    assert transaction['compo_struct'] == result1
    assert 'compo_lookup' not in transaction

    transaction.set_component('child_node',
                              {'ccid': 'root_node'})

    assert transaction['compo_struct'] == result2
    assert 'compo_lookup' in transaction
    assert transaction['compo_lookup'] == {'child_node': 'root_node'}

    compo = transaction.get_component('child_node')
    assert compo == {'ccid': 'root_node',
                     'cid': 'child_node'}

    transaction.set_component('child_node2',
                              {'ccid': 'child_node'})
    assert transaction['compo_struct'] == result3

    transaction.del_component('child_node')
    assert transaction['compo_struct'] == OrderedDict([('root_node', {'cid': 'root_node',
                                                                      'compo_struct': OrderedDict()})])


def test_component_mass_insert(pyramid_req):
    transaction = Transaction(pyramid_req)

    transaction.set_component('root_node', {})
    transaction.set_component('child_node', {'ccid': 'root_node'})

    for i in range(0, 10000):
        transaction.set_component('sub_child_node_%s' % i, {'ccid': 'child_node'})
    assert transaction.has_component('child_node')
    assert transaction.has_component('sub_child_node_123')

    transaction.del_component('child_node')
    assert transaction['compo_struct'] == OrderedDict([('root_node', {'cid': 'root_node',
                                                                      'compo_struct': OrderedDict()})])
    assert not transaction.has_component('child_node')
    assert not transaction.has_component('sub_child_node_123')


def test_has_component(pyramid_req):
    transaction = Transaction(pyramid_req)

    assert not transaction.has_component('root_node')

    transaction.set_component('root_node', {})
    transaction.set_component('child_node', {'ccid': 'root_node'})
    assert transaction.has_component('root_node')

    transaction.del_component('root_node')
    assert not transaction.has_component('root_node')


def test_performance_has_and_set_component(pyramid_req):
    transaction = Transaction(pyramid_req)
    transaction.set_component('child_node_0', {})

    compo_depth = 50
    compo_width = 1000

    steps = [time.time()]
    for i in range(0, compo_depth):
        transaction.set_component('child_node_%s' % (i + 1), {'ccid': 'child_node_%s' % i})
        for x in range(0, compo_width):
            transaction.set_component('child_node_%s_%s' % (i + 1, x), {'ccid': 'child_node_%s' % (i + 1)})

    steps.append(time.time())

    for i in range(0, 1000):
        transaction.has_component('child_node_51')
        transaction.has_component('child_node_51_735')
    steps.append(time.time())

    # print (steps[-1] - steps[-2]) / 1000
    # print (steps[-2] - steps[0]) / compo_depth / compo_width, (steps[-2] - steps[0])
    # Some aggressive timing constraints to keep everyone on his toes!
    assert (steps[-2] - steps[0]) / compo_depth / compo_width < 1. / 5000
    assert (steps[-1] - steps[-2]) / 1000 < 0.00001
