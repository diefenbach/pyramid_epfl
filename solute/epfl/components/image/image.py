# coding: utf-8

"""

"""

import types
import copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil
from solute.epfl.components import Droppable
import json


class Image(epflcomponentbase.ComponentBase):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    template_name = "image/image.html"
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["image/image.js"]
    asset_spec = "solute.epfl.components:image/static"

    css_name = ["image.css"]
    js_name = ["color-thief.min.js", "imagesloaded.pkgd.min.js", "image.js"]

    compo_config = []
    compo_state = ["image_path"]

    image_path = ""
    show_dominant_color = False
    show_additional_colors = False
    height = None

    def get_image_path(self):
        return self.image_path

    def set_image_path(self, path):
        self.image_path = path


class ImageList(Droppable):
    template_name = "image/image_list.html"
    
    js_parts = Droppable.js_parts + ["image/image_list.js"]

    show_borders=False
    
    def handle_add_dragable(self, cid, position):
        """
        Insert a copy of the dragable image in the image list and leave the original dragable as is 
        """
        origin_comp = self.page.components[cid].components[0]
        origin_comp_box = self.page.components[cid].container_compo
        
        new_image = self.add_component(Image())
        new_image.image_path = origin_comp.image_path
        origin_comp_box.redraw()
        self.redraw()
    
    def __init__(self, *args, **extra_params):
        super(ImageList, self).__init__(*args, **extra_params)
        if "show_borders" in extra_params:
            self.show_borders = extra_params["show_borders"]
        else:
            self.show_borders = False