# * encoding: utf-8

import time
import pytest
import inspect

from pyramid import testing

from solute.epfl import extract_static_assets_from_components
from solute.epfl.core.epflassets import ModelBase
from solute.epfl.core.epflpage import Page
from solute.epfl.core.epflpage import MissingEventTargetException
from solute.epfl.core.epflcomponentbase import MissingEventHandlerException
from solute.epfl.core.epflcomponentbase import ComponentBase
from solute.epfl.core.epflcomponentbase import ComponentContainerBase

# helper page objects
from page import PageWithJS
from page import PageWithJSNoBundle
from page import PageWithCSS
from page import PageWithCSSNoBundle
from page import PageWithCSSandJS
from page import PageWithCSSandJSNoBundle
from page import PageWithEventHandler


pytestmark = pytest.mark.page_api


def test_basic_component_operations(pyramid_req):
    """Test the basic component operations of the page api.
    """
    page = Page(None, pyramid_req)
    t = page.transaction

    # A component set as root_node must appear in the transaction after handle_transaction.
    page.root_node = ComponentContainerBase
    page.handle_transaction()
    assert t.has_component('root_node')

    # After handle_transaction it must be possible to add child components dynamically to the root_node.
    page.root_node.add_component(ComponentBase(cid='child_node',
                                               compo_state=['test'],
                                               test=None))
    assert t.has_component('child_node')


def test_basic_component_regeneration(pyramid_req):
    """Test the component regeneration operations of the page api.
    """

    # Create a Transaction with assigned components.
    page = Page(None, pyramid_req)
    page.root_node = ComponentContainerBase
    t = page.transaction
    t['components_assigned'] = True

    t.set_component('root_node', {'cid': 'root_node',
                                  'slot': None,
                                  'config': {},
                                  'class': (ComponentContainerBase,
                                            {},
                                            ('27a3d2ef7f76417bb2ebde9853f0c2a6', None))})

    t.set_component('child_node', {'slot': None,
                                   'ccid': 'root_node',
                                   'config': {'test': None,
                                              'compo_state': ['test']},
                                   'class': (ComponentBase,
                                             {'test': None,
                                              'compo_state': ['test']},
                                             ('child_node', None)),
                                   'cid': 'child_node',
                                   'compo_state': {'test': 'foobar'}})

    # handle_transaction now has to restore the components from the transaction into their loaded state.
    page.handle_transaction()

    assert page.root_node is not None and page.child_node is not None, \
        "Components inserted into transaction were not loaded in epfl."
    assert page.child_node.test == 'foobar', \
        "Component attributes inserted into transaction were not loaded in epfl."

    # Set a value into a child node attribute that should be in the compo_state.
    page.child_node.test = {'some': 'dict'}

    assert t.get_component('child_node')['compo_state']['test'] == {'some': 'dict'}, \
        "Stored attribute wasn't stored properly in the transaction compo_state."

    # Generate a new Page instance and regenerate everything from the transaction again.
    new_page = Page(None, pyramid_req, transaction=t)
    new_page.handle_transaction()

    # If this seems familiar you have payed attention. Congratulations. For everyone else: Read two comments up.
    assert t.get_component('child_node')['compo_state']['test'] == {'some': 'dict'}
    assert new_page.child_node.test == {'some': 'dict'}


def test_component_regeneration_performance(pyramid_req):
    """Test the speed of the component regeneration operations of the page api.
    """

    # Create a page, then create a transaction with a ton of components.
    page = Page(None, pyramid_req)
    transaction = page.transaction
    transaction['components_assigned'] = True
    transaction.set_component('root_node',
                              {'cid': 'root_node',
                               'slot': None,
                               'config': {},
                               'class': (ComponentContainerBase,
                                         {},
                                         ('root_node', None))})
    transaction.set_component('child_node_0',
                              {'ccid': 'root_node',
                               'cid': 'child_node_0',
                               'slot': None,
                               'config': {},
                               'class': (ComponentContainerBase,
                                         {},
                                         ('child_node_0', None))})

    # There still is a non linear scaling factor in EPFLs rendering process.The non linear part is strongly depth
    # dependent so this test reflects what happens in 2 layers with 10.000 child components total.
    compo_depth = 10
    compo_width = 1000

    # Store time for beginning, then start adding the components into the transaction.
    steps = [time.time()]
    for i in range(0, compo_depth):
        transaction.set_component('child_node_%s' % (i + 1),
                                  {'ccid': 'child_node_%s' % i,
                                   'cid': 'child_node_%s' % (i + 1),
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('child_node_%s' % (i + 1), None))})
        for x in range(0, compo_width):
            transaction.set_component('child_node_%s_%s' % (i + 1, x),
                                      {'ccid': 'child_node_%s' % i,
                                       'cid': 'child_node_%s_%s' % (i + 1, x),
                                       'slot': None,
                                       'config': {},
                                       'class': (ComponentContainerBase,
                                                 {},
                                                 ('child_node_%s_%s' % (i + 1, x), None))})
    steps.append(time.time())

    # Calling this will generate everything. Or rather, will setup everything so it can be generated just in time. This
    # tends to be quite speedy nowadays, but it used to be a major bottleneck.
    page.handle_transaction()
    steps.append(time.time())
    output = page.render()
    steps.append(time.time())

    assert (steps[2] - steps[1]) * 1. / compo_depth / compo_width < 1. / 10000, \
        'Component transaction handling exceeded limits. (%r >= %r)' % (
            (steps[2] - steps[1]) * 1. / compo_depth / compo_width, 1. / 10000)  # 0.0001s per component are OK.

    assert (steps[3] - steps[2]) * 1. / compo_depth / compo_width < 1. / 100, \
        'Component transaction handling exceeded limits. (%r >= %r)' % (
            (steps[3] - steps[2]) * 1. / compo_depth / compo_width, 1. / 100)  # .01s for rendering a component are ok.


def test_component_rendering_ajax(pyramid_req):
    """Check if the rendering process generates all required AJAX scripts.
    """

    # Create a Transaction with an assigned root_node.
    page = Page(None, pyramid_req)
    page.request.is_xhr = True
    page.page_request.params = {"q": []}
    transaction = page.transaction
    transaction['components_assigned'] = True
    transaction.set_component('root_node',
                              {'cid': 'root_node',
                               'slot': None,
                               'config': {},
                               'class': (ComponentContainerBase,
                                         {},
                                         ('root_node', None))})

    page.handle_transaction()

    base_components = 10
    leaf_components = 200

    # Generate a nice round 210 child components.
    page.root_node.add_component(ComponentContainerBase(cid='child_node_0'))
    for i in range(0, base_components):
        getattr(page, 'child_node_%s' % i) \
            .add_component(ComponentContainerBase(cid='child_node_%s' % (i + 1)))
        for x in range(0, leaf_components):
            getattr(page,
                    'child_node_%s' % (i + 1)) \
                .add_component(ComponentContainerBase(cid='child_node_%s_%s' % (i + 1, x)))

    # Redraw and handle_ajax_events, so that all necessary output will be generated.
    page.root_node.redraw()

    page.handle_ajax_events()

    assert True not in [c.is_rendered for c in page.get_active_components()]

    # start_time = time.time()
    out = page.render()
    # print base_components, leaf_components, int((time.time() - start_time) * 1000000)


def test_component_deletion_and_recreation(pyramid_req):
    """Check if anything goes wrong when components are deleted and then created fresh.
    """

    page = Page(None, pyramid_req)
    transaction = page.transaction
    transaction['components_assigned'] = True
    transaction.set_component('root_node',
                              {'cid': 'root_node',
                               'slot': None,
                               'config': {},
                               'class': (ComponentContainerBase,
                                         {},
                                         ('root_node', None))})

    page.handle_transaction()

    def create_child_components():
        page.root_node.add_component(ComponentContainerBase(cid='child_node_0'))
        for i in range(0, 10):
            getattr(page, 'child_node_%s' % i) \
                .add_component(ComponentContainerBase(cid='child_node_%s' % (i + 1)))
            for x in range(0, 3):
                getattr(page,
                        'child_node_%s' % (i + 1)) \
                    .add_component(ComponentContainerBase(cid='child_node_%s_%s' % (i + 1, x)))

    # Create child components...
    create_child_components()

    # ... make sure they're available...
    assert len(page.root_node.components) == 1
    # ... delete them...
    page.child_node_0.delete_component()

    # ... make sure they've been deleted properly...
    assert transaction['compo_store'].keys() == ['root_node']
    assert transaction.get_component('root_node') == {'cid': 'root_node',
                                                      'compo_struct': [],
                                                      'slot': None,
                                                      'config': {},
                                                      'class': (ComponentContainerBase,
                                                                {},
                                                                ('root_node', None))}
    assert len(page.root_node.components) == 0

    # ... create new child components...
    create_child_components()
    # ... make sure they're available...
    assert len(page.root_node.components) == 1

    # ... make sure they're available in transaction as well...
    assert len(transaction['compo_store']) == 42
    # ... make sure a random child node is available as well. Random numbers generated by fair dice roll.
    assert page.child_node_4_1


def test_component_deletion(pyramid_req):
    """Check if anything goes wrong when components are deleted.
    """

    page = Page(None, pyramid_req)
    transaction = page.transaction
    transaction['components_assigned'] = True
    transaction.set_component('root_node',
                              {'cid': 'root_node',
                               'slot': None,
                               'config': {},
                               'class': (ComponentContainerBase,
                                         {},
                                         ('root_node', None))})

    # Instantiate the pre generated component from the transaction.
    page.handle_transaction()

    # Add a container for our children doomed to be deleted.
    page.root_node.add_component(ComponentContainerBase(cid='child_node_0'))

    # Generate some doomed children.
    for i in range(0, 10):
        getattr(page, 'child_node_%s' % i) \
            .add_component(ComponentContainerBase(cid='child_node_%s' % (i + 1)))
        getattr(page, 'child_node_%s' % (i + 1))
        for x in range(0, 3):
            getattr(page,
                    'child_node_%s' % (i + 1)) \
                .add_component(ComponentContainerBase(cid='child_node_%s_%s' % (i + 1, x)))
            getattr(page, 'child_node_%s_%s' % (i + 1, x))

    # Chop the children off at their respective root.
    page.child_node_0.delete_component()

    # Make sure they're really dead.
    assert transaction.has_component('child_node_0') is False
    for i in range(0, 10):
        assert transaction.has_component('child_node_%s' % (i + 1)) is False
        for x in range(0, 3):
            assert transaction.has_component('child_node_%s_%s' % (i + 1, x)) is False


def test_re_rendering_components(pyramid_req):
    """Check if components can be rendered correctly when regenerated from a Transaction.
    """
    # Generate a transaction with the appropriate components.
    page = Page(None, pyramid_req)
    page.request.is_xhr = True
    page.page_request.params = {"q": []}
    transaction = page.transaction
    transaction['components_assigned'] = True
    transaction.set_component('root_node',
                              {'cid': 'root_node',
                               'slot': None,
                               'config': {},
                               'class': (ComponentContainerBase,
                                         {},
                                         ('root_node', None))})
    transaction.set_component('child_node_0',
                              {'ccid': 'root_node',
                               'cid': 'child_node_0',
                               'slot': None,
                               'config': {},
                               'class': (ComponentContainerBase,
                                         {},
                                         ('child_node_0', None))})
    # This one is about precision, 55 components suffice, we're not after performance here.
    compo_depth = 5
    compo_width = 10

    for i in range(0, compo_depth):
        transaction.set_component('child_node_%s' % (i + 1),
                                  {'ccid': 'child_node_%s' % i,
                                   'cid': 'child_node_%s' % (i + 1),
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('child_node_%s' % (i + 1), None))})
        for x in range(0, compo_width):
            transaction.set_component('child_node_%s_%s' % (i + 1, x),
                                      {'ccid': 'child_node_%s' % i,
                                       'cid': 'child_node_%s_%s' % (i + 1, x),
                                       'slot': None,
                                       'config': {},
                                       'class': (ComponentContainerBase,
                                                 {},
                                                 ('child_node_%s_%s' % (i + 1, x), None))})

    # Set everything up.
    page.handle_transaction()

    # root_node redraw should supersede following child redraws.
    page.root_node.redraw()
    page.child_node_3_1.redraw()

    page.handle_ajax_events()

    out = page.render()

    # Make sure the appropriate replace_component calls are all there. Almost exclusively JS, since HTML will be in the
    # root_node replace_component.
    for i in range(0, compo_depth):
        assert out.count(
            "epfl.replace_component('child_node_%s'" % (i + 1)
        ) == out.count("epfl.replace_component('child_node_0'")
        for x in range(0, compo_width):
            assert out.count(
                "epfl.replace_component('child_node_%s_%s'" % (i + 1, x)
            ) == out.count("epfl.replace_component('child_node_0'")


def test_container_assign(pyramid_req):
    """Check if components are assigned to the proper containers.
    """
    class MyPage(Page):

        root_node = ComponentContainerBase(
            cid='root_node',
            node_list=[
                ComponentContainerBase(
                    cid='container_1',
                    node_list=[
                        ComponentBase(cid='compo_1')
                    ]
                ),
                ComponentContainerBase(
                    cid='container_2',
                    node_list=[
                        ComponentBase(cid='compo_2')
                    ]
                ),
                ComponentContainerBase(
                    cid='container_3',
                    node_list=[
                        ComponentBase(cid='compo_3')
                    ]
                ),
                ComponentContainerBase(
                    cid='container_4',
                    node_list=[
                        ComponentBase(cid='compo_4')
                    ]
                ),
            ]
        )

    page = MyPage(None, pyramid_req)

    page.handle_transaction()

    # The two trailing chars have to be the same.
    for compo in page.root_node.components:
        assert compo.cid[-2:] == compo.compo_info['compo_struct'][0][-2:]


@pytest.mark.xfail
def test_documentation(pyramid_req):
    """Some general checks for documentation completion in the epflpage.py
    """

    missing_docstring = 0
    missing_param_doc = 0
    missing_param_doc_absolute = 0
    errors = []
    methods = inspect.getmembers(Page, inspect.ismethod)
    for name, method in methods:
        if not method.__doc__:
            errors.append('Page method "{name}" is missing docstring.'.format(
                name=name
            ))
            missing_docstring += 1
            continue

        code = method.func_code
        var_names = code.co_varnames
        missing_param_doc_count = 0
        for var_name in var_names:
            if var_name in ['self', 'cls']:
                continue
            if ":param {var_name}:" not in method.__doc__:
                errors.append('Page method "{name}" is missing parameter "{var_name}" in docstring.'.format(
                    name=name,
                    var_name=var_name
                ))
            missing_param_doc_count += 1

        if missing_param_doc_count > 0:
            missing_param_doc += 1
            missing_param_doc_absolute += missing_param_doc_count

    errors = '\n'.join(errors + [
        '{0}/{1} methods undocumented.'.format(
            missing_docstring,
            len(methods)
        ),
        '{0} methods with {1} undocumented parameters.'.format(
            missing_param_doc,
            missing_param_doc_absolute,
        )])

    assert len(errors) == 0, "\n" + errors


def test_unicode_ajax_response(pyramid_req):
    """Check if the rendering process generates all a valid utf-8 encoded response
    """

    # Create a Transaction with an assigned root_node.
    page = Page(None, pyramid_req)
    page.request.is_xhr = True
    page.page_request.params = {"q": []}
    transaction = page.transaction
    transaction['components_assigned'] = True
    transaction.set_component('root_node',
                              {'cid': 'root_node',
                               'slot': None,
                               'config': {},
                               'class': (ComponentContainerBase,
                                         {},
                                         ('root_node', None))})

    page.handle_transaction()

    # Generate a response with a unicode string.
    page.root_node.add_js_response(u'console.log("ää");')

    # Redraw and handle_ajax_events, so that all necessary output will be generated.
    page.root_node.redraw()

    page.handle_ajax_events()

    assert True not in [c.is_rendered for c in page.get_active_components()]

    out = page.render()
    assert u'console.log("ää");' in out
    out.encode('utf-8')


def test_css_js_combination():
    cls_list = [PageWithJS, PageWithJSNoBundle, PageWithCSS, PageWithCSSNoBundle, PageWithCSSandJS,
                PageWithCSSandJSNoBundle]

    js_name = [cls.js_name for cls in cls_list]
    css_name = [cls.css_name for cls in cls_list]

    extract_static_assets_from_components(cls_list)

    assert js_name[0] == PageWithJS.js_name
    assert js_name[1] != PageWithJSNoBundle.js_name
    assert js_name[1] + PageWithJSNoBundle.js_name_no_bundle == PageWithJSNoBundle.js_name
    assert css_name[0] == PageWithJS.css_name
    assert css_name[1] == PageWithJSNoBundle.css_name

    assert js_name[2] == PageWithCSS.js_name
    assert js_name[3] == PageWithCSSNoBundle.js_name
    assert css_name[2] == PageWithCSS.css_name
    assert css_name[3] != PageWithCSSNoBundle.css_name
    assert css_name[3] + PageWithCSSNoBundle.css_name_no_bundle == PageWithCSSNoBundle.css_name

    assert js_name[4] == PageWithCSSandJS.js_name
    assert js_name[5] != PageWithCSSandJSNoBundle.js_name
    assert js_name[4] + PageWithCSSandJSNoBundle.js_name_no_bundle == PageWithCSSandJSNoBundle.js_name
    assert css_name[4] == PageWithCSSandJS.css_name
    assert css_name[5] != PageWithCSSandJSNoBundle.css_name
    assert css_name[5] + PageWithCSSandJSNoBundle.css_name_no_bundle == PageWithCSSandJSNoBundle.css_name


def test_handle_ajax_events_page_events(pyramid_req):
    """ Ajax events are given as json to the page_request object. Event Type ('t') for page events is 'pe'.
    The event name 'e' is used to call the corrosponding handle function. Given event params 'p' are used. """

    # Create a page with a registered root node
    page = PageWithEventHandler(None, pyramid_req)
    page.request.is_xhr = True
    page.page_request.params = {"q": []}
    page.root_node = ComponentContainerBase
    page.handle_transaction()

    # initial call - no events registered, so the counter is set to 0
    assert page.counter == 0
    page.handle_ajax_events()
    assert page.counter == 0

    # now add an valid event: this increases the counter
    page.page_request.params = {"q": [{u'p': {}, u'e': u'increase_counter', u'id': 1, u't': u'pe'}]}
    page.handle_ajax_events()
    assert page.counter == 1
    page.handle_ajax_events()
    assert page.counter == 2

    # next try to call an event, which has no handler
    page.page_request.params = {"q": [{u'p': {}, u'e': u'foobar', u'id': 1, u't': u'pe'}]}
    with pytest.raises(AttributeError) as excinfo:
        page.handle_ajax_events()
    assert "object has no attribute 'handle_foobar'" in str(excinfo.value)

    # events can have params, too. check if they are used.
    page.page_request.params = {"q": [{u'p': {u'counter': 666}, u'e': u'increase_counter', u'id': 1, u't': u'pe'}]}
    page.handle_ajax_events()
    assert page.counter == 666


def test_handle_ajax_events_component_events(pyramid_req):
    """ Ajax events are given as json to the page_request object. Event Type ('t') for component events is 'ce'.
    The event name 'e' is used to call the corrosponding handle function. Given event params 'p' are used. The
    component is identified by its id via cid. """
    # define a component with handler method
    class CounterComponent(ComponentBase):
        counter = 0

        def handle_increase_counter(self, counter=None):
            if counter is None:
                self.counter += 1
            else:
                self.counter = counter

    page = PageWithEventHandler(None, pyramid_req)
    page.request.is_xhr = True
    page.page_request.params = {"q": []}
    page.root_node = ComponentContainerBase(
        node_list=[CounterComponent(cid='counter_compo')]
    )
    page.handle_transaction()

    # initial call - no events registered, so the counter is set to 0
    assert page.counter_compo.counter == 0
    page.handle_ajax_events()
    assert page.counter_compo.counter == 0

    # now add an valid event: this increases the counter
    page.page_request.params = {
        "q": [{u'cid': 'counter_compo', u'p': {}, u'e': u'increase_counter', u'id': 1, u't': u'ce'}]
    }
    page.handle_ajax_events()
    assert page.counter_compo.counter == 1
    page.handle_ajax_events()
    assert page.counter_compo.counter == 2

    # next try to call an event, which has no handler,
    # note: spot the different exception, in opposite to the page test above!
    page.page_request.params = {
        "q": [{u'cid': 'counter_compo', u'p': {}, u'e': u'foobar', u'id': 1, u't': u'ce'}]
    }
    with pytest.raises(MissingEventHandlerException) as excinfo:
        page.handle_ajax_events()

    # events can have params, too. check if they are used.
    page.page_request.params = {
        "q": [{u'cid': 'counter_compo', u'p': {u'counter': 666}, u'e': u'increase_counter', u'id': 1, u't': u'ce'}]
    }
    page.handle_ajax_events()
    assert page.counter_compo.counter == 666

    # make sure all event handlers did not modified the counter of the page, as the test above
    assert page.counter == 0

    # now try to handle an event to an unexisting compo
    page.page_request.params = {
        "q": [{u'cid': 'not_existing', u'p': {}, u'e': u'increase_counter', u'id': 1, u't': u'ce'}]
    }
    with pytest.raises(MissingEventTargetException) as excinfo:
        page.handle_ajax_events()
    assert "Target element with CID 'not_existing' for event" in str(excinfo.value)


def test_handle_ajax_events_invalid_types(pyramid_req):
    """ Event types are either 'pe' for page events or 'ce' for component events. 'upl' is deprecated and all
    others are invalid. """

    # Create a page with a registered root node
    page = PageWithEventHandler(None, pyramid_req)
    page.request.is_xhr = True
    page.page_request.params = {"q": []}
    page.root_node = ComponentContainerBase
    page.handle_transaction()

    # check the depraction warning for 'upl' events
    page.page_request.params = {"q": [{u'cid': 'counter_compo', u'p': {}, u'e': u'foobar', u'id': 1, u't': u'upl'}]}
    with pytest.raises(Exception) as excinfo:
        page.handle_ajax_events()
    assert "The event type 'upl' is deprecated." == str(excinfo.value)

    # check the unknown event type exception
    page.page_request.params = {"q": [{u'cid': 'counter_compo', u'p': {}, u'e': u'foobar', u'id': 1, u't': u'foobar'}]}
    with pytest.raises(Exception) as excinfo:
        page.handle_ajax_events()
    assert str(excinfo.value).startswith('Unknown ajax-event:')


def test_page_init_transaction_handling(pyramid_req, another_route):
    """ each page has it's unique transaction. changing the page must lead to a different transaction. """

    # first get the standard page object with the default "dummy route" used in all tests.
    page = Page(None, pyramid_req)
    page_tid = page.transaction.tid
    page.transaction.store()

    # then create another request, with the another_route
    another_request = testing.DummyRequest()
    another_request.content_type = ''
    another_request.is_xhr = False
    another_request.matched_route = another_route

    # now use the transaction id of the first page object as id to this one
    another_request.params = {'tid': page_tid}
    another_page = Page(None, another_request)

    # this sould lead to a new tid for the another_page
    assert another_page.transaction.tid != page.transaction.tid

    # but using the some tid for the same route/page will use the old tid.
    pyramid_req.params = {'tid': page_tid}
    page_reload = Page(None, pyramid_req)
    assert page_reload.transaction.tid == page.transaction.tid


def test_page_call_ajax(pyramid_req):
    page = Page(None, pyramid_req)

    # a page without _the_ root node will fail.
    with pytest.raises(AttributeError) as excinfo:
        page()
    assert str(excinfo.value) == "'Page' object has no attribute 'root_node'"

    # so add it:
    page.root_node = ComponentContainerBase

    # but a request with enabled xhr fails also until the "q" param is given
    page.request.is_xhr = True
    with pytest.raises(KeyError):
        page()

    # so set it:
    page.page_request.params = {"q": []}
    response = page()

    # will result in text/javascript content type
    assert response.content_type == 'text/javascript'


def test_page_call_html(pyramid_req):
    page = Page(None, pyramid_req)
    page.root_node = ComponentContainerBase

    response = page()

    # we excpect a html page
    assert response.content_type == 'text/html'

    # with an element with the id root_node
    assert '<div id="root_node"' in response.text

    # and also as epflid
    assert 'epflid="root_node"' in response.text


def test_page_call_with_prevent_transaction_loss_html(pyramid_req):
    # first create a default setup: a page with a root node and a valid transaction
    page = Page(None, pyramid_req)
    page.root_node = ComponentContainerBase
    page.handle_transaction()

    original_tid = page.transaction.tid
    # thats what we want and how it should be
    assert '__initialized_components__' in page.transaction
    assert 'root_node' in page.transaction['__initialized_components__']

    # a transaction can be lost (for example) by reaching the timeout setting of the transaction store
    # we simulate this deleting the memory storage and the transaction cache via _data
    page.request.registry.transaction_memory = {}
    page.transaction._data = {}

    # now there are no __initialized_components__ in it any more
    assert '__initialized_components__' not in page.transaction

    # calling the page will call prevent_transaction_loss which should add the __initialized_components__ again
    page()

    assert '__initialized_components__' in page.transaction
    assert 'root_node' in page.transaction['__initialized_components__']

    # also note: this is not a _new_ transaction object - the tid is the same as before
    # but the data will be resetted to the initial state
    assert original_tid == page.transaction.tid


def test_page_call_with_prevent_transaction_loss_ajax(pyramid_req):
    # first create a default setup: a page with a root node and a valid transaction
    page = Page(None, pyramid_req)
    page.root_node = ComponentContainerBase
    page.handle_transaction()

    # thats what we want and how it should be
    assert '__initialized_components__' in page.transaction
    assert 'root_node' in page.transaction['__initialized_components__']

    # a transaction can be lost (for example) by reaching the timeout setting of the transaction store
    # we simulate this deleting the memory storage and the transaction cache via _data
    page.request.registry.transaction_memory = {}
    page.transaction._data = {}

    # now there are no __initialized_components__ in it any more
    assert '__initialized_components__' not in page.transaction

    # setting up a valid ajax request
    page.request.is_xhr = True
    page.page_request.params = {"q": []}

    # now calling the page will force a location.reload() on the browser
    result = page()
    assert result.text == 'window.location.reload();'

    # this will then reload the page which is tested in the test above and will yield to a new valid transaction


def test_setup_model(page):
    """ check if the models gets instantiated for the 3 kinds (see docstring of setup_model). """
    class MyModel(ModelBase):
        pass

    # first kind: model is a type
    page.model = MyModel
    page.setup_model()

    # the model is now an instance of MyModel
    assert page.model != MyModel
    assert isinstance(page.model, MyModel)

    # second kind: model is a list of types
    page.model = [MyModel]
    page.setup_model()

    assert isinstance(page.model, list)
    assert len(page.model) == 1
    assert isinstance(page.model[0], MyModel)

    # notable: tuples are not supported
    page.model = (MyModel,)
    with pytest.raises(TypeError):
        page.setup_model()

    # third kind: model is a dict
    page.model = {'foo': MyModel}
    page.setup_model()

    assert isinstance(page.model, dict)
    assert 'foo' in page.model
    assert isinstance(page.model['foo'], MyModel)


@pytest.mark.parametrize(
    'function_name, kwargs, snippet_in_response',
    [
        ('jump_extern',
         {'target_url': 'http://www.billiger.de'},
         'epfl.jump_extern(\'http://www.billiger.de\', \'_blank\')'),
        ('jump_extern',
         {'target_url': 'http://www.billiger.de', 'target': 'some_frame'},
         'epfl.jump_extern(\'http://www.billiger.de\', \'some_frame\')'),
        ('go_next',
         {'route': None, 'target_url': 'http://www.billiger.de'},
         'epfl.go_next(\'http://www.billiger.de\')'),
        # failing
        # ('go_next',
        #  {'route': 'dummy_route', 'target_url': 'http://www.billiger.de'},
        #  'epfl.go_next(\'/\')'),
        ('jump',
         {'route': 'dummy_route'},
         'epfl.jump(\'/\', 0, "")'),
        ('jump',
         {'route': 'dummy_route', 'wait': 10},
         'epfl.jump(\'/\', 10, "")'),
        ('jump',
         {'route': 'dummy_route', 'wait': 10, 'confirmation_msg': 'Sure?'},
         'epfl.jump(\'/\', 10, "Sure?")'),
        ('reload',
         {},
         'epfl.reload_page();'),
        ('show_message',
         {'msg': 'Foobar'},
         'epfl.show_message({"msg":"Foobar","typ":null,"fading":false});'),
        ('show_message',
         {'msg': 'Foobar', 'typ': 'info'},
         'epfl.show_message({"msg":"Foobar","typ":"info","fading":false});'),
        ('show_message',
         {'msg': 'Foobar', 'typ': 'error', 'fading': True},
         'epfl.show_message({"msg":"Foobar","typ":"error","fading":true});'),
        ('show_fading_message',
         {'msg': 'FadingFoobar', 'typ': 'info'},
         'epfl.show_message({"msg":"FadingFoobar","typ":"info","fading":true});'),
        ('prevent_page_leave',
         {},
         'epfl.prevent_page_leave(true,null);'),
        ('prevent_page_leave',
         {'prevent_leave': False},
         'epfl.prevent_page_leave(false,null);'),
        ('prevent_page_leave',
         {'message': 'Foobar'},
         'epfl.prevent_page_leave(true,"Foobar");'),
    ]
)
def test_js_helper_methods(pyramid_req, function_name, kwargs, snippet_in_response):
    """ test the functions with their parameters which use add_js_response add result. """
    page = Page(None, pyramid_req)
    page.root_node = ComponentContainerBase
    page.handle_transaction()

    func = getattr(page, function_name)
    func(**kwargs)
    response = page()

    assert snippet_in_response in response.text


def test_add_js_response(pyramid_req):
    # XXX: add test for the tuple parameter variant, if relevant
    pass
