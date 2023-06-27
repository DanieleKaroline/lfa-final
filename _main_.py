from sources.afd import *

file = open("entrada.txt", "r")
fileString = file.read()
fileList = fileString.split('\n')
auxList = fileList.copy()
print(fileString)
afnd(fileList, auxList)
