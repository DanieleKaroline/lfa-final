from re import findall as find, match, split #biblioteca de expressões 

def joinAut(afd, afndTemp):
    mapaNovosEstados = {x: x + len(afd) for x in range(len(afndTemp))} # cria um dicionário, com as novas posições na afnd principal das regras do afnd
    aux = []

    if '&' in afd[0].keys():     # É criado uma nova regra S' que leva a regra S por epsilon transição
        afd[0]['&'].append(mapaNovosEstados[0])
    else:
        afd[0].update({'&': [mapaNovosEstados[0]]})
    
    for chave in afndTemp.keys(): #percorre os estados do afnd temporario
        for ch in afndTemp[chave].keys(): #percorre os simbolos/transições dos estados
            if ch == '*': # se for terminal, continua o loop
                continue
            aux = [] #lista auxiliar com os novos estados da afnd temporario
            for i in afndTemp[chave][ch]: # percorre os estados atingiveis pelo simbolo
                aux.append(mapaNovosEstados[i]) 
            afndTemp[chave][ch] = aux #atualiza os estados atingiveis da afnd temporaria, para os novos estados que serão criados na afnd principal
    
    for chave in afndTemp.keys():
        afd.update({mapaNovosEstados[chave] : afndTemp[chave]}) #cria os novos estados na afnd principal

def joinList(l1, l2):
    return l1 + list(set(l2) - set(l1))


def joinState(automato, estados):
    # É feita a união de todos os estados do automato que estão na lista estados
    final = {} #simbolos e os estados acessíveis a partir dele, é atualizado a cada passagem pela função 
    def unir(estado):
        for e in estado:
            if e in final:
                final[e] = joinList(final[e], estado[e])
            else:
                final.update({e: estado[e]})

    for estado in estados: # percorre os estados que precisam ser unidos, e adiciona as transições de cada simbolo para o dicionario final
        unir(automato[estado])
    return final

def eliminarInalcancaveis(afnd):
    visitados = set()

    def elimina(regra, estado):        # Utiliza uma dfs para remover recursivamente
        if estado in visitados:
            return
        
        visitados.add(estado)
        
        for chave in regra.keys():
            if chave == '*':
                continue
            for i in regra[chave]:
                elimina(afnd[i], i)

    elimina(afnd[0], 0)
    x = len(afnd)

    for i in range(x):
        if i not in visitados:      # Após a dfs estados não visitados são eliminados
            del afnd[i]
            
def eliminarEpsilonTransicoes(afnd):
    epsilon = []

    for chave in afnd.keys(): #mapeia os estados que possuem epsilon transição
        if '&' in afnd[chave]:
            epsilon.append(chave)

    def copiarRegras(regras, nRegra):  # Recursivamente copia regras que são acessadas por uma epsilon transição
        if nRegra not in epsilon:
            return  # Caso não tenha epsilon transições na regra
        
        epsilon.remove(nRegra) 
        
        for regra in regras['&']: #percorre os estados que são acessíveis por epsilon transição
            chaves = afnd[regra].keys() #salva os simbolos dos estados atingidos por epsilon transição
            
            if '&' in chaves: #caso os estados atingidos tenham epsilon transição, remove recursivamente
                copiarRegras(afnd[regra], regra)
                regras['&'] = joinList(regras['&'], afnd[regra]['&'])
        
        # une as transições de cada simbolo dos estados atingidos por epsilon transição, com as regras do estado que tem epsilon transição
        afnd[nRegra] = joinState(afnd, regras['&'] + [nRegra]) 

    epAux = epsilon.copy()
    
    for ep in epAux:
        copiarRegras(afnd[ep], ep) #copia as regras dos estados atingidos por epsilon transição, para o estado que tinha epsilon transição
    
    for ep in epAux:
        del afnd[ep]['&'] #apaga as regras dos estados que tenham epsilon transição

def eliminarInalcancaveis(afnd):
    visitados = set()

    def elimina(regra, estado):        # Utiliza uma dfs para remover recursivamente
        if estado in visitados:
            return
        
        visitados.add(estado)
        
        for chave in regra.keys():
            if chave == '*':
                continue
            for i in regra[chave]:
                elimina(afnd[i], i)

    elimina(afnd[0], 0)
    x = len(afnd)

    for i in range(x):
        if i not in visitados:      # Após a dfs estados não visitados são eliminados
            del afnd[i]




def gerarAutToken(afnd, token, alphabet):
    if not afnd:
        afnd.update({len(afnd): {}}) #gera o afnd com o index == (tamanho atual da afnd = 0, 1, 2, 3 -- Criando assim as regras), transição 0 é a inicial
    
    tokenInicial = True #primeiro caracter inicial, o que vai guiar para as próximas regras
    
    for tk in token: # percorre a string do token 
        if tk not in alphabet: # se o caracter ainda não estiver no alfabeto aceito
            alphabet.append(tk) # adiciona no alfabeto da linguagem
        
        if tokenInicial:   # Token inicial vai para o primeiro estado do automato
            mapeado = afnd[0] # 'ponteiro' para o estado inicial

            if tk in mapeado.keys():
                mapeado[tk].append(len(afnd)) #caso já exista uma regra com esse simbolo, adiciona uma transição para um novo estado para essa regra
            else:
                mapeado.update({tk : [len(afnd)]})
            tokenInicial = False
        else:
            afnd.update({len(afnd) : {tk: [len(afnd) + 1]}}) # cria um novo estado, que irá levar para o próximo a partir do simbolo
    
    afnd.update({len(afnd) : {'*': [1]}}) # quando chega ao final do token, o novo estado criado é final

def gerarAfndGramatica(afnd, gramatica, alfabeto):
    if not afnd: #se não tiver palavras reservadas, cria o afnd
        afnd.update({0: {}})
    
    afndTemporario = {}
    mapaRegras = {}
    
    for regra in gramatica: #percorre as produções da gramática
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

            if terminal not in alfabeto: #caso o caracter nao esteja no alfabeto
                alfabeto.append(terminal) #adiciona ao alfabeto da gramática

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

    joinState(afnd, afndTemporario)

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

#print do automato
def printAut(afnd, alfabeto):
    alfabeto.sort()
    print('     {}'.format('-----'*len(alfabeto)))
    print('     |', end='')
    for i in alfabeto:
        print('  {:2}|'.format(i), end='')
    print('\n     {}'.format('-----'*len(alfabeto)))
    for i in afnd.keys():
        if '*' in afnd[i].keys():
            print('*', end='')
        else:
            print(' ', end='')
        print('{:3}:|'.format(i), end='')
        for j in alfabeto:
            if j in afnd[i].keys():
                print(' {:2} |'.format(afnd[i][j][0]), end='')
            else:
                print(' {:2} |'.format('-'), end='')
        print('')
    print('     {}'.format('-----'*len(alfabeto)))