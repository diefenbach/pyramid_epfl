# coding: utf-8

"""

"""
from solute.epfl.core import epflcomponentbase


class Box(epflcomponentbase.ComponentContainerBase):

    # core internals
    asset_spec = "solute.epfl.components:box/static"
    theme_path = ['box/theme']
    compo_state = epflcomponentbase.ComponentContainerBase.compo_state + ['title', 'read_only']
    css_name = ["box.css"]
    js_name = ["box.js"]

    # js settings
    new_style_compo = True
    compo_js_params = ['hover_box', 'hover_box_remove_on_close', 'hover_box_close_on_outside_click', 'is_removable',
                       'read_only']
    compo_js_extras = ['handle_click']
    compo_js_name = 'Box'

    # custom compo attributes

    #: The title of a box. If it is set, a heading panel is rendered that contains the title.
    title = None
    #: the visibility of the box depends on the visibility of the containing template-elements
    #: if none of them (compos or form-fields) are visible the box to is not visible
    #: else the box is visible
    auto_visibility = True
    #: Set to true if box should not be displayed inside its parent component, but rendered as modal hover box on the
    #: overall page.
    hover_box = False
    #: Indicates whether a hover box component should be deleted upon close or just be hidden.
    hover_box_remove_on_close = True
    #: Indicates whether a hover box component should be closed when the user clicks outside of the box.
    hover_box_close_on_outside_click = True
    box_shown = True  #: Indicates of a border should be drawn around the box.
    #: Indicates if the title of the box should be shown. Sometimes, you want to specify a title but not show it inside
    #: the box. For example, a box inside a :class:`solute.epfl.components.tabs_layout.tabs_layout.TabsLayout`
    #: component.
    show_title = True
    #: Indicates whether a box can be closed by clicking on a special 'close' button
    is_removable = False
    #: Indicates whether a box can be closed and by clicking on a special 'refresh' button
    is_refreshable = False
    #: If readonly is true an overly will be shown over the whole container and prevent inputs
    read_only = False

    def __init__(self, page, cid,
                 title=None,
                 auto_visibility=None,
                 hover_box=None,
                 hover_box_remove_on_close=None,
                 hover_box_close_on_outside_click=None,
                 box_shown=None,
                 show_title=None,
                 is_removable=None,
                 is_refreshable=None,
                 read_only=None,
                 **extra_params):
        """A simple box with a heading that can contain other components. It can be set to hover and/or be closable with
        a cross on the top right.

        :param title: The title of the box will be shown on top of the container in its headbar.
        :param auto_visibility: Defaulting to true any component with this set to true will be only visible if it
         contains visible child components.
        :param hover_box: If set to true the box will be hovering in the center of the screen with everything else being
         forced into the background by a transparent gray overlay.
        :param hover_box_remove_on_close: Defaulting to true any hover box will be removed when clicking the X, else it
         will be set hidden.
        :param hover_box_close_on_outside_click: Defaulting to true any hover box will be closed when clicking outside
         of the box.
        :param box_shown: Defaulting to true the border around the box will only be visible if this is true.
        :param show_title: Defaulting to true the title will only be shown if this is true.
        :param is_removable: Defaulting to false the box will only show its removal button if this is true.
        :param is_refreshable: Defaulting to false the box will only show its refresh button if this is true.
        :param read_only: If readonly is true an overly will be shown over the whole container and prevent inputs
        """
        super(Box, self).__init__()

    def after_event_handling(self):
        super(Box, self).after_event_handling()

        # calculate visibility by checking all sub-element's visibility
        if self.auto_visibility:

            if not self.components:
                return True  # No subelements -> I am visible!

            some_visible = False
            for el in self.components:
                if el.is_visible(check_parents=False):
                    some_visible = True  # at least one subelement is visible -> I am visible!
                    break

            # Automatic redraw-handling based on the old visibility state:
            if some_visible:
                old_visibility = self.set_visible()
                if not old_visibility:
                    self.redraw()
            else:
                old_visibility = self.set_hidden()
                if old_visibility:
                    self.redraw()

    def handle_removed(self):
        self.delete_component()

    def handle_hide(self):
        self.set_hidden()
        self.redraw()
