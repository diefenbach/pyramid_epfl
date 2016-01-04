import time
import pytest

from solute.epfl.core.epfltransaction import Transaction
from collections2.dicts import OrderedDict


pytestmark = pytest.mark.transaction_api


def test_basic_component_operations(pyramid_req):
    """Tests for basic component operations, this includes:
        * Setting component information,
        * Inserting child components into root_node,
        * Inserting child components into other non root components,
        * Deleting a component.
    """

    transaction = Transaction(pyramid_req, None)

    # Set component information
    transaction.set_component('root_node', {})
    # compo_struct must match expected result1
    assert transaction['compo_struct'] == ['root_node']

    # Insert a child component.
    transaction.set_component('child_node',
                              {'ccid': 'root_node'})

    # compo_struct must match result2, compo_lookup must be present and point to the single child component existing.
    assert transaction['compo_struct'] == ['root_node']
    assert transaction['compo_store']['root_node']['compo_struct'] == ['child_node']

    # Get compo_info, check for correct data.
    compo = transaction.get_component('child_node')
    assert compo == {'ccid': 'root_node',
                     'cid': 'child_node'}

    # Add a child component to the first child, result3 must apply.
    transaction.set_component('child_node2',
                              {'ccid': 'child_node'})
    assert transaction['compo_struct'] == ['root_node']
    assert transaction['compo_store']['root_node']['compo_struct'] == ['child_node']
    assert transaction['compo_store']['child_node']['compo_struct'] == ['child_node2']

    # Delete a component.
    transaction.del_component('child_node')
    assert transaction['compo_store'].keys() == ['root_node']


def test_component_mass_insert(pyramid_req):
    """Tests for mass inserting components.
    """
    transaction = Transaction(pyramid_req, None)

    transaction.set_component('root_node', {})
    transaction.set_component('child_node', {'ccid': 'root_node'})

    for i in range(0, 10000):
        transaction.set_component('sub_child_node_%s' % i, {'ccid': 'child_node'})
    assert transaction.has_component('child_node')
    assert transaction.has_component('sub_child_node_123')

    transaction.del_component('child_node')
    assert transaction['compo_struct'] == ['root_node']
    assert transaction['compo_store']['root_node']['compo_struct'] == []
    assert transaction['compo_store'].keys() == ['root_node']

    assert not transaction.has_component('child_node')
    assert not transaction.has_component('sub_child_node_123')


def test_has_component(pyramid_req):
    """Test for proper functionality of has_component function.
    """
    transaction = Transaction(pyramid_req, None)

    assert not transaction.has_component('root_node')

    transaction.set_component('root_node', {})
    transaction.set_component('child_node', {'ccid': 'root_node'})
    assert transaction.has_component('root_node')

    transaction.del_component('root_node')
    assert not transaction.has_component('root_node')


def test_performance_has_and_set_component(pyramid_req):
    """Testing the performance of has_component and set_component.
    """
    transaction = Transaction(pyramid_req, None)
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

    # Some aggressive timing constraints to keep everyone on his toes!
    assert (steps[-2] - steps[0]) / compo_depth / compo_width < 1. / 5000  # Setting components in under 0.0002s
    assert (steps[-1] - steps[-2]) / 1000 < 0.00001  # Checking if the component exists in under 0.00001s.


def test_duplicated_cid_on_set_component(pyramid_req):
    """ There can be only one cid in the compo_store per transaction """
    transaction = Transaction(pyramid_req, None)
    transaction.set_component('child_node_0', {})

    with pytest.raises(Exception):
        transaction.set_component('child_node_0', {})
