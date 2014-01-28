import os
from util.utils import NonUniqueMap, generateProject

__author__ = 'PHo'

class Domains(NonUniqueMap):
    def __init__(self):
        NonUniqueMap.__init__(self)

    def createCSModels(self):
        mainClassName = self.get("-main-")

        if not mainClassName:
            raise Exception, "Main XAML window not defined"

        mainClassName = "%s.xaml" % mainClassName[0].replace(".", os.path.sep)
        projectPath = generateProject("wpftest", mainClassName, "NONE")
        for domain, contents in self.iteritems():
        #osDomainPath = domain.replace(".", "/")
        #os.makedirs(osDomainPath)
            for content in contents:
                if hasattr(content, "createCsCode"):
                    content.createCsCode(projectPath)
                    #filePath = osDomainPath + "/" + str(content) + ".cs"
                    #with open(filePath, 'w') as f:
                    #f.write(content.getCsCode())