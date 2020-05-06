class Structure:
    _fields = []
    _type = []

    def __init__(self, **kwargs):

        for name, type_ in zip(self._fields, self._type):
            setattr(self, name, kwargs.pop(name, type_))

        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

    def dict(self):
        """
        :return: All data for model
        """
        return {name: self.__getattribute__(name) for name in self.__class__._fields}
