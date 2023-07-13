from sources.functions import *
    
####### main #######
afnd = {}
alfabeto = []
gramatica = []

file = open("entrada.txt", "r") #abre arquivo
fileString = file.read() #le e salva numa string
fileList = fileString.split('\n') #separa a string, cada linha é uma da lista 
auxList = fileList.copy() #copia a lista

#carga do automato
for tokenLido in auxList:
    #if not executará se tokenLido for vazio
    if not tokenLido: #terminou de ler os tokens
        fileList.remove(tokenLido) #remove da lista de entrada
        break 
    #adiciona as regras de produção para o token lido ao autômato
    gerarAutToken(afnd, tokenLido, alfabeto) #adiciona ao afnd as regras de produção para o token lido
    fileList.remove(tokenLido) #remove da lista de entrada

auxList = fileList.copy() #na lista de entrada temos apenas as gramáticas para serem lidas

while fileList:
    for regraGLida in auxList:    
        # Esta condição verifica se regraGLida é vazio. Se for vazio, significa que terminou de ler todas as regras da gramática.
        if not regraGLida: #após ler todas as regras da gramática, une as regras da gramática com as dos tokens
            #adiciona as regras da gramática ao autômato.
            gerarAutGramatica(afnd, gramatica, alfabeto) 
            #limpa gramaticas
            gramatica.clear() 

            fileList.remove(regraGLida)
        #se a condição if not regraGLida não for satisfeita, significa que ainda há regras da gramática a serem lidas
        else:
            gramatica.append(regraGLida) 
            fileList.remove(regraGLida)
        
printAut(afnd, alfabeto)
print("\n Determinizado: \n")
determinizar(afnd)
printAut(afnd, alfabeto)
print("\n Após eliminar Epsilon Transição e Inalcançáveis: \n")
eliminarEpsilonTransicoes(afnd)
eliminarInalcancaveis(afnd) 
printAut(afnd, alfabeto)