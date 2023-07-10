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
