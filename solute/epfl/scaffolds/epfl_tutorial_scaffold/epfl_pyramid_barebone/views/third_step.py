# * encoding: utf-8

from pyramid.view import view_config
from solute import epfl
from pyramid import security

from .first_step import FirstStepRoot

from solute.epfl.components import Box
from solute.epfl.components import Form
from solute.epfl.components import TextInput
from solute.epfl.components import Button
from solute.epfl.components import PasswordInput

from solute.epfl.core.epflassets import EPFLView
from solute.epfl.core.epflacl import epfl_acl, epfl_has_role


@epfl_acl([('admin', 'access')])
class Admin(Box):
    title = 'Admin Box'

    def handle_hidden(self):
        print "I'm hidden!"


@epfl_acl([('system.Authenticated', 'access')])
class Logout(Box):
    title = 'Logout Box'
    node_list = [Button(value='Logout',
                          event_name='logout')]

    def handle_logout(self):
        self.page.forget()
        self.page.reload()


@epfl_acl(['access',  #: With default_allow=True and default_principle='system.Everyone', this is equal to the epfl
                      #: default __acl__ in ComponentBase. To make sure the default settings do not influence this you
                      #: can give the tuple (True, 'system.Everyone', 'access') instead the string 'access'.
           (False, 'system.Authenticated', 'access')])
class Login(Box):
    title = 'Login Box'

    users = {'admin': 'abcdefg',
             'someuser': '12345'}

    node_list = [Form(cid='login_form',
                      node_list=[TextInput(label='Username',
                                           name='username'),
                                 PasswordInput(label='Password',
                                               name='password'),
                                 Button(value='Login',
                                        event_name='login')])]

    def handle_login(self):
        if not self.page.login_form.validate():
            return
        values = self.page.login_form.get_values()

        if self.users.get(values['username'], None) != values['password']:
            self.show_fading_message('Invalid authentication details!', 'error')
            return

        self.page.remember(values['username'])
        self.page.reload()


class ThirdStepRoot(FirstStepRoot):
    node_list = FirstStepRoot.node_list + [Login(),
                                           Logout(),
                                           Admin(cid='admin_box')]

    def init_struct(self):
        pass


@EPFLView(route_name='ThirdStep', route_pattern='/third')
class ThirdStepPage(epfl.Page):
    root_node = ThirdStepRoot()
