class TypedProperty:

    def __init__(self, name, type_):
        self.name = name
        self.type = type_

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('Expected an {} for {}'.format(self.type, self.name))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError('Attribute cann\'t be remove')


class Structure:
    _fields = {}

    def __init__(self, **kwargs):

        for name, type_ in self._fields.items():
            setattr(self.__class__, name, TypedProperty(name, type_))
            setattr(self, name, kwargs.pop(name, type_()))
        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

    def dict(self):
        """
        :return: All data for model
        """
        return {name: self.__getattribute__(name) for name in self._fields.keys()}

    def __str__(self):
        return "{!s}".format(self.dict()).replace("''", "None").replace("'", "").strip("{}")

    def __repr__(self):
        return "{!r}".format(self.__class__)
