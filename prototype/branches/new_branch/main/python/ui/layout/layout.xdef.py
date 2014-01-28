output = "empty.py"
header = """from main.python.model.models import Model"""

layout= [
   "layout",
    "Model Extra Information",
    "object",
        {
        "id":(),
        "width":("str"),
        "height":("str"),
        "rows":("object"),
        "columns":("object"),
        "margin":("str"),
        "padding":("str"),
        "parent":("str"),
        "flowDirection":("str")
    }]

row=[
    "row",
    "Model Extra Information",
    "object",
        {
        "id":(),
        "height":("str"),
        "valign":("str"),
        "halign":("str")
    }]

height=[
    "columns",
    "Model Extra Information",
    "object",
    {
        "id":(),
        "width":("str"),
        "rowSpan":("number"),
        "colSpan":("number"),
        "valign":("str"),
        "halign":("str"),
        "flowDirection":("str")
    }]




