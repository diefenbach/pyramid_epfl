# coding: utf-8

"""

"""

from solute.epfl.components import LinkListLayout
from solute.epfl.components import PaginatedListLayout


class HoverLinkListLayout(LinkListLayout):

    theme_path = {'default': LinkListLayout.theme_path['default'],
                  'row': ['hover_link_list_layout/theme']}

    # LinkListLayout is not new style, so we go one more up
    js_name = LinkListLayout.js_name + [('solute.epfl.components:hover_link_list_layout/static',
                                              'hover_link_list_layout.js')]
    new_style_compo = True
    compo_js_name = 'HoverLinkListLayout'
    compo_js_params = ['src']

    data_interface = {
        'id': None,
        'text': None,
        'src': None,
        'url': None
    }
