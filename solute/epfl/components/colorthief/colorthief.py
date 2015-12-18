# * encoding: utf-8

from solute.epfl.components.form.inputbase import FormInputBase
from urllib2 import urlopen
import io
from urlparse import urlparse
import base64

try:
    from solute.epfl.components.colorthief.mmcq import get_palette
except ImportError:
    pass


class ColorThief(FormInputBase):
    js_name = FormInputBase.js_name + [("solute.epfl.components:colorthief/static", "colorthief.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorthief/static", "colorthief.css")]
    template_name = "colorthief/colorthief.html"
    js_parts = []
    compo_state = FormInputBase.compo_state + ["image_src", "dominat_colors_count", "color_count", "add_icon_size",
                                               "compress_image"]

    height = None  #: Compo height in px if none nothing is set

    width = None  #: Compo width in px if none nothing is set

    image_src = None  #: image src if set the drop zone is hidden

    color_count = 7  #: Count of colors which got extracted from the image

    add_icon_size = "5x"  #: The add icon size use font awesome sizes

    #:  If set to true the image get compressed first to 200x200 px this is faster but less accurate
    compress_image = False

    new_style_compo = True
    compo_js_params = FormInputBase.compo_js_params + ['color_count']
    compo_js_name = 'ColorThief'
    compo_js_extras = ['handle_click', 'handle_drop']

    def __init__(self, page, cid, height=None, width=None, image_src=None, color_count=None, add_icon_size=None,
                 compress_image=None,
                 **extra_params):
        """ColorThief Compo: A Drop Area where images can be dropped and their colors get extracted

        :param height: Compo height in px if none nothing is set
        :param width: Compo width in px if none nothing is set
        :param image_src: image src if set the drop zone is hidden
        :param color_count: Count of colors which got extracted from the image
        :param add_icon_size: The add icon size use font awesome sizes
        :param compress_image: If set to true the image get compressed first to 200x200 px this is faster but less accurate
        :return:
        """
        super(ColorThief, self).__init__(page=page, cid=cid, height=height, width=width, image_src=image_src,
                                         color_count=color_count, add_icon_size=add_icon_size, **extra_params)

    def __new__(cls, *args, **config):
        try:
            import PIL
            from solute.epfl.components.colorthief.mmcq import get_palette
        except ImportError:
            raise ImportError("Colorthief needs pillow, "
                              "check: http://pillow.readthedocs.org/installation.html#basic-installation ")

        return super(ColorThief, cls).__new__(cls, *args, **config)

    def handle_change(self, value, image_src=None):
        if image_src is not None:
            url_result = urlparse(image_src)
            dominant_colors = None
            if url_result.scheme == u"data":
                dominant_colors = set(self.get_dominant_colors_from_binary(image_src, color_count=self.color_count))
            else:
                dominant_colors = set(self.get_dominant_colors_from_url(image_src, color_count=self.color_count))
            self.value = [{"rgb": "#%x%x%x" % (val[0], val[1], val[2]), "selected": False} for val in dominant_colors]
        else:
            self.value = None
        self.image_src = image_src
        self.redraw()

    def handle_drop_accepts(self, cid, moved_cid):
        self.add_ajax_response('true')

    def handle_click_color(self, color):
        for val in self.value:
            if val["rgb"] == color:
                val["selected"] = not val["selected"]
                break

        self.redraw()

    def get_dominant_colors_from_url(self, url, color_count=8):
        """Fetch the image from the url and extract the dominant colors

        :param url: image url
        :param color_count: count of dominant colors
        """
        bytes = io.BytesIO(urlopen(url).read())
        with get_palette(blob=bytes, color_count=color_count, compress_image=self.compress_image) as palette:
            return palette

    def get_dominant_colors_from_binary(self, binary, color_count=8):
        """Get image from javascript filereader and extract dominant colors

        :param binary: javascript filereader result
        :param color_count: count of dominant colors
        """
        info, coded_string = str.split(str(binary), ',')
        bytes = io.BytesIO(base64.b64decode(coded_string))
        with get_palette(blob=bytes, color_count=color_count, compress_image=self.compress_image) as palette:
            return palette
