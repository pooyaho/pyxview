import string
#from model.layout.layoutmodel import Layout, Row, Cell, Page
from model.widget.widgetmodel import *

import xmlutils.xutils

__author__ = 'namnik'

import xmlutils.xutils


def createModelFromXml(filePath, schemaPath):
    xpathR = xmlutils.xutils.XpathResult(filePath, schemaPath)
    mainPage = Page()



    #    def getAttributeValue(nodeName, attName):
    #        result = xpathR.getXpathResult("//" + nodeName + "/@" + attName)
    #        if len(result) <= 0:
    #            return None
    #        return result[0].content

    #    def fillWidget():
    #        widgets = xpathR.getXpathResult("//page/*")
    #        for wdg in widgets:
    #            mainWidget.addWidget(wdg)



    def fillMainAttributes():
        innerWidgets = xpathR.getXpathResult("//page")
        for innerWidget in innerWidgets:
            util = xmlutils.xutils.XmlUtil(innerWidget, xpathR.getContext())
            atts = util.getAttributesMapFromNode()
            mainPage.fillAttributes(atts)
            #            mainPage.name=atts["name"]

    def fillMainLayout():
        result = xpathR.getXpathResult("/page/layout")

        if len(result) > 1:
            raise Exception, "In main page, only one layout has allowed"
        if not len(result):
            return False
            #        for layout in result:
        mainPage.layout = fillLayout(result[0])

        return  True


    def fillLayout(layout):
        i = 1
        l = Layout()

        util = xmlutils.xutils.XmlUtil(layout, xpathR.getContext())
        atts = util.getAttributesMapFromNode()

        l.name = atts.get("name", None)

        grid = xmlutils.xutils.XmlUtil(util.getChild("grid"), xpathR.getContext())
        atts["flow"] = grid.getAttributesMapFromNode().get("flow", "none")
        l.fillAttributes(atts)

        rows = grid.getChild("row")

        if rows is None:
            return l

        for r in rows:
            row = Row()
            rowUtil = xmlutils.xutils.XmlUtil(r, xpathR.getContext())
            atts = rowUtil.getAttributesMapFromNode()
            row.fillAttributes(atts)

            cols = rowUtil.getChild("cell")
            for c in cols:
                cell = Cell()
                cellUtil = xmlutils.xutils.XmlUtil(c, xpathR.getContext())
                atts = cellUtil.getAttributesMapFromNode()

                cell.fillAttributes(atts)
                cell.name = atts.get("name", None)

                for w in cellUtil.getContent():
                    widget = WidgetSelector.selectWidget(w.name)

                    if w.name == "layout":
                        widget = fillLayout(w)
                    else:
                        widgetUtil = xmlutils.xutils.XmlUtil(w, xpathR.getContext())
                        atts = widgetUtil.getAttributesMapFromNode()

                        widget.fillAttributes(atts)

                        if not atts.has_key("name"):
                            atts["name"] = w.name + str(i)
                            i += 1

                        widget.name = atts["name"]

                    mainPage.widgetNames.append(widget.name)

                    cell.addWidget(widget)

                row.addCell(cell)

            l.addRow(row)
        return l

    #        hasLayout = True
    #        mainPage.setLayout(l)
    #        return hasLayout

    #            mainClassModel.setClassName(atts["name"])
    #            domain.setDomainName(atts["domain"])

    def fillFreeWidgets():
        result = xpathR.getXpathResult("/page/*")

        for widget in result:
            w = WidgetSelector.selectWidget(widget.name)
            util = xmlutils.xutils.XmlUtil(widget, xpathR.getContext())
            atts = util.getAttributesMapFromNode()
            w.fillAttributes(atts)
            w.name = atts["name"]
            mainPage.addWidget(w)


    fillMainAttributes()
    if not fillMainLayout():
        fillFreeWidgets()

    return mainPage


def createHtmlTemplate(widgetModel):
    htmlTemplate = string.Template(
        """
        <html>
        <head>
            <title>$title</title>
        </head>
        <body>
            $body
        </body>
        </html>
        """
    )

    formTemplate = string.Template(
        """
        <form>
        </form>
        """
    )
    bodyTemplate = string.Template(
        """
        <input $attributes/>
        """
    )
    attributeTemplate = string.Template(
        """
        $name=\"$value\"
        """
    )


def createXamltemplate(widgetModel):
    baseTemplate = string.Template(
        """
        <Grid>
        <Grid.RowDefinitions>
        $rows
        </Grid.RowDefinitions>
         <Grid.ColumnDefinitions>
         $cols
         </Grid.ColumnDefinitions>
        $widgets
        <Grid>
        """)


def  __createXamlWidgetTemplate():
    widgetMap = {
        "button": "Button",
        "checkBoc": "CheckBox",
        "textBox": "TextBox",
        "combo": "ComboBox",
        "listBox": "ListBox",
        "radioButton": "RadioButton",
        "image": "Image",
        "label": "Label",
        "grid": "Grid",
        }

    propMap = {
        "button": "Button",
        }

x = createModelFromXml("/home/pooya/I2Project/trunk/main/schema/form.xml", "xviewfd.xsd")

print x.layout.getXamlCode()

#    htmlCode=widget.getNoneEmptyAttributes()
#
#    for i in htmlCode:
#        print i
#
#