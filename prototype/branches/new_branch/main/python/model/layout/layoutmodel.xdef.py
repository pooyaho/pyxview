__author__ = "pooya"

#output = "Enter Your Output path to generate your model"
#header = """Enter Your File Headers [like import ,comments and etc]"""
#
#yourVar1 = [
#    "Model Name",
#    "Model Extra Information",
#        {
#        "Your Field Name": (type : ("number"|"str"|"list"|"dict"),default Value,ReadOnly, Custom Regex Constraint)}
#        above type is list
#
#
#        yourVar2 = {"name": "Model Name", "comment": "Model Extra Information",
#                    "fields":
#                            {
#                            ("Your Field Name": ("type : ("number"|"str"|"list"|"
#                            dict"),default Value,ReadOnly, Custom Regex Constraint)
#                        }}
#    above type is dict


output = "layoutmodel.py"
BASE_CLASS, CLASS_NAME, FIELDS = "baseClass", "name", "fields"

a = {CLASS_NAME: "Page", BASE_CLASS: "object",
     FIELDS: {
         "widgets": ("dict:BaseWidget->name"),
         "widgetName": ("list:widgetName")
     }
}

#a = {CLASS_NAME: "BaseWidget", "comment": "Base class for all widgets.", BASE_CLASS: "object",
#     FIELDS:
#             {
#             "source": ("str", "", False, "^[a-zA-Z][\._\w\d]*[_\w\d]$"),
#             "name": ("str", "", False, "^[a-zA-Z][_\w\d]*$"),
#
#         }
#}