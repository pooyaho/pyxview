import string
from model.datamodel.objectmodel import BaseType
from model.models import Model
from util.utils import UniqueMap

__author__ = 'PHo'


class  DataModelElement(BaseType, Model):
    classTemplate = string.Template("""
public class $name : BaseDataModel {
    #region Inners
    $inners
    #endregion

    #region Props
    $fields
    #endregion
}
""")

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)

    def __defaults(self):
        return {'fields': {'value': UniqueMap()},
                'innerClass': {'value': UniqueMap()},
                'types': {}
        }


    fields = property(lambda self: self.getAttribute("fields"))
    innerClass = property(lambda self: self.getAttribute("innerClass"))
    types = property(lambda self: self.getAttribute("types"))
    name = property(lambda self: self.getAttribute("name"), lambda self, data: self.setAttribute('name', data))

    @staticmethod
    def isType(iType):
    #        return type(widget) in WidgetSelector.widgets.itervalues()
        return isinstance(iType, AbstractType)

    def addType(self, type):
        if not MainClass.isType(type):
            raise Exception("Unknown widget type %s" % type)
        self.types[type.name] = type

    def getCsCode(self):
        fields = ""
        inners = ""
        for cField in self.fields.itervalues():
            fields += cField.getCsCode() + "\n"
        for className, innerClass in self.innerClass.iteritems():
            inners += innerClass.getCsCode() + "\n"
        return self.classTemplate.substitute(inners=inners, fields=fields, name=self.name)

    def hasField(self, fieldName):
        return  self.fields.has_key(fieldName)
