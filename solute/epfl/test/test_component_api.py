import pytest

from component_asserts import AssertCoherence, AssertRendering, AssertStyle

from solute.epfl.core.epflcomponentbase import ComponentBase, ComponentContainerBase


@pytest.fixture(params=['static', 'dynamic'])
def base_type(request, page, component_base_type_class):
    """Generates test scenarios for ComponentBase components.
    """

    # For dynamic tests the Component will be added dynamically to a ComponentContainerBase root_node.
    root_node = ComponentContainerBase
    # For static tests the Component will be added as root_node itself.
    if request.param == 'static':
        root_node = component_base_type_class

    # EPFL house keeping.
    transaction = page.transaction
    page.root_node = root_node
    page.handle_transaction()

    # Ensure the root_node is set visible, select the root_node as tested component and fetch the compo_info from the
    # transaction.
    if request.param == 'static':
        compo_info = transaction.get_component('root_node')
        page.root_node.set_visible()
        tested_component = page.root_node

    # Add the component to the root_node, select it as tested component and fetch the compo_info from the transaction.
    else:
        page.root_node.add_component(component_base_type_class(cid='tested_component'))
        compo_info = transaction.get_component('tested_component')
        tested_component = page.tested_component

    return page, tested_component, compo_info


@pytest.fixture(params=['static', 'static_with_child', 'static_as_child', 'dynamic', 'dynamic_with_child'])
def container_type(request, page, component_container_type_class):
    """Generates test scenarios for ComponentContainerBase components.
    """
    # The child_cls to be used if one is required. If possible the components own default_child_cls is used for better
    # compatibility.
    child_cls = getattr(component_container_type_class, 'default_child_cls', None)
    if child_cls is None:
        child_cls = ComponentBase

    default_args = getattr(component_container_type_class, 'data_interface', {})
    if type(default_args) is property:
        default_args = component_container_type_class.__original_attribute_data_interface

    # For dynamic tests the Component will be added dynamically to a ComponentContainerBase root_node.
    root_node = ComponentContainerBase

    # For static tests the Component will be added as root_node itself.
    if request.param == 'static':
        root_node = component_container_type_class()

    # For static with child tests the Component will be added as root_node itself and receive a child_cls component in
    # its node_list.
    elif request.param == 'static_with_child':
        root_node = component_container_type_class(
            node_list=[child_cls(cid='child_compo', **default_args)]
        )

    # For static as child tests the Component will be added as child component in the node_list of a
    # ComponentContainerBase component.
    elif request.param == 'static_as_child':
        root_node = ComponentContainerBase(
            node_list=[
                component_container_type_class(cid='tested_component')
            ])

    # EPF house keeping.
    page.root_node = root_node
    page.handle_transaction()

    # For dynamic tests the Component will be added dynamically to the root_node.
    if request.param == 'dynamic':
        page.root_node.add_component(
            component_container_type_class(cid='tested_component')
        )

    # For dynamic with child tests the Component will be added dynamically to the root_node while containing a child_cls
    # component in its node_list.
    elif request.param == 'dynamic_with_child':
        page.root_node.add_component(
            component_container_type_class(
                cid='tested_component',
                node_list=[child_cls(**default_args)]
            ))

    # Return the appropriate set of test objects. If injected as root_node the cid is forced to be root_node.
    try:
        return page, page.tested_component, page.transaction.get_component('tested_component')
    except AttributeError:
        return page, page.root_node, page.transaction.get_component('root_node')


def test_base_type(base_type, result):
    """Tests ComponentBase inheriting components coherence and rendering.
    """
    page, tested_node, compo_info = base_type

    AssertCoherence(tested_node, compo_info, result)

    rendered_html = page.root_node.render()
    rendered_js = page.root_node.render(target='js')

    AssertRendering(compo_info, rendered_html, rendered_js, result)


def test_base_type_style(component_base_type_class, result):
    """Tests ComponentBase inheriting components adherence to style guide.
    """
    AssertStyle(component_base_type_class, result)


def test_container_type(container_type, result):
    """Tests ComponentContainerBase inheriting components coherence and rendering.
    """
    page, tested_node, compo_info = container_type

    AssertCoherence(tested_node, compo_info, result)

    rendered_html = page.root_node.render()
    rendered_js = page.root_node.render(target='js')

    AssertRendering(compo_info, rendered_html, rendered_js, result)


def test_container_type_style(component_container_type_class, result):
    """Tests ComponentContainerBase inheriting components adherence to style guide.
    """
    AssertStyle(component_container_type_class, result)


