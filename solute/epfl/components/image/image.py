# coding: utf-8

from solute.epfl.core import epflcomponentbase


class Image(epflcomponentbase.ComponentBase):

    # core internals
    template_name = "image/image.html"
    js_parts = []
    asset_spec = "solute.epfl.components:image/static"
    css_name = ["image.css"]
    js_name = ["color-thief.min.js", "imagesloaded.pkgd.min.js", "image.js"]
    compo_state = ["image_path"]

    # js settings
    compo_js_auto_parts = True
    compo_js_name = 'Image'
    compo_js_params = ['show_dominant_color', 'show_additional_colors']
    compo_js_extras = ['handle_drag']

    # custom compo attributes
    image_path = None  #: Path to be used as the source of the image.
    show_dominant_color = False  #: Show the color dominant in the picture.
    show_additional_colors = False  #: Show additional prevalent colors in the picture.
    height = None  #: Set a fixed height. This is used directly in css so use "120px" or "10em", etc.
    width = None  #: Set a fixed width. This is used directly in css so use "120px" or "10em", etc.
    padding = False  #: Set a padding. This is used directly in css so use "120px" or "10em", etc.
    label = None  #: Label to be used for this text component.
    #: If set to True, the label will be rendered above the text instead of left before the text.
    #: This attribute is only regarded if the :attr:`label` attribute is set.
    layout_vertical = False  #: Set to True if label should be displayed on top of the compo and not on the left before it
    label_col = 2  #: Set the width of the label of the component (default: 2, max: 12)
    compo_col = 12  #: Set the width of the complete component (default: 12, max: 12)
    label_style = None  #: Can be used to add additional css styles for the label

    def __init__(self, page, cid,
                 image_path=None,
                 show_dominant_color=None,
                 show_additional_colors=None,
                 height=None,
                 width=None,
                 padding=None,
                 compo_col=None,
                 label_col=None,
                 layout_vertical=None,
                 label_style=None,
                 label=None,
                 **extra_params):
        """Displays an Image.

        :param image_path: Path to be used as the source of the image.
        :param show_dominant_color: Show the color dominant in the picture.
        :param show_additional_colors: Show additional prevalent colors in the picture.
        :param height: Set a fixed height. This is used directly in css so use "120px" or "10em", etc.
        :param width: Set a fixed width. This is used directly in css so use "120px" or "10em", etc.
        :param padding: Set a padding. This is used directly in css so use "120px" or "10em", etc.
        :param label: Label to be used for this text component.
        :param layout_vertical: Set to True if label should be displayed on top of the compo and not on the left before it
        :param label_col: Set the width of the label of the component (default: 2, max: 12)
        :param compo_col: Set the width of the complete component (default: 12, max: 12)
        :param label_style: Can be used to add additional css styles for the label
        """
        pass

    def get_image_path(self):
        if self.image_path is None:
            self.image_path = ""
        return self.image_path

    def set_image_path(self, path):
        self.image_path = path
