from re import match

__author__ = 'PHo'


class Model(object):
    """Base class for all model classes. Provides common operations for these classes."""

    def __init__(self, items):
        super(Model, self).__init__()
        self.__reader = None
        self.__writer = None
        self.__items = items

    def __str__(self):
        return "%s %s" % (repr(self), str(self.__items))

    def setAttribute(self, name, value):
        """
        sets value to attribute
        """

        if name in self.__items.keys():
            constraint = self.__items[name]["constraint"]
            if match(constraint, str(value)):
                self.__items[name]["value"] = value
                return value
            else:
                raise ValueError, "Format of value of %s is not correct" % name
        else:
            raise ValueError, "No such attribute: '%s'" % name

    def getAttribute(self, name):
        if name in self.__items.keys():
            return self.__items[name]["value"]
        else:
            raise ValueError, "No such attribute: '%s'" % name


class ModelReader:
    def read(self, source, target):
        pass


class ModelWriter:
    def write(self, source, target):
        pass

