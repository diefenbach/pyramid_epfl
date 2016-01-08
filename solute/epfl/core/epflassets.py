from pyramid.view import view_config
from pyramid import security
from pyramid.settings import aslist

from functools import wraps
from solute.epfl.components import GroupedLinkListLayout
from solute.epfl.core import epflutil

from epflacl import epfl_acl, ACL


def get_item_or_attr(obj, key):
    """
    Helper function returning the item key from obj or, failing that the attribute key. If both do not exist an
    Exception is raised by getattr.
    """
    try:
        return obj[key]
    except (KeyError, TypeError):
        return getattr(obj, key)


class ModelBase(object):
    """
    Use this class as a base for your own bound models.
    """

    def __init__(self, request):
        self.request = request

    def get(self, compo, key, old_args, data_interface):
        """Select the loading function defined by key, call it with the provided parameters and map its output using
        data_interface.

        Args:
            compo (solute.epfl.epflcomponentbase.ComponentBase): The calling component.
            key (str): The name of the load function to be called on the model.
            old_args (tuple): The set of args and kwargs of the original _get_data call.
            data_interface (dict): The map to be used on the output of the load function.
        """
        args, kwargs = old_args
        output = []
        for row in getattr(self, 'load_' + key)(compo, *args, **kwargs):
            tmp_data = data_interface.copy()
            for k, v in tmp_data.items():
                if type(v) in [str, unicode]:
                    try:
                        v.format()
                        tmp_data[k] = get_item_or_attr(row, tmp_data[k])
                    except KeyError:
                        if type(row) is dict:
                            tmp_data[k] = v.format(**row)
                        else:
                            tmp_data[k] = v.format(**row.__dict__)
                else:
                    tmp_data[k] = get_item_or_attr(row, k)

            output.append(tmp_data)

        return output


class EPFLView(object):
    acl = []

    config = None
    register = []
    counter = {'id': 0}

    skip_init = False
    forbidden_view = False

    def __init__(
            self, route_name=None, route_pattern=None, menu_group=None,
            permission=None, route_text=None, rank=None, forbidden_view=False,
            slot=None, icon=None, route_url=None
    ):
        """
        Adds a route, adds the view with the given permissions to that route and creates a link that appears in
        :meth:`get_nav_list`.
        For future expansion the parameters of this method might be extended to allow sub-links and fine tuning of link
        order.
        """
        if self.skip_init:
            return

        self.route_name = route_name
        self.route_url = route_url or route_name
        self.route_text = route_text
        self.route_pattern = route_pattern
        self.menu_group = menu_group
        self.permission = permission
        self.rank = rank
        self.slot = slot
        self.icon = icon
        self.forbidden_view = forbidden_view

        if not self.forbidden_view:
            self._config.add_route(self.route_name, self.route_pattern)

        self.add_link()

    def __call__(self, cb):
        if self.skip_init:
            return cb
        if not self.forbidden_view:
            self._config.add_view(cb,
                                  route_name=self.route_name,
                                  permission=self.permission, )
        else:
            self._config.add_forbidden_view(cb)

        return cb

    def add_link(self):
        if not self.route_text:
            return
        self.counter['id'] += 1
        self.register.append({'id': self.counter['id'],
                              'route': self.route_url,
                              'text': self.route_text,
                              'rank': self.rank,
                              'menu_group': self.menu_group,
                              'slot': self.slot,
                              'icon': self.icon})

    @property
    def _config(self):
        if self.config:
            return self.config
        raise Exception('No config found, have you added this module in the config entry epfl.active_modules?')

    @staticmethod
    def configure(config):
        EPFLView.config = config

        active_modules = aslist(config.registry.settings.get('epfl.active_modules', ''))
        for m in active_modules:
            module = config.maybe_dotted(m)
            epflutil.Discover().discover_module(module)
            if hasattr(module, 'includeme'):
                config.include(m)

        if EPFLView.acl:
            acl_wrapper = epfl_acl(EPFLView.acl, use_as_global=True)
            acl_wrapper(EPFLViewLinks)
            EPFLView.acl = None

        EPFLView.config = None

    @staticmethod
    def get_nav_list(slot=None):
        """
        Return a LinkListLayout Component with links to all registered EPFLViews visible if the current user has the
        correct permissions.
        """
        return EPFLViewLinks(
            links=[view for view in EPFLView.register if view.get('slot') is slot],
            show_search=False,
            show_pagination=False,
            data_interface={
                'id': None,
                'text': None,
                'route': None,
                'menu_group': None,
                'icon': None
            }
        )

    @staticmethod
    def register_acl(*args, **kwargs):
        """
        Register ACLs to be used in the navigation provided by EPFLView and as global ACLs. They will only be registered
        as global ACLs if :meth:`the get_nav_list` is called.
        """
        acl = ACL([])
        epfl_acl(*args, **kwargs)(acl)
        EPFLView.acl.extend(acl.__acl__)


class EPFLViewLinks(GroupedLinkListLayout):
    pass
