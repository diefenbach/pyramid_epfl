# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class ListLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "list_layout/list_layout.html"

    theme_path_default = 'list_layout/default_theme'
    theme_path = []
    #: inheriting lists should override this attribute. It may be used in parent lists to
    #: identify the actual list type
    list_type = ["list-layout"]

    new_style_compo = True
    compo_js_name = 'ListLayout'

    def __init__(self, page, cid, **extra_params):
        """Simple list style container component.
        """
        super(ListLayout, self).__init__()
