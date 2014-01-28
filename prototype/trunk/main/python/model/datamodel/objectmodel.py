from string import Template
import string
from model.models import Model
from util.utils import UniqueMap
import os

__author__ = 'PHo'

class BaseType(Model):
    def __init__(self):
        Model.__init__(self, self.__defaults())


    def __defaults(self):
        return {'name': {},
                'readonly': {},
                'constraints': {'value': UniqueMap()},
                'combination': {}
        }

    constraintMap = {
        "minsize": {"cs": "$name.Count>=$value"},
        "maxsize": {"cs": "$name.Count<=$value"},
        "notcontains": {"cs": "!value.Contains(($itemType)Convert.ChangeType($value, typeof($itemType)))"},
        "minvalue": {" cs": "value>=$value"},
        "maxvalue": {"cs": "value<=$value"},
        "format": {"cs": "System.Text.RegularExpressions.Regex.Match(value,@\"$value\").Success"},
        "notnull": {"cs": "value!=null"},
        "notzero": {"cs": "value!=0"},
        "notequalto": {"cs": "value!=$value"},
        "positive": {"cs": "value>0"},
        "negative": {"cs": "value<0"},
        "type": {"cs": "value is $value"},
        "regex": {"cs": "System.Text.RegularExpressions.Regex.Match(value,@\"$value\").Success"},
        "maxlen": {"cs": "System.Text.RegularExpressions.Regex.Match(value,@\"^.{0,$value}$$\").Success"},
        "minlen": {"cs": "System.Text.RegularExpressions.Regex.Match(value,@\"^.{$value,}$$\").Success"},
        }

    csTemplate = Template("""
       private  $type _$name;
       public $type $name {
       get{ return _$name; }
       set{
            if (_$name == value)
                return;
            if ($constraint){
                _$name=value;
            }
            else {
                throw new Exception("Inserted value for $name is not valid!");
            }

            RaisePropertyChanged ("$name");
            }
       }
        """
    )

    combination = property(lambda self: self.getAttribute("combination"),
                           lambda self, data: self.setAttribute('combination', data))
    name = property(lambda self: self.getAttribute("name"), lambda self, data: self.setAttribute('name', data))
    readonly = property(lambda self: self.getAttribute("readonly"),
                        lambda self, data: self.setAttribute('readonly', data))

    constraints = property(lambda self: self.getAttribute("constraints"))

    def getJsCode(self):
        pass

    def getCsCode(self):
        pass


    def generateCsCode(self, **kwargs):
        consts = ""
        itemType = ""
        if self.hasAttribute("itemType"):
            itemType = self.itemType

        if self.constraints:
            for constK, constV in self.constraints.iteritems():
                t = Template(self.constraintMap.get(constK.lower()).get("cs", "true"))
                if self.combination == "all":
                    consts += "(%s) &&" % t.substitute(value=constV, name=self.name, itemType=itemType)
                elif  self.combination == "none":
                    consts += "!(%s) &&" % t.substitute(value=constV, name=self.name, itemType=itemType)
                elif  self.combination == "any":
                    consts += "(%s) ||" % t.substitute(value=constV, name=self.name, itemType=itemType)

            if consts.endswith("&&"):
                consts += " true"
            else:
                consts += " false"

        kwargs.update(dict(constraint=consts, name=self.name))
        return self.csTemplate.substitute(kwargs)


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
                'types': {},
                "domain": {}
        }


    fields = property(lambda self: self.getAttribute("fields"))
    innerClass = property(lambda self: self.getAttribute("innerClass"))
    types = property(lambda self: self.getAttribute("types"))
    domain = property(lambda self: self.getAttribute("domain"), lambda self, data: self.setAttribute('domain', data))


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


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class DateTime(BaseType, Model):
    """"""
    attribMap = {
        "calendarTypes": {"cs": ""},
        "timeZone": {"cs": ""},
        }

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)

    def __defaults(self):
        return {'calendarTypes': {},
                'timeZone': {}}


    calendarTypes = property(lambda self: self.getAttribute("calendarTypes"),
                             lambda self, data: self.setAttribute('calendarTypes', data))

    timeZone = property(lambda self: self.getAttribute("timeZone"),
                        lambda self, data: self.setAttribute('timeZone', data))


    def getCsCode(self):
        return self.generateCsCode(type="DateTime")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class List(BaseType, Model):
    attribMap = {
        "itemType": {}
    }

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)

    def __defaults(self):
        return {'itemType': {}}


    itemType = property(lambda self: self.getAttribute("itemType"),
                        lambda self, data: self.setAttribute('itemType', data))

    def getCsCode(self):
        if self.itemType:
            mType = "System.Collections.Generic.List<%s>" % self.itemType
        else:
            mType = "System.Collections.Generic.List<Object>"
        return self.generateCsCode(type=mType)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Decimal(BaseType, Model):
    """"""

    attribMap = {
        "digits": {"cs": ""},
        "precision": {"cs": ""},
        }

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)


    def __defaults(self):
        return {'digits': {},
                'precision': {}}


    digits = property(lambda self: self.getAttribute("digits"),
                      lambda self, data: self.setAttribute('digits', data))

    precision = property(lambda self: self.getAttribute("precision"),
                         lambda self, data: self.setAttribute('precision', data))


    def getCsCode(self):
        return self.generateCsCode(type="Decimal")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Currency(BaseType, Model):
    """"""

    attribMap = {
        "currencyType ": {"cs": ""}
    }

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)

    def __defaults(self):
        return {'currencyType': {}}


    currencyType = property(lambda self: self.getAttribute("currencyType"),
                            lambda self, data: self.setAttribute('currencyType', data))

    def getCsCode(self):
        return self.generateCsCode(type="Currency")

        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Double(BaseType, Model):
    """"""

    attribMap = {
        "digits": {"cs": ""},
        "precision": {"cs": ""},
        }

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)


    def __defaults(self):
        return {'digits': {},
                'precision': {}}

    digits = property(lambda self: self.getAttribute("digits"),
                      lambda self, data: self.setAttribute('digits', data))

    precision = property(lambda self: self.getAttribute("precision"),
                         lambda self, data: self.setAttribute('precision', data))

    def getCsCode(self):
        return self.generateCsCode(type="Double")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Integer(BaseType, Model):
    """"""

    attribMap = {
        "digits": {"cs": ""},
        "precision": {"cs": ""},
        }

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)


    def __defaults(self):
        return {'digits': {},
                'precision': {}}


    digits = property(lambda self: self.getAttribute("digits"),
                      lambda self, data: self.setAttribute('digits', data))

    precision = property(lambda self: self.getAttribute("precision"),
                         lambda self, data: self.setAttribute('precision', data))

    def getCsCode(self):
        return self.generateCsCode(type="Int32")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Map(BaseType, Model):
    """"""

    attribMap = {

        "item": {"cs": ""},
        }

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)


    def __defaults(self):
        return {'item': {'value': []}}


    item = property(lambda self: self.getAttribute("item"), lambda self, data: self.setAttribute('item', data))

    def getCsCode(self):
        return self.generateCsCode(type="HashTable")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Boolean(BaseType, Model):
    """"""

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)

    def __defaults(self):
        return {}


    def getCsCode(self):
        return self.generateCsCode(type="Boolean", )

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class String(BaseType, Model):
    """"""

    attribMap = {
        "lang": {"cs": ""},
        }

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)

    def __defaults(self):
        return {'lang': {}}


    lang = property(lambda self: self.getAttribute("lang"), lambda self, data: self.setAttribute('lang', data))

    def getCsCode(self):
        return self.generateCsCode(type="string")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Composition(BaseType, Model):
    """"""

    attribMap = {
        "type": {"cs": ""}
    }

    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)

    def __defaults(self):
        return {'typename': {}}

    typename = property(lambda self: self.getAttribute("typename"),
                        lambda self, data: self.setAttribute('typename', data))

    def getCsCode(self):
        return self.generateCsCode(type=self.typename)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



class DataModel(BaseType, Model):
    csTemplate = string.Template("""
using System;
using System.ComponentModel;
using System.Windows.Input;

namespace $name{
public class BaseDataModel : INotifyPropertyChanged{

public event PropertyChangedEventHandler PropertyChanged;
protected void RaisePropertyChanged (string propertyName) {

    PropertyChangedEventHandler handler = PropertyChanged;

    if (handler != null) {
        handler (this, new PropertyChangedEventArgs (propertyName));
    }
}
}
$classData
}
""")


    def __init__(self):
        #Only Model will initialize
        Model.__init__(self, self.__defaults())
        BaseType.__init__(self)

    def __defaults(self):
        return {
            "classModel": {},
            "domain": {}

        }

    classModel = property(lambda self: self.getAttribute("classModel"),
                          lambda self, data: self.setAttribute('classModel', data))
    domain = property(lambda self: self.getAttribute("domain"), lambda self, data: self.setAttribute('domain', data))


    def createCsCode(self, outputPath):
        classStr = ""
        #        for mClass in self.classModel.innerClass.itervalues():
        #            classStr += mClass.getCsCode() + "\n"
        classStr = self.classModel.getCsCode()
        osDomainPath = self.domain.replace(".", "/")
        osDomainPath = os.path.join(outputPath, osDomainPath)
        try:
            os.makedirs(osDomainPath)
        except:
            pass

        tData = self.csTemplate.substitute(name=self.name, classData=classStr)
        filePath = osDomainPath + "/" + self.name + ".cs"
        #        filePath = os.path.join(outputPath, filePath)
        with open(filePath, 'w') as f:
            f.write(tData)


#    def hasClass(self, className):
#        return self..has_key(className)

#    def __str__(self):
#        if len(self.classes) > 0:
#            return self.classes.iterkeys().next()
#
#  def __int__(self):
#        return 0


def selectType(name):
    dmMap = {
        "datetime": DateTime,
        "boolean": Boolean,
        "composition": Composition,
        "string": String,
        "duration": None,
        "currency": Currency,
        "decimal": Decimal,
        "integer": Integer,
        "double": Double,
        "map": Map,
        "list": List
    }

    result = dmMap.get(name.lower())

    if result:
        return result()
    raise Exception("%s not defined as a data model type" % name)