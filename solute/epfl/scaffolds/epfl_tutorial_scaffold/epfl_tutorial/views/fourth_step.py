# * encoding: utf-8

from pyramid.view import view_config
from solute import epfl
from pyramid import security

from .first_step import FirstStepRoot

from solute.epfl.components import Box
#from solute.epfl.components import DragBox
from solute.epfl.core.epflassets import EPFLView


class DropBox(Box):
    drop_position = None

    #js_name = Box.js_name + [('epfl_pyramid_barebone:static', 'drop.js')]
    #js_parts = Box.js_parts + ['epfl_pyramid_barebone:templates/drop.js']

    def handle_drag_stop(self, position=None, cid=None, over_cid=None):
        if position is None:
            position = self.drop_position
            if cid in self.struct_dict and self.struct_dict.key_index(cid) < position:
                position -= 1
        if over_cid is not None and over_cid in self.struct_dict:
            position = self.struct_dict.key_index(over_cid)
            if cid in self.struct_dict and self.struct_dict.key_index(cid) < position:
                position -= 1
        self.switch_component(self.cid, cid, position=position)

    def handle_drop_accepts(self):
        pass


class FourthStepRoot(FirstStepRoot):
    node_list = []
    # node_list = FirstStepRoot.node_list + [DropBox(slot='west',
    #                                                node_list=[DragBox(title=1),
    #                                                           DragBox(title=2),
    #                                                           DragBox(title=3),
    #                                                           DragBox(title=4),
    #                                                           DragBox(title=5), ]),
    #                                        DropBox(cid='second_drop')]

    def init_struct(self):
        pass


@EPFLView(route_name='FourthStep', route_pattern='/fourth')
class FourthStepPage(epfl.Page):
    root_node = FourthStepRoot()
