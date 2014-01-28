#from re import match
#
#attValidationMap = {
#    "source": "^[a-zA-Z][\._\w\d]*[_\w\d]$",
#    "name": "^[a-zA-Z][_\w\d]*$",
#    "label": "^.*$",
#    "tooltip": "^.*$",
#    "enabled": "(true|false)",
#    "visible": "(true|false)",
#    "tabindex": "^\d+$",
#    "height": "^\d+$",
#    "width": "^\d+$",
#    "horizontalAlignment": "(center|left|right|stretch)",
#    "verticalAlignment": "(center|left|right|stretch)",
#    "location": "^[a-zA-Z][\._\w\d]*[_\w\d]$",
#    "anchor": ".*",
#    "cellSpacing": "^\d+$",
#    "cellPadding": "^\d+$",
#    "layout": "^[a-zA-Z][\._\w\d]*[_\w\d]$",
#    "dataModel": "^[a-zA-Z][\._\w\d]*[_\w\d]$",
#    "flow": "(horizontal|vertical|none)",
#    "groupName": "^[a-zA-Z][_\w\d]*$",
#    "src": ".*",
#    "alt": ".*",
#    "rows": "^\d+$",
#    "selectionMode": "",
#    "maxValue": "^\d+$",
#    "minValue": "^\d+$",
#    "type": "",
#    "checked": "(true|false)",
#    "readonly": "(true|false)",
#    "text": ".*"
#}
#
#class BaseType(object):
#    def __init__(self, name=None, atts=None):
#        if not atts: atts = {}
#        super(BaseType, self).__init__()
#        self.__dict__["atts"] = atts
#        self.__dict__["name"] = name
#
#    def setAttributes(self, atts):
#        for k, v in atts.iteritems():
#            regex = attValidationMap.get(k, None)
#            if regex is None:
#                raise Exception, "Unknown attribute name : %s " % k
#            if v is None:
#            #                raise Exception, "Value of : %s  is Null" % k
#                continue
#
#            if match(regex, v) is None:
#                raise  Exception, "In:%s value:%s of %s attribute is not valid" % (self.__dict__["name"], v, k)
#
#        self.__dict__["atts"] = atts
#
#    def getAttributes(self, atts):
#        self.__dict__["atts"] = atts
#
#    def setName(self, name):
#        self.__dict__["name"] = name
#
#    def getName(self):
#        return self.__dict__["name"]
#
#
#class Page(BaseType):
#    def __init__(self, name=None, widgets=None, layout=None, atts=None):
#        if not atts: atts = {}
#        if not widgets: widgets = []
#        super(Page, self).__init__(name, atts)
#        self.__dict__["widgets"] = widgets
#        self.__dict__["widgetNames"] = []
#        self.__dict__["layout"] = layout
#
#    def addWidget(self, widget):
#        if self.__dict__["layout"] <> None:
#            raise  Exception, "When layout already defined, widget should not add"
#        self.addWidgetName(widget.getName())
#        self.__dict__["widgets"].append(widget)
#
#    def addWidgetName(self, name):
#        if name in self.__dict__["widgetNames"]:
#            raise  Exception, "Duplicate widget name : %s " % name
#        self.__dict__["widgetNames"].append(name)
#
#    def setLayout(self, layout):
#        self.__dict__["layout"] = layout
#
#
#class Widget(BaseType):
#    def __init__(self, name=None, atts=None):
#        if not atts: atts = {}
#        super(Widget, self).__init__(name, atts)
#        self.__widgets = []
#
#    def addWidget(self, widget):
#        self.__widgets[widget.getName()] = widget
#
#
#class  Layout(BaseType):
#    def __init__(self, name=None, atts=None):
#        if not atts: atts = {}
#        super(Layout, self).__init__(name, atts)
#        self.__name = name
#        self.__rows = []
#
#    def addRow(self, row):
#        self.__rows.append(row)
#
#
#class  Row(BaseType):
#    def __init__(self, atts=None):
#        if not atts: atts = {}
#        super(Row, self).__init__("", atts)
#        self.__cells = []
#
#    def addCell(self, cell):
#        self.__cells.append(cell)
#
#
#class  Cell(BaseType):
#    def __init__(self, name=None, atts=None):
#        if not atts: atts = {}
#        super(Cell, self).__init__(name, atts)
#        self.__name = name
#        self.__widgets = {}
#
#    def addWidget(self, widget):
#        self.__widgets[widget.getName()] = widget