#!/usr/bin/python
from optparse import OptionParser
import os
import re

from string import Template

import imp

classTemplate = Template("""
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<<<<  Generated by mutil version "1.1"    >>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class $name($baseClass):
    \"\"\"$documentation\"\"\"


    def __init__(self):
        #Only Model will initialize
        Model.__init__(self,self.__defaults())


    def __defaults(self):
        return $defaultValues

    $addItems

    $properties
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<   end of class    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
""")

getterSetterTemplate = Template("""
    $name=property(lambda self: self.getAttribute("$name"), lambda self, data: self.setAttribute('$name', data))
""")

getterTemplate = Template("""
    $name=property(lambda self: self.getAttribute("$name"))
""")

putItemTemplate = Template("""
    def put$name(self,$name):
        if isinstance($name,$constraint):
            raise Exception, "Unknown $name type %s" % $name
        self.$name[$name.$item] = $name
    """)


def buildModel(name, baseName, documentation, fields):
    if baseName is None:
        baseName = "object"

    def mapTokenizer(data):
        inp = data
        if type(data) == tuple:
            inp = data[0]
        result = re.compile(r"(->|:)").split(inp)
        if len(result) < 5 or not re.match("^(\w*):(\w*)->(\w*)$", inp):
        #            raise Exception, "Corrupted format"
            return None

        return result[0], result[2], result[4]


    def _typeOf(desc):
        if type(desc) == dict and desc.has_key("type"):
            return desc["type"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 0:
            return desc[0]
        elif type(desc) == str:
            return desc
        else:
            return "str"

    def _safeTypeOf(desc):
        t = _typeOf(desc)
        if t in ("str", "number", "bool", "list", "dict", "any"):
            return t
        else:
            raise TypeError, "Invalid field type '%s'" % t

    def _defaultValueOf(desc):
        if type(desc) == dict and desc.has_key("default"):
            return desc["default"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 1:
            return desc[1]
        else:
            return None

    def _safeDefaultValueOf(desc):
        v = _defaultValueOf(desc)
        if v is None:
            defVals = {"str": "", "number": 0, "bool": False, "list": [], "dict": {}, "any": ""}
            return defVals[_safeTypeOf(desc)]
        else:
            return v

    def _isReadOnly(desc):
        if type(desc) == dict and desc.has_key("readOnly"):
            return desc["readOnly"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 2:
            return desc[2]
        else:
            return False

    def _documentationOf(desc, doc=""):
        if type(desc) == dict and desc.has_key("doc"):
            return desc["doc"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 4:
            return desc[4]
        else:
            return doc

    def _matchConditionOf(desc):
        m = None
        if type(desc) == dict and desc.has_key("regexp"):
            m = desc["regexp"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 3:
            m = desc[3]

        if m is None:
            if desc == "str":
                return ".*"
            elif desc == "number":
                return "^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?$"
            elif desc == "bool":
                return "^(True|False|true|false)$"
            else:
                return ".*"
        else:
            return m

    initialFields = {}
    properties = ""
    slots = ""
    for k in fields.keys():
        desc = ""
        tokenism = mapTokenizer(fields[k])
        addItem = ""
        if tokenism:
            addItem = putItemTemplate.substitute(dict(name=k, constraint=tokenism[1], item=tokenism[2]))
            desc = tokenism[0]
        else:
            desc = fields[k]

        #        slots += slotsTemplate.substitute({"propertyName": k})

        initialFields[k] = {"value": _safeDefaultValueOf(desc), "constraint": _matchConditionOf(desc)}

        if _isReadOnly(desc):
            properties = properties + getterTemplate.substitute(
                    {"name": k, "documentation": _documentationOf(desc, "Property for   %s" % k)})
        else:
            properties = properties + getterSetterTemplate.substitute(
                    {"name": k, "documentation": _documentationOf(desc, "Property for   %s" % k)})

            #    baseClasses = ""
    if baseName.lower() == "object":
        baseClasses = "{0:>s},{1:>s}".format("Model", baseName)
    else:
        baseClasses = "{0:>s},{1:>s}".format(baseName, "Model")

    return classTemplate.substitute({"name": name, "documentation": documentation, "defaultValues": initialFields,
                                     "slots": slots, "properties": properties, "baseClass": baseClasses,
                                     "addItems": ""})


def loadTemplate(templatePath):
    fileData = ""
    f = open(templatePath, "r")
    for line in f.readlines():
        fileData += line + "\n"

    return Template(fileData)


def main():
    def __createOptions():
        usage = "usage: %prog [options] [-c ClassTemplate] [-s GetterSetterTemplate] [-g GetterTemplate] [Input "\
                "Definition Files]"
        parser = OptionParser(usage)
        parser.add_option("-c", "--class_template",
                          action="store", type="string", dest="ctemplate",
                          help="Input template file for Class Template")
        parser.add_option("-s", "--setget_template",
                          action="store", type="string", dest="gstemplate",
                          help="Input template file for Getter and Setter Template")
        parser.add_option("-g", "--get_template",
                          action="store", type="string", dest="gtemplate",
                          help="Input template file for Getter Template")
        parser.add_option("-i", "--ignore",
                          dest="ignore", action="store_true", default=False,
                          help="Ignore model namespace searching")
        #
        return parser.parse_args()


    (options, args) = __createOptions()
    if options.gtemplate is not None:
        global getterTemplate
        getterTemplate = loadTemplate(options.gtemplate)

    if options.gstemplate is not None:
        global getterSetterTemplate
        getterSetterTemplate = loadTemplate(options.gstemplate)
    if options.ctemplate is not None:
        global classTemplate
        classTemplate = loadTemplate(options.ctemplate)

    #for arg in sys.argv[1:]:
    #    Template.()
    variables = {}
    local = {}
    for arg in args:
        execfile(arg, {}, local)


        #print variables["a"]
        if local.has_key("output"):
            output = local["output"]
        else:
            raise Exception, "Define output in your file!"

        header = list(local.get("header", """sys"""))
        #            header = local["header"]

        f = open(output, 'w')
        #        f.write(trim(header))
        if not options.ignore:
            modelPaths = findModulePath("/home/pooya/I2Project/trunk", "Model",
                                        "/home/pooya/I2Project/trunk/main/python")
        else:
            modelPaths = "model.models",


        #########################
        #f.write(baseModel)
        #########################
        for i in header:
            f.write("import %s \n" % i)

        for i in modelPaths:
            f.write("from %s import Model" % i)

        for k, v in local.iteritems():
            if type(v) == list and  len(v) >= 4 and type(v[3] == dict):
                f.write(buildModel(v[0], v[2], v[1], v[3]))
            if type(v) == dict and len(v) >= 3:
                baseClass = v.get("baseClass", None)
                if v.has_key("name") and v.has_key("fields"):
                    if not v.has_key("comment"):
                        f.write(buildModel(v["name"], baseClass, "", v["fields"]))
                    else:
                        f.write(buildModel(v["name"], baseClass, v["comment"], v["fields"]))

        f.close()


def findModulePath(path, className, basePackagePath):
    attributes = {}
    for root, dirs, files in os.walk(path):
        for source in (s for s in files if s.endswith(".py")):
            name = os.path.splitext(os.path.basename(source))[0]

            full_name = os.path.splitext(source)[0].replace(os.path.sep, '.')
            m = imp.load_module(full_name, *imp.find_module(name, [root]))

            try:
                attr = getattr(m, className)
                myPath = "%s/%s" % (root, full_name)
                package = myPath.replace(basePackagePath, "").replace("/", ".")
                if package.startswith("."):
                    package = package[1:]

                attributes[package] = attr
            except Exception:
                continue
    if len(attributes) <= 0:
        raise Exception, "Class %s not found" % className

    result = ["%s" % aPath for aPath, attr in attributes.iteritems()    if "." not in attr.__module__]

    return result

if __name__ == "__main__":
    main()