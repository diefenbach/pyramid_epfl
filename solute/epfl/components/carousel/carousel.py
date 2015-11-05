from solute.epfl.core.epflcomponentbase import ComponentBase


class Carousel(ComponentBase):

    """
    Implements Bootstrap Carousel

    .. code:: python

        button = Carousel(entries=["image.png","image2.png")

    """

    height = None  #: Sets the height in px of the compo if None it will be ignored
    width = None  #: Sets the width in px of the compo if None it will be ignored
    entries = []  #: List of image src urls

    template_name = "carousel/carousel.html"
    js_name = [("solute.epfl.components:carousel/static", "carousel.js")]
    js_parts = []
    css_name = [("solute.epfl.components:carousel/static", "carousel.css")]
    compo_state = ComponentBase.compo_state + ["entries","width","height"]

    new_style_compo = True
    compo_js_params = []
    compo_js_name = 'Carousel'
    compo_js_extras = []

    def __init__(self, page, cid,
                 width=None,
                 height=None,
                 entries=None,
                 **extra_params):
        """
        Carousel Component

        :param height: Sets the height in px of the compo if None it will be ignored
        :param width: Sets the width in px of the compo if None it will be ignored
        :param entries: List of image src urls

        """
        super(Carousel, self).__init__(page=page,
                                       cid=cid,
                                       **extra_params)

