import os
import sys
sys.path.insert(0, '..')

def getDoc(body: list)-> str:
    s = ""
    toCut = 0
    for el in body:
        b = True
        for e in el.split('\n'):
            if b:
                s += "- " + e.strip() + "\n"
                b = False
                toCut = len(e.strip()) + 3
            else:
                s += "  - " + e.strip() + "\n"
                toCut = len(e.strip()) + 5
    return s[:-toCut]

def scanFile(fName: str, dirName: str)-> str:
    f = open("../" + dirName + "/" + fName, "r")
    s = ""
    fileContent = f.read()

    for line in fileContent.split("def"):
        if line.__contains__("\"\"\""):
            line = line.split("\"\"\"")
            func, docs = line[0], line[1]
            s += "\n\n ### Function Header --> \n\n`" + func + "` \n\n "
            s += getDoc(docs.split("\n\n"))
        

    return s

def getDocumentation(files: list, d: str)-> str:
    s = "## Directory " + d + " \n\n "
    for f in files:
        s += "### File " + f + " \n\n "
        s += scanFile(f, d)
        s += " \n\n <hr> \n\n"
    return s

def getFileList(dir: str)-> list:
    l = list()
    for e in os.scandir('../' + dir):
        if e.name.__contains__('.py'):
            l.append(e.name)
    return l

entries = os.scandir('../')
for e in entries:
    if e.is_dir() and not e.name.__contains__('.'):
        directory = e.name
        files = getFileList(directory)
        mdString = getDocumentation(files, directory)
        f = open("../" + directory + "/Doc.md", "w")
        f.write(mdString)
        f.close()