# * encoding: utf-8

from solute.epfl.components.text_input.text_input import TextInput


class AutoCompleteInput(TextInput):

    #: Set to true if typeahead should be provided by the input (if supported)
    typeahead = True

    #: Set the name of the function that is used to generate the typeahead values
    type_func = 'typeahead'

    def handle_typeahead(self, query):
        """Override Me
        :param query: the text typed in input
        """
        pass
