# coding: utf-8

import urllib
import urlparse
from os.path import exists
import logging
import time
import socket

from pyramid import security
from pyramid import path
from pyramid import threadlocal

import solute.epfl
from solute.epfl import core
import threading
import functools
import itertools
from os import getpid

# statsd is preferred over pystatsd since the latter is apparently not maintained any longer.
use_statsd = True
try:
    import statsd
except ImportError:
    use_statsd = False
    import pystatsd


COMPONENT_COUNTER = itertools.count()
COMPONENT_COUNTER_PREFIX = socket.getfqdn().replace('.', '_')
DYNAMIC_CLASS_COUNTER = itertools.count()


def generate_cid():
    """Generates a CID using next(), which is an atomic operation on itertools.count() generators.
    """
    return COMPONENT_COUNTER_PREFIX + "_" + str(getpid()) + "_" + str(COMPONENT_COUNTER.next())


def generate_dynamic_class_id():
    """Generates a dynamic class id using next(), which is an atomic operation on itertools.count() generators.
    """
    return str(DYNAMIC_CLASS_COUNTER.next())


def log_timing(key, timing, server=None, port=None, request=None):
    if not server or not port:
        if not request:
            request = threadlocal.get_current_request()
        registry = request.registry
        settings = registry.settings
        if not server:
            server = settings.get('epfl.performance_log.server')
        if not port:
            port = int(settings.get('epfl.performance_log.port'))

    if use_statsd:
        client = statsd.StatsClient(server, port)
    else:
        client = pystatsd.Client(server, port)

    client.timing(key, timing)


class Lifecycle(object):
    _state = {}

    start_time = None
    end_time = None

    def __init__(self, name, log_time=False):
        self.name = name
        self.log_time = log_time

    @property
    def state(self):
        return self.get_state()

    def checkin(self):
        if self.log_time:
            self.start_time = time.time()
        self.state.append(self.name)

    def checkout(self):
        state = self.state.pop()
        assert state == self.name, Exception("Checkout failed, potential threading problem! %r %r %r" % (state,
                                                                                                         self.name,
                                                                                                         self.state))
        if self.log_time:
            self.end_time = time.time()
            self.log_run_time()

    def __call__(self, cb):
        @functools.wraps(cb)
        def _cb(*args, **kwargs):
            try:
                self.checkin()
                result = cb(*args, **kwargs)
            except Exception as e:
                raise
            finally:
                self.checkout()
            return result

        return _cb

    @staticmethod
    def get_state():
        return Lifecycle._state.setdefault(threading.current_thread().getName(), [])

    @staticmethod
    def get_current():
        return Lifecycle.get_state()[-1]

    @staticmethod
    def depth():
        return len(Lifecycle.get_state())

    def log_run_time(self):
        """Log the time this state was active (between checkin and checkout) to the configured graphite server.
        """
        request = threadlocal.get_current_request()
        if not request:
            return

        registry = request.registry
        settings = registry.settings

        if settings.get('epfl.performance_log.enabled') != 'True':
            return

        server, port = settings.get('epfl.performance_log.server'), int(settings.get('epfl.performance_log.port'))

        route_name = request.matched_route.name
        lifecycle_name = self.name
        if type(lifecycle_name) is tuple:
            lifecycle_name = '_'.join(lifecycle_name)

        key = settings.get(
            'epfl.performance_log.prefix',
            'epfl.performance.{route_name}.{lifecycle_name}'
        ).format(
            host=socket.gethostname().replace('.', '_'),
            fqdn=socket.getfqdn().replace('.', '_'),
            route_name=route_name.replace('.', '_'),
            lifecycle_name=lifecycle_name.replace('.', '_'),
        )

        log_timing(key, int((self.end_time - self.start_time) * 1000), server=server, port=port)


class DictTransformer(object):
    def __init__(self, target_keys):
        self.target_keys = target_keys

    def __call__(self, data):
        out = {}
        for key in self.target_keys:
            out[key] = data[key]
        return out


class Dict2ListTransformer(object):
    def __init__(self, target_keys):
        self.target_keys = target_keys

    def __call__(self, data):
        out = []
        for key in self.target_keys:
            out.append(data[key])
        return out


def make_dict_transformer(target_keys):
    return DictTransformer(target_keys)


def make_dict2list_transformer(target_keys):
    return Dict2ListTransformer(target_keys)


class ClassAttributeExtender(type):
    def __new__(cls, name, bases, dct):
        return type.__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(ClassAttributeExtender, cls).__init__(name, bases, dct)

def add_extra_contents(response, obj):
    """ Adds CSS and JS extra-Contents of this object to the response.
    The object must have the following attributes:
    asset_spec
    js_name
    css_name
    """

    if obj.js_name:
        for js_name in obj.js_name:
            js_script_src = create_static_url(obj, js_name, wrapper_class=core.epflclient.JSLink)
            response.add_extra_content(js_script_src)

    if obj.css_name:
        for css_name in obj.css_name:
            css_link_src = create_static_url(obj, css_name, wrapper_class=core.epflclient.CSSLink)
            response.add_extra_content(css_link_src)

static_url_cache = {}


def create_static_url(obj, mixin_name, spec=None, wrapper_class=None):
    if spec is None:
        spec = obj.asset_spec
    if type(mixin_name) is tuple:
        spec, mixin_name = mixin_name
    asset_spec = "{spec}/{name}".format(spec=spec, name=mixin_name)
    try:
        return static_url_cache[(asset_spec, wrapper_class)]
    except KeyError:
        pass

    if spec[0:12] != 'solute.epfl:' and spec[0:12] != 'solute.epfl.':
        static_url_cache[(asset_spec, wrapper_class)] = obj.request.static_path(asset_spec)
        if wrapper_class:
            static_url_cache[(asset_spec, wrapper_class)] = wrapper_class(static_url_cache[(asset_spec, wrapper_class)])
        return static_url_cache[(asset_spec, wrapper_class)]
    static_path = obj.request.static_path(asset_spec)

    static_mixin = 'static/'
    if spec == 'solute.epfl:static':
        static_mixin = ''

    output = {'base_path': path.package_path(solute.epfl),
              'relative_path': static_path[5:len(static_path) - len(mixin_name)],
              'mixin': static_mixin,
              'mixin_name': mixin_name}
    absolute_path = "{base_path}{relative_path}{mixin}{mixin_name}".format(**output)

    if exists(absolute_path):
        static_url_cache[(asset_spec, wrapper_class)] = obj.request.static_path(asset_spec)
        if wrapper_class:
            static_url_cache[(asset_spec, wrapper_class)] = wrapper_class(static_url_cache[(asset_spec, wrapper_class)])
        return static_url_cache[(asset_spec, wrapper_class)]
    elif spec != 'solute.epfl:static':
        static_url_cache[(asset_spec, wrapper_class)] = create_static_url(obj, mixin_name, 'solute.epfl:static')
        if wrapper_class:
            static_url_cache[(asset_spec, wrapper_class)] = wrapper_class(static_url_cache[(asset_spec, wrapper_class)])
        return static_url_cache[(asset_spec, wrapper_class)]
    else:
        # return obj.request.static_path(asset_spec)
        raise Exception('Static dependency not found. %s' % asset_spec)


def get_page_class_by_name(request, page_name):
    """
    Given a page-name (the page.get_name()-result), it returns this page - or raises an error.
    todo: This needs some caching!
    """
    introspector = request.registry.introspector

    for intr in introspector.get_category("views"):
        view_callable = intr["introspectable"]["callable"]
        if type(view_callable) is type and issubclass(view_callable, core.epflpage.Page):
            if view_callable.get_name() == page_name:
                return view_callable

    raise ValueError, "Page '" + page_name + "' not found!"


def get_page_classes_from_route(request, route_name):
    """
    Given the request and a route-name, it collects all Page-Objects that are bound to this route.
    It returns a list of the page-classes.

    todo: This needs some caching!
    """
    introspector = request.registry.introspector

    candidates = []
    for intr in introspector.get_category("views"):
        if intr["introspectable"]["route_name"] == route_name:
            view_callable = intr["introspectable"]["callable"]
            if type(view_callable) is type and issubclass(view_callable, core.epflpage.Page):
                candidates.append(view_callable)

    return candidates


def has_permission_for_route(request, route_name, permission=None):
    """
    Given a request, a route-name and a permission, it checks, if the current user has this permission for at least
    one of the page-objects that are bound to this route.
    """

    page_objs = get_page_classes_from_route(request, route_name)

    for resource in page_objs:
        if not security.has_permission("access", resource, request):
            return False

    default = True

    views = request.registry.introspector.get_category('views')
    for related in views:
        if related['introspectable']['route_name'] == route_name:
            related = related['related']

            for r in related:
                if r.type_name != 'permission':
                    continue
                default = False
                if request.has_permission(r['value'], request.root):
                    return True

            break

    return default


def get_component(request, tid, cid):
    """
    If you do not have a page_obj (maybe you are in a pure pyramid-view-function), and you need a component,
    this is the function for you!
    """

    transaction = core.epfltransaction.Transaction(request, tid)
    page_name = transaction.get_page_name()
    page_class = get_page_class_by_name(request, page_name)
    page_obj = page_class(request, transaction)
    page_obj.setup_components()
    return page_obj.components[cid]


def get_component_from_root_node(request, tid, cid):
    """
    Same as get_component but for the new pages which always have a root node with the compos in it
    """

    transaction = core.epfltransaction.Transaction(request, tid)
    page_name = transaction.get_page_name()
    page_class = get_page_class_by_name(request, page_name)
    page_obj = page_class(request, transaction)
    page_obj.setup_components()
    root_node = page_obj.components['root_node']
    root_node.init_transaction()
    return page_obj.components[cid]


def get_widget(request, tid, cid, wid):
    """
    Same as get_component, but it returns a widget - in case the compo is a form!
    """
    compo_obj = get_component(request, tid, cid)
    return compo_obj.get_widget_by_wid(wid)


class URL(object):
    def __init__(self, url):
        self.parsed_url = urlparse.urlsplit(url)

    def update_query(self, **kwargs):
        qsl = urlparse.parse_qsl(self.parsed_url.query)
        for key, value in kwargs.items():
            qsl.append((key, value))
        new_url = urlparse.SplitResult(scheme=self.parsed_url.scheme,
                                       netloc=self.parsed_url.netloc,
                                       path=self.parsed_url.path,
                                       query=urllib.urlencode(qsl),
                                       fragment=self.parsed_url.fragment)

        return new_url.geturl()


import inspect


class Discover(object):
    instance = None

    discovered_modules = set()
    discovered_components_set = set()
    discovered_components = []
    discovered_pages = []

    depth = 0

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Discover, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.discover_module(solute.epfl)

    def discover_module(self, module):
        if module in self.discovered_modules:
            return
        self.discovered_modules.add(module)

        for name in dir(module):
            try:
                obj = getattr(module, name)
            except (AttributeError, ImportError):
                continue
            if type(obj) is not type:
                continue
            if issubclass(obj, core.epflcomponentbase.ComponentBase):
                self.discover_component(obj)
            elif issubclass(obj, core.epflpage.Page):
                self.discover_page(obj)
        try:
            for name, m in inspect.getmembers(module, predicate=inspect.ismodule):
                self.discover_module(m)
        except ImportError:
            pass

    @classmethod
    def discover_component(cls, input_class):
        if input_class in cls.discovered_components_set:
            return
        if not getattr(input_class, '__epfl_do_not_track', False):
            cls.discovered_components.append(input_class)
            cls.discovered_components_set.add(input_class)
        input_class.discover()

    @classmethod
    def discover_page(cls, input_class):
        if input_class in cls.discovered_pages:
            return
        cls.discovered_pages.append(input_class)
        input_class.discover()
