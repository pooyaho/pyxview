__author__ = 'PHo'
BASE_CLASS, CLASS_NAME, FIELDS = "baseClass", "name", "fields"

output = "widgetmodel.py"
header = "sys", "os"

a = {CLASS_NAME: "BaseWidget", "comment": "Base class for all widgets.", BASE_CLASS: "object",
     FIELDS:
             {
             "source": ("str", "", False, "^[a-zA-Z][\._\w\d]*[_\w\d]$"),
             "name": ("str", "", False, "^[a-zA-Z][_\w\d]*$"),
             "label": ("str"),
             "tooltip": ("str"),
             "enabled": ("bool"),
             "visible": ("bool"),
             "tabindex": ("number"),
             "height": ("number"),
             "width": ("number"),
             "horizontalAlignment": ("str", "", False, "^(center|left|right|stretch)$"),
             "verticalAlignment": ("str", "", False, "^(center|left|right|stretch)$"),
             "location": ("str", "", False, "^[a-zA-Z][\._\w\d]*[_\w\d]$")
         }
}

b = {CLASS_NAME: "Spinner", BASE_CLASS: "BaseWidget",
     FIELDS: {
         "maxValue": ("number"),
         "minValue": ("number"),
         "type": ("any")
     }
}

z = {CLASS_NAME: "Button", BASE_CLASS: "BaseWidget",
     FIELDS: {

     }
}

c = {
    CLASS_NAME: "DateTimePicker", BASE_CLASS: "BaseWidget",
    FIELDS: {
        "selectionMode": ("str"),
        "showNextPrevMonth": ("str"),
        "showDayHeader": ("str")
    }
}
d = {
    CLASS_NAME: "Combo", BASE_CLASS: "BaseWidget",
    FIELDS: {

    }
}
e = {
    CLASS_NAME: "CheckBox", BASE_CLASS: "BaseWidget",
    FIELDS: {
        "checked": ("bool")
    }
}
f = {
    CLASS_NAME: "RadioButton", BASE_CLASS: "BaseWidget",
    FIELDS: {
        "checked": ("bool"),
        "groupName": ("str", "", False, "^[a-zA-Z][_\w\d]*$")
    }

}
g = {
    CLASS_NAME: "Image", BASE_CLASS: "BaseWidget",
    FIELDS: {
        "src": ("str", "", False, ".*"),
        "alt": ("str", "", False, ".*")
    }
}
h = {
    CLASS_NAME: "Label", BASE_CLASS: "BaseWidget",
    FIELDS: {

    }
}
i = {
    CLASS_NAME: "ListBox", BASE_CLASS: "BaseWidget",
    FIELDS: {
        "selectionMode": ("str", "", False, "(single|multiple)")
    }
}
j = {
    CLASS_NAME: "TextBox", BASE_CLASS: "BaseWidget",
    FIELDS: {
        "readonly": ("bool"),
        "textMode":("str", "", False, "(single|multiple)"),
        "textAlignment":("str", "", False, "(left|right|center|justify)")
    }
}