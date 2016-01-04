# * encoding: utf-8

from solute.epfl.core import epflacl
from solute.epfl.components import Box, Form, TextInput, Text, Link, Image, Button


class LoginBox(Box):

    # custom compo attributes
    title = 'Login'  #: Default title for the login box.
    hover_box = True  #: Show the login box hovering in the center of the page.
    unauthorized_warning = 'You are not authorized to see this page!'  #: Default Warning for a forbidden page.
    unauthorized_title = 'Forbidden View'  #: Default title for a forbidden page.
    return_path = '/'  #: Path for the return link on the forbidden page.
    return_text = 'Return to Home'  #: Text for the return link on the forbidden page.
    img_path = None  #: Path to an image to be displayed above the login form.
    img_width = None  #: Width a potential image will be displayed with.
    img_height = None  #: Height a potential image will be displayed with.

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
                 **kwargs):
        """Convenience component handling user login by forwarding it to a custom page function.

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
        pass

    def init_struct(self):
        self.node_list = [
            Form(
                cid='login_form',
                handle_submit=None,
                node_list=[
                    TextInput(
                        name='username',
                        label='Username',
                        placeholder='Username',
                        mandatory=True,
                    ),
                    TextInput(
                        name='password',
                        label='Password',
                        placeholder='Password',
                        password=True,
                        mandatory=True
                    ),
                    Button(
                        event_name='submit',
                        color='primary',
                        value='Login'
                    )
                ]
            )
        ]

        if epflacl.epfl_check_role('system.Authenticated', self.page.request):
            self.title = self.unauthorized_title
            self.node_list = [
                Text(
                    value=self.unauthorized_warning
                ),
                Link(
                    url=self.return_path,
                    name=self.return_text
                )
            ]

        if self.img_path:
            self.node_list.insert(0, Image(
                image_path=self.img_path,
                width=self.img_width,
                height=self.img_height,
                padding=True
            ))

    def handle_submit(self):
        form = self.page.login_form
        if not form.validate():
            return

        values = form.get_values()

        if self.page.login(username=values['username'], password=values['password']):
            self.page.jump(self.page.request.matched_route.name)
