.. _tutorial_3:

Tutorial Part 3: Authentication & Authorization
===============================================

In the following part of the tutorial, we show how rights management works in EPFL.
We are going to build a view that provides a login dialog and UI elements which should only be visible upon login.

We start with an empty skeleton like this as file third_step in the views folder:

.. code-block:: python

    # * encoding: utf-8

    from solute import epfl
    from solute.epfl import components
    from solute.epfl.core.epflassets import EPFLView
    from solute.epfl.core.epflassets import ModelBase

    from .first_step import NoteLayout

    class ThirdStepAuthenticatedRoot(NoteLayout):

        pass


    @EPFLView(route_name='third', route_pattern='/third', permission='access')
    class ThirdStep(epfl.Page):

        root_node = ThirdStepAuthenticatedRoot()

Then add this to the list of active modules, like it was already done for the second step:


.. code-block:: ini

    epfl.active_modules = epfl_starter.views.first_step
                          epfl_starter.views.third_step

Note: if you also have made the second step of the tutorial, you will have three module entries here with all three steps.

After starting your pyramid instance and accessing the /third url with your browser you will notice a 403 Error with message Forbidden.

This is caused by the permission 'access' which is added to the view definition of the third page. If you remove the permission parameter, the empty page with the menu is displayed. Try it!

So, next thing is to provide a custom Forbidden view cause the current one is pyramid's default one and doesn't look that nice. To do so, we add a new page, which will have just one parameter, named forbidden_view.

.. code-block:: python

    ## the forbidden view is used without route. If there is no custom
    ## Page used, the pyramid's default 403 permission view is shown.
    @EPFLView(forbidden_view=True)
    class LoginPage(epfl.Page):

        root_node = components.Text(value='This is a custom forbidden view')

After reloading (and don't forget to set the permission parameter back to the ThirdStep Page again) the given text of the Text component is displayed.

In general, the forbidden view should handle two cases: provide a login if the current user is not already authenticated or provide some informations if the user is logged in but the access to "something" (lika a page) is prohibited.

So first, add the login component by extending the node list of the root component.

.. code-block:: python

    ## This root node is used for the forbidden view. It displays the LoginBox
    ## integrated in the NoteLayout
    class ThirdStepLogin(NoteLayout):

        def init_struct(self):
            self.node_list.extend([components.LoginBox(hover_box=False)])


And use it in your LoginPage:

.. code-block:: python

    @EPFLView(forbidden_view=True)
    class LoginPage(epfl.Page):

        root_node = ThirdStepLogin()

Now the forbidden view shows a nice Login box based on the LoginBox component declared above.

Let's add authentication checks: we simple add a hard-coded dict of two users to our Login box, and check in the handle_login method whether the form is valid and the
corresponding users can be found in our user dict. In this case, we know that the user has passed valid credentials and can authenticate
the user.

Note that you should normally perform this operation on your authentication backend, and never store sensitive user information such as passwords as plain text!
Your view should then use its model to access the authentication logic.

.. code-block:: python

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

The LoginBox component calls a method login() on the page object, so we define it there. By calling self.remember(username) we delegate the authentication to pyramids api.

Now you can try it: given wrong credentials, the fading error message 'Invalid authentication details' are displayed. Given one of the two example users, the login will succeed.

This also covers the second case of the Forbidden view mentioned above: now the user is authenticated, but still has no permission "access" which is declared to view the ThirdStep page. So a accordingly message is shown. You can change this text via parameters, given to the LoginBox.

The assignment of permissions to some users EPFL is based on pyramid's authentication and authorisation system. This might be a good time to read some general fundamental concepts about it here: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html

To fullfill this tutorial, we need to grant the permission 'access' to all authenticated users. This is done globally for all the complete app like this:

.. code-block:: python

    from solute.epfl.core.epflacl import epfl_acl

    ## grant authenticated users the authenticated permission globally
    ## which is used below to pretect the "Homepage" Page
    epfl_acl([(True, 'system.Authenticated', 'access')], use_as_global=True)


epfl_acl() expects a list of tuples where the first value is True or False which maps to pyramids Allow or Deny. The second value is the principal, so in your case pyramid's default prinicipal for all authenticad users. And last, we declare the 'access' permission for them. epfl_acl() can also be used to declare accesses or denys to views or components. But as written above, in this case the use_as_global parameter is used to grant this permissions globally.

We will see next, how single components can be proteced with epfl_acl. But first try to reload your Browser to see the effect after adding the last lines. The Login will succeed and an empty page is displayed (which should not wonder, cause we didn't define any useful components for the third page until now).

So next we will add two components, that will display some Text, either the authenticated user is the admin one or just the general one. So let's define two components:

.. code-block:: python

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


And add them to the root node of the page:

.. code-block:: python

    ## This root node is used on the ThirdStep page
    class ThirdStepAuthenticatedRoot(NoteLayout):

        def init_struct(self):
            self.node_list.extend([Admin(),
                                   User()])


So after browser reload you will get displayed either the User and the Admin Box or just the User Box - depending on the login you used last. As written, this is handled again by epfl_acl which are now used as decorators for the according component.

And finally, to complete this tutorial we also need a some logout mechanism. So we add another component that is only viewable for authenticated users:

.. code-block:: python

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


And add it again to the list of nodes for your page.

Now you can try to log out and log in back with the different users and see how the page content changes depending on the permissions of the current user.

The important step of the logout mechanism is, to call forget() on your page, which gets delegated to pyramid's api. The logout handler ends with a page.jump call to force a reload of the current page. This finally will show the login box (of the forbidden view) again.

You can have a look of the complete file of this step at https://github.com/solute/pyramid_epfl/blob/master/solute/epfl/scaffolds/epfl_tutorial_scaffold/epfl_tutorial/views/third_step.py
