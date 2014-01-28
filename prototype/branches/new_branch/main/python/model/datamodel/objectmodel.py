__author__ = 'PHo'


class BaseClassModel(object):
    def addType(self, typeName):
        pass

    def addField(self, field):
        pass

    def getClassName(self):
        pass

    def setClassName(self, value):
        pass

    def getFields(self):
        pass


class  UniqueMap(dict):
    def __init__(self):
        dict.__init__(self)

    def addAttribute(self, name, value):
        if self.has_key(name):
            raise Exception, "Duplicate value"
        self[name] = value


class Field(object):
    def __init__(self, fieldType, fieldName, atts=None, rests=None):
        if not atts: atts = {}
        if not rests: rests = {}

        super(Field, self).__init__()
        self.__fieldType, self.__atts, self.__rests = fieldType, atts, rests
        self.__fieldName = fieldName


    def getFieldType(self):
        return self.__fieldType

    def getFieldName(self):
        return self.__fieldName

    def getFieldAtts(self):
        return self.__atts

    def getFieldConstraints(self):
        return self.__rests


class ClassModel(BaseClassModel):
#    def addField(self, fieldType, fieldAttributes, restriction):
#        if  not fieldAttributes.has_key("name"):
#            raise Exception, "Type %s has not name" % fieldType
#
#        if self.__fieldTypes.has_key(fieldAttributes["name"]):
#            raise Exception, "Duplicate field name in %s", self.__className
#
#        self.__fieldTypes[fieldAttributes["name"]] = [fieldAttributes, restriction]

    def addField(self, field):
    #        if  not field.getName().has_key("name"):
    #            raise Exception, "Type %s has not name" % fieldType

        if self.__fieldTypes.has_key(field.getFieldName()):
            raise Exception, "Duplicate field name in %s", self.__className

        self.__fieldTypes[field.getFieldName()] = field


    def __init__(self, className=None):
        super(ClassModel, self).__init__()
        self.__types = {}
        self.__className = className
        self.__fieldTypes = {}

    def addType(self, typeClass):
        if type(typeClass) is not ClassModel:
            raise Exception, "Incorrect TypeClass type!"
        if self.__types.has_key(typeClass.getClassName()):
            raise Exception, "Duplicate type name in %s", self.__className
        self.__types[typeClass.getClassName()] = typeClass


    #    lambda self, c: setattr(self, "__className", c)
    def setClassName(self, value):
        self.__className = value

    def getClassName(self):
        return self.__className

    def getFields(self):
        return self.__fieldTypes

    def getTypes(self):
        return self.__types


class Domain(object):
    def __init__(self, domainName=None):
        super(Domain, self).__init__()
        self.__domain = domainName
        self.__classes = {}

    def addClassModel(self, classModel):
        if self.__classes.has_key(classModel.getClassName()):
            raise Exception, "Duplicate Class name %s in %s Domain" % (classModel.getClassName(), self.__domain)
        self.__classes[classModel.getClassName()] = classModel

    def getDomainName(self):
        return self.__domain

    def getClasses(self):
        return self.__classes

    def setDomainName(self, domainName):
        self.__domain = domainName
