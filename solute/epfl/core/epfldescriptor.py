class Descriptor(object):
    def __init__(self):
        raise NotImplementedError('You have to implement the __init__ method of the Descriptor!')

    def __get__(self, obj, cls):
        raise NotImplementedError('You have to implement the __get__ method of the Descriptor!')

    def __set__(self, obj, value):
        raise NotImplementedError('You have to implement the __set__ method of the Descriptor!')

    def __getstate__(self):
        raise NotImplementedError('You have to implement the pickle __getstate__ method of the Descriptor!')

    def __setstate__(self, state):
        raise NotImplementedError('You have to implement the pickle __setstate__ method of the Descriptor!')

    def __eq__(self, other):
        raise NotImplementedError('You have to implement the __eq__ method of the Descriptor!')


class Reference(Descriptor):
    def __init__(self, target=None, parent=None):
        self.target = target
        self.parent = parent

    @property
    def container_compo(self):
        return Reference('container_compo', self)

    @property
    def page(self):
        return Reference('page', self)

    def __getattr__(self, item):
        if item == '__value':
            raise AttributeError()
        return Reference(item, self)

    def __get__(self, instance, owner):
        if instance is None or isinstance(instance, CompoStateAttribute):
            return self

        if hasattr(self, '__value'):
            return self.__value

        if self.target == 'container_compo':
            return self.parent.__get__(instance, owner).container_compo
        if self.target == 'page':
            return self.parent.__get__(instance, owner).page
        if self.target is not None:
            return getattr(self.parent.__get__(instance, owner), self.target)
        return instance

    def __set__(self, instance, value):
        self.__value = value

    def __getstate__(self):
        value = AttributeError
        if hasattr(self, '__value'):
            value = self.__value
        return self.target, self.parent, value

    def __setstate__(self, state):
        self.target, self.parent, value = state
        if value is not AttributeError:
            self.__value = value

    def __repr__(self):
        if self.target is None and self.parent is None:
            return '<Ref base reflection>'
        return '<Ref %r on %r>' % (self.target, self.parent)

    def __eq__(self, other):
        if isinstance(other, Reference):
            return repr(self) == repr(other)
        return False


class CompoStateAttribute(object):
    """Descriptor for component state attributes.
    """

    def __init__(self, initial_value=None, name='var'):
        """Wrapper to provide just in time access to the compo state in the transaction,

        :param initial_value: The initial value of this compo state attribute.
        :param name: The name of this compo state attribute.
        """
        self.initial_value = initial_value
        self.name = name
        self.type = CompoStateAttribute

    def __get__(self, obj, cls):
        if obj:
            return obj.get_state_attr(self.name, self.initial_value)
        return self

    def __set__(self, obj, value):
        return obj.set_state_attr(self.name, value)