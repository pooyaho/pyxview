from re import match

__author__ = 'PHo'


class Model(object):
    """Base class for all model classes. Provides common operations for these classes."""
    #    warnings.warn("Deprecated, it removed", DeprecationWarning, stacklevel=2)
    DEFAULT_CONSTRAINT = ".*"

    def __init__(self, items):
        super(Model, self).__init__()
        #        warnings.warn("Deprecated, it removed", DeprecationWarning, stacklevel=2)
        self.__reader = None
        self.__writer = None
        self.__dict__.update(items)

    def __str__(self):
        return "%s %s" % (repr(self), str(self.__dict__))

    def setAttribute(self, name, value):
        """
        sets value to attribute
        """
        #        warnings.warn("Deprecated, it removed", DeprecationWarning, stacklevel=2)
        if name in self.__dict__.iterkeys():
            constraint = self.__dict__[name].get("constraint", Model.DEFAULT_CONSTRAINT)
            if match(constraint, str(value)) or value is None:
                self.__dict__[name]["value"] = value
                return value
            else:
                raise ValueError, "Format of value of %s is not %s" % (name, constraint)
        else:
            raise ValueError, "No such attribute: '%s'" % name

    def getAttribute(self, name):
    #        warnings.warn("Deprecated, it removed", DeprecationWarning, stacklevel=2)
        if name in self.__dict__.iterkeys():
            return self.__dict__[name].get("value", None)
        else:
            raise ValueError, "No such attribute: '%s'" % name

    def fillAttributes(self, types=None):
        if not types: types = {}
        for k, v in types.iteritems():
            self.setAttribute(k, v)

    def tryFillAttributes(self, types=None):
        if not types: types = {}
        for k, v in types.iteritems():
            if self.hasAttribute(k):
                self.setAttribute(k, v)

    def hasAttribute(self, attributeName):
        return attributeName in self.__dict__.keys()

    def printAll(self):
        for k, v in self.__dict__.iteritems():
            if v <> None and v.has_key("value"):
                print k, v["value"]

    def getAttributes(self):
        return [(element, value) for element, value in self.__dict__.iteritems() if
                                 type(value) == dict and  (value.has_key('value') or value.has_key('constraint'))]

    def getNoneEmptyAttributes(self):
        return [(element, value) for element, value in self.__dict__.iteritems() if
                                 type(value) == dict and  value.has_key('value') and value['value'] <> None]


class ModelReader:
    def read(self, source, target):
        pass


class ModelWriter:
    def write(self, source, target):
        pass