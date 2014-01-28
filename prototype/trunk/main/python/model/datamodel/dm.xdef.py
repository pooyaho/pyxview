__author__ = 'namnik'
BASE_CLASS, CLASS_NAME, FIELDS = "baseClass", "name", "fields"

output = "dataobjectmodel.py"
header = "sys", "os"

a = {CLASS_NAME: "DateTime", BASE_CLASS: "BaseClassModel",
     FIELDS: {
         "timeZone": ("str"),
         "CalendarTypes": ("number")
     }
}

b = {CLASS_NAME: "Currency", BASE_CLASS: "BaseClassModel",
     FIELDS: {
         "currencyType": ("str"),
         }
}

c = {CLASS_NAME: "Decimal", BASE_CLASS: "BaseClassModel",
     FIELDS: {
         "digits": ("number"),
         "precision": ("number")
     }
}

d = {CLASS_NAME: "Integer", BASE_CLASS: "BaseClassModel",


     FIELDS: {
         "digits": ("number"),
         "precision": ("number")
     }
}

e = {CLASS_NAME: "Double", BASE_CLASS: "BaseClassModel",


     FIELDS: {
         "digits": ("number"),
         "precision": ("number")
     }
}

f = {CLASS_NAME: "Map", BASE_CLASS: "BaseClassModel",
     FIELDS: {
         "item": ("list")
     }
}
g = {CLASS_NAME: "Duration", BASE_CLASS: "BaseClassModel",
     FIELDS: {
         "name": ("str")
     }
}

h = {CLASS_NAME: "String", BASE_CLASS: "BaseClassModel",
     FIELDS: {
         "lang": ("number"),
         }
}

i = {CLASS_NAME: "Composition", BASE_CLASS: "BaseClassModel",
     FIELDS: {
         "type": ("str"),
         }
}

j = {CLASS_NAME: "Boolean", BASE_CLASS: "BaseClassModel",
     FIELDS: {
     }
}






