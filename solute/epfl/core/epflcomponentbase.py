# coding: utf-8
from pprint import pprint
from collections2 import OrderedDict as odict
from collections import MutableSequence, MutableMapping

import types, copy, string, inspect

from pyramid import security

from solute.epfl.core import epflclient, epflutil, epflacl, epflvalidators
from solute.epfl import validators
from solute.epfl.core.epflutil import Lifecycle

import ujson as json

import jinja2
import jinja2.runtime
from jinja2.exceptions import TemplateNotFound


class MissingContainerComponentException(Exception):
    pass


class MissingEventHandlerException(Exception):
    pass


class CallWrap(object):
    """Special helper class to convert a list of callables into a single callable object.
    """
    caller = None

    def __init__(self, cb_chain, env, part):
        """Extract the required parameters from input.

        :param cb_chain: Tuple of direction String ('<', '>', '') and callable list.
        :param env: ComponentRenderEnvironment instance.
        :param part: The name of the part this CallWrap is made up for.
        """
        direction, self.callables = cb_chain
        if direction == '<':
            self.callables.reverse()
        self.env = env
        self.part = part

    def __call__(self, *args, **kwargs):
        """On call the original caller is executed, and its output chained into the callable chain.

           :param args: Original arguments to the jinja2 template call.
           :param kwargs: Original keyworded arguments to the jinja2 template call, the caller attribute is required.
        """
        self.caller = kwargs.get('caller', lambda *args, **kwargs: None)

        extra_kwargs = dict(self.env)
        extra_kwargs.update(kwargs)

        out = self.caller()

        for cb in self.callables:
            extra_kwargs['caller'] = lambda *a, **k: out
            out = cb(*args, **extra_kwargs)

        return out


class ComponentRenderEnvironment(MutableMapping):
    """Convenience class to manage the different themes and the theme wrapping mechanism. Implements MutableMapping
    Interface.

    .. graphviz::

        digraph foo {
            "Component" -> "ComponentRenderEnvironment";
            "jinja2 environment" -> "ComponentRenderEnvironment";
            "ComponentRenderEnvironment" -> "__call__" [label="provides"];
            "ComponentRenderEnvironment" -> "__getitem__" [label="provides"];
            "ComponentRenderEnvironment" -> "__init__" [label=""];
            "ComponentRenderEnvironment" -> "data dict" [label="provides"];
            "__call__" -> "jinja2.Markup" [label="returns"];

            "ComponentBase.get_themed_template" -> "callable chain";
            "callable chain" -> "data dict" [label=""];

            "__getitem__" -> "data dict" [label="accesses"];
            "__getitem__" -> "callable generator" [label="provides"];
            "callable generator" -> "CallWrap" [label="returns"];
            "callable chain" -> "CallWrap" [label="wrapped by"];
        }
    """

    def __iter__(self):
        """Expose data attribute."""
        return self.data.__iter__()

    def __delitem__(self, key):
        """Expose data attribute."""
        return self.data.__delitem__(key)

    def __len__(self):
        """Expose data attribute."""
        return self.data.__len__()

    def __setitem__(self, key, value):
        """Expose data attribute."""
        return self.data.__setitem__(key, value)

    def __getitem__(self, item):
        """Exposes the wrapped theme template jinja2 callables just in time. Every parameter besides the bypass is
        treated as a list of callables. Wrapping relies on :class:`CallWrap` to allow for n-deep template chains.

        :param item: The key of the environment that is to be accessed.
        """

        # Parameter Bypass, currently only the compo key.
        if item in ['compo']:
            return self.data[item]

        # Ensure that only items that should be callables are used here.
        if item not in ['container', 'inner_container', 'row', 'before', 'after']:
            raise KeyError('Unknown ')

        return CallWrap(self.data[item], self, item)

    def __init__(self, compo, env):
        """Exposes the data attribute via the python MutableMapping Interface.
        """
        self.data = {'compo': compo,
                     'container': compo.get_themed_template(env, 'container'),
                     'inner_container': compo.get_themed_template(env, 'inner_container'),
                     'row': compo.get_themed_template(env, 'row'),
                     'before': compo.get_themed_template(env, 'before'),
                     'after': compo.get_themed_template(env, 'after')}


class UnboundComponent(object):
    """
    This is one of two main classes used by epfl users, though probably few will notice. Any
    :class:`.ComponentBase` derived subclass will return an :class:`.UnboundComponent` wrapping it, unless specifically
    instructed to return an instance. See :func:`ComponentBase.__new__` for further details.

    Warning: Instantiation should be handled by the epfl core!

    If you encounter an :class:`.UnboundComponent` you are likely trying to access a component in an untimely manner.
    Assign it a cid and access that component via page.cid after init_transaction() is done by
    :class:`.ComponentContainerBase`. :func:`ComponentContainerBase.add_component` will return the actually
    instantiated component if it is called with an :class:`.UnboundComponent`.
    """
    __dynamic_class_store__ = None  #: Internal caching for :attr:`UnboundComponent.__dynamic_class__`
    __global_dynamic_class_store__ = {}  #: Global caching for :attr:`UnboundComponent.__dynamic_class__`

    def __init__(self, cls, config):
        """
        Create dynamic cid for unbound components without a cid entry in config, store the calling class and create a
        copy of the config.
        """
        self.__unbound_cls__ = cls
        self.__unbound_config__ = config.copy()

        # Copy config and create a cid if none exists.
        self.position = (
            self.__unbound_config__.pop('cid', None) or epflutil.generate_cid(),
            self.__unbound_config__.pop('slot', None)
        )

    def __call__(self, *args, **kwargs):
        """
        Pseudo instantiation helper that returns a new UnboundComponent by updating the config. This can also be used to
        generate an instantiated Component if one is needed with the __instantiate__ keyword set to True.
        """
        if kwargs.pop('__instantiate__', None) is None:
            config = self.__unbound_config__.copy()
            config.update(kwargs)
            return UnboundComponent(self.__unbound_cls__, config)
        else:
            self.__unbound_config__.update(kwargs)
            self.__dynamic_class_store__ = None
            kwargs['__instantiate__'] = True

        cls = self.__dynamic_class__
        return cls(*args, **kwargs)

    @classmethod
    def create_from_state(cls, state):
        ubc = cls(None, {})
        ubc.__setstate__(state)
        return ubc

    @property
    def __dynamic_class__(self):
        """
        If the config contains entries besides cid and slot a dynamic class is returned. This offers just in time
        creation of the actual class object to be used by epfl.
        """
        if self.__dynamic_class_store__:
            return self.__dynamic_class_store__

        stripped_conf = self.__unbound_config__.copy()
        stripped_conf.pop('cid', None)
        stripped_conf.pop('slot', None)
        if len(stripped_conf) > 0:
            conf_hash = str(stripped_conf).__hash__()
            try:
                return self.__global_dynamic_class_store__[(conf_hash, self.__unbound_cls__)]
            except KeyError:
                pass

            dynamic_class_id = epflutil.generate_dynamic_class_id()
            name = '{name}_auto_{dynamic_class_id}'.format(
                name=self.__unbound_cls__.__name__,
                dynamic_class_id=dynamic_class_id
            )
            self.__dynamic_class_store__ = type(name, (self.__unbound_cls__, ), {})
            for param in self.__unbound_config__:
                setattr(self.__dynamic_class_store__, param, self.__unbound_config__[param])
            setattr(self.__dynamic_class_store__, '___unbound_component__', self)
            self.__global_dynamic_class_store__[(conf_hash, self.__unbound_cls__)] = self.__dynamic_class_store__
            return self.__global_dynamic_class_store__[(conf_hash, self.__unbound_cls__)]

        else:
            return self.__unbound_cls__

    def register_in_transaction(self, container, slot=None, position=None):
        compo_info = {'class': self.__getstate__(),
                      'config': self.__unbound_config__,
                      'ccid': container.cid,
                      'cid': self.position[0],
                      'slot': slot}
        container.page.transaction.set_component(self.position[0], compo_info, position=position)
        return getattr(container.page, self.position[0])

    def create_by_compo_info(self, *args, **kwargs):
        """
        Expose the :func:`ComponentBase.create_by_compo_info` in order to allow storing UnboundComponent instances
        instead of raw classes. This is required in order to have dynamic classes at all with a pickling session store,
        since only static classes can be pickled. The class is setup with all dynamic attributes by
        :func:`__dynamic_class__`.
        """
        return self.__dynamic_class__.create_by_compo_info(*args, **kwargs)

    def __getstate__(self):
        """
        Pickling helper.
        """
        return self.__unbound_cls__, self.__unbound_config__, self.position

    def __setstate__(self, state):
        """
        Pickling helper.
        """
        self.__unbound_cls__, self.__unbound_config__, self.position = state

    def __eq__(self, other):
        """
        Checks class and config equality.
        """
        if type(other) is not UnboundComponent \
                or other.__unbound_cls__ != self.__unbound_cls__ \
                or other.__unbound_config__ != self.__unbound_config__:
            return False

        return True

    def __repr__(self):
        return '<UnboundComponent of {cls} with config {conf} and position {position}>'.format(
            cls=self.__unbound_cls__,
            conf=self.__unbound_config__,
            position=self.position
        )


@epflacl.epfl_acl(['access'])
class ComponentBase(object):
    """
    Components are the building-blocks of any :class:`.epflpage.Page` containing python, html, css and javascript.
    Ajax-events are sent by javascript to the server-side python-parts. They can respond by sending back javascript
    which will be executed in the browser.

    There are two kinds of html, css and javascript associated with any component: Static and dynamic.
    Static code will be loaded into the browser once per :class:`.epfltransaction.Transaction`, this is normally
    used for css and javascript. The css and javascript files are taken from the Components css_name and js_name
    respectively, both being lists of strings that are resolved via jinja2.
    Dynamic code will be loaded everytime a component is rendered to be inserted or reinserted into a new or existing
    :class:`.epfltransaction.Transaction`, this is normally used for html and javascript. The html and javascript
    files are taken from the Components string template_name and js_parts respectively, the latter being a list of
    strings that are resolved via jinja2.

    Components are instantiated every request, their state is managed by the :class:`.epflpage.Page` and stored in the
    :class:`.epfltransaction.Transaction`. To facilitate this, every component must define which of its attributes
    is to be stored in the :class:`.epfltransaction.Transaction` and which to be used as it is by default. To notify
    the :class:`.epflpage.Page` how to store and reinstantiate a Component there are two attributes: compo_state and
    compo_config

    compo_state is a list of strings naming attributes whose current and up to date value is stored into the
    :class:`.epfltransaction.Transaction` at the end of a  request by the :class:`.epflpage.Page` and loaded from the
    :class:`.epfltransaction.Transaction` at the  beginning of a request.

    As an example see the following forms input field whose value may change multiple times during an
    :class:`.epfltransaction.Transaction`, requests for example being changes uploaded via ajax.

    .. code:: python

        class InputField(ComponentBase):
            compo_state = ['value']


    compo_config: By default everything that is not in the compo_state will be the result of pythons instantiation
    process, all attributes being references to the attributes of the components class. For non trivial attributes this
    means that changes to class attributes will affect all instances of this class. compo_config offers an easy way to
    avoid this behaviour, by copying the attribute using copy.deepcopy from the class to the instance.

    """

    template_name = "empty.html"  #: Filename of the template for this component (if any).
    js_parts = []  #: List of files to be parsed as js-parts of this component.
    js_name = []  #: List of javascript files to be statically loaded with this component.
    js_name_no_bundle = []  #: List of js files to be statically loaded with this component but never in a bundle.
    css_name = []  #: List of css files to be statically loaded with this component.
    css_name_no_bundle = []  #: List of css files to be statically loaded with this component but never in a bundle.
    compo_state = []  #: List of object attributes to be persisted into the :class:`.epfltransaction.Transaction`.
    compo_config = []  #: List of attributes to be copied into instance-variables using :func:`copy.deepcopy`.

    #: Flag this component as event sink, any event will stop here if True. If no handler is found it is discarded.
    event_sink = False

    visible = True  #: Flag for component rendering. Use via :func:`set_visible` and :func:`set_hidden`.

    #: Internal reference to this Components :class:`UnboundComponent`. If it is None and something breaks because of it
    #: this component has not been correctly passed through the :func:`__new__`/:class:`UnboundComponent` pipe.
    ___unbound_component__ = None

    epfl_event_trace = None  #: Contains a list of CIDs an event bubbled through. Only available in handle\_ methods

    #: These are the compo_state-names for this ComponentBase-Class
    base_compo_state = ['visible', 'name', 'value', 'mandatory', 'validation_error', 'validators']

    is_template_element = True  #: Needed for template-reflection: this makes me a template-element (like a form-field)

    is_rendered = False  #: True if this component was rendered calling :meth:`render`
    redraw_requested = False  #: Flag if this component wants to be redrawn.

    _compo_info = None  #: Compo_info cache.
    _handles = None  #: Cache for a list of handle_event functions this component provides.
    combined_compo_state = frozenset()  #: The combined compo_state + base_compo_state
    deleted = False  #: Flag if this component has been deleted this request.

    post_event_handlers = None  #: Overwrite with a dict of post_event_handlers.

    #: True if this component has initialisation routines that prevent it from being correctly updated by
    #: :meth:`ComponentContainerBase.update_children`. It will be deleted and recreated instead.
    disable_auto_update = False

    #: New style components use the new default mechanism to update client side javascript states automatically.
    new_style_compo = False
    compo_js_params = []  #: Attributes to be provided as JS parameters.
    compo_js_extras = []  #: New style features to be activated.
    compo_js_name = 'ComponentBase'  #: Name of the JS Class.

    render_cache = None  #: If the component has been rendered this request the cache is filled.

    # Input Helper:
    value = None  #: The actual value of the input element that is posted upon form submission.

    validation_error = ''  #: Set during call of :func:`validate` with an error message if validation fails.
    validation_type = None  #: Form validation selector.
    validation_helper = []  #: Deprecated! Use proper Validators via :attr:`validators`.
    validators = []  #: List of :class:`~solute.epfl.core.epflvalidators.ValidatorBase` instances.

    #: Set to true if value has to be provided for this element in order to yield a valid form.
    mandatory = False

    name = None  #: An element without a name cannot have a value.
    default = None  #: The default value to be applied to the component upon initialisation or reset.


    @classmethod
    def add_pyramid_routes(cls, config):
        """ Adds the static pyramid routes needed by this component. This only works for native components stored in
        :mod:`solute.epfl.components`. """
        fn = inspect.getfile(cls)
        pos = fn.index("/epfl/components/")
        epos = fn.index("/", pos + 17)
        compo_path_part = fn[pos + 17: epos]

        config.add_static_view(name="epfl/components/" + compo_path_part,
                               path="solute.epfl.components:" + compo_path_part + "/static")

    @classmethod
    def create_by_compo_info(cls, page, compo_info, container_id):
        compo_obj = cls(page, compo_info['cid'], __instantiate__=True, **compo_info["config"])
        if container_id:
            container_compo = page.components[container_id]  # container should exist before their content
            compo_obj.set_container_compo(container_compo, compo_info["slot"])
            container_compo.add_component_to_slot(compo_obj, compo_info["slot"])
        return compo_obj

    def __new__(cls, *args, **config):
        """
        Calling a class derived from ComponentBase will normally return an UnboundComponent via this method unless
        __instantiate__=True has been passed as a keyword argument.

        Any component developer may thus overwrite the :func:`__init__` method without causing any problems in order to
        expose runtime settable attributes for code completion and documentation purposes.
        """
        if config.pop('__instantiate__', None) is None:
            return UnboundComponent(cls, config)

        epflutil.Discover.discover_component(cls)

        self = super(ComponentBase, cls).__new__(cls, **config)

        self.cid = args[1]
        self._set_page_obj(args[0])

        self.__config = config

        for attr_name in self.compo_config:
            if attr_name in config:
                config_value = config[attr_name]
            else:
                config_value = getattr(self, attr_name)

            setattr(self, attr_name, copy.deepcopy(config_value))  # copy from class to instance

        return self

    def __init__(self, *args, **kwargs):
        """
        Overwrite this for auto completion features on component level.
        """
        pass

    def get_state_attr(self, key, value=None):
        """Get the attribute as stored in the compo_state or return the original value. If the original value is not
        hashable - as all mutable builtins are - a copy is generated in the compo state.
        """
        try:
            return self.compo_info['compo_state'][key]
        except KeyError:
            try:
                hash(value)
            except TypeError:
                # Only the immutable builtins are hashable, mutable builtins are not and cause a TypeError.
                setattr(self, key, copy.deepcopy(value))
                return getattr(self, key, value)
            return value

    def set_state_attr(self, key, value):
        self.compo_info.setdefault('compo_state', {})[key] = value

    @property
    def compo_info(self):
        if self._compo_info is None:
            self._compo_info = self.page.transaction.get_component(self.cid)
        return self._compo_info or {}

    @property
    def position(self):
        return self.container_compo.compo_info['compo_struct'].key_index(self.cid)

    @property
    def slot(self):
        return self.compo_info['slot']

    @property
    def __unbound_component__(self):
        if self.___unbound_component__ is None:
            slot = None
            try:
                slot = getattr(self, 'slot', None)
            except KeyError:
                pass
            self.___unbound_component__ = self.__class__(cid=self.cid, slot=slot)
        return self.___unbound_component__

    @property
    def struct_dict(self):
        return self.compo_info.setdefault('compo_struct', odict())

    @property
    def container_slot(self):
        return self.compo_info.get('slot', None)

    @container_slot.setter
    def container_slot(self, value):
        self.compo_info['slot'] = value

    @property
    def container_compo(self):
        if self.compo_info.get('ccid', None) is None\
                or 'ccid' not in self.compo_info\
                or self.compo_info['ccid'] is None:
            return None
        return getattr(self.page, self.compo_info['ccid'])

    @container_compo.setter
    def container_compo(self, value):
        self.compo_info['ccid'] = value.cid

    def register_in_transaction(self, container, slot=None, position=None):
        compo_info = {'class': self.__unbound_component__.__getstate__(),
                      'config': self.__config,
                      'ccid': container.cid,
                      'cid': self.cid,
                      'slot': slot}
        self.page.transaction.set_component(self.cid, compo_info, position=position, compo_obj=self)

    def get_component_info(self):
        info = {"class": self.__unbound_component__.__getstate__(),
                "config": self.__config,
                "cid": self.cid,
                "slot": self.container_slot}
        if getattr(self, 'container_compo', None) is not None:
            info['ccid'] = self.container_compo.cid
        return info

    def _set_page_obj(self, page_obj):
        """ Will be called by __new__. Multiple initialisation-routines are called from here, so a component is only
        set up after being assigned its page.
        """
        self.page = page_obj
        self.request = page_obj.request
        self.response = page_obj.response

    def set_container_compo(self, compo_obj, slot, position=None):
        """
        Set the container_compo for this component and create any required structural information in the transaction.
        """

        self.container_compo = compo_obj
        self.container_slot = slot

    def delete_component(self):
        """ Deletes itself. You can call this method on dynamically created components. After it's deletion
        you can not use this component any longer in the layout. """
        if not self.container_compo:
            raise ValueError("Only dynamically created components can be deleted")

        if self.name:
            self.unregister_field(self)

        for compo in list(getattr(self, 'components', [])):
            compo.delete_component()

        self.page.transaction.del_component(self.cid)
        self.add_js_response('epfl.destroy_component("{cid}");'.format(cid=self.cid))

        self.page.transaction['__initialized_components__'].remove(self.cid)

    @Lifecycle(name=('component', 'finalize'))
    def finalize(self):
        """ Called from the page-object when the page is finalized
        [request-processing-flow]
        """
        pass

    def has_access(self):
        """ Checks if the current user has sufficient rights to see/access this component.
        Normally called by a condition in the jinja-template.
        """
        try:
            return self._access
        except AttributeError:
            self._access = security.has_permission("access", self, self.request)

        return self._access

    def set_visible(self):
        """ Shows the complete component. You need to redraw it!
        It returns the visibility it had before.
        """
        try:
            super(ComponentBase, self).__delattr__('_is_visible')
        except AttributeError:
            pass
        current_visibility = self.visible
        self.visible = True
        return current_visibility

    def set_hidden(self):
        """ Hides the complete component. You need to redraw it!
        It returns the visibility it had before.
        """
        try:
            del self._is_visible
        except AttributeError:
            pass
        current_visibility = self.visible
        self.visible = False
        return current_visibility

    def is_visible(self, check_parents=True):
        """ Checks wether the component should be displayed or not. This is affected by "has_access" and
        the "visible"-component-attribute.
        If check_parents is True, it also checks if the template-element-parents are all visible - so it checks
        if this compo is "really" visible to the user.
        """
        try:
            return self._is_visible
        except AttributeError:
            pass

        if not self.visible:
            self._is_visible = False
        elif not self.has_access():
            self._is_visible = False
        elif check_parents and self.container_compo is not None:
            self._is_visible = self.container_compo.is_visible()
        else:
            self._is_visible = True

        return self._is_visible

    def add_ajax_response(self, resp_string):
        """ Adds to the response some string (ajax or js or whatever the clients expects here).
        Not to be confused with self.add_js_link (which adds a js-file to the page at full-page-request-time).
        In conjunction with callback-functions to a epfl.send(event, cb_func) call consider using "return_ajax_response".
        The Callback-Function then gets the ajax-response as first argument. Do not forget to json.encode(...) the data.
        Use only if sure that this was an ajax-request. If not so sure, use "add_js_response".
        """
        self.response.add_ajax_response(resp_string)

    def return_ajax_response(self, resp_string):
        """ Nearly the same as "add_ajax_response". Only difference: Only this response is returned, nothing else.
        This is needed if you make the request with epfl.send() and use a callback to process the returned data.
        Only with this function you can be sure, that nothing else from other components is sent back.
        """
        self.response.answer_json_request(resp_string)

    def add_js_response(self, js_string):
        """ Shortcut to epflpage """
        self.page.add_js_response(js_string)

    @Lifecycle(name=('component', 'init_transaction'))
    def init_transaction(self):
        """
        This function will be called only once a transaction for this component.
        It is called just before the event-handling of the page takes place.

        You can overwrite this method to manipulate the initial state once.
        Use this to load data-objects you want to manipulate within this transaction.

        Input initialisation is handled here.

        [request-processing-flow]
        """
        if self.name:
            if self.value is None and self.default is not None:
                self.value = self.default
            self.register_field(self)

            if self.validation_type in ['email', 'text', 'number', 'float']:
                self.validators.insert(0, epflvalidators.ValidatorBase.by_name(self.validation_type)())

    @Lifecycle(name=('component', 'setup_component'))
    def setup_component(self):
        """ Called from the system every request when the component-state of all components in the page is setup. Here
        component-individual additional setup can be made. This is called after a potential call to "init_transaction".
        So no events have been handled so far.

        [request-processing-flow]
        """
        pass

    @Lifecycle(name=('component', 'after_event_handling'))
    def after_event_handling(self):
        """ Called from the system every request after all events
        for all components have been handeled.
        Here component-individual additional modifications can be made.

        [request-processing-flow]
        """
        pass

    def show_fading_message(self, msg, typ="ok"):
        """ Shortcut to epflpage.show_fading_message(msg, typ).
        typ = "info" | "ok" | "error"
        """
        return self.page.show_fading_message(msg, typ)

    def show_message(self, msg, typ="info"):
        """ Shortcut to epflpage.show_message(msg, typ)
        typ = "info" | "ok" | "error"
        """
        return self.page.show_message(msg, typ)

    def show_confirm(self, msg, cmd_ok):
        """
        Displays a box with "ok" and "cancel" to the user.
        If the user clicks "ok" the event named in "cmd_ok" will be fired.
        """
        ##todo: msg = epfli18n.get_text(msg)
        js = """if (confirm(%s)) {
                    var ev = epfl.make_component_event("%s", "%s", {});
                    epfl.send(ev);
             }""" % (json.encode(msg), self.cid, cmd_ok)

        self.page.add_js_response(js)

    def get_component_id(self):
        return self.cid

    @epflacl.epfl_has_permission('access')
    @Lifecycle(name=('component', 'handle_event'))
    def handle_event(self, event_name, event_params):
        """
        Called by the system for every ajax-event in the ajax-event-queue from the browser.
        epflpage.Page.handle_ajax_request routes the event to the corresponding component -
        identified by it´s "component_id" (self.cid).
        May be overridden by concrete components.
        """

        event_handler = getattr(self, "handle_" + event_name, None)
        epfl_event_trace = event_params.pop('epfl_event_trace', [])
        try:
            if event_handler is None:
                raise MissingEventHandlerException('Received None as event handler, have you setup an '
                                                   'event handler for %s in %s? %s' % (event_name,
                                                                                       self.__class__,
                                                                                       epfl_event_trace))
            elif not hasattr(event_handler, '__call__'):
                raise MissingEventHandlerException('Received non callable for event handling.')

            self.epfl_event_trace = epfl_event_trace
            event_handler(**event_params)
            if self.post_event_handlers and self.post_event_handlers.get(event_name, None):
                self.post_event_handling(self.post_event_handlers[event_name], event_params)
            self.epfl_event_trace = None
        except MissingEventHandlerException:
            if self.event_sink is True:
                pass
            elif self.container_compo is not None:
                event_params.setdefault('epfl_event_trace', epfl_event_trace).append(self.cid)
                self.container_compo.handle_event(event_name, event_params)
            elif event_name in ['drag_stop', 'drop_accepts']:
                pass
            else:
                raise

    def post_event_handling(self, post_event_handlers, event_params):
        """Receives a post_event_handlers object and execute all callables found with event_params. epfl_event_trace
         argument is still available at this time.

        :param post_event_handlers: Either a string with a function name, tuple of cid and function name, or a list\n
                                    of multiple of the previous two.
        :param event_params: The original parameters of the previously called event.
        """
        if type(post_event_handlers) is str:
            cid, post_event = self.cid, post_event_handlers
        elif type(post_event_handlers) is tuple:
            cid, post_event = post_event_handlers
        elif type(post_event_handlers) is list:
            for entry in post_event_handlers:
                self.post_event_handling(entry, event_params)
            return
        else:
            raise Exception('Programming Error: Unknown post event handler type.')

        try:
            post_event_callable = getattr(self.page.components[cid], 'on_%s' % post_event)
        except AttributeError:
            raise Exception('Programming Error: Component {cid} has no post event handler named {post_event}.'.format(
                cid=cid, post_event=post_event
            ))

        post_event_callable(**event_params)

    def get_render_environment(self, env):
        """
        Creates a dictionary containing a reference to the component that is used as render kwargs.
        """
        return {'compo': self}

    def reset_render_cache(self, recursive=False):
        self.render_cache = None
        if recursive and hasattr(self, 'components'):
            for compo in self.components:
                compo.reset_render_cache(recursive=recursive)

    def render(self, target='main'):
        """Called to render this component including all potential sub components.

        .. graphviz::

            digraph foo {
                "ComponentBase.render" -> "not ComponentBase.is_visible" -> "jinja2.Markup";
                "ComponentBase.render" -> "ComponentBase.is_visible" -> "render sub component js";
                "render sub component js" -> "Request.get_epfl_jinja2_environment" ->
                "ComponentBase.get_compo_init_js" ->
                "ComponentBase.get_render_environment" -> "ComponentRenderEnvironment" ->
                "ComponentBase.js_parts" -> "jinja2.Markup";
                "ComponentRenderEnvironment" -> "ComponentBase.main" -> "jinja2.Markup";
            }
        """

        if self.render_cache is not None:
            return self.render_cache[target]

        self.render_cache = {'main': '', 'js': '', 'js_raw': ''}

        if not self.is_visible():
            # this is the container where the component can be placed if visible afterwards
            self.render_cache['main'] = jinja2.Markup("<div epflid='{cid}'></div>".format(cid=self.cid))
            return self.render_cache[target]

        js_raw = []

        if hasattr(self, 'components'):
            for compo in self.components:
                compo.render()
                js_raw.append(compo.render(target='js_raw'))

        self.is_rendered = True

        # Prepare the environment and output of the render process.
        env = self.request.get_epfl_jinja2_environment()

        context = self.get_render_environment(env)

        js_raw.append(self.get_compo_init_js())

        for js_part in self.js_parts:
            # Render context can be supplied as a dict.
            js_raw.append(env.get_template(js_part).render(context))

        template = env.get_template(self.template_name)
        rendered_data = template.render(context)
        rendered_data = rendered_data.strip()
        self.render_cache['main'] = jinja2.Markup(rendered_data)

        handles = self.get_handles()
        if handles:
            set_component_info = 'epfl.set_component_info("%(cid)s", "handle", %(handles)s);'
            set_component_info %= {'cid': self.cid,
                                   'handles': handles}
            js_raw.append(set_component_info)

        self.render_cache['js_raw'] = ''.join(js_raw)
        self.render_cache['js'] = jinja2.Markup('<script type="text/javascript">%s</script>'
                                                % self.render_cache['js_raw'])

        return self.render_cache[target]

    @classmethod
    def discover(cls):
        """Handles one time actions on this specific class. Should only be called once per individual class.
        """
        cls.set_handles(force_update=True)
        cls.combined_compo_state = set(cls.compo_state + cls.base_compo_state)

        for name in cls.combined_compo_state:
            original = getattr(cls, name, None)
            if type(original) is property:
                continue

            setattr(cls, '__original_attribute_%s' % name, original)

            def getter(n):
                return lambda self: self.get_state_attr(n, getattr(self, '__original_attribute_%s' % n))

            def setter(n):
                return lambda self, value: self.set_state_attr(n, value)

            setattr(cls, name, property(
                fget=getter(name),
                fset=setter(name),
            ))

        if hasattr(cls, 'request_handle_submit'):
            raise Exception('Deprecated Feature: Submit requests are no longer supported by EPFL.')

        if not cls.template_name:
            raise Exception("You did not setup the 'self.template_name' in " + repr(cls))

        if hasattr(cls, 'cid'):
            raise Exception("You illegally set a cid as a class attribute in " + repr(cls))

    @classmethod
    def set_handles(cls, force_update=True):
        """Put the names of all handle functions this class provides into a list that can be supplied to the javascript.
        This allows the client side epfl parts to be aware of which component actually handles which events.

        :param force_update: If True the handles will be set anew irregardless of whether they have been set before.
        """
        if cls._handles is None or force_update:
            cls._handles = []
            for name in dir(cls):
                if not name.startswith('handle_') or name == 'handle_event':
                    continue
                cls._handles.append(name[7:])

    def get_handles(self):
        self.set_handles(False)
        return self._handles

    def redraw(self, parts=None):
        """ This requests a redraw. All components that are requested to be redrawn are redrawn when
        the ajax-response is generated (namely page.handle_ajax_request()).
        You can specify the parts that need to be redrawn (as string, as list or None for the complete component).
        If a super-element (speaking of template-elements) of this component wants to be redrawn -
        this one will not request it's redrawing.
        """

        if parts is not None:
            raise Exception('Deprecated: Partial redraws are no longer possible.')

        self.redraw_requested = True

    def __call__(self, *args, **kwargs):
        """ For direct invocation from the jinja-template. the args and kwargs are also provided by the template """
        return self.render(*args, **kwargs)

    @Lifecycle(name=('component', 'compo_destruct'))
    def compo_destruct(self):
        """ Called before destruction of this component by a container component.

        [request-processing-flow]
        """
        pass

    def switch_component(self, target, cid, slot=None, position=None):
        """
        Switches a component from its current location (whatever component it may reside in at that time) and move it to
        slot and position in the component determined by the cid in target. Largely handled by the identically named
        :meth:`epfltransaction.Transaction.switch_component` method. Calls the js function epfl.switch_component in AJAX
        requests.

        :param target: The cid of the target the element with cid is to be moved to.
        :param cid: The cid of the element to be moved.
        :param slot: Deprecated.
        :param position: Position the moved element is to hold in the target container.
        """

        if slot is not None:
            raise DeprecationWarning('The slot parameter is no longer supported on this method. You can change the slot'
                                     ' attribute on the component directly.')

        if self.page.request.is_xhr:
            self.add_js_response('epfl.switch_component("{cid}");'.format(cid=cid))
        self.page.transaction.switch_component(cid, target, position=position)

    @classmethod
    def check_new_style_js_parts(cls):
        if not cls.js_parts:
            return

        inherited_cls = cls.__bases__[0]
        if inherited_cls.new_style_compo == cls.new_style_compo:
            return inherited_cls.check_new_style_js_parts()

        if inherited_cls.js_parts is cls.js_parts:
            raise Exception(
                'CompatibilityError: You have inherited a non empty js_parts attribute on a new style component %s. '
                'Set your own new_style_compo compliant js_parts attribute or set new_style_compo to False.'
                % cls
            )

    def get_compo_init_js(self):
        if not self.new_style_compo:
            return ''

        self.check_new_style_js_parts()

        params = {}
        for param_name in self.compo_js_params:
            params[param_name] = getattr(self, param_name)

        for param_name in self.compo_js_extras:
            params['extras_%s' % param_name] = True

        return 'epfl.init_component("{cid}", "{compo_cls}", {params});'.format(
            cid=self.cid,
            compo_cls=self.compo_js_name,
            params=json.encode(params)
        )

    def handle_reinitialize(self):
        """Deletes the component and recreates it at the same position with the same cid it had before.
        Requires a component that has a container component!
        """
        if not self.container_compo:
            raise Exception('Tried using handle_reinitialize on a component without a container component.')
        position, slot, cid, ubc = self.position, self.slot, self.cid, self.__unbound_component__
        self.delete_component()
        self.container_compo.add_component(ubc(cid=cid, slot=slot), position=position)
        self.container_compo.redraw()

    ###########################
    # Start of value handling #
    ###########################

    def handle_change(self, value):
        """Default handle method to update a value. Will rebubble if the current component is not a valid carrier for a
        value.
        """
        if self.name is None:
            raise MissingEventHandlerException
        self.value = value

    def register_field(self, field):
        """Recursive lookup to find a component that considers itself a valid field registration target and register
        with it.
        """
        if self.container_compo:
            self.container_compo.register_field(field)

    def unregister_field(self, field):
        """Recursive lookup to find a component that considers itself a valid field unregistration target and unregister
        from there.
        """
        if self.container_compo:
            self.container_compo.unregister_field(field)

    def get_parent_form(self):
        """Recursive lookup to find a component that considers it self a form, courtesy of having a get_parent_form
        method that stops the bubbling by returning itself or a form instance.
        """
        if self.container_compo:
            return self.container_compo.get_parent_form()

    @staticmethod
    def reset():
        """Originally was used to reset the value of a FormInputBase element. Deprecated in favor of set_to_default for
        clearer naming.
        """
        raise DeprecationWarning("Reset function is deprecated use set_to_default instead.")

    def set_to_default(self):
        """Initialize the field with its default value and clear all validation error messages.
        """
        if self.default is not None:
            self.value = self.default
        else:
            self.value = None
        self.validation_error = ""

    def validate(self):
        """Recursive validation of components starting from this component and continuing over all visible child components.
        """
        validation_result = True
        if hasattr(self, 'components'):
            for compo in self.components:
                if not compo.is_visible(check_parents=False):
                    continue
                validation_result &= compo.validate()
        if self.name is not None and self.is_visible():
            validation_result &= self._validate()

        return validation_result

    def _validate(self):
        """
        Validate the value and return True if it is correct or False if not. Set error messages to self.validation_error
        """
        result, text = True, []

        # Deprecated!
        for helper in self.validation_helper:
            if not result:
                break
            result = helper[0](self)
            text.append(helper[1])
        # /Deprecated!

        for validator in self.validators:
            if validator(self) is False:
                text.append(validator.error_message)
                result = False

        if result is False and text:
            self.redraw()
            self.validation_error = '\n'.join(text)
            return False

        # If a previous validation failed the existing validation error needs to be erased from both the rendered html
        # and the compo_state.
        if self.validation_error:
            self.redraw()
        self.validation_error = ''

        return True

    def get_values(self):
        """Recursive lookup to find all values including this components value and all component values below.
        """
        out = {}
        if hasattr(self, 'components'):
            for compo in self.components:
                out.update(compo.get_values())

        if self.name is not None:
            out[self.name] = self.get_value()

        return out

    def get_value(self):
        """
        Return the field value without conversions.
        """
        return self.value

    #########################
    # End of value handling #
    #########################


class ComponentContainerBase(ComponentBase):
    """
    This component automatically adds components based on the UnboundComponent objects its node_list contains once per
    transaction.

    Components inheriting from it can overwrite init_struct in order to dynamically return different lists per
    transaction instead of one static list for the lifetime of the epfl service.
    """
    template_name = 'tree_base.html'
    theme_path_default = 'container/default_theme'
    #: List of folders to check for additional theme parts. May inherit from or extend previous themes by using < for
    #: extending ({{ caller() }} will be the previous template) or > for inheriting (result of the last template will be
    #: placed as {{ caller() }} inside the previous template).
    theme_path = []

    #: Used to generate the children of this component.
    node_list = []

    compo_config = ['node_list']
    compo_state = ['row_offset', 'row_limit', 'row_count', 'row_data']

    default_child_cls = None
    data_interface = {'id': None}

    row_offset = 0  #: Offset for get_data calls.
    row_limit = 30  #: Limit for get_data calls.
    row_data = {}  #: Adaptable data store for get_data calls.
    row_count = 30  #: Count of currently loaded rows, should be set by get_data.

    #: Updates are triggered every request in after_event_handling if True.
    auto_update_children = True
    #: Update is triggered initially in :meth:`init_transaction` if True
    auto_initialize_children = True

    #: True if update children has been called at least once. Will be used for duplicate call prevention.
    __update_children_done__ = False

    #: True if the child components of this component have been initialized.
    components_initialized = False

    def __new__(cls, *args, **kwargs):
        self = super(ComponentContainerBase, cls).__new__(cls, *args, **kwargs)
        if isinstance(self, cls):
            self.setup_component_slots()

        return self

    def get_themed_template(self, env, target):
        """
        Return a list of templates in the order they should be used for rendering. Deals with template inheritance based
        on the theme_path and the target templates found in the folders of the theme_path.
        """
        theme_paths = self.theme_path
        if type(theme_paths) is dict:
            theme_paths = theme_paths.get(target, theme_paths['default'])
        render_funcs = []
        direction = '<'
        for theme_path in reversed(theme_paths):
            try:
                if theme_path[0] in ['<', '>']:
                    direction = theme_path[0]
                    render_funcs.insert(0, env.get_template('%s/%s.html' % (theme_path[1:], target)).module.render)
                    continue
                tpl = env.get_template('%s/%s.html' % (theme_path, target))
                render_funcs.append(tpl.module.render)
                return direction, render_funcs
            except TemplateNotFound:
                continue

        tpl = env.get_template('%s/%s.html' % (self.theme_path_default, target))
        render_funcs.append(tpl.module.render)

        return direction, render_funcs

    def get_render_environment(self, env):
        """
        Creates a dictionary containing references to the different theme parts and the component. Theme parts are
        wrapped as callables containing their respective inheritance chains as defined by :attr:`theme_path`.
        """
        return ComponentRenderEnvironment(self, env)

    @Lifecycle(name=('container_component', 'after_event_handling'))
    def after_event_handling(self):
        """
        After all events have been handled :meth:`update_children` is executed once for components that follow
        the :meth:`get_data` pattern.
        """
        super(ComponentContainerBase, self).after_event_handling()
        if self.auto_update_children:
            self.update_children(force=True)

    def is_smart(self):
        """Returns true if component uses get_data scheme."""
        return self.default_child_cls is not None

    def update_children(self, force=False):
        """If a default_child_cls has been set this updates all child components to reflect the current state from
        get_data(). Will raise an exception if called twice without the force parameter present."""

        if self.__update_children_done__ and not force:
            raise Exception('update_children called twice without force parameter for component %s.' % self.cid)
        self.__update_children_done__ = True

        if not self.is_smart():
            return

        data = self._get_data(self.row_offset, self.row_limit, self.row_data)

        tipping_point = len([c for c in self.components if not hasattr(c, 'id')])

        current_order = []
        new_order = []

        data_dict = {}
        data_cid_dict = {}

        for v in self.components:
            if getattr(v, 'id', None) is None:
                continue
            current_order.append(v.id)
            data_cid_dict[v.id] = v.cid

        for i, d in enumerate(data):
            new_order.append(d['id'])
            data_dict[d['id']] = d

        # IDs of components no longer present in data. Their matching components are deleted.
        for data_id in set(current_order).difference(new_order):
            self.del_component(data_cid_dict.pop(data_id))
            self.redraw()

        # IDs of data represented by a component. Matching components are updated.
        for data_id in set(new_order).intersection(current_order):
            compo = getattr(self.page, data_cid_dict[data_id])
            # A component may decide that it can not be updated by this mechanism. Relevant for components doing heavy
            # lifting in their :meth:`ComponentBase.init_transaction`.
            if compo.disable_auto_update:
                self.del_component(data_cid_dict.pop(data_id))
                current_order.remove(data_id)
                self.redraw()
                continue
            for k, v in data_dict[data_id].items():
                if getattr(compo, k) != v:
                    setattr(compo, k, v)
                    compo.redraw()

        # IDs of data not yet represented by a component. Matching components are created.
        for data_id in set(new_order).difference(current_order):
            position = new_order.index(data_id)
            if position > len(self.components):
                position = None
            ubc = self.default_child_cls(**data_dict[data_id])
            bc = self.add_component(ubc, position=position)
            data_cid_dict[data_id] = bc.cid

            self.redraw()

        # Rebuild order.
        compo_struct = self.compo_info['compo_struct']
        for i, data_id in enumerate(new_order):
            try:
                key = compo_struct.keys()[i + tipping_point]
                if compo_struct[key].get('config', {}).get('id', None) != data_id:
                    self.switch_component(self.cid, data_cid_dict[data_id], position=i + tipping_point)
                    self.redraw()
            except AttributeError:
                pass

    def _get_data(self, *args, **kwargs):
        """
        Internal wrapper for :meth:`get_data` to decide wether it is to be called as a function or only contains a
        reference to a model on :attr:`.epflpage.Page.model`.
        """
        # get_data is a string pointing to a model load function.
        if type(self.get_data) is str and self.page.model is not None:
            return self.page.model.get(self, self.get_data, (args, kwargs), self.data_interface)
        # get_data is a tuple with a string or integer pointing to a model and a string pointing to a model load
        # function.
        elif type(self.get_data) is tuple and self.page.model is not None:
            return self.page.model[self.get_data[0]].get(self, self.get_data[1], (args, kwargs), self.data_interface)
        # default: get_data is a callable.
        return self.get_data(*args, **kwargs)

    def get_data(self, row_offset=None, row_limit=None, row_data=None):
        """ Overwrite this method to automatically provide data to this components children.

        The list must comprise of dict like data objects with an id key. The data objects will be used as parameters for
        the creation of a default_child_cls component.

        May also be overwritten with a method selector string linking to a load\_ method of a page model or a tuple
        containing a model selector and a method selector.
        """
        return []

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        """
        Default handler to deal with setting row offset, limit and data parameters.
        """
        self.row_offset, self.row_limit, self.row_data = row_offset, row_limit, row_data

    def init_struct(self):
        """
        Called before the :attr:`node_list` is used to create the sub structures of this component.
        """
        pass

    @Lifecycle(name=('container_component', 'init_transaction'))
    def init_transaction(self):
        """
        Components derived from :class:`ComponentContainerBase` will use their :attr:`node_list` to generate their
        children automatically. After initial setup :meth:`update_children` is executed once for components that follow
        the :meth:`get_data` pattern.
        """
        super(ComponentContainerBase, self).init_transaction()

        self.node_list = self.init_struct() or self.node_list  # if init_struct returns None, keep original value.
        for node in self.node_list:
            cid, slot = node.position
            self.add_component(node(self.page, cid, __instantiate__=True),
                               slot=slot,
                               cid=cid)

        if self.auto_initialize_children:
            self.update_children(force=True)

    def replace_component(self, old_compo_obj, new_compo_obj):
        """Replace a component with a new one. Handles deletion bot keeping position and cid the same."""
        cid = old_compo_obj.cid
        position = self.components.index(old_compo_obj)
        old_compo_obj.delete_component()
        return self.add_component(new_compo_obj(cid=cid), position=position)

    def add_component(self, compo_obj, slot=None, cid=None, position=None):
        """ You can call this function to add a component to its container.
        slot is an optional parameter to allow for more complex components, cid will be used if no cid is set to
        compo_obj, position can be used to insert at a specific location.
        """

        if isinstance(compo_obj, UnboundComponent):
            cid, slot = compo_obj.position
            compo_obj = compo_obj.register_in_transaction(self, slot, position=position)
        else:
            # Generate UUID if no cid has been set previously.
            if not cid:
                cid = epflutil.generate_cid()
            compo_obj.register_in_transaction(self, slot, position=position)

        # the transaction-setup has to be redone because the component can be displayed directly in this request.
        compo_obj.init_transaction()
        self.page.transaction['__initialized_components__'].add(cid)
        if ('page', 'handle_transaction') not in Lifecycle.get_state():
            compo_obj.setup_component()

        return compo_obj

    def setup_component_slots(self):
        """ Overwrite me. This method must initialize the slots that this
        container-component provides to accumulate components """
        self.components = ComponentList(self)

    def add_component_to_slot(self, compo_obj, slot, position=None):
        """ This method must fill the correct slot with the component """
        if position is not None:
            self.components.insert(position, compo_obj)
        else:
            self.components.append(compo_obj)

    def del_component(self, cid, slot=None):
        """
        Removes the component from the slot and form the compo_info. Accepts either a component instance or a cid.
        """
        return getattr(self.page, cid).delete_component()


class ComponentList(MutableSequence):
    """

    """

    def __init__(self, container_compo):
        self.container_compo = container_compo

    def __setitem__(self, index, value):
        pass

    def insert(self, index, value):
        pass

    def __len__(self):
        return len(self.container_compo.struct_dict)

    def __getitem__(self, index):
        try:
            return self.container_compo.page.transaction.get_component_instance(
                self.container_compo.page,
                self.container_compo.struct_dict._keys[index]
            )
        except Exception as e:
            e.message += '\nParent cid was %s.' % self.container_compo.cid
            raise e

    def __delitem__(self, index):
        pass
