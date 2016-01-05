# coding: utf-8

"""

"""
from pyramid import security

from solute.epfl.core import epflcomponentbase


class Image(epflcomponentbase.ComponentBase):
    template_name = "image/image.html"
    js_parts = []
    asset_spec = "solute.epfl.components:image/static"

    css_name = ["image.css"]
    js_name = ["color-thief.min.js", "imagesloaded.pkgd.min.js", "image.js"]

    compo_state = ["image_path"]

    image_path = None  #: Path to be used as the source of the image.
    show_dominant_color = False  #: Show the color dominant in the picture.
    show_additional_colors = False  #: Show additional prevalent colors in the picture.
    height = None  #: Set a fixed height. This is used directly in css so use "120px" or "10em", etc.
    width = None  #: Set a fixed width. This is used directly in css so use "120px" or "10em", etc.
    padding = False  #: Set a padding. This is used directly in css so use "120px" or "10em", etc.

    compo_js_auto_parts = True
    compo_js_name = 'Image'
    compo_js_params = ['show_dominant_color', 'show_additional_colors']
    compo_js_extras = ['handle_drag']

    def __init__(self, page, cid, image_path=None, height=None, width=None, padding=None, **extra_params):
        """Displays an Image.

        :param image_path: Path to be used as the source of the image.
        :param height: Set a fixed height. This is used directly in css so use "120px" or "10em", etc.
        :param width: Set a fixed width. This is used directly in css so use "120px" or "10em", etc.
        :param padding: Set a padding. This is used directly in css so use "120px" or "10em", etc.
        """
        super(Image, self).__init__(page, cid, **extra_params)

    def get_image_path(self):
        if self.image_path is None:
            self.image_path = ""
        return self.image_path

    def set_image_path(self, path):
        self.image_path = path
