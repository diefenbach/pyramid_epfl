# * encoding: utf-8

from solute import epfl
from solute.epfl import components
from solute.epfl.core.epflassets import EPFLView
from solute.epfl.core.epflacl import epfl_acl

from .first_step import NoteLayout

## Grant the access permission only to the principal admin
@epfl_acl([(True, 'admin', 'access')])
class Admin(components.Box):
    """ Display a box to verify, that the current user is 'admin'. """

    title = 'Admin Box'

    node_list = [
        components.Text(value='This box is only visible for the admin prinicipal.')
    ]

## Grant the access permission to all authenticated users
@epfl_acl([(True, 'system.Authenticated', 'access')])
class User(components.Box):
    """ Display a box to verify, that the current user is authenticated. """
    title = 'User Box'

    node_list = [
        components.Text(value='This box is visible for all authenticated prinicipals.')
    ]

## The Logout Box is only displayed, if the user is authenticated
@epfl_acl([(True, 'system.Authenticated', 'access')])
class Logout(components.Box):
    """ Component that displays the Logout Button with some text. """
    title = 'Logout Box'
    node_list = [
        components.Text(value='This box is only visible for all authenticated users'),
        components.Button(value='Logout',
                          color='warning',
                          event_name='logout')]

    def handle_logout(self):
        self.page.forget()
        self.page.show_fading_message('Logout done.', 'success')
        self.page.jump(self.page.request.matched_route.name, 1000)

## This root node is used for the forbidden view. It displays the LoginBox
## integrated in the NoteLayout
class ThirdStepLogin(NoteLayout):

    def init_struct(self):
        self.node_list.extend([components.LoginBox(hover_box=False)])


## This root node is used on the ThirdStep page
class ThirdStepAuthenticatedRoot(NoteLayout):

    def init_struct(self):
        self.node_list.extend([Admin(),
                               User(),
                               Logout()])

## the forbidden view is used without route. If there is no custom
## Page used, the pyramid's default 403 permission view is shown.
@EPFLView(forbidden_view=True)
class LoginPage(epfl.Page):

    root_node = ThirdStepLogin()
    users = {'admin': 'adminsecret',
             'user': 'usersecret'}

    def login(self, username, password):
        if self.users.get(username, None) != password:
            self.show_fading_message('Invalid authentication details!', 'error')
            return False

        self.remember(username)
        return True

## grant authenticated users the authenticated permission globally
## which is used below to pretect the "Homepage" Page
epfl_acl([(True, 'system.Authenticated', 'access')], use_as_global=True)

## because auf the permission parameter, this view is only accessable for users
## with the 'access' permission, which is globally assigned to all authenticated
## ones above.
@EPFLView(route_name='third', route_pattern='/third', permission='access')
class ThirdStep(epfl.Page):

    root_node = ThirdStepAuthenticatedRoot()
