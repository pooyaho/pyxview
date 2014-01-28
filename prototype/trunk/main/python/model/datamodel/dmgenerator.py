__author__ = 'PHo'

#x = createModelFromXml("../../../schema/main.xml", "xview-dm.xsd")
#print createCSDataModel(x)
#print createJSDataModel(x)



#    def getDataType(objType):
#        typeName = removeNSFromValue(objType.tag)
#        modelType = selectType(typeName)
#        dataType.attrib["combination"] = dataType.restriction.attrib.get("combination", "all")
#        modelType.fillAttributes(dataType.attrib)
#        for rest in dataType.restriction.getchildren():
#            modelType.constraints.addAttribute(removeNSFromValue(rest.tag), rest.text)
#
#        mainClassModel.fields.addAttribute(dataType.attrib['name'], modelType)
#    def getDataType(dataType):
#    #        util = xmlutils.xutils.XmlUtil(dataType, xpathR.getContext())
#    #        attMaps = util.getAttributesMapFromNode()
#
#    #        atts = model.datamodel.objectmodel.UniqueMap()
#
#    #        for k, v in dataType.attrib.iteritems():
#    #            atts.addAttribute(k, v)
#
#    #        rests = model.datamodel.objectmodel.UniqueMap()
#
#        #        constChildren = util.getChild("restriction")
#        #        constChildren = dataType.restriction
#        #        combinationType = "all"
#        #        if constChildren is not None:
#        #            if len(constChildren) >= 1:
#        #                constUtil = xmlutils.xutils.XmlUtil(constChildren[0], xpathR.getContext())
#        #                combinationType = constUtil.getAttributesMapFromNode().get("combination", None)
#        combinationType = constChildren.attrib.get("combination", "all")
#
#        #        atts["combination"] = combinationType
#
#        for const in constChildren.getchildren():
#            if getConstraintType(const.tag) == UNARRY_CONSTRAINT and (const.text == "" or const is None):
#                raise Exception, "Constraint {%s} of %s type is empty" % (const.tag, const.text)
#            rests.addAttribute(const.tag, const.text)
#
#        return model.datamodel.objectmodel.Field(dataType.name, attMaps["name"], atts, rests)


#def  createCSDataModel(domainModel):
#    baseClassTemplate = string.Template(
#        """
#using System;
#using System.ComponentModel;
#using System.Windows.Input;
#
#namespace $nsName{
#    public class BaseDataModel : INotifyPropertyChanged{
#
#	    public event PropertyChangedEventHandler PropertyChanged;
#	    protected void RaisePropertyChanged (string propertyName) {
#
#		    PropertyChangedEventHandler handler = PropertyChanged;
#
#            if (handler != null) {
#                handler (this, new PropertyChangedEventArgs (propertyName));
#            }
#	    }
#    }
#    $classData
#}
#        """
#
#    )
#
#    tClassData = ""
#    for domainClass in domainModel.classes.itervalues():
#        tClassData += __createCSClassTemplate(domainClass)
#    return  baseClassTemplate.substitute(dict(classData=tClassData, nsName=domainModel.getDomainName()))
#
#
##    return classTemplate.substitute(dict(className=dataModel.getClassName(), fields=properties))
#

#def  __createCSClassTemplate(dataModel):
#    typesMap = {"boolean": "System.Boolean",
#                "list": "System.Collections.Generic.List<System.Object>",
#                "map": "System.Collections.HashMap",
#                #                "composition": "",
#                "dateTime": "System.DateTime",
#                "currency": "System.Decimal",
#                "decimal": "System.Decimal",
#                "file": "",
#                "double": "System.Double",
#                "duration": "",
#                "integer": "System.Int32",
#                "string": "string"}
#
#    #    a = {
#    #        "ns": "ns2",
#    #        "content": [{"name": "ppp",
#    #                     "innerClass":"hkkkkkk"
#    #                ,
#    #                     "content":
#    #                         [
#    #                                 {"name": "field1",
#    #                                  "type": "string",
#    #                                  "readonly": "true",
#    #                                  "constraint": "(value !=null) && true"}
#    #                             ,
#    #                                 {"name": "field2",
#    #                                  "type": "int",
#    #                                  "readonly": "false",
#    #                                  "constraint": "(value !=null) && true"}
#    #                         ]
#    #        }
#    #        ]
#    #    }
#    constraintMap = {
#        "minSize": "value.",
#        "maxSize": "",
#        "notContains": "",
#        "minValue": "value>=$value",
#        "maxValue": "value<=$value",
#        "format": "System.Text.RegularExpressions.Regex.Match(value,\"$value\").Success",
#        "notNull": "value!=null",
#        "notZero": "value!=0",
#        "notEqualTo": "value!=$value",
#
#        "positive": "value>0",
#        "negative": "value<0",
#        "locale": "",
#        "type": "value is $value",
#        "regex": "System.Text.RegularExpressions.Regex.Match(value,\"$value\").Success",
#        "maxLen": "System.Text.RegularExpressions.Regex.Match(value,\"^.{0,$value}$$\").Success",
#        "minLen": "System.Text.RegularExpressions.Regex.Match(value,\"^.{$value,}$$\").Success",
#        }
#
#    constraintAllTemplate = string.Template("""
#    ($constraint) &&
#    """)
#
#    propertyTemplate = string.Template("""
#    private  $fieldType _$fieldName;
#    public $fieldType $fieldName {
#        get{ return _$fieldName; }
#
#        set{
#            if ($constraints){
#                _$fieldName=value;
#            }else {
#                throw new Exception("Inserted value for $fieldName is not valid!");
#            }
#            if (_$fieldName == value)
#                return;
#            _$fieldName = value;
#            RaisePropertyChanged ("$fieldName");
#        }
#    }
#    """)
#
#    classTemplate = string.Template("""
#        public class $className : BaseDataModel {
#            #region Inners
#            $inners
#            #endregion
#
#            #region Props
#            $fields
#            #endregion
#        }
#        """)
#
#    properties = ""
#
#    innerClasses = ""
#
#    for _, innerType in dataModel.getTypes().iteritems():
#        innerClasses += __createCSClassTemplate(innerType)
#
#    for fName, field in dataModel.getFields().iteritems():
#        fType = typesMap.get(field.getFieldType(), None)
#        if fType is None:
#            fType = field.getFieldAtts().get("type", None)
#        constraint = ""
#
#        if fType is None:
#            raise Exception, "What are you doing? what is that input file?"
#
#        for k, v in field.getFieldConstraints().iteritems():
#            constTValue = string.Template(constraintMap[k]).substitute(dict(value=v))
#            constraint += constraintAllTemplate.substitute(dict(constraint=constTValue))
#        constraint += "true"
#        properties += propertyTemplate.substitute(dict(constraints=constraint, fieldType=fType, fieldName=fName))
#
#    return classTemplate.substitute(dict(className=dataModel.getClassName(), fields=properties, inners=innerClasses))
#
#
#def createJSDataModel(domain):
#    tmpData = ""
#    for _, domainClass in domain.getClasses().iteritems():
#        tmpData += __createJSDataModel(domainClass)
#
#    return  tmpData
#
#
#def __createJSDataModel(dataModel):
#    constraintMap = {
#        "minSize": "",
#        "maxSize": "",
#        "notContains": "",
#        "minValue": "$var>=$value",
#        "maxValue": "$var<=$value",
#        "format": "new RegExp($value).test($var)",
#        "notNull": "$var!=null",
#        "notZero": "$var!=0",
#        "notEqualTo": "$var!=$value",
#        "positive": "$var>0",
#        "negative": "$var<0",
#
#        "locale": "",
#        "type": "typeof ($var)==$val",
#        "regex": "new RegExp($value).test($var)",
#        "maxLen": "new RegExp('^.{0,$value}$$').test($var)",
#
#        "minLen": "new RegExp('^.{$value,}$$').test($var)",
#        }
#
#    classTemplate = string.Template(
#        """
#        var $className = function () {
#            $innerClass
#            $fields
#        };
#        """
#    )
#    fieldTemplate = string.Template(
#        """
#        var $name=$fType;
#        Object.defineProperty(this, "$name", {
#        get:function () { return $name; },
#        set:function (newValue) {
#        if($constContent){
#            $name = newValue;
#        }
#        },
#        configurable:$configurable});
#        """
#    )
#    constraintContentAllTemplate = string.Template(
#        """
#        ($content) &&
#        """
#    )
#
#    constraintContentAnyTemplate = string.Template(
#        """
#        ($content) ||
#        """
#    )
#    constraintContentNoneTemplate = string.Template(
#        """
#        !($content) &&
#        """
#    )
#    innerClasses = ""
#
#    for _, innerType in dataModel.getTypes().iteritems():
#        innerClasses += __createJSDataModel(innerType)
#    stField = ""
#
#    for fName, field in dataModel.getFields().iteritems():
#        fType = "undefined"
#
#        if getElementType(field.getFieldType()) == COMPLEX_TYPE:
#            fType = field.getFieldAtts()["type"] + "()"
#        constStr = ""
#
#        neutralBooleanOps = None
#        constraintContentTemplate = None
#        if field.getFieldAtts()["combination"] == "all":
#        #            global neutralBooleanOps
#        #            global constraintContentTemplate
#            neutralBooleanOps = "true"
#            constraintContentTemplate = constraintContentAllTemplate
#        elif field.getFieldAtts()["combination"] == "any":
#        #            global neutralBooleanOps
#        #            global constraintContentTemplate
#            neutralBooleanOps = "false"
#            constraintContentTemplate = constraintContentAnyTemplate
#        elif field.getFieldAtts()["combination"] == "none":
#        #            global neutralBooleanOps
#        #            global constraintContentTemplate
#            constraintContentTemplate = constraintContentNoneTemplate
#            neutralBooleanOps = "true"
#        else:
#        #            global neutralBooleanOps
#        #            global constraintContentTemplate
#            neutralBooleanOps = "true"
#            constraintContentTemplate = constraintContentAllTemplate
#
#        for const, constVal in field.getFieldConstraints().iteritems():
#            mapData = constraintMap[const]
#            if mapData == "":
#                mapData = neutralBooleanOps
#            tmp = string.Template(mapData).substitute(dict(var="newValue", value=constVal))
#
#            constStr += constraintContentTemplate.substitute(dict(content=tmp))
#
#        constStr += neutralBooleanOps
#
#        configurable = "true"
#        if field.getFieldAtts().get("readonly", None):
#            configurable = str(not bool(field.getFieldAtts().get("readonly"))).lower()
#
#        stField += fieldTemplate.substitute(dict(name=fName, fType=fType, constContent=constStr,
#                                                 configurable=configurable))
#
#    return classTemplate.substitute(dict(className=dataModel.getClassName(), fields=stField,
#                                         innerClass=innerClasses))
#
#
#def getElementType(elementName):
#    simpleTypesList = ["boolean",
#                       "list",
#                       "map",
#                       "dateTime",
#                       "currency",
#                       "decimal",
#                       "file",
#                       "double",
#                       "duration",
#                       "integer",
#                       "string"]
#    complexTypesList = [
#        "composition"
#    ]
#    if elementName in simpleTypesList:
#        return SIMPLE_TYPE
#    if elementName in complexTypesList:
#        return  COMPLEX_TYPE
#    return  UNKNOWN_TYPE
#
#
#def getConstraintType(constName):
#    unarryConstsList = ["minSize",
#                        "maxSize",
#                        "notContains",
#                        "minValue",
#                        "maxValue",
#                        "format",
#
#                        "notEqualTo",
#                        "locale",
#                        "type",
#                        "regex",
#                        "maxLen",
#                        "minLen"]
#
#    nullaryConstsList = ["notNull", "positive",
#                         "negative", "notZero"]
#
#    if constName in nullaryConstsList:
#        return  NULLARY_CONSTRAINT
#    if constName in unarryConstsList:
#        return  UNARRY_CONSTRAINT
#    return UNKNOWN_CONSTRAINT

#    def getAttributeValue(nodeName, attName):
#        result = xpathR.getXpathResult("//" + nodeName + "/@" + attName)
#        if len(result) <= 0:
#            return None
#        return result[0].content

#    xpathR = xmlutils.xutils.XpathResult(filePath, schemaPath)
#        types = xpathR.getXpathResult("//dataModel/elements/*")

#        models = xpathR.getXpathResult("//dataModel")
#        for dataModel in models:
#        util = xmlutils.xutils.XmlUtil(dataModel, xpathR.getContext())
#        atts = util.getAttributesMapFromNode()

#        types = xpathR.getXpathResult("//dataModel/type")
#            util = xmlutils.xutils.XmlUtil(dataType, xpathR.getContext())
#            atts = util.getAttributesMapFromNode()
#            c.name = dataType.attrib["name"]