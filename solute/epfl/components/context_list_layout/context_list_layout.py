# * encoding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import ListLayout, PaginatedListLayout, Link


class ContextListLayout(PaginatedListLayout):
    """
    A searchable list layout with a context menu in every row.

    Its content and the context menu type is configured using get_data() the menu type than can be defined as attribute
    get_data example

    .. code-block:: python

        data = []
        for i in range(0, 100):
            data.append({'id': i, "data": "test" + str(i), 'context_menu':menu_type})

    component example

    .. code-block:: python

         components.ContextListLayout(
                            get_data=list_data,
                            menu_one=[{'name': u"Menu 1", 'event': "delete", 'type': "link"},
                                      {'name': "Rename", 'event': "rename", 'type': "link"}],
                            menu_two=[{'name': u"Menu 2", 'event': "delete", 'type': "link"},
                                      {'name': "Rename", 'event': "rename", 'type': "link"}],
                            handle_delete=None,
                            handle_rename=None
                            )


    A click on a context menu entry emits an event which have to be handled
    for example the entry

    .. code-block:: python

        {'name':"rename", 'event':"rename", 'type':"link"}

    have to be handled by

    .. code-block:: python

        def handle_rename(self, id, data):
            pass

    """

    def __init__(self, page, cid, show_search=True, get_data=None, data_interface=None, *args, **kwargs):
        """ContextListLayout Component

        :param get_data: A get_data source that is used for this component
        :param show_search: Enables a search field on top of the ContextList
        :param data_interface: Data interface to translate the results from get_data polling.
        """
        kwargs.update({
            'show_search': show_search,
            'get_data': get_data,
            'data_interface': data_interface
        })
        super(ContextListLayout, self).__init__(page, cid, *args, **kwargs)

    theme_path = {'row': ['context_list_layout/theme'],
                  'default': ['pretty_list_layout/theme', '<paginated_list_layout/theme'],
                  'inner_container': ['pretty_list_layout/theme', '>context_list_layout/theme']
                  }

    js_parts = PaginatedListLayout.js_parts + ['context_list_layout/context_list_layout.js']
    default_child_cls = Link

    show_pagination = False  #: see :attr:`PaginatedListLayout.show_pagination`
    show_search = True  #: see :attr:`PaginatedListLayout.show_search`

    auto_update_children = True

    js_name = PaginatedListLayout.js_name + [
        ("solute.epfl.components:context_list_layout/static", "context_list_layout.js")]
    css_name = PaginatedListLayout.css_name + [
        ("solute.epfl.components:context_list_layout/static", "context_list_layout.css")]

    data_interface = {'id': None, 'text': None, 'context_menu': None}


    def handle_delete(self, entry_id, data):
        pass

    def handle_rename(self, entry_id, data):
        pass

    def context_menu(self, context_menu_type):
        return getattr(self, context_menu_type)
