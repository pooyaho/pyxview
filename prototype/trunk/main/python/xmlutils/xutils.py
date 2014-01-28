from lxml import objectify

__author__ = 'pooya'

from io import StringIO
from tokenize import generate_tokens
import libxml2


class XpathResult:
    def __init__(self, filePath, schemaPath):
        self.__doc = libxml2.parseFile(filePath)
        self.__ctxt = self.__doc.xpathNewContext()
        self.__ctxt.xpathRegisterNs("app", schemaPath)

    def getXpathResult(self, xpathQuery):
        xpathQueryWithNs = self.__makeXpathQueryWithNS(xpathQuery)
        res = self.__ctxt.xpathEval(xpathQueryWithNs)
        return  res

    def __getNs(self):
        return "app"


    def __makeXpathQueryWithNS(self, xpathQuery):
        s = unicode(xpathQuery)
        #    result = []
        g = generate_tokens(StringIO(s).readline)   # tokenize the string
        string = ""
        prevToken = ""
        for _, tokval, _, _, _ in g:
            if prevToken != "@" and tokval.isalpha() and  prevToken != "/@":
                string += self.__getNs() + ":" + tokval
            else:
                string += tokval
            prevToken = tokval
        return  string

    def __del__(self):
        self.__doc.freeDoc()
        self.__ctxt.xpathFreeContext()

    def getContext(self):
        return self.__ctxt


class XmlUtil:
    def __init__(self, xmlNode, ctxt):
        self.__xmlNode = xmlNode
        self.__xpathContext = ctxt

    def getAttributesMapFromNode(self):
        if self.__xmlNode is None or (type(self.__xmlNode) == list  and len(self.__xmlNode) == 0):
            return {}
        a = {}
        if type(self.__xmlNode) == list and len(self.__xmlNode) > 0:
            self.__xmlNode = self.__xmlNode[0]

        if self.__xmlNode.properties is not None:
            for att in [i for i in self.__xmlNode.properties if i.type == "attribute"]:
                a[att.name] = att.content
        return  a

    def getChildContent(self, childName):
        if self.__xmlNode is None:
            return None

        if  self.__xmlNode.get_children() is None:
            return  None

        #        s= libxml2.xpathContext()
        #        s.
        self.__xpathContext.setContextNode(self.__xmlNode)
        #
        children = self.__xpathContext.xpathEval("app:" + childName + "/*")

        return children

    def getContent(self):
        if self.__xmlNode is None or (type(self.__xmlNode) == list  and len(self.__xmlNode) == 0):
            return None

        if  self.__xmlNode.get_children() is None:
            return  None

        self.__xpathContext.setContextNode(self.__xmlNode)
        content = self.__xpathContext.xpathEval("app:*")

        return content

    def getChild(self, childName):
        if self.__xmlNode is None or (type(self.__xmlNode) == list  and len(self.__xmlNode) == 0):
            return None

        if  self.__xmlNode.get_children() is None:
            return  None

        #        s= libxml2.xpathContext()
        #        s.
        self.__xpathContext.setContextNode(self.__xmlNode)
        #
        children = self.__xpathContext.xpathEval("app:" + childName)

        return children

    #        for c in self.__xmlNode.get_children():
    #            if c.name == childName:
    #                return c

    def getChildMapFromNode(self, childName):
        children = self.getChildContent(childName)
        tMap = {}
        if children is None:
            return {}

        for node in children:
        #            if node.type == "element":
            tMap[node.name] = node.content
        return tMap


        #def getObjectFromXMl(xmlPath, schemaPath=None):
        #    from lxml import  objectify
        #
        #    objectify.XML()
        #    return objectify.fromstring()


def parseAndObjectifyXml(xmlPath, xsdPath=None):
    from lxml import  etree


    xmlinput = open(xmlPath)
    xmlContent = xmlinput.read()

    if xsdPath:
        xsdFile = open(xsdPath)

        schema = etree.XMLSchema(file=xsdFile)

        xmlinput.seek(0)
        myxml = etree.parse(xmlinput)

        try:
            schema.assertValid(myxml)

        except etree.DocumentInvalid as x:
            print "In file %s error %s has occurred." % (xmlPath, x.message)
        finally:
            xsdFile.close()

    xmlinput.close()
    return objectify.fromstring(xmlContent)


def removeNSFromValue(value):
    import  re

    name = re.split("\\{.*\\}", value)
    if len(name) <= 1:
        return value
    else:
        return name[1]
        #root = parseAndObjectifyXml("/home/pooya/I2Project/trunk/main/schema/form.xml",
        #                            "/home/pooya/I2Project/trunk/main/schema/xviewfd.xsd")