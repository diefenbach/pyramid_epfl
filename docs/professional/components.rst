.. components:

EPFL components
===============

At its core EPFL components are a simple thing: They have visual code, are filled with data and then interact with that
data and its sources based on user interaction. While simple on the outside the number of convenience layers complicates
handling components in the core to a somewhat large degree.

Binding components
------------------

.. code-block:: python

    class MyRootNode(ComponentContainerBase):
        node_list = [
            Box(
                cid='my_box',
                title='My Box!'
            )
        ]

        def setup_component(self):
            print self.page.my_box

    @view_config(route_name='data')
    class MyPage(Page):
         root_node = MyRootNode()

You have seen this time and again, as a developer using EPFL or even as a component developer what is going on here is
not of great importance to you. Inside the core however there's a lot going on. Depending on where you got Box from this
could take three separate ways until it actually ends up as a bound and initialized component available via
self.page.my_box. Let's take a look where this all starts: In the :class:`solute.epfl.core.epflpage.Page`.

.. code-block:: python

    def setup_components(self):
        """
        Overwrite this function!
        In this method all components needed by this page must be initialized and assigned to the page (self). It is
        called only once per transaction to register the "static" components of this page. No need to call this (super)
        method in derived classes.

        [request-processing-flow]
        """
        self.root_node = self.root_node(self, 'root_node', __instantiate__=True)

The oddity is easily visible: __instantiate__. Unless you deviated quite far from best practices you probably have never
seen this flag used when calling a component before. It is used only if you are assigning a component to a
:class:`~solute.epfl.core.epflpage.Page` statically.

Looking under the hood of this call you'll first have to figure out what you are actually dealing with in
self.root_node. It might be any of two things, an |unbound_compo| instance or a |compo_base| class object.

Usually you'd find an |unbound_compo| instance and not a sub-class of |compo_base|. This is due to a simple trick:

.. code-block:: python

    def __new__(cls, *args, **config):
        """
        Calling a class derived from ComponentBase will normally return an UnboundComponent via this method unless
        __instantiate__=True has been passed as a keyword argument.

        Any component developer may thus overwrite the :func:`__init__` method without causing any problems in order to
        expose runtime settable attributes for code completion and documentation purposes.
        """
        if config.pop('__instantiate__', None) is None:
            return UnboundComponent(cls, config)
        [...]

Any sub-class of |compo_base| will yield an |unbound_compo| instance if called without that parameter. So there's a huge
difference between those two:

+-----------------------------+-----------------------------+
|.. code-block:: python       |.. code-block:: python       |
|                             |                             |
|    root_node = MyRootNode() |    root_node = MyRootNode   |
+-----------------------------+-----------------------------+
| an |unbound_compo| instance | and a |compo_base| sub-class|
+-----------------------------+-----------------------------+

Thus when defining components you are usually working with |unbound_compo| instances. Those will be converted to
|compo_base| instances during the :meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.init_transaction`
call of any :class:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase` sub-class. So there's two ways to follow
for the call of :meth:`solute.epfl.core.epflpage.Page.setup_components`.

Any |unbound_compo| instance is a callable, thus the instantiation will be handled by
:meth:`~solute.epfl.core.epflcomponentbase.UnboundComponent.__call__`.

.. code-block:: python

    # solute/epfl/core/epflcomponentbase.py
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

If no instantiation is in process calling any |unbound_compo| will simply return a new instance with its config updated.
Otherwise this updates the configuration, empties the
:attr:`~solute.epfl.core.epflcomponentbase.UnboundComponent.__dynamic_class_store__` then uses the property
:attr:`~solute.epfl.core.epflcomponentbase.UnboundComponent.__dynamic_class__` to dynamically generate a python
type-class that is then used to create an instance of this |compo_base| sub-class.

.. _dynamic_type_classes:

Dynamic Type Classes
--------------------
You probably are aware of the possibility to create such a class, so here's what EPFL does:
 1. Check if this |unbound_compo| has already generated its actual class and return it if possible.

    .. code-block:: python

        @property
        def __dynamic_class__(self):
            """
            If the config contains entries besides cid and slot a dynamic class is returned. This offers just in time
            creation of the actual class object to be used by epfl.
            """
            if self.__dynamic_class_store__:
                return self.__dynamic_class_store__

 2. Check if the config actually requires generating a dynamic class, return base class if not.

    .. code-block:: python

            stripped_conf = self.__unbound_config__.copy()
            stripped_conf.pop('cid', None)
            stripped_conf.pop('slot', None)
            if len(stripped_conf) > 0:
                [...]
            else:
                return self.__unbound_cls__

 3. Generate a dynamic class id, a name based on that and the original class name.

    .. code-block:: python

                name = self.__unbound_cls__.__name__ + '_auto_' + generate_dynamic_class_id()

 4. Create the actual class of this |unbound_compo| with the given config.

    .. code-block:: python

                self.__dynamic_class_store__ = type(name, (self.__unbound_cls__, ), self.__unbound_config__)

 5. Assign necessary attributes and return it.

    .. code-block:: python

                setattr(self.__dynamic_class_store__, '___unbound_component__', self)
                setattr(self.__dynamic_class_store__, '__epfl_do_not_track', True)

                return self.__dynamic_class_store__

Component instantiation
-----------------------
Let's take a closer look at what happens in the __new__ method of |compo_base|.

The discover mechanism
``````````````````````

.. code-block:: python

        epflutil.Discover.discover_class(cls)

This call has many implications, usually it shouldn't do anything, since most actual classes will be well known to EPFL
from its initial discovery process. With :ref:`dynamic_type_classes` however this actually executes some very important
steps in order to get a usable component. We will only take a look at the direct implications to the component at this
time. A more complete overview of what is happening here and its context can be found here: :ref:`setting_up`

The only immediate consequence of this call is a possible call to
:meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.discover` which does several important jobs.

Housekeeping
............
Some functions are no longer available in the epfl core, and some errors are difficult to catch at runtimes. In order to
avoid those a set of prohibitions is hardwired into the discover methods. Specifically:

.. code-block:: python

        if not cls.template_name:
            raise Exception("You did not setup the 'self.template_name' in " + repr(cls))

        if hasattr(cls, 'cid'):
            raise Exception("You illegally set a cid as a class attribute in " + repr(cls))

Other prohibitions may apply but can not be handled here. Overall it is considered best practice to check for such at
this stage since it prevents EPFL from starting up at all, instead of only producing exceptions during certain requests.

Setting up the Component State
..............................
The attribute names listed in the :attr:`~solute.epfl.core.epflcomponentbase.ComponentBase.compo_state` and
:attr:`~solute.epfl.core.epflcomponentbase.ComponentBase.base_compo_state` originally were kept up to date against the
:class:`~solute.epfl.core.epfltransaction.Transaction` by means of overwriting the __getattribute__ function. This
however proved to be a major performance pitfall. Since using this process was no longer possible the recently
implemented discovery mechanism was utilized to make the server side state work with very good performance.

In a nutshell, the original attribute value is preserved in a python descriptor instance
(:class:`~solute.epfl.core.epflcomponentbase.CompoStateAttribute`). The original attribute value
is then replaced by this instance which accesses the transaction using
:meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.get_state_attr` and
:meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.set_state_attr`.

Generating a usable object instance
```````````````````````````````````

.. code-block:: python

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

This part is straight forward thankfully. The original __new__ mechanism is used to create an instance of the class
provided by the :class:`~solute.epfl.core.epflcomponentbase.UnboundComponent`. The cid and page object are set to the
instance and the config is stored. Finally the component config attributes are copied to destroy any possible
references that might taint the objects stored there.

.. |unbound_compo| replace:: :class:`~solute.epfl.core.epflcomponentbase.UnboundComponent`
.. |compo_base| replace:: :class:`~solute.epfl.core.epflcomponentbase.ComponentBase`

.. _Traversal: http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/traversal.html
.. _`URL Dispatch`: http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/urldispatch.html
.. _odict: https://github.com/therealfakemoot/collections2
.. _collections2: https://github.com/therealfakemoot/collections2
