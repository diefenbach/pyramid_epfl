# * encoding: utf-8

from solute.epfl.components.text_input.text_input import TextInput


class PasswordInput(TextInput):
    """ Convenience for TextInput with password set to True. """

    #: Set to true if input field should be used as a password field
    password = True
