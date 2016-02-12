# coding: utf-8

import time
import socket

from pyramid import security
from pyramid import path
from pyramid import threadlocal
from pyramid.settings import asbool
from pyramid.path import AssetResolver

import solute.epfl
from solute.epfl import core
import threading
import functools
import itertools
from os import getpid
import hashlib
import inspect

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

        if not asbool(settings.get('epfl.performance_log.enabled', False)):
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


class ClassAttributeExtender(type):
    def __new__(cls, name, bases, dct):
        return type.__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(ClassAttributeExtender, cls).__init__(name, bases, dct)


class StaticUrlFactory(object):
    asset_resolver = AssetResolver()
    hash_cache = {}
    static_url_cache = {}

    @classmethod
    def create_static_url(cls, page, mixin_name, spec):
        asset_spec = "{spec}/{name}".format(spec=spec, name=mixin_name)
        try:
            return cls.static_url_cache[asset_spec]
        except KeyError:
            pass

        resolved_asset = cls.asset_resolver.resolve(asset_spec)

        if not resolved_asset.exists():
            raise ValueError('Static dependency not found. %s' % asset_spec)

        cls.static_url_cache[asset_spec] = page.request.static_path(asset_spec)
        if asbool(page.request.registry.settings.get('epfl.cache_breaker.active', False)):
            cls.static_url_cache[asset_spec] += '?' + cls.get_static_file_hash(resolved_asset)
        return cls.static_url_cache[asset_spec]

    @classmethod
    def get_static_file_hash(cls, resolved_asset):
        absolute_path = resolved_asset.abspath()
        try:
            return cls.hash_cache[absolute_path]
        except KeyError:
            cls.hash_cache[absolute_path] = hashlib.md5(resolved_asset.stream().read()).hexdigest()
            return cls.hash_cache[absolute_path]


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
