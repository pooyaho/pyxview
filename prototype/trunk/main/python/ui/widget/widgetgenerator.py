import string
#from model.layout.layoutmodel import Layout, Row, Cell, Page


__author__ = 'PHo'

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

    #x = createModelFromXml("/home/pooya/I2Project/trunk/main/schema/form.xml", "xviewfd.xsd")
    #
    #
    #print x.getXamlCode()


    #x = parseAndObjectifyXml("/home/pooya/I2Project/trunk/main/schema/form.xml",
    #                         "/home/pooya/I2Project/trunk/main/schema/xviewfd.xsd")
    #y = createModelFromXml(x)
    #print y.getXamlCode()
    #    htmlCode=widget.getNoneEmptyAttributes()
    #
    #    for i in htmlCode:
    #        print i
    #
    #