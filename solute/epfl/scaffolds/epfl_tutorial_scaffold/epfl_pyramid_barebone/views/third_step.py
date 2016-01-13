# * encoding: utf-8

from solute import epfl
from solute.epfl import components
from solute.epfl.core.epflassets import EPFLView
from solute.epfl.core.epflacl import epfl_acl

from .first_step import NoteLayout

## Grant the access permission only to the principal admin
@epfl_acl([('admin', 'access')])
class Admin(components.Box):

    title = 'Admin Box'

    node_list = [
        components.Text(value='This box is only visible for the admin prinicipal.')
    ]


## The Logout Box is only displayed, if the user is authenticated
@epfl_acl([('system.Authenticated', 'access')])
class Logout(components.Box):

    tester = 'foobar'
    title = 'Logout Box'
    node_list = [
        components.Text(value='This box is only visible for all authenticated users'),
        components.Button(value='Logout',
                          color='warning',
                          event_name='logout')]

    def handle_logout(self):
        self.page.forget()
        self.page.reload()

## The Login Box is displayed for every user, beside the authenticated ones.
## That means: unauthorized ones.
@epfl_acl(['access',
           (False, 'system.Authenticated', 'access')])
class Login(components.Box):

    title = 'Login Box'
    users = {'admin': 'adminsecret',
             'user': 'usersecret'}
    node_list = [
        components.Form(
            cid='login_form',
            node_list=[components.TextInput(label='Username',
                                            name='username',
                                            mandatory=True),
                       components.PasswordInput(
                           label='Password',
                           name='password',
                           submit_form_on_enter=True,
                           mandatory=True),
                       components.Button(value='Login',
                                         color='primary',
                                         event_name='login')])]

    def handle_submit(self):
        """ This handler gets triggered on <enter> keypress by the password field. """
        return self.handle_login()

    def handle_login(self):
        if not self.page.login_form.validate():
            return

        values = self.page.login_form.get_values()

        if self.users.get(values['username'], None) != values['password']:
            self.show_fading_message('Invalid authentication details!', 'error')
            return

        self.show_fading_message('Success', 'success')
        self.page.remember(values['username'])
        self.page.reload()


class ThirdStepRoot(NoteLayout):

    def init_struct(self):
        self.node_list.extend([Login(),
                               Logout(),
                               Admin(cid='admin_box')])

@EPFLView(route_name='ThirdStep', route_pattern='/third')
class ThirdStepPage(epfl.Page):

    root_node = ThirdStepRoot()
