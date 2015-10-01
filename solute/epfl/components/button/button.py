from solute.epfl.core.epflcomponentbase import ComponentBase


class Button(ComponentBase):

    """
    This component provides basic button functionality.

    To use a button, a event handling method for handling button clicks has to be provided:

    .. code:: python

        button = Button(name="Do something", event_name="submit")

        def handle_submit(self):
            pass
            # do something: button has been clicked

    """

    template_name = "button/button.html"
    js_name = [("solute.epfl.components:button/static", "button.js")]
    js_parts = []
    css_name = [("solute.epfl.components:button/static", "button.css")]
    compo_state = ComponentBase.compo_state + \
        ['disabled', 'icon', 'value', 'color', 'icon_size', 'icon_color']

    label = None  #: If set, the label is rendered before the button.
    value = None  #: The value is used as button text if no icon is provided.
    #: Optional color of the button. Possible values: default, primary, warning, danger, success, transparent
    color = None
    #: Optional font-awesome icon to be rendered as button value instead of :attr:`value` text.
    icon = None
    icon_size = None  #: Optional font-awesome icon-size possible values: 'lg', 2, 3, 4, 5
    #: Optional color of the button icon. Possible values default, primary, warning, danger, success
    icon_color = None
    tooltip = None  #: Optional tooltip text that is placed on the button.
    #: Mandatory name of the event handling method (without trailing "handle\_").
    event_name = None
    event_target = None  #: Optional target where the event handling method can be found.
    is_submit = False  #: Set to true if button should have html type "submit".
    disabled = None  #: Set to true if button should be disabled.
    #: Set to true if user should be asked for confirmation first before the button event is triggered
    confirm_first = False
    #: Adapt this text for a custom confirmation dialog message.
    confirm_message = "Do you want to proceed?"
    button_size = None  #: Optional button size. Possible values: 'btn-lg', 'btn-sm', 'btn-xs'
    #: If set to true, the button is set to disabled on a click. Caution: Currently, only the html part is set to
    #: disabled in order to avoid multiple clicks on the button. to set the component attribute to disabled as well,
    #: this has to be done in the event handling method.
    disable_on_click = False
    stop_propagation_on_click = False  #: Set to true if click event should not be propagated to parent components

    new_style_compo = True
    compo_js_params = ['event_target', 'event_name', 'confirm_first', 'confirm_message',
                       'stop_propagation_on_click', 'disable_on_click']
    compo_js_name = 'Button'
    compo_js_extras = ['handle_click']

    def __init__(self, page, cid,
                 label=None,
                 value=None,
                 color=None,
                 icon=None,
                 icon_size=None,
                 icon_color=None,
                 tooltip=None,
                 event_name=None,
                 event_target=None,
                 is_submit=False,
                 confirm_first=False,
                 confirm_message="Do you want to proceed?",
                 button_size=None,
                 disable_on_click=None,
                 stop_propagation_on_click=None,
                 **extra_params):
        """
        Button Component

        :param label: If set, the label is rendered before the button
        :param value: The value is used as button text if no icon is provided
        :param color: Optional color of the button. Possible values: default, primary, warning, danger, success, transparent
        :param icon: Optional font-awesome icon to be rendered as button value instead of the text attribute
        :param icon_size: Optional font-awesome icon-size possible values: 'lg', 2, 3, 4, 5
        :param icon_color: Optional color of the button icon. Possible values default, primary, warning, danger, success
        :param tooltip: Optional tooltip text that is placed on the button
        :param event_name: Mandatory name of the event handling method (without trailing "handle\_")
        :param event_target: Optional target where the event handling method can be found
        :param is_submit: Set to true if button should have html type "submit"
        :param disabled: Set to true if button should be disabled
        :param confirm_first: Set to true if user should be asked for confirmation first before the button event is triggered
        :param confirm_message: Adapt this text for a custom confirmation dialog message
        :param button_size: Optional button size. Possible values: 'btn-lg', 'btn-sm', 'btn-xs'
        :param disable_on_click: If set to true, the html button (not the component!) is set to disabled on a click
        :param stop_propagation_on_click: Set to true if click event should not be propagated to parent components
        """
        super(Button, self).__init__(page=page, cid=cid,
                                     label=label,
                                     value=value,
                                     color=color,
                                     icon=icon,
                                     icon_size=icon_size,
                                     icon_color=icon_color,
                                     tooltip=tooltip,
                                     event_name=event_name,
                                     event_target=event_target,
                                     is_submit=is_submit,
                                     confirm_first=confirm_first,
                                     confirm_message=confirm_message,
                                     button_size=button_size,
                                     disable_on_click=disable_on_click,
                                     stop_propagation_on_click=stop_propagation_on_click,
                                     **extra_params)
        if not self.event_target:
            self.event_target = self.cid
