from glob import glob
import os
from lxml import  etree, objectify
from sys import stderr
from lxml.objectify import StringElement, ObjectifiedElement
from model.datamodel.objectmodel import *
from model.domain import Domains
from model.widget.widgetmodel import *
from util.utils import separateClassName
from xmlutils.xutils import removeNSFromValue


__author__ = 'PHo'


def main(path):
    LAYOUT, DATA, WIDGET, APPLICATION = 0, 1, 2, 3 # sorted by priority (Lowest has highest)

    domains = Domains()
    objectModels = []


    def getRootTag(xmlPath):
        from xmlutils.xutils import XpathResult

        try:
            x = XpathResult(xmlPath, "")
            result = x.getXpathResult("/*")

            return result[0].name
        except Exception, x:
            print >> stderr, "Error occurred in file %s" % xmlPath, x
            return None


    def createLayoutModel(layout ):
        l = Layout()

        layout.attrib["flow"] = layout.grid.attrib.get("flow", "none")
        l.fillAttributes(layout.attrib)

        if layout.grid.row is None:
            return l

        for r in layout.grid.row:
            row = Row()
            row.fillAttributes(r.attrib)

            for c in r.cell:
                cell = Cell()

                cell.fillAttributes(c.attrib)

                row.addCell(cell)

            l.addRow(row)

        domains[layout.attrib["domain"]] = l

    def createDataModel(objectModel):
        dataModel = DataModel()


        def fillDataTypes(objModel):
            classModel = DataModelElement()
            classModel.fillAttributes(objModel.attrib)
            for dataType in objModel.elements.getchildren():
                typeName = removeNSFromValue(dataType.tag)
                modelType = selectType(typeName)
                modelType.fillAttributes(dataType.attrib)

                if hasattr(dataType, "restriction"):
                    modelType.combination = dataType.restriction.attrib.get("combination", "all")
                    for rest in dataType.restriction.getchildren():
                        modelType.constraints[removeNSFromValue(rest.tag)] = rest.text

                classModel.fields[modelType.name] = modelType
            return classModel

        def fillDefinedTypes():
            if not hasattr(objectModel, "type"):
                return

            for dataType in objectModel.type:
                c = fillDataTypes(dataType)

                dataModel.classModel.innerClass[c.name] = c


        dataModel.classModel = fillDataTypes(objectModel)
        dataModel.fillAttributes(objectModel.attrib)
        fillDefinedTypes()

        #        dataModel.domain = mainClassModel.domain

        domains[objectModel.attrib["domain"]] = dataModel


    def createWidgetModel(objectModel, isMain=False):
        mainPage = Page()
        nameInc = 1

        def fillRepeater(w):
            r = Repeater()
            for widget in w.getchildren():
                widgetType = removeNSFromValue(widget.tag)
                if widgetType == "repeater":
                    r.addWidget(fillRepeater(widget))
                elif widgetType == "layout":
                    r.addWidget(fillLayout(widget))
                w = selectWidget(widgetType)
                r.addWidget(w)
            return r

        def fillMainAttributes():
            mainPage.fillAttributes(objectModel.attrib)

            #            rindex = mainPage.dataModel.rfind(".")
            #            dataModelPackage = mainPage.dataModel[:rindex]
            #            dataModelClass = mainPage.dataModel[rindex + 1:]
            dataModelPackage, dataModelClass = separateClassName(mainPage.dataModel)
            #            dataModelClass = mainPage.dataModel[rindex + 1:]
            if not domains.has_key(dataModelPackage):
                raise Exception("Data model package %s not found!" % dataModelPackage)
                #            if not domains[dataModelPackage].hasClass(dataModelClass):
                #                raise Exception, "Data model Class %s not found!" % dataModelClass
            if not domains.searchItemName(dataModelPackage, dataModelClass):
                raise Exception, "Class %s in package %s has not found!" % (dataModelClass, dataModelClass)


        def fillMainLayout():
            if not hasattr(objectModel, "layout"):
                return False
            layout = objectModel.layout
            if len(layout) > 1:
                raise Exception("In main page, only one layout has allowed")
            if not len(layout):
                return False
            mainPage.layout = fillLayout(layout)

            return  True


        def createWidgetFromXMLObject(w):
            wType = removeNSFromValue(w.tag)
            widget = selectWidget(wType)

            if wType == "layout":
                widget = fillLayout(w)
            elif wType == "repeater":
                widget = fillRepeater(w)
            else:
                widget.fillAttributes(w.attrib)
                if not widget.name:
                    widget.name = w.name + str(nameInc)
                    #                    global nameInc
                    nameInc += 1
            return widget

        def fillLayout(layout):
            l = Layout()

            layout.attrib["flow"] = layout.grid.attrib.get("flow", "none")
            l.fillAttributes(layout.attrib)

            if layout.grid.row is None:
                return l

            for r in layout.grid.row:
                row = Row()
                row.fillAttributes(r.attrib)

                for c in r.cell:
                    cell = Cell()

                    cell.fillAttributes(c.attrib)
                    for w in c.getchildren():
                        if w.tag == "comment" or (type(w) is not StringElement and type(w) is not ObjectifiedElement):
                            continue

                        widget = createWidgetFromXMLObject(w)
                        #                        name = removeNSFromValue(w.tag)
                        #
                        #                        widget = selectWidget(name)
                        #
                        #                        if name == "layout":
                        #                            widget = fillLayout(w)
                        #                        else:
                        #                            widget.fillAttributes(w.attrib)
                        #
                        #                            if not widget.name:
                        #                                widget.name = w.name + str(i)
                        #                                i += 1

                        mainPage.widgetNames.append(widget.name)

                        cell.addWidget(widget)

                    row.addCell(cell)

                l.addRow(row)
            return l

        def fillFreeWidgets():
            if not mainPage.layout:
                raise Exception, "Layout path in the page not defined"

            layoutPackage, layoutName = separateClassName(mainPage.layout)
            if not domains.has_key(layoutPackage):
                raise Exception, "Package %s not defined in layout packages" % layoutPackage
            l = domains.searchItemName(layoutPackage, layoutName)
            if not l:
                raise Exception, "Layout %s not defined in layout packages" % layoutName
            locations = UniqueMap()

            for w in objectModel.getchildren():
                if w.tag == "comment" or (type(w) is not StringElement and type(w) is not ObjectifiedElement):
                    continue
                name = removeNSFromValue(w.tag)

                #                widget = selectWidget(name)

                if name == "layout":
                    raise  Exception, "Layout in free widget!"
                else:
                    widget = createWidgetFromXMLObject(w)
                    #                    widget.fillAttributes(w.attrib)
                    #                    mainPage.addWidget(widget)
                    locations[widget.location] = widget
                    mainPage.widgetNames.append(widget.name)

            for row in l.rows:
                for cell in row.cells:
                    widget = locations.pop(cell.name)
                    if widget:
                        cell.addWidget(widget)

            if len(locations) > 0:
                raise Exception, "There is some unknown location in layout %s of package %s" % (
                    layoutName, layoutPackage)
            mainPage.layout = l

        fillMainAttributes()
        if not fillMainLayout():
            fillFreeWidgets()

        domains[objectModel.attrib["domain"]] = mainPage
        if isMain:
            domains["-main-"] = mainPage.domain + "." + mainPage.name

    xsdPathsMap = {
        "dataModel": ("/home/pooya/I2Project/trunk/main/schema/xview-dm.xsd", DATA, createDataModel),
        "layout": ("/home/pooya/I2Project/trunk/main/schema/xview-ld.xsd", LAYOUT, createLayoutModel),
        "page": ("/home/pooya/I2Project/trunk/main/schema/xviewfd.xsd", WIDGET, createWidgetModel),
        "application": ("/home/pooya/I2Project/trunk/main/schema/xviewfd.xsd", APPLICATION, createWidgetModel)
    }

    files = glob(os.path.join(path, '*.xml'))

    for f in files:
        xmlinput = open(f)
        root = getRootTag(f)
        if not root:
            continue
        xmlContent = xmlinput.read()

        result = xsdPathsMap[root]
        xsdPath = result[0]

        #            schema = etree.parse(xmlinput)
        xsdFile = open(xsdPath)
        xmlschema = etree.XMLSchema(etree.parse(xsdFile))
        xmlinput.seek(0)

        try:
            xmlschema.assertValid(etree.parse(xmlinput))
        except etree.DocumentInvalid as x:
            print ("In file %s error %s has occurred." % (f, x.message))
        finally:
            xsdFile.close()

        xmlinput.close()
        a = objectify.fromstring(xmlContent)
        a.modelType = result[1]
        #        a.base = result[2]
        objectModels.append(a)

    objectModels = sorted(objectModels, key=lambda k: k.modelType)
    for obj in objectModels:
        if obj.modelType == DATA:
            createDataModel(obj)
        elif obj.modelType == LAYOUT:
            createLayoutModel(obj)
        elif obj.modelType == WIDGET:
            createWidgetModel(obj)
        elif obj.modelType == APPLICATION:
            createWidgetModel(obj, True)
    return domains

a = main("/home/pooya/I2Project/trunk/main/schema/test")
a.createCSModels()