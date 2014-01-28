import codecs
import os
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

__author__ = 'PHo'

class UniqueMap(dict):
    def __init__(self):
        dict.__init__(self)

    def __setitem__(self, i, y):
        if dict.has_key(self, i):
            raise Exception, "Duplicate item %s" % i
        dict.__setitem__(self, i, y)


class NonUniqueMap(dict):
    def __init__(self):
        dict.__init__(self)

    def __setitem__(self, i, y):
        if dict.has_key(self, i):
            dict.__getitem__(self, i).append(y)
        else:
            dict.__setitem__(self, i, [y])

    def searchItemName(self, key, itemName):
        """
        This method is very ready to raise exception, Because it assumes that all elements has name attribute
        """
        result = [c for c in dict.__getitem__(self, key) if c.name == itemName]
        if result:
            return result[0]


class CaseInsensitiveMap(dict):
    def __init__(self):
        dict.__init__(self)

    def __setitem__(self, i, y):
        self[i.lower()] = [y]

    def __getitem__(self, item):
        return self[item.lower()]


class ResettableMap(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)
        self.__oldMap = {}

    #        self.__oldMap.update(kwargs)


    def __setitem__(self, i, y):
        if not self.__oldMap.has_key(i):
            self.__oldMap[i] = dict.__getitem__(self, i)

        dict.__setitem__(self, i, y)

    def pop(self, k, d=None):
        self.__oldMap[k] = self[k]
        return super(ResettableMap, self).pop(k, d)

    def popitem(self):
        result = super(ResettableMap, self).popitem()
        self.__oldMap[result[0]] = result[1]
        return result

    def update(self, E=None, **F):
        for k in E.iterkeys():
            if dict.has_key(self, k) and not self.__oldMap.has_key(k):
                self.__oldMap[k] = dict.__getitem__(self, k)
        return super(ResettableMap, self).update(E, **F)

    def reset(self):
        self.update(self.__oldMap)
        self.__oldMap.clear()

    def __str__(self):
        return dict.__str__(self)

    def __repr__(self):
        return super(ResettableMap, self).__repr__()


def separateClassName(classRef):
    rindex = classRef.rfind(".")

    return classRef[:rindex], classRef[rindex + 1:]


def generateProject(projectName, mainXamlPath, outputPath):
    templatePath = "../../resources/template/csproj-template"
    env = Environment(loader=FileSystemLoader(templatePath))

    for root, dirs, files in os.walk(templatePath):
    #        print root.replace(a,"")
        for file in files:
            fPath = root[len(templatePath) + 1:]
            newPath = (fPath + "/" if fPath else '') + file
            template = env.get_template(newPath)
            oPath = os.path.join(outputPath, fPath)
            try:
                os.makedirs(oPath)
            except:
                pass

            template.module.projectname = projectName

            filename = template.module.filename(projectName)

            oPath = os.path.join(oPath, filename)
            with codecs.open(oPath, 'w', "utf-8") as f:
                f.write(template.render(projectname=projectName, mainxmlpath=mainXamlPath))

    return outputPath

    #        for f in files:
    #            print( os.path.join(root, f))

    #generateProject("pooya", "ppp", "None")


    #attributesMap = ResettableMap(
    #    tabindex={"cs": "TabIndex='$value'"},
    #    name={"cs": "Name='$value'"},
    #    width={"cs": "Width='$value'"},
    #    enabled={"cs": "IsEnabled='$value'"},
    #    height={"cs": "Height='$value'"},
    #    visible={"cs": "Visibility='$value'"},
    #    source={"cs": "='$value'"},
    #    verticalalignment={"cs": "VerticalAlignment='$value'"},
    #    horizontalalignment={"cs": "HorizontalAlignment='$value'"},
    #    label={"cs": "Content='$value'"},
    #    location={"cs": "='$value'"},
    #    rowindex={'cs': "Grid.Row='$value'"},
    #    colindex={'cs': "Grid.Column='$value'"}
    #)
    #
    #attributesMap["name"] = "pooya"
    #
    #print attributesMap
    #
    #attributesMap["name"] = "pooya"
    #
    #attributesMap.reset()
    #
    #print attributesMap

    #print "pooya"*3