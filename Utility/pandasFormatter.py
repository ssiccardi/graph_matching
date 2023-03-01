import pandas as  pd
import sys
sys.path.insert(0, '..')

def _max(s):
    s = s.split(",")
    if len(s) < 8:
        return 0
    tmp1 = s[6].count(" -- ")
    tmp2 = s[7].count(" -- ")
    if tmp1 > tmp2:
        return tmp1
    return tmp2
def _getMax(s):
    m = 0
    for row in s:
        tmp = max(row)
        if tmp > m:
            m = tmp
    return m
def _getNewIndex(s1, m):
    tmp = ""
    for st in s1:
        if st.find("Attr.") != -1:
            for i in range(0, m):
                tmp += st + "[" + str(i+1) + "], "
        else:
            tmp += st + ", "
    return tmp[:-2]
def _newContents(s):
    tmp = s.split(",")
    if len(tmp) < 8:
        return s
    s = ""
    for i in range(0, 8):
        if i < 6:
            s += tmp[i] + ", " 
        else:
            newCols = tmp[i].split(" -- ")
            for nc in newCols:
                s += nc + ", "
            s = s[:-2]
    return s

def formatCSV():
    file1 = open("../Contents/RelationMatchingAnalisi.csv", "r")
    tmpStr = file1.read().split("\n")
    maxValue = _getMax(tmpStr[1:])

    newFileContent = _getNewIndex(tmpStr[0].split(","), maxValue)

    for s in tmpStr[1:]:
        newFileContent += "\n" + _newContents(s)

    file2 = open("../Contents/RelationMatchingAnalisiFormatted.csv", "w")
    file2.write(newFileContent)

    file1.close()
    file2.close()
