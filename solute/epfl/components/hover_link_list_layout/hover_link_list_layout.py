# coding: utf-8

"""

"""

from solute.epfl.components import LinkListLayout


class HoverLinkListLayout(LinkListLayout):
    data_interface = {
        'id': None,
        'text': None,
        'src': None,
        'url': None
    }

    js_parts = LinkListLayout.js_parts + ["hover_link_list_layout/hover_link_list_layout.js"]
