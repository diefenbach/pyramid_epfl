# coding: utf-8
from solute.epfl.core import epflcomponentbase


class ListLayout(epflcomponentbase.ComponentContainerBase):

    # core internals
    template_name = "list_layout/list_layout.html"
    theme_path_default = 'list_layout/default_theme'
    theme_path = []

    # derived attribute overrides

    #: inheriting lists should override this attribute. It may be used in parent lists to
    #: identify the actual list type
    list_type = ["list-layout"]

    def __init__(self, page, cid,
                 node_list=None,
                 **extra_params):
        """Simple list style container component.

        :param node_list: List of child components.
        """
        pass
