import string
import model.datamodel.objectmodel
import xmlutils.xutils

__author__ = 'PHo'

SIMPLE_TYPE, COMPLEX_TYPE, UNKNOWN_TYPE = 0, 1, 2
NULLARY_CONSTRAINT, UNARRY_CONSTRAINT, UNKNOWN_CONSTRAINT = 0, 1, 2


def createModelFromXml(filePath, schemaPath):
    """

    """
    BASE_NODE = "dataModel"

    xpathR = xmlutils.xutils.XpathResult(filePath, schemaPath)
    domain = model.datamodel.objectmodel.Domain()
    mainClassModel = model.datamodel.objectmodel.ClassModel()

    def getAttributeValue(nodeName, attName):
        result = xpathR.getXpathResult("//" + nodeName + "/@" + attName)
        if len(result) <= 0:
            return None
        return result[0].content


    def fillDataTypes():
        types = xpathR.getXpathResult("//dataModel/elements/*")
        for dataType in types:
            mainClassModel.addField(getDataType(dataType))


    def getDataType(dataType ):
        util = xmlutils.xutils.XmlUtil(dataType, xpathR.getContext())
        attMaps = util.getAttributesMapFromNode()

        atts = model.datamodel.objectmodel.UniqueMap()
        for k, v in attMaps.iteritems():
            atts.addAttribute(k, v)

        rests = model.datamodel.objectmodel.UniqueMap()

        constChildren = util.getChild("restriction")
        combinationType = "all"
        if constChildren is not None:
            if len(constChildren) >= 1:
                constUtil = xmlutils.xutils.XmlUtil(constChildren[0], xpathR.getContext())
                combinationType = constUtil.getAttributesMapFromNode().get("combination", None)

        atts["combination"] = combinationType

        for k, v in util.getChildMapFromNode("restriction").iteritems():
            if getConstraintType(k) == UNARRY_CONSTRAINT and (v == "" or v is None):
                raise Exception, "Constraint {%s} of %s type is empty" % (k, attMaps["name"])
            rests.addAttribute(k, v)

        return model.datamodel.objectmodel.Field(dataType.name, attMaps["name"], atts, rests)


    def fillMainAttributes():
        models = xpathR.getXpathResult("//dataModel")
        for dataModel in models:
            util = xmlutils.xutils.XmlUtil(dataModel, xpathR.getContext())
            atts = util.getAttributesMapFromNode()
            mainClassModel.setClassName(atts["name"])
            domain.setDomainName(atts["domain"])

    def fillDefinedTypes():
        types = xpathR.getXpathResult("//dataModel/type")
        for dataType in types:
            util = xmlutils.xutils.XmlUtil(dataType, xpathR.getContext())
            atts = util.getAttributesMapFromNode()
            c = model.datamodel.objectmodel.ClassModel(atts["name"])

            for k in util.getChildContent("elements"):
                field = getDataType(k)
                c.addField(field)

            mainClassModel.addType(c)

    fillMainAttributes()
    fillDefinedTypes()
    fillDataTypes()

    domain.addClassModel(mainClassModel)

    return  domain


def  createCSDataModel(domainModel):
    baseClassTemplate = string.Template(
        """
using System;
namespace $nsName{
    $classData
}
        """

    )
    tClassData = ""
    for _, domainClass in domainModel.getClasses().iteritems():
        tClassData += __createCSClassTemplate(domainClass)
    return  baseClassTemplate.substitute(dict(classData=tClassData, nsName=domainModel.getDomainName()))


#    return classTemplate.substitute(dict(className=dataModel.getClassName(), fields=properties))


def  __createCSClassTemplate(dataModel):
    typesMap = {"boolean": "System.Boolean",
                "list": "System.Collections.Generic.List<System.Object>",
                "map": "System.Collections.HashMap",
                #                "composition": "",
                "dateTime": "System.DateTime",
                "currency": "System.Decimal",
                "decimal": "System.Decimal",
                "file": "",
                "double": "System.Double",
                "duration": "",
                "integer": "System.Int32",
                "string": "string"}

    #    constraintMap = {
    #        "minSize": "",
    #        "maxSize": "",
    #        "notContains": "",
    #        "minValue": "",
    #        "maxValue": "",
    #        "format": "",
    #        "notNull": "Microsoft.Practices.EnterpriseLibrary.Validation.Validators.NotNullValidator()",
    #        "notZero": "Microsoft.Practices.EnterpriseLibrary.Validation.Validators.PropertyComparisonValidator
    # (\"__zero\","
    #                   "ComparisonOperator.NotEqual)",
    #        "notEqualTo": "",
    #
    #        "positive": "Microsoft.Practices.EnterpriseLibrary.Validation.Validators.PropertyComparisonValidator"
    #                    "(\"__zero\","
    #                    "ComparisonOperator.GraterThan)",
    #        "negative": "Microsoft.Practices.EnterpriseLibrary.Validation.Validators.PropertyComparisonValidator"
    #                    "(\"__zero\",ComparisonOperator.SmallerThan)"
    #        ,
    #
    #        "locale": "",
    #        "type": "",
    #        "regex": "",
    #        "maxLen": "",
    #
    #        "minLen": "",
    #        }

    constraintMap = {
        "minSize": "value.",
        "maxSize": "",
        "notContains": "",
        "minValue": "value>=$value",
        "maxValue": "value<=$value",
        "format": "System.Text.RegularExpressions.Regex.Match(value,\"$value\").Success",
        "notNull": "value!=null",
        "notZero": "value!=0",
        "notEqualTo": "value!=$value",

        "positive": "value>0",
        "negative": "value<0",
        "locale": "",
        "type": "value is $value",
        "regex": "System.Text.RegularExpressions.Regex.Match(value,\"$value\").Success",
        "maxLen": "System.Text.RegularExpressions.Regex.Match(value,\"^.{0,$value}$$\").Success",
        "minLen": "System.Text.RegularExpressions.Regex.Match(value,\"^.{$value,}$$\").Success",
        }

    constraintAllTemplate = string.Template("""
    ($constraint) &&
    """)

    propertyTemplate = string.Template("""

    public $fieldType $fieldName {get; set{
            if ($constraints){
                $fieldName=value;
            }else {
                throw new Exception("Inserted value for $fieldName is not valid!");
            }

    }}
    """)

    classTemplate = string.Template(
        """
public class $className {
    #region Inners
    $inners
    #endregion

    #region Props
    $fields
    #endregion
}
        """
    )
    properties = ""

    innerClasses = ""

    for _, innerType in dataModel.getTypes().iteritems():
        innerClasses += __createCSClassTemplate(innerType)

    for fName, field in dataModel.getFields().iteritems():
        fType = typesMap.get(field.getFieldType(), None)
        if fType is None:
            fType = field.getFieldAtts().get("type", None)
        constraint = ""

        if fType is None:
            raise Exception, "What are you doing? what is that input file?"

        for k, v in field.getFieldConstraints().iteritems():
            constTValue = string.Template(constraintMap[k]).substitute(dict(value=v))
            constraint += constraintAllTemplate.substitute(dict(constraint=constTValue))
        constraint += "true"
        properties += propertyTemplate.substitute(dict(constraints=constraint, fieldType=fType, fieldName=fName))

    return classTemplate.substitute(dict(className=dataModel.getClassName(), fields=properties, inners=innerClasses))


def createJSDataModel(domain):
    tmpData = ""
    for _, domainClass in domain.getClasses().iteritems():
        tmpData += __createJSDataModel(domainClass)

    return  tmpData


def __createJSDataModel(dataModel):
    constraintMap = {
        "minSize": "",
        "maxSize": "",
        "notContains": "",
        "minValue": "$var>=$value",
        "maxValue": "$var<=$value",
        "format": "new RegExp($value).test($var)",
        "notNull": "$var!=null",
        "notZero": "$var!=0",
        "notEqualTo": "$var!=$value",
        "positive": "$var>0",
        "negative": "$var<0",

        "locale": "",
        "type": "typeof ($var)==$val",
        "regex": "new RegExp($value).test($var)",
        "maxLen": "new RegExp('^.{0,$value}$$').test($var)",

        "minLen": "new RegExp('^.{$value,}$$').test($var)",
        }

    classTemplate = string.Template(
        """
        var $className = function () {
            $innerClass
            $fields
        };
        """
    )
    fieldTemplate = string.Template(
        """
        var $name=$fType;
        Object.defineProperty(this, "$name", {
        get:function () { return $name; },
        set:function (newValue) {
        if($constContent){
            $name = newValue;
        }
        },
        configurable:$configurable});
        """
    )
    constraintContentAllTemplate = string.Template(
        """
        ($content) &&
        """
    )

    constraintContentAnyTemplate = string.Template(
        """
        ($content) ||
        """
    )
    constraintContentNoneTemplate = string.Template(
        """
        !($content) &&
        """
    )
    innerClasses = ""

    for _, innerType in dataModel.getTypes().iteritems():
        innerClasses += __createJSDataModel(innerType)
    stField = ""

    for fName, field in dataModel.getFields().iteritems():
        fType = "undefined"

        if getElementType(field.getFieldType()) == COMPLEX_TYPE:
            fType = field.getFieldAtts()["type"] + "()"
        constStr = ""

        neutralBooleanOps = None
        constraintContentTemplate = None
        if field.getFieldAtts()["combination"] == "all":
        #            global neutralBooleanOps
        #            global constraintContentTemplate
            neutralBooleanOps = "true"
            constraintContentTemplate = constraintContentAllTemplate
        elif field.getFieldAtts()["combination"] == "any":
        #            global neutralBooleanOps
        #            global constraintContentTemplate
            neutralBooleanOps = "false"
            constraintContentTemplate = constraintContentAnyTemplate
        elif field.getFieldAtts()["combination"] == "none":
        #            global neutralBooleanOps
        #            global constraintContentTemplate
            constraintContentTemplate = constraintContentNoneTemplate
            neutralBooleanOps = "true"
        else:
        #            global neutralBooleanOps
        #            global constraintContentTemplate
            neutralBooleanOps = "true"
            constraintContentTemplate = constraintContentAllTemplate

        for const, constVal in field.getFieldConstraints().iteritems():
            mapData = constraintMap[const]
            if mapData == "":
                mapData = neutralBooleanOps
            tmp = string.Template(mapData).substitute(dict(var="newValue", value=constVal))

            constStr += constraintContentTemplate.substitute(dict(content=tmp))

        constStr += neutralBooleanOps

        configurable = "true"
        if field.getFieldAtts().get("readonly", None):
            configurable = str(not bool(field.getFieldAtts().get("readonly"))).lower()

        stField += fieldTemplate.substitute(dict(name=fName, fType=fType, constContent=constStr,
                                                 configurable=configurable))

    return classTemplate.substitute(dict(className=dataModel.getClassName(), fields=stField,
                                         innerClass=innerClasses))


def getElementType(elementName  ):
    simpleTypesList = ["boolean",
                       "list",
                       "map",
                       "dateTime",
                       "currency",
                       "decimal",
                       "file",
                       "double",
                       "duration",
                       "integer",
                       "string"]
    complexTypesList = [
        "composition"
    ]
    if elementName in simpleTypesList:
        return SIMPLE_TYPE
    if elementName in complexTypesList:
        return  COMPLEX_TYPE
    return  UNKNOWN_TYPE


def getConstraintType(constName):
    unarryConstsList = ["minSize",
                        "maxSize",
                        "notContains",
                        "minValue",
                        "maxValue",
                        "format",

                        "notEqualTo",
                        "locale",
                        "type",
                        "regex",
                        "maxLen",
                        "minLen"]

    nullaryConstsList = ["notNull", "positive",
                         "negative", "notZero"]

    if constName in nullaryConstsList:
        return  NULLARY_CONSTRAINT
    if constName in unarryConstsList:
        return  UNARRY_CONSTRAINT
    return UNKNOWN_CONSTRAINT

    #x = createModelFromXml("../../../schema/main.xml", "DataModel.xsd")
    #print createCSDataModel(x)
    #print createJSDataModel(x)