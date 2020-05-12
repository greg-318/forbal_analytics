from DataBase import mongo_default as mongod


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
            try:
                instance.__dict__[self.name] = self.type(value)
                return
            except:
                raise TypeError('Expected an {} for {}'.format(self.type, self.name))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError('Attribute cann\'t be remove')


class Structure:
    _fields = {}
    _collection = {"name": "", "key": ""}
    _teams = []
    _teamindicators = []
    _gameindicators = []
    _players = []
    _noneList = []

    def __init__(self, **kwargs):
        {
            True: self.__class__._noneList.append,
            "teams" == self.__class__.__name__.lower(): self.__class__._teams.append,
            "teamindicators" == self.__class__.__name__.lower(): self.__class__._teamindicators.append,
            "gameindicators" == self.__class__.__name__.lower(): self.__class__._gameindicators.append,
            "players" == self.__class__.__name__.lower(): self.__class__._players.append,

         }[True](self)

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

    def sendToMongo(self):
        """
        :return: Response from mongo
        """
        if not self._collection["name"]:
            raise TypeError("Method don't work for this model")

        with mongod.MongoDefault(self._collection["name"]) as md:
            value_to = self.dict()
            key = self._collection["key"]
            response = md.insertUpdate(value_to[key], value_to)
            return response

    def getFromMongo(self, dict):
        removeFrom = ("_id", "datetime")
        with mongod.MongoDefault(self._collection["name"]) as md:
            response = md.select(dict)
            if response:
                res = next(response)
                tuple(res.pop(x) for x in removeFrom)
                [Structure._gameindicators.pop(index) for index, item in enumerate(Structure._gameindicators)
                 if self is item]
                self.__init__(**res)

    def __str__(self):
        return "{!s}".format(self.dict()).replace("''", "None").replace("'", "").strip("{}")

    def __repr__(self):
        return "{!r}".format(self.__class__)
