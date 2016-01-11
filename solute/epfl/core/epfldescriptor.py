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

    def __deepcopy__(self, memo):
        raise NotImplementedError('You have to implement the __deepcopy__ method of the Descriptor!')

    def __eq__(self, other):
        """This method has to be implemented in order for the transaction to correctly recognize equivalence. Instances
        generated from equal state must always equal themselves, else the transaction initialisation fails.
        """
        raise NotImplementedError('You have to implement the __eq__ method of the Descriptor!')


class Reference(Descriptor):
    def __init__(self, target=None, parent=None):
        self.target = target
        self.parent = parent

    @property
    def container_compo(self):
        """Same behavior as :meth:`__getattr__`, primarily present as autocomplete helper.
        """
        return Reference('container_compo', self)

    @property
    def page(self):
        """Same behavior as :meth:`__getattr__`, primarily present as autocomplete helper.
        """
        return Reference('page', self)

    def __getattr__(self, item):
        """This allows for free attribute names to be accessed, even chained, on a reflection. Only __value is a special
        case, since it not being present (thus being searched using this function) makes the AttributeError mandatory.
        You may change this behavior in order to implement storage chains using :class:`Reference`.
        """
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
        """Sets a shadow value to the private attribute __value. This method may be overwritten or expanded in order to
        implement storage chains.
        """
        raise NotImplementedError("This method is not yet supported.")

    def __getstate__(self):
        value = AttributeError
        if hasattr(self, '__value'):
            value = self.__value
        return self.target, self.parent, value

    def __setstate__(self, state):
        self.target, self.parent, value = state
        if value is not AttributeError:
            self.__value = value

    def __deepcopy__(self, memo):
        copy = Reference()
        copy.__setstate__(self.__getstate__())
        return copy

    def __repr__(self):
        """Reflections should always behave the same, no matter what instance you have. If the path of the reflection
        is equal, their behavior has to be identical. No id(obj) is thus used in their representation.
        """
        if self.target is None and self.parent is None:
            return '<Ref base reflection>'
        return '<Ref %r on %r>' % (self.target, self.parent)

    def __eq__(self, other):
        """Reflections are equivalent if their pickled state is equivalent. Overall behavior is instance independent.
        """
        if isinstance(other, Reference):
            return self.__getstate__() == other.__getstate__()
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
