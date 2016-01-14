# * encoding: utf-8

from solute import epfl
from solute.epfl import components
from solute.epfl.core.epflassets import EPFLView
from solute.epfl.core.epflassets import ModelBase


class NoteLayout(components.CardinalLayout):
    """ Define the global cardinal based layout with the links to the other tutorial steps.
    This is also used as root for the other steps, so all will have a consistent layout. """

    # avoid extra margin for the north slot
    plain = ['north']

    # this forces a none-fluid base container
    constrained = True

    # define the list of sub components used in this component
    node_list = [
        components.NavLayout(
            slot='north',
            title='Epfl Tutorial App',
            node_list=[
                components.Link(
                    text='First step',
                    url='/',
                    slot='right'),
                components.Link(
                    text='Second step',
                    url='/second',
                    slot='right'),
                components.Link(
                    text='Third step',
                    url='/third',
                    slot='right')]
        )]


class FirstStepRoot(NoteLayout):

    pass


@EPFLView(route_name='FirstStep', route_pattern='/')
class FirstStepPage(epfl.Page):

    root_node = FirstStepRoot()
