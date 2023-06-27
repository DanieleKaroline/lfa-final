def afnd(fileList, auxList):
    afnd = {}
    alphabet = []
    grammatic = []
    for tokenR in auxList:
        if not tokenR: #terminou de ler os tokens
            fileList.remove(tokenR) #remove da lista de entrada
            break 
        gAfndToken(afnd, tokenR, alphabet)
        fileList.remove(tokenR) #remove da lista de entrada


    auxList = fileList.copy() #agora na lista de entrada, temos apenas as gramáticas para serem lidas

    while fileList:
        for ruleGread in auxList:    
            if not ruleGread: #após ler todas as regras da gramática, une as regras da gramática com as dos tokens
                #gAfndgrammatic(afnd, grammatic, alphabet) 
                grammatic.clear() 
                fileList.remove(ruleGread)
            else:
                grammatic.append(ruleGread) 
                fileList.remove(ruleGread)
    print(grammatic)

def gAfndToken(afnd, token, alphabet):
    if not afnd:
        afnd.update({len(afnd): {}}) #gera o afnd com o index == (tamanho atual da afnd = 0, 1, 2, 3 -- Criando assim as regras), transição 0 é a inicial
    
    initialToken = True #primeiro caracter inicial, o que vai guiar para as próximas regras
    
    for tk in token: # percorre a string do token 
        if tk not in alphabet: # se o caracter ainda não estiver no alfabeto aceito
            alphabet.append(tk) # adiciona no alfabeto da linguagem
        
        if initialToken:   # Token inicial vai para o primeiro estado do automato
            listed = afnd[0] # 'ponteiro' para o estado inicial

            if tk in listed.keys():
                listed[tk].append(len(afnd)) #caso já exista uma regra com esse simbolo, adiciona uma transição para um novo estado para essa regra
            else:
                listed.update({tk : [len(afnd)]})
            tokenInicial = False
        else:
            afnd.update({len(afnd) : {tk: [len(afnd) + 1]}}) # cria um novo estado, que irá levar para o próximo a partir do simbolo
    
    afnd.update({len(afnd) : {'*': [1]}}) 
    print(afnd)