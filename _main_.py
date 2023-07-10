from re import findall as find, match, split #biblioteca de expressões regulares
from sources.functions import *

#função que faz a carga do afnd
def Charge(fileList, auxList, afnd):
    for tokenR in auxList: #Lê os tokens da lista de entrada
        if not tokenR: #terminou de ler os tokens
            fileList.remove(tokenR) #remove da lista de entrada
            break 
        GenAutToken(afnd, tokenR, alphabet)
        fileList.remove(tokenR) #remove da lista de entrada

    auxList = fileList.copy() #na lista de entrada temos apenas as gramáticas para serem lidas

    while fileList:
        for ruleGrRead in auxList:    
            if not ruleGrRead: #após ler todas as regras da gramática, une as regras da gramática com as dos tokens
                GenAfndGrammatic(afnd, grammatic, alphabet) 
                grammatic.clear() 
                fileList.remove(ruleGrRead)
            else:
                grammatic.append(ruleGrRead) 
                fileList.remove(ruleGrRead)
                
#função que gera a carga de tokens do automato
def GenAutToken(afnd, token, alphabet):
    if not afnd:
        afnd.update({len(afnd): {}}) #gera o afnd com o index == o tamanho atual do afnd, gerando as regras, transição 0 é a inicial
    
    initialToken = True #primeiro caracter inicial, o que vai guiar para as próximas regras
    
    for tk in token: # percorre a string do token 
        if tk not in alphabet: # se o caracter ainda não estiver no alfabeto aceito
            alphabet.append(tk) # adiciona no alfabeto 
        if initialToken:   # o token inicial vai para o primeiro estado do automato
            listed = afnd[0] # aponta para o estado inicial e lista

            if tk in listed.keys():
                listed[tk].append(len(afnd)) #caso já exista uma regra com esse simbolo, adiciona uma transição para um novo estado
            else:
                listed.update({tk:[len(afnd)]}) #se não, continua normalmente
            tokenInicial = False
        else:
            afnd.update({len(afnd):{tk:[len(afnd)+1]}}) # cria um novo estado, que irá levar para o próximo a partir do simbolo
    
    afnd.update({len(afnd):{'*':[1]}}) 
    

def GenAfndGrammatic(afnd, grammatic, alphabet):
    if not afnd: #se não tiver palavras reservadas, cria o afnd
        afnd.update({0: {}})
    
    afndTemporario = {}
    mapaRegras = {}
    
    for regra in grammatic: #percorre as produções da gramática
        simbolos = find(r'(\w*<\w+>|\w+|&)', regra) # quebra em regra e suas produções
        
        if simbolos[0] in mapaRegras.keys():     # Verifica se a regra já foi criada
            indiceRegra = mapaRegras[simbolos[0]] 
        else:
            indiceRegra = len(afndTemporario) #indice da regra
            afndTemporario.update({indiceRegra : {}}) #cria um novo estado do automato temporario
            mapaRegras.update({simbolos[0]: indiceRegra}) #mapeia a regra, relacionando-a com o indice do novo estado criado no automato

        for simbolo in simbolos[1:]: #percorre as produções da regra
            terminal = find(r'^\w+', simbolo) 
            naoTerminal = find(r'<\w+>', simbolo) 
            terminal = '&' if not terminal else terminal[0] #caso nao ache simbolo terminal, cria um epsilon transição

            if terminal not in alphabet: #caso o caracter nao esteja no alfabeto
                alphabet.append(terminal) #adiciona ao alfabeto da gramática

            if not naoTerminal:       # produção sem não terminal, gera uma regra que tem transição para um estado terminal
                rg = afndTemporario[indiceRegra] #ponteiro para o estado correspondente a regra sendo lida

                if terminal in rg.keys(): #se ja existir esse terminal no estado
                    rg[terminal].append(len(afndTemporario)) #acrescenta nova transição no simbolo
                else:
                    rg.update({terminal : [len(afndTemporario)]}) #cria um novo simbolo no estado

                afndTemporario.update({len(afndTemporario): {'*':[1]}}) #cria um novo estado/regra terminal
            else:
                naoTerminal = naoTerminal[0]

                if naoTerminal in mapaRegras.keys(): #caso a regra ja tenha sido mapeada
                    rg = mapaRegras[naoTerminal] #armazena o indice do estado do automato correspondente a regra lida
                else: # se nao estiver mapeada, cria um novo estado no automato
                    rg = len(afndTemporario) #indice do novo estado
                    mapaRegras.update({naoTerminal: rg}) #mapeia a regra, relacionando-a com o indice do novo estado criado no automato
                    afndTemporario.update({rg: {}}) #cria um novo estado do automato temporario
                
                mp = afndTemporario[indiceRegra] #ponteiro para o estado do automato corresponde a regra sendo lida
                
                if terminal in mp.keys(): #caso o simbolo ja esteja no estado do automato
                    mp[terminal].append(rg) #cria a transição para o estado do referente ao nao terminal
                else:
                    mp.update({terminal: [rg]}) #acrescenta mais uma transição para o simbolo ja existente

    joinAut(afnd, afndTemporario)


def determinizar(afnd):
    mpRgs = {}
    visitados = set()

    def determiniza(regra, nReg):  # Recursivamente determiniza o automato
        if nReg in visitados: 
            return
        visitados.add(nReg) 
        chaves = list(regra.keys()) 

        for chave in chaves:
            if len(regra[chave]) > 1: #se a regra tiver mais que uma transição
                regra[chave].sort()
                nRg = str(regra[chave])  # É gerada uma nova regra que será mapeada no mpReg
                
                if nRg not in mpRgs.keys(): 
                    nEst = len(afnd)  # Novo estado que será mapeado pela variavel nRg
                    mpRgs.update({nRg: nEst})
                    afnd.update({len(afnd): joinState(afnd, regra[chave])})
                    determiniza(afnd[nEst], nEst) # determiniza os novos estados criados
                
                regra.update({chave: [mpRgs[nRg]]}) # atualiza a regra que tinha mais que uma transição, para o novo estado criado

    i, t = 0, len(afnd)
    while i < t:
        determiniza(afnd[i], i)
        i, t = i + 1, len(afnd)  # Cada nova regra criada também deve ser determinizada
    print(afnd)



####### main #######
afnd = {}
alphabet = []
grammatic = []

file = open("entrada.txt", "r") #abre arquivo
fileString = file.read() #le e salva numa string
fileList = fileString.split('\n') #separa a string, cada linha é uma da lista 
auxList = fileList.copy() #copia a lista

#carga 
Charge(fileList, auxList, afnd)
print("AFND: \n")
printAut(afnd, alphabet)
eliminarEpsilonTransicoes(afnd)
determinizar(afnd)
print("Após Determinização e Eliminação de epsilon transições: \n")
printAut(afnd, alphabet)
eliminarInalcancaveis(afnd)
print("Após eliminação de inalcançaveis: \n")
printAut(afnd, alphabet)