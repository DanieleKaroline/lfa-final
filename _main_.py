from sources.afd import *

file = open("entrada.txt", "r") #abre arquivo
fileString = file.read() #le e salva numa string
fileList = fileString.split('\n') #separa a string, cada linha é uma da lista 
auxList = fileList.copy() #copia a lista
#teste print(fileString)


afnd(fileList, auxList)
