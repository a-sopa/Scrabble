"""
+---------------------------------------------------------+
| Projeto 1 - Fundamentos de Programação                  |
| Tema: Jogo Scrabble                                     |   
|                                                         |       
| Autor: Afonso Miguel Loureiro Sopa                      |   
| Número: ist1118098                                      |
| Email: afonso.sopa@tecnico.ulisboa.pt                   |
| Curso: LEIC-A 2025/2026                                 |
| Data de início: 27/09/2025                              |
| Data de término:                                        |
+---------------------------------------------------------+
"""
#---------------------------------------------
#3.1 Representação e Funções das letras

LETRAS = ['A','B','C','Ç','D','E','F','G','H','I','J','L','M','N','O',
'P','Q','R','S','T','U','V','X','Z']
DIMENSOES = 15

def ordena_letras(conj_letras): #Função auxiliar
    """
    Função auxliar que ordena, em ordem alfabética, uma lista de letras 

    Argumentos:
        conj_letras -> dicionário ou lista
    Return:
        lista_ordenada -> lista
    """
    if not type(conj_letras) == list:
        lista_letras = criar_lista_letras(conj_letras)
    else:
        lista_letras = conj_letras
    
    lista_ordenada = []
    for letra in LETRAS:
        lista_ordenada.extend([letra]*lista_letras.count(letra))
    return lista_ordenada


def cria_conjunto(let, occ): #3.1.1 
    """
    Recebe letras e as respetivas ocorrências e devolve um conjunto de letras definido por um dicionário
    
    Argumentos:
        let -> tuplo | occ -> tuplo
    Return:
        conj_letras -> dicionário
    Raises:
        ValueError -> 'cria_conjunto: argumentos inválidos' se:
            - let ou occ não forem tuplos;
            - let e occ não tiverem o mesmo comprimento;
            - let tiver letras repetidas;
            - occ tiver valores não inteiros ou menores ou iguais a 0
            - let tiver elementos não pertencentes ao abecedário português
            - let tiver elementos que não sejam strings de comprimento 1
    """
    #Validação dos argumentos
    if not type(let) == tuple or not type(occ) == tuple or len(let) != len(occ) or len(set(let)) != len(let):
        raise ValueError('cria_conjunto: argumentos inválidos')
    
    for i in range(len(occ)):
        if not type(occ[i]) == int or occ[i] <= 0 or let[i] not in LETRAS or not type(let[i]) == str or len(let[i]) != 1:
            raise ValueError('cria_conjunto: argumentos inválidos')
    
    conj_letras = {}
    for i in range(len(let)): #Inserir as letras(keys) com as respetivas ocorrências(values) no dicionário
        conj_letras[let[i]] = occ[i]
        
    return conj_letras


def gera_numero_aleatorio(estado): #3.1.2
    """
    Recebe um estado e devolve um número pseudoaleatório baseado no estado inicial.

    - inteiro -> inteiro
    Argumentos:
        estado -> inteiro
    Return:
        estado -> inteiro
    """
    
    #Gerador do tipo xorshift
    estado ^= (estado << 13) & 0xFFFFFFFF
    estado ^= (estado >> 17) & 0xFFFFFFFF
    estado ^= (estado << 5) & 0xFFFFFFFF

    return estado


def permuta_letras(letras, estado): #3.1.3 
    """
    Recebe uma lista de letras e o estado inicial do gerador pseudo-aleatório da função 
    << gera_numero_aleatorio >> e retorna uma lista ordenada de forma pseudoaleatória

    - lista x inteiro -> {}
    Argumentos:
        letras -> lista | estado -> inteiro
    Return:
        letras -> lista
    """
    tamanho = len(letras) 
    for i in range(tamanho - 1, 0, -1): # Fisher-Yates 
        estado = gera_numero_aleatorio(estado)
        n = estado % (i+1)
        letras[i], letras[n] = letras[n], letras[i]

    return


def criar_lista_letras(conj): #Função Auxiliar
    """
    Função para auxiliar a criação de uma lista com todas as letras disponíveis.
    Recebe um conjunto em forma de dicionário e transforma-o numa lista

    Argumento:
        conj -> dicionário 
    Return:
        lista_letras -> lista
    """
    tuplo_ocorrencias = list(conj.values())
    lista_keys = list(conj.keys())
    lista_letras = []
    ocorrencias = []

    for i in range(len(tuplo_ocorrencias)):
        ocorrencias.append(tuplo_ocorrencias[i])

    for i in range(len(lista_keys)):
        letra = lista_keys[i]
        for j in range(ocorrencias[i]):
            lista_letras.append(letra)
    
    return lista_letras    


def baralha_conjunto(conj, estado): #3.1.4
    """ 
    Recebe um conjunto e um estado e devolve uma lista baralhada pseudo aleatoriamente com todas as letras
    contidas no conjunto de letras

    - conjunto letras x inteiro -> lista
    Argumentos:
        conj -> dicionário | estado -> inteiro
    Return:
        lista_ordenada -> lista
    """

    lista = criar_lista_letras(conj) #Criar uma lista do conjunto
    lista_ordenada = ordena_letras(lista) #Ordenar a lista 
    permuta_letras(lista_ordenada,estado) #Baralhar a lista

    return lista_ordenada


def testa_palavra_padrao(palavra, padrao, conj): #3.1.5 
    """ Esta função tem como objetivo testar se a palavra que o utilizador quer inserir no tabuleiro é válida no que toca:
        1) Às letras:
            -> Se a palavra apenas contém letras que estão no conjunto de letras;
            -> Se a palavra contém letras que estejam no padrão
        2) Ao padrão:
            -> Se a palavra contém o mesmo comprimento que o padrão;
        
        - string x string x conj letras -> Bool
        Argumentos:
            palavra -> string | padrao -> string | conj -> dicionário 
        Return:
            True -> bool (se for válida) | False -> bool (se for inválida) 
        
    """
    lista_letras = criar_lista_letras(conj)
    lista_interna = lista_letras.copy() #Criar uma lista interna, para não modificar os argumentos da lista original 

    if len(palavra) != len(padrao):
        return False
    
    for pad, let in zip(padrao,palavra):
        if pad == '.':
            if let not in lista_interna:
                return False
            lista_interna.remove(let)
        elif pad != let:
            return False
            
    return True

#------------------------------------------------------------------------
#3.2 Representações e funções do tabuleiro


def cria_tabuleiro(): #3.2.1
    """
    Cria uma lista de listas com n elementos e n listas que irá representar o tabuleiro de jogo

    Argumentos: Função sem parâmetros
    Return:
        tab -> Tabuleiro
    #
    """
    tab = []
    for i in range(DIMENSOES):
        linha = ['.'] * DIMENSOES
        tab.append(linha)

    return tab


def cria_casa(l,c): #3.2.2
    """
    Recebe dois valores inteiros (linha, coluna) referentes a um par de coordenadas e devolve
    um tuplo que contém as mesmas

    - inteiro x inteiro -> Casa    
    Argumentos:
        l -> (linha) inteiro | c -> (coluna) inteiro
    Return:
        casa -> tuplo
    Raises:
        ValueError: 'cria_casa: argumentos inválidos' se:
            - l e c não forem inteiros
            - l e c forem menores que 1 ou maiores que 15
    """
    #Validação de erros
    if not type(l) == int or not type(c) == int or l < 1 or l > 15 or c < 1 or c > 15:
        raise ValueError('cria_casa: argumentos inválidos')
    casa = (l,c)
    return casa


def obtem_valor(tab, casa): #3.2.3 
    """
    Recebe um tabuleiro e uma casa e devolve uma string com o valor contido nessa casa

    tabuleiro x casa -> string
    Argumentos:
        tab -> tabuleiro | casa -> tuplo
    Return:
        valor -> string
    """
    l, c = casa[0] - 1, casa[1] - 1 
    valor = tab[l][c]
    return valor


def insere_letra(tab, casa, letra): #3.2.4
    """ 
    Recebe um tabuleiro, uma casa pertencente ao mesmo e uma letra, e insere a letra na casa indicada.
    Esta função modifica destrutivamente o tabuleiro

    - tabuleiro x casa x string -> tabuleiro c/ letra
    Argumentos:
        tab -> tabuleiro | casa -> tuplo | letra -> string
    Return:
        tab -> tabuleiro (modificado)
    """
    l, c = casa[0] - 1, casa[1] - 1 
    tab[l][c] = letra
    return tab


def obtem_sequencia(tab, casa, direcao, tamanho): #3.2.5 
    """
    Obtém uma sequência de caracteres a partir de uma casa numa direção e retorna a mesma string.

    Argumentos:
        tab -> tabuleiro | casa -> tuplo | direcao -> 'H' ou 'V' | tamanho -> inteiro
    Return:
        string -> sequência de letras ou pontos
    Raises:
        ValueError: 'obtem_sequencia: direção inválida' se:
            - A direção é diferente de 'H' ou 'V'
    """
    l, c = casa[0] - 1, casa[1] - 1
    sequencia = []

    if direcao == 'H': 
        for i in range(tamanho):
            sequencia.append(tab[l][c+i])
    elif direcao == 'V':
        for i in range(tamanho):
            sequencia.append(tab[l+i][c])
    else: 
        raise ValueError('obtem_sequencia: direção inválida')
    
    return ''.join(sequencia)


def insere_palavra(tab,casa,direcao,palavra): #3.2.6
    """
    Recebe um tabuleiro, uma casa pertencente ao mesmo e uma palavra, e insere a palavra na casa indicada, através da função insere_letra (3.2.4).
    Esta função modifica destrutivamente o tabuleiro.

    Argumentos:
        tab -> tabuleiro | casa -> tuplo | direcao -> string ('H' ou 'V') | palavra -> string
    Return:
        tabuleiro -> tabuleiro (com a palavra)
    """
    linha = casa[0]
    coluna = casa[1]
    
    if direcao == 'H':
        for i in palavra:
            tab = insere_letra(tab, (linha,coluna), i)
            coluna +=1
        
    elif direcao == 'V':
        for i in palavra:
            tab = insere_letra(tab, (linha,coluna), i)
            linha += 1
    return tab

#3.2.7 Funções Auxiliares para tabuleiro_para_str numero_linhas = 15

def borda_superior_inferior(DIMENSOES):
    """
    Constrói a borda inferior/superior do tabuleiro '+--...--+'
    O comprimento da borda depende das dimensões do tabuleiro

    Argumentos:
        DIMENSOES -> inteiro (tamanho do tab)
    Return:
        borda -> string
    """
    espaco = '   '
    borda = espaco + '+' + '-'*(2*DIMENSOES + 1)+ '+' # O número de '-' é igual ao dobro do comprimento do tabuleiro, menos o caracter final
    return borda


def cabecalho(DIMENSOES):
    """
    Constrói as duas linhas de cabeçalho:
        - Primeira linha: dígito dezenas (ou espaços)
        - Segunda linha: dígito unidades
    
    Argumentos:
        DIMENSOES -> inteiro 
    Return:
        linha_dezenas -> string | linha_unidades -> string
    """
    #Criar conjunto das unidades
    unidades = []
    for i in range(1, DIMENSOES+1):
        if i < 10:
            unidades.append(str(i))
        else:
            dig = i % 10
            unidades.append(str(dig))
    
    #Criar o conjunto das dezenas
    dezenas = [] 
    for i in range(1, DIMENSOES+1):
        digito = i//10
        if i < 10:
            dezenas.append(' ')
        else:
            digito = str(digito)
            dezenas.append(digito)
    
    espaco = '     '
    linha_dezenas = espaco + ' '.join(dezenas)
    linha_unidades = espaco + ' '.join(unidades)

    return linha_dezenas, linha_unidades


def linha_para_str(numero_linha, conteudo_linha):
    """
    Formata uma linha do tabuleiro:
    - numero_linha: (1..n)
    - conteudo_linha: ['.', '.', 'A', ...]
    Resultado: string formatada, ex:
    " 1 | . . . A . . . |"

    Argumentos:
        numero_linha -> inteiro | conteudo_linha -> lista
    Return:
        linha_str -> string
    """

    linha_conteudos = ' '.join(conteudo_linha)

    #Formatar o número da linha com largura 2 (à direita)
    indice_linha = f'{numero_linha:2}' 

    linha_str = f'{indice_linha} | {linha_conteudos} |'
    return linha_str
    

def tabuleiro_para_str(tab): #3.2.7
    """
    Recebe a lista de listas da função cria_tabuleiro e representa o tabuleiro como uma string
    contínua, com os números de linha e coluna e com as bordas
    
    Argumentos:
        tab -> lista (tabuleiro)
    Return:
        tabuleiro -> string (tabuleiro formatado)
    """
    DIMENSOES = len(tab)
    linhas = []

    #Adicionar os cabecalhos
    cabecalho_dezenas, cabecalho_unidades = cabecalho(DIMENSOES)
    linhas.append(cabecalho_dezenas)
    linhas.append(cabecalho_unidades)

    #Adicionar a borda superior
    borda_sup = borda_superior_inferior(DIMENSOES)
    linhas.append(borda_sup)

    #Adicionar a linhas do tabuleiro
    for i in range(0, DIMENSOES):
        linhas.append((linha_para_str(i + 1, tab[i]))) 

    #Adicionar a borda inferior
    borda_inf = borda_superior_inferior(DIMENSOES)
    linhas.append(borda_inf)

    #Criar o tabuleiro final
    tabuleiro = '\n'.join(linhas)

    return tabuleiro


#-----------------------------------------------------------
#3.3- Representação e Funções de Jogador


def cria_jogador(ordem, pontos, conj_letras): #3.3.1
    """
    Através do número, pontuação e conjunto de letras a função cria um dicionário com as informações do jogador. 

    Argumentos:
        ordem -> inteiro | pontos -> inteiro | conj_letras -> conjunto de letras
    Return:
        jogador -> dicionário com chaves: 'id', 'pontos' e 'letras'
    Raises:
        ValueError -> 'cria_jogador: argumentos inválidos' se:
            - ordem não for um inteiro entre 1 e 4
            - pontos não for um inteiro maior ou igual a 0
            - conj_letras não for um dicionário
            - conj_letras contiver letras inválidas ou não pertencentes ao abecedário português
            - conj_letras contiver ocorrências não inteiras ou menores ou iguais a 0
            - o total de letras exceder 7
    """
    
    if ordem > 4 or ordem < 1 or not type(ordem) == int or not type(pontos) == int or pontos < 0 or not type(conj_letras) == dict:
        raise ValueError('cria_jogador: argumentos inválidos')
    
    for l in conj_letras.keys():
        if not type(l) == str or l not in LETRAS:
            raise ValueError('cria_jogador: argumentos inválidos')

    for o in conj_letras.values():
        if not type(o) == int or o <= 0:
            raise ValueError('cria_jogador: argumentos inválidos')

    lista_letras = criar_lista_letras(conj_letras)
    if len(lista_letras) > 7:
        raise ValueError('cria_jogador: argumentos inválidos')


    jogador = {'id': ordem, 'pontos': pontos, 'letras':conj_letras}
    return jogador


def jogador_para_str(jog): #3.3.2
    """
    Converte o dicionário jogador numa string para ser apresentada ao utilizador durante o jogo.

    Argumentos:
        jog -> jogador (dicionário)
    Return:
        string -> representação visual do jogador
    """
    #Armazenar os dados do jogador em variáveis
    id_jogador = jog['id']
    pontos = jog['pontos']
    letras = jog['letras']

    #Transformar o dicionário em lista
    letras_ordenadas = ordena_letras(letras) #Função auxiliar

    #Criar uma string com as letras todas
    str_letras = ''
    for i in letras_ordenadas:
        str_letras = str_letras + ' ' + str(i)

    #Criar a string player
    player = f'#{id_jogador} ({pontos:3d}):{str_letras}'

    return player


def distribui_letra(letras, jogador): #3.3.3
    """
    Retira a última letra de uma lista e adiciona ao baralho do jogador.

    Argumentos:
        letras -> lista | jogador -> dicionário
    Return:
        True -> bool (se foi distribuída uma letra) | False -> bool (se a lista estiver vazia)
    """
    #Verificar se a lista é vazia
    if len(letras) == 0:
        return False
    
    #Retirar o úlitmo elemento da lista
    letra = letras.pop()
    
    #Adicionar a letra ao dicionário
    if letra in jogador['letras']:
        jogador['letras'][letra] += 1
    else:
        jogador['letras'][letra] = 1

    return True


#------------------------------------------------------------
#3.4- Funções de Jogo

    
def joga_palavra(tab, palavra, casa, direcao, conj_letras, primeira): #3.4.1
    """
    Primeira função de jogo que assegura as regras e coloca a palavra no tabuleiro

    Argumentos: 
        tab -> tabuleiro |  palavra -> string | casa -> tuplo | direcao -> string |
        conj_letras -> conjunto de letras (tuplo) | primeira -> Bool
    Return:
        () -> tuplo (vazio) se a jogada for inválida | letras_usadas -> lista
    """
    #Atribuir valores às variáveis
    l, c = casa[0], casa[1]
    tamanho_palavra = len(palavra) 

    #Verificar se as palavras excedem os limites do tabuleiro
    if direcao == 'H':
        if c + tamanho_palavra - 1 > len(tab[0]):
            return ()
    elif direcao == 'V':
        if l + tamanho_palavra - 1 > len(tab):
            return ()
    else:
        return ()
    
    #Verificar se a primeira palavra jogada interseta o centro do tabuleiro
    if primeira:
        if tamanho_palavra < 2: #Testar se o comprimento da primeira palavra é maior do que 1
            return()
        centro = (len(tab[0]) + 1) // 2 
        coordenadas_centro = (centro, centro) #Definir o par de coordenadas do centro
        passou_pelo_centro = False 
        #Coordenadas iniciais
        linha = l 
        coluna = c
        for i in range(tamanho_palavra):
            if (linha, coluna) == coordenadas_centro: #Se alguma letra da palavra passar pela coordenada centro
                passou_pelo_centro = True #
                break
            if direcao == 'H':
                coluna += 1
            elif direcao == 'V':
                linha += 1
            
        if not passou_pelo_centro: #Caso não tenha passado no centro do tabuleiro
            return ()
    
    #Verificar se a palavra pode ser formada com as letras do conjunto
    
    conj_temp = conj_letras.copy() #Criar um conjunto temporário para não alterar destrutivamente a lista original
    letras_usadas = [] #Criar uma lista para armazenar as letras já utilizadas

    padrao = ''.join(obtem_sequencia(tab, casa, direcao, tamanho_palavra))
    if not primeira:
        contador = 0
        for i in padrao:
            if i in LETRAS:
                break
            contador += 1
        if contador == len(padrao):
            return ()

    if not testa_palavra_padrao(palavra, padrao, conj_letras):
        return ()

    if padrao == palavra:
        return ()
    
    for p, l in zip(padrao, palavra):       
        if p == '.' and l in conj_temp and conj_temp[l] > 0:
            letras_usadas.append(l)
            conj_temp[l] -= 1

    tab = insere_palavra(tab, casa, direcao, palavra)
    letras_usadas = ordena_letras(letras_usadas)
    letras_usadas = tuple(letras_usadas)

    return letras_usadas


def processa_jogada(tab, jog, pilha, pontos, primeira): #3.4.2
    """
    Processar o turno completo do jogador. 

    - 'P' -> Passar a vez
    - 'T ...' -> Trocar as letras do baralho
    - 'J (casa) direcao palavra' -> Jogar a palavra no tabuleiro

    Argumentos:
        tab -> tabuleiro  | jog -> jogador (dicionário) | pilha -> Lista de letras |
        pontos -> inteiro | primeira -> Bool
    Return:
        False -> bool (se a jogada for Passar) | True -> bool (se a jogada for Jogar ou Trocar)
    """
    while True:
        letras_troca = []
        #Pedir uma jogada ao utilizador
        entrada = input(f'Jogada J{jog["id"]}: ')
        #Separar os vários passos da jogada numa lista
        jogada = entrada.split(' ') 

        #Verificar a validade da jogada
        if len(jogada) < 1:
            return processa_jogada(tab, jog, pilha, pontos, primeira)
        
        #Opção Passar a vez
        if entrada.strip() == 'P':
            return False
            
        #Opção Trocar Letras
        elif jogada[0] == 'T':
            #Verificação
            letras_para_troca = jogada[1:]
        
            if len(letras_para_troca) == 0 or len(letras_para_troca) > 7:
                continue
        
            validacao = True
            for letra in letras_para_troca:
                if letra not in jog['letras'] or jog['letras'].get(letra, 0) == 0:
                        validacao = False
                        break

            if not validacao:
                continue

            #Retirar as letras do baralho do jogador
            for l in letras_para_troca:
                jog['letras'][l] -= 1
                letras_troca.append(l)
                if jog['letras'][l] == 0:
                    del jog['letras'][l]
                      
            #Adicionar as letras à pilha
            for i in range(len(letras_troca)): 
                distribui_letra(pilha, jog)
            
            primeira = False                   
            return True
        
        #Opção Jogar
        elif jogada[0] == 'J':
            if len(jogada) != 5:
                continue

            linha_str = jogada[1]
            coluna_str = jogada[2]

            if not linha_str.isdigit() or not coluna_str.isdigit(): #Verificar se a linha e a coluna são dígitos
                continue

            #Converter ambos para inteiro
            linha = int(linha_str)
            coluna = int(coluna_str)

            if DIMENSOES < linha or linha < 0 or DIMENSOES < coluna or coluna < 0 or not type(coluna) == int or not type(linha) == int: #Verificar se estão dentro do limite do tabuleiro
                continue

            casa = (linha, coluna) #Criar o tuplo casa

            direcao = jogada[3]
            if direcao not in ('H', 'V'):
                continue

            palavra = jogada[4]
            tamanho_palavra = len(palavra)

            if direcao == 'H' and tamanho_palavra + coluna > 15:
                continue
            elif direcao == 'V' and tamanho_palavra + linha > 15:
                continue

            padrao = ''.join(obtem_sequencia(tab, casa, direcao, tamanho_palavra)) #Obter o padrão
            
            if not testa_palavra_padrao(palavra, padrao, jog['letras']):
                continue

            letras_usadas = joga_palavra(tab, palavra, casa, direcao, jog['letras'], primeira)
            if letras_usadas == ():
                continue

            for letra in palavra:
                jog['pontos'] += pontos[letra]
            
            for let in letras_usadas:
                if let in jog['letras']:
                    jog['letras'][let] -= 1
                    if jog['letras'][let] == 0:
                        del jog['letras'][let]

            for i in range(len(letras_usadas)):
                distribui_letra(pilha, jog)

            primeira = False
            return True
        
        else:
            continue


def scrabble(jogadores, saco, pontos, seed): #3.4.3
    """
    Função principal que permite o funcionamento do jogo completo

    Argumentos:
        jogadores -> inteiro [2,4] | saco -> dicionário | pontos -> dicionário | seed -> inteiro (estado inicial)
    Return:
        tuplo_final -> tuplo (Pontuação final dos jogadores)
    Raises:
        ValueError -> 'scrabble: argumentos inválidos' se:
            - jogadores não for um inteiro entre 2 e 4;
            - saco não for um dicionário ou estiver vazio;
            - pontos não for um dicionário e se os seus valores não forem inteiros
            - seed não for um inteiro positivo;
            - as letras nos dicionários (saco e pontos) não estiverem no abecedário português (LETRAS)
        
    """
    #Verificação dos parâmetros
    if not type(jogadores) == int or jogadores < 2 or jogadores > 4:
        raise ValueError('scrabble: argumentos inválidos')
    if not type(saco) == dict or len(saco) == 0:
        raise ValueError('scrabble: argumentos inválidos')
    if not type(pontos) == dict or len(pontos) != len(LETRAS):
        raise ValueError('scrabble: argumentos inválidos')
    if not type(seed) == int or seed <= 0:
        raise ValueError('scrabble: argumentos inválidos')
    for letra in saco:
        if letra not in LETRAS:
            raise ValueError('scrabble: argumentos inválidos')
    for letra in pontos:
        if letra not in LETRAS:
            raise ValueError('scrabble: argumentos inválidos')
    for p in pontos.values():
        if not type(p) == int or p <= 0:
            raise ValueError('scrabble: argumentos inválidos')
    for s in saco.values():
        if not type(s) == int or s < 0:
            raise ValueError('scrabble: argumentos inválidos')
    
    #Preparação do Jogo
    tab = cria_tabuleiro()
    pilha = baralha_conjunto(saco, seed)
    lista_jogadores = []

    for i in range(1, jogadores + 1): #Criar Jogadores
        letras_iniciais = {}
        for j in range(7):
            distribui_letra(pilha, {'letras': letras_iniciais})
        lista_jogadores.append(cria_jogador(i, 0, letras_iniciais))

    #Mensagem para o utilizador
    print('Bem-vindo ao SCRABBLE.')
    
    #Jogo
    primeira = True #Indicar a primeira jogada
    passes = 0 #Armazenar o número de passes consecutivos (condição para terminar o jogo)

    while True:
        for jogador in lista_jogadores:
            #Apresentar o tabuleiro
            print(tabuleiro_para_str(tab))
            #Mostrar o id, pontos e baralho dos jogadores
            for j in lista_jogadores:
                print(jogador_para_str(j))

            resultado = processa_jogada(tab, jogador, pilha, pontos, primeira)
            
            #Verificar se os jogadores passaram
            if not resultado:
                passes += 1
            else:
                passes = 0
            
            #Verificar se é a primeira jogada
            meio = DIMENSOES // 2 + 1
            tuplo_centro = (meio,meio)
            centro = obtem_valor(tab, tuplo_centro)
            if centro != '.': 
                primeira = False

            #Final do Jogo
            tuplo_final = ()
            if passes == jogadores: #Se todos os jogadores passarem a sua vez termina
                for jog in lista_jogadores:
                    tuplo_final = tuplo_final + (jog['pontos'],)
                return tuplo_final

            baralho_jogador = criar_lista_letras(jogador['letras'])
            if len(pilha) == 0 and len(baralho_jogador) == 0:
                for jog in lista_jogadores:
                    tuplo_final = tuplo_final + (jog['pontos'],)
                return tuplo_final 
        
    
