"""
+---------------------------------------------------------+
| Projeto 2 - Fundamentos de Programação                  |
| Tema: Extensão do Jogo Scrabble                         |   
|                                                         |       
| Autor: Afonso Miguel Loureiro Sopa                      |   
| Número: ist1118098                                      |
| Email: afonso.sopa@tecnico.ulisboa.pt                   |
| Curso: LEIC-A 2025/2026                                 |
| Data de início: 12/10/2025                              |
| Data de término: 25/10/2025                             |
+---------------------------------------------------------+
"""
#---------------------------------------------
#Constantes

LETRAS = ['A','B','C','Ç','D','E','F','G','H','I','J','L','M','N','O','P','Q','R','S','T','U','V','X','Z'] #Abecedario português 
DIMENSOES = 15 #Dimensão do tabuleiro

#------------------------------------------------------------------------
#TAD Casa
def cria_casa(lin,col):
    """
    Recebe dois valores inteiros (linha, coluna) referentes a um par de coordenadas e devolve
    um tuplo que contém as mesmas
    
    Args:
        l -> (linha) inteiro | c -> (coluna) inteiro
    Return:
        casa -> tuplo
    Raises:
        ValueError: 'cria_casa: argumentos inválidos' se:
            - l e c não forem inteiros
            - l e c forem menores que 1 ou maiores que 15
    """
    if type(lin) != int or lin > 15 or lin <= 0:
        raise ValueError('cria_casa: argumentos inválidos') 
    if type(col) != int or col > 15 or col <= 0:
        raise ValueError('cria_casa: argumentos inválidos') 
    
    casa = (lin, col)
    return casa


def obtem_col(casa):
    """
    Recebe uma casa e devolve a coluna da casa.

    Args: 
        casa -> tuplo 
    Return:
        coluna -> inteiro
    """
    coluna = casa[1]
    return coluna


def obtem_lin(casa):
    """
    Recebe uma casa e devolve a linha da casa.

    Args: 
        casa -> tuplo 
    Return:
        linha -> inteiro
    """
    linha = casa[0]
    return linha


def eh_casa(arg):
    """
    Verifica se o argumento representa uma casa válida.

    Args:
        arg (any): Valor a verificar.

    Returns:
        bool: True se for uma casa válida, False caso contrário.
    """
    if not isinstance(arg, (tuple, set, list, str)) or len(arg) != 2:
        return False 
    
    l, c = arg 
    if type(l) == str or type(c) == str and (l.isdigit() and c.isdigit()):
        l = int(l)
        c = int(c)        

    if type(l) != int or type(c) != int:
        return False  
    
    return l > 0 and l <= 15 and c > 0 and c <= 15


def casas_iguais(c1,c2):
    """
    Verifica se duas casas são iguais.
    
    Args:
        c1 -> tuplo |c2 -> tuplo
    Return:
        bool -> True se as casas forem iguais, False caso contrário
    """
    #Verificar o formato da casa
    if isinstance(c1, str):
        c1 = str_para_casa(c1)
    if isinstance(c2, str):
        c2 = str_para_casa(c2)          

    #Comparar as casas
    if obtem_lin(c1) == obtem_lin(c2) and obtem_col(c1) == obtem_col(c2):
        return True
    return False


def casa_para_str(c):
    """
    Converte uma casa para a sua representação em string.
    
    Args:
        c -> tuplo (casa)
    Return:
        string (casa)
    """
    if eh_casa(c):
        linha = c[0]
        coluna = c[1]
        return f'({linha},{coluna})'


def str_para_casa(s):
    """
    Converte uma string no formato '(linha,coluna)' para uma casa.
    
    Args:
        s -> string(casa)
    Return:
        tuplo (casa)
    """
    return eval(s)


def incrementa_casa(c, d, s):
    """
    Calcula a casa resultante ao mover uma casa numa direção.

    Args:
        c -> tuplo (casa inicial) | d -> string ('H' ou 'V').
        s -> inteiro (número de casas a avançar)

    Returns:
        tuplo (casa final)
    """
    if not eh_casa(c) or d not in ('H', 'V') or type(s) != int:
        return c
    
    linha = obtem_lin(c)
    coluna = obtem_col(c)

    if d == 'H':
        coluna_final = coluna + s
        if coluna_final > 15:
            return c
        casa_final = (linha, coluna_final)
        if eh_casa(casa_final):
            return casa_final
    
    elif d == 'V':
        linha_final = linha + s
        if linha_final > 15:
            return c
        casa_final = (linha + s, coluna)
        if eh_casa(casa_final):
            return casa_final
        
    return c


#---------------------------------------------------------------
#TAD Jogador
def ordena_letras(conj_letras): #Função auxiliar
    """
    Função auxiliar que ordena, em ordem alfabética, uma lista de letras 

    Argumentos:
        conj_letras -> dicionário ou lista
    Return:
        lista_ordenada -> lista
    """
    #Verificar se o tipo do conjunto de entrada, para converter para uma lista caso necessário
    if type(conj_letras) != list:
        lista_letras = criar_lista_letras(conj_letras)            
    else:
        lista_letras = conj_letras
    
    lista_ordenada = []
    #Adicionar as letras de forma ordenada à lista
    for letra in LETRAS:
        lista_ordenada.extend([letra]*lista_letras.count(letra))

    return lista_ordenada #Retornar a lista ordenada


def chave(palavra):
    """
    Função auxiliar que tem como objetivo substituir o Ç por um C de modo a facilitar a ordenação de palavras

    Args: 
        palavra -> string
    Return:
        string (Ç substituido temporariamente por Cz)
    """
    #Tratar o Ç como se fosse um Cz para aparecer depois do C mas antes do D
    return palavra.replace('Ç', 'Cz')


def criar_lista_letras(conj): #Função Auxiliar
    """
    Função para auxiliar a criação de uma lista com todas as letras disponíveis.
    Recebe um conjunto em forma de dicionário e transforma-o numa lista

    Argumento:
        conj -> dicionário 
    Return:
        lista_letras -> lista
    """
    if isinstance(conj, (str, tuple)):
        lista_letras = []
        for let in conj:
            lista_letras.append(let)
        return lista_letras

    tuplo_ocorrencias = list(conj.values()) #Armazenar o valor das ocorrencias
    lista_keys = list(conj.keys()) #Armazenar as letras do conjunto
    lista_letras = []
    ocorrencias = []

    #Criar uma lista com as ocorrencias
    for i in range(len(tuplo_ocorrencias)):
        ocorrencias.append(tuplo_ocorrencias[i])

    #Adicionar as letras de acordo com o número de ocorrências
    for i in range(len(lista_keys)):
        letra = lista_keys[i]
        for j in range(ocorrencias[i]):
            lista_letras.append(letra)
    
    return lista_letras    


#Construtores
def cria_humano(nome):
    """
    Cria um jogador humano com nome e baralho vazio.
    
    Args:
        nome -> string
    Return:
        dicionário -> jogador humano
    """
    if type(nome) != str:
        raise ValueError('cria_humano: argumento inválido')
    nome = nome.strip()
    if nome == '':
        raise ValueError('cria_humano: argumento inválido')
    
    return {'nome': nome, 'pontos': 0, 'letras': {}}


def cria_agente(nivel):
    """
    Cria um agente com nível de dificuldade.
    
    Args:
        nivel -> string ('FACIL', 'MEDIO' ou 'DIFICIL')
    Return:
        dicionário -> jogador agente
    """
    if nivel not in ('FACIL', 'MEDIO', 'DIFICIL'):
        raise ValueError('cria_agente: argumento inválido')
    
    return {'nome': f'{nivel.upper()}', 'pontos': 0, 'letras': {}}


#Seletores
def jogador_identidade(j):
    """
    Recebe um jogador e indica o seu nome.
    
    Args:
        j -> dicionário
    Return:
        string -> nome do jogador
    """
    if eh_jogador(j):
        return j['nome']


def jogador_pontos(j):
    """
    Devolve os pontos atuais do jogador.
    
    Args:
        j -> dicionário
    Return:
        inteiro -> pontos do jogador
    """
    return j['pontos']


def jogador_letras(j):
    """
    Devolve as letras atuais do jogador.
    
    Args:
        j -> dicionário
    Return:
        letras do jogador -> string
    """
    letras_jog = criar_lista_letras(j['letras'])
    letras_jog = ordena_letras(letras_jog)
    letras_str = ''
    for l in letras_jog:
        letras_str += l

    return letras_str.strip()


#Modificadores
def recebe_letra(j, l):
    """
    Adiciona uma ocorrência da letra l ao baralho do jogador j.

    Args:
        j -> jogador (TAD; tipicamente dicionário com chave 'letras') | l -> string 
    Return:
        j -> jogador atualizado
    """
    if l in j['letras']:
        j['letras'][l] += 1
    else:
        j['letras'][l] = 1
    return j


def usa_letra(j,l):
    """
    Remove uma ocorrência da letra l do baralho do jogador j.

    Args:
        j -> jogador (TAD; tipicamente dicionário com chave 'letras') | l -> string 
    Return:
        j -> jogador atualizado
    """
    letras = criar_lista_letras(jogador_letras(j))
    if l not in letras:
        return j
    
    ocorrencias = letras.count(l)

    if ocorrencias == 1:
        j['letras'].pop(l)
    else:
        j['letras'][l] = ocorrencias - 1
    return j


def soma_pontos(j, p):
    """
    Acrescenta p pontos ao total do jogador j.

    Args:
        j -> jogador (TAD; tipicamente dicionário com chave 'pontos')
        p -> inteiro 
    Return:
        j -> jogador atualizado
    """
    j['pontos'] += p
    return j


#Reconhecedores
def eh_jogador(arg):
    """
    Reconhecedor de tipo abstrato: indica se arg representa um jogador válido.

    Args:
        arg -> qualquer argumento
    Return:
        bool -> True se arg respeita o TAD jogador
    """
    return type(arg) == dict and 'nome' in arg and 'pontos' in arg and 'letras' in arg and type(arg['nome']) == str and type(arg['pontos']) == int and type(arg['letras']) == dict
 

def eh_humano(arg):
    """
    Indica se o argumento é um jogador humano.

    Args:
        arg -> argumento
    Return:
        bool -> True se arg for um jogador e o seu nome não corresponder a um nível de agente
    """
    return eh_jogador(arg) and jogador_identidade(arg) not in ('FACIL', 'MEDIO', 'DIFICIL')


def eh_agente(arg):
    """
    Indica se o argumento é um agente (bot).

    Args:
        arg -> jogador
    Return:
        bool -> True se arg for um jogador e o seu nome corresponder a um dos níveis de dificuldade
    """
    return eh_jogador(arg) and jogador_identidade(arg) in ('FACIL', 'MEDIO', 'DIFICIL') 


#Teste
def jogadores_iguais(j1, j2):
    """
    Verifica se dois jogadores (TAD) são iguais.

    Args:
        j1, j2 -> jogadores
    Return:
        bool -> True se ambos forem jogadores válidos e tiverem nome, pontos e baralho iguais
    """
    return (eh_jogador(j1) and eh_jogador(j2) and jogador_identidade(j1) == jogador_identidade(j2) 
            and jogador_pontos(j1) == jogador_pontos(j2) and jogador_letras(j1) == jogador_letras(j2))


#Transformador
def jogador_para_str(j):
    """
    Transforma o jogador (dicionário) numa representação (em string), para apresentar ao utilizador 

    Args:
        j -> jogador
    Return:
        string -> formato:
            - agente: 'BOT("NIVEL") ("pontos"): "letras"'
            - humano: '"nome" ("pontos"): "letras"'
    """
    letras_str = ''
    for i in jogador_letras(j):
        letras_str += ' ' + i

    if eh_agente(j):
        return f'BOT({jogador_identidade(j)}) ({jogador_pontos(j):3d}):{letras_str}'
    elif eh_humano(j):
        return f'{jogador_identidade(j)} ({jogador_pontos(j):3d}):{letras_str}'


def distribui_letras(jogador, saco, num): #3.3.3
    """
    Retira a última letra de uma lista e adiciona ao baralho do jogador.

    Argumentos:
        letras -> lista | jogador -> dicionário
    Return:
        True -> bool (se foi distribuída uma letra)
        False -> bool (se a lista estiver vazia)
    """
    #Verificar se a lista é vazia
    if len(saco) == 0:
        return jogador
    

    #Retirar o último elemento da lista
    for l in range(num):
        if len(saco) == 0:
            break
        letra = saco.pop()
        jogador = recebe_letra(jogador, letra) #Adicionar a letra ao jogador

    return jogador

#---------------------------------------------------------------
#TAD Vocabulário
PONTOS = {
    'A': 1, 'B': 3, 'C': 2, 'Ç': 3, 'D': 2, 'E': 1,
    'F': 4, 'G': 4, 'H': 4, 'I': 1, 'J': 5, 'L': 2,
    'M': 1, 'N': 3, 'O': 1, 'P': 2, 'Q': 6, 'R': 1,
    'S': 1, 'T': 1, 'U': 1, 'V': 4, 'X': 8, 'Z': 8 }

#Construtor
def cria_vocabulario(v):
    """
    Cria o TAD vocabulario responsável por armazenar todas as palavras que irão ser aceites pelo jogo

    Args:
        v -> tuplo
    Return:
        vocab -> dicionário
    """
    if not isinstance(v, (set, list, tuple)):
        raise ValueError('cria_vocabulario: argumento inválido')
    if len(v) < 2:
        raise ValueError('cria_vocabulario: argumento inválido')
    
    vocab = {}
    for palavra in v:
        if type(palavra) != str:
            raise ValueError('cria_vocabulario: argumento inválido')
        palavra = palavra.strip()
        if 2 > len(palavra) or len(palavra)> 15:
            continue
        for letra in palavra:
            if letra not in LETRAS:
                raise ValueError('cria_vocabulario: argumento inválido')

        #palavra = palavra.upper()    
        
        comp = len(palavra)
        inicial = palavra[0]
        pontuacao = 0
        for letra in palavra:
            pontuacao += PONTOS[letra] 

        #O vocabulário vai ser do tipo «comprimento de palavra» : {«letra inicial» : [(palavras, pontuacao), ...]
        if comp not in vocab:
            vocab[comp] = {}
        if inicial not in vocab[comp]:
            vocab[comp][inicial] = []
        
        vocab[comp][inicial].append((palavra, pontuacao))

    #Ordenar as palavras por 1) Comprimento -> 2) Pontuação -> 3) Ordem lexicográfica
    for comp in vocab:
        for inicial in vocab[comp]:
            vocab[comp][inicial].sort(key=lambda x: (-x[1], chave(x[0])))

    return vocab


def obtem_pontos(vocabulario, palavra):
    """
    Obtém a pontuação de uma palavra segundo o vocabulário.

    Args:
        vocabulario -> dicionário do TAD vocabulário | palavra -> string
    Return:
        pts -> inteiro (pontos)
    """
    if type(palavra) != str:
        return 0 
    
    palavra = palavra.strip().upper()
    comp = len(palavra)
    inicial = palavra[0]
    #Procurar a palavra no dicionário
    if comp in vocabulario and inicial in vocabulario[comp]:
        for pal, pts in vocabulario[comp][inicial]: #Obter a palavra e a pontuação correspondente
            if pal == palavra:
                return pts        
    return 0


def obtem_palavras(vocabulario, comp, letra):
    if comp not in vocabulario or letra not in vocabulario[comp]:
        return ()
    palavras = vocabulario[comp][letra]

    #Criar um dicionário para auxiliar a ordenação por pontos
    pontos_dict = {}
    for palavra, pontos in palavras:
        if pontos not in pontos_dict:
            pontos_dict[pontos] = []
        pontos_dict[pontos].append(palavra)
    
    #Ordenar a pontuação das palavras por ordem decrescente
    pontos_ordenados = sorted(pontos_dict, reverse = True)
    #Ordenar a lista de palavras em cada grupo de pontos
    res = ()
    for pontuacao in pontos_ordenados:
        #Ordenar tendo em conta o Ç
        dict_ordenado = sorted(pontos_dict[pontuacao], key=chave) 
        for palavra in dict_ordenado:
            res = res + ((palavra, pontuacao),)

    return res


def testa_palavra_padrao(vocabulario, palavra, padrao, letras):
    #Verificar se a palavra e o padrao têm o mesmo tamanho
    if len(palavra) != len(padrao): 
        return False
    
    comp = len(palavra)
    inicial = palavra[0]
    #Verificar se o comprimento e a inicial existem no vocabulário
    if comp not in vocabulario or inicial not in vocabulario[comp]:
        return False

    """if not any(palavra == item[0] for item in vocabulario[comp][inicial]):
        return False"""

    """existe_no_vocab = False
    for i in range(len(vocabulario[comp][inicial])):
        if palavra in vocabulario[comp][inicial][i][0]:
            existe_no_vocab = True
            break
    
    if not existe_no_vocab:
        return False"""

    #Criar uma lista com todas as letras disponíveis
    if isinstance(letras, list):
        letras_disponiveis = list(letras)
    else:
        letras_disponiveis = criar_lista_letras(letras)
    
    for pad, let in zip(padrao,palavra): #Criar um tuplo para facilitar comparação entre padrao e palavra
        if pad == '.':
            if let not in letras_disponiveis: #Verificar as letras
                return False
            letras_disponiveis.remove(let) 
        elif pad != let: #Não permitir a sobreposição de letras 
            return False
    return True

#Transformadores 
def ficheiro_para_vocabulario(nome_fich):
    """
    Lê palavras de um ficheiro e devolve um tuplo com palavras válidas para o vocabulário.

    Args:
        nome_fich -> string (nome do ficheiro)
    Return:
        vocab -> tuplo de palavras válidas
    """
    letras_validas = set(LETRAS)
    vocab = set()
    with open(nome_fich, 'r') as f:
        for linha in f:
            palavra = linha.upper().strip()
            if len(palavra) >= 2 and len(palavra) <= 15 and set(palavra).issubset(letras_validas):
                vocab.add(palavra)

    return cria_vocabulario(tuple(vocab))


def vocabulario_para_str(vocabulario):
    if not type(vocabulario) == dict:
        vocabulario = cria_vocabulario(vocabulario) 

    vocab_lst = []
    #Percorrer por comprimento (crescente)
    for comprimento in sorted(vocabulario.keys()): #Ordenar as palavras por ordem crescente
        # Para cada comprimento percorrer as iniciais
        for inicial in sorted(vocabulario[comprimento], key = chave): #Ordenar as palavras por ordem lexicográfica 
            # Percorrer todas as palavras por ordem
            for i in vocabulario[comprimento][inicial]:
                palavra = i[0]
                vocab_lst.append(palavra)  

    return '\n'.join(vocab_lst) 


def procura_palavra_padrao(vocabulario, padrao, letras, min_pontos):
    if type(vocabulario) != dict:
        vocabulario = cria_vocabulario(vocabulario)
    
    palavras_possiveis = []
    res = ('', 0)
    inicial = padrao[0]
    comprimento = len(padrao)

    letras_para_testa = ordena_letras(letras)

    if inicial in LETRAS: #O padrão começa por uma letra 
        palavras_possiveis = vocabulario.get(comprimento, {}).get(inicial, []) #Retorna o tuplo (palavra, pontos)
        for palavra, pontos in palavras_possiveis:
            #A pontuação da palavra tem que ser maior do que min_pontos
            if pontos < min_pontos: 
                continue
            #Verificar se a palavra pode ser colocada no padrão
            if testa_palavra_padrao(vocabulario, palavra, padrao, letras_para_testa):
                #Apenas armazenar a palavra com maior pontuação
                if pontos > res[1]:
                    res = (palavra, pontos)
                elif pontos == res[1] and (res[0] == '' or chave(palavra) < chave(res[0])):  # Ordem lexicográfica
                        res = (palavra, pontos)
    
    if inicial == '.':  # O padrão começa por um espaço livre
        comps = vocabulario.get(comprimento, {})
        for l in letras_para_testa:
            palavras_possiveis = comps.get(l, [])
            for palavra, pontos in palavras_possiveis:
                if pontos < min_pontos: 
                    continue
                if testa_palavra_padrao(vocabulario, palavra, padrao, letras_para_testa):
                    if pontos > res[1]:
                        res = (palavra, pontos)
                    elif pontos == res[1] and (res[0] == '' or chave(palavra) < chave(res[0])):  # Ordem lexicográfica
                        res = (palavra, pontos)
    
    return res


#-------------------------------------------------------
#TAD Tabuleiro

#Construtor
def cria_tabuleiro():
    """
    Cria uma lista de listas com n elementos e n listas que irá representar o tabuleiro de jogo

    Argumentos: Função sem parâmetros
    Return:
        tab -> Tabuleiro
    #
    """
    tab = [] 
    #Criar a lista de listas
    for i in range(DIMENSOES):
        linha = ['.'] * DIMENSOES
        tab.append(linha)

    return tab


#Seletores
def obtem_letra(t, c):
    #Obter o caracter que está na casa (c)
    linha, coluna = obtem_lin(c) - 1, obtem_col(c) - 1 #Compensar o facto de o índice começar em 0
    return t[linha][coluna]


#Modificadores
def insere_letra(t,c,l):
    linha, coluna = obtem_lin(c) - 1, obtem_col(c) - 1
    #Inserir a letra no tabuleiro
    t[linha][coluna] = l
    return t


#Reconhecedores
def eh_tabuleiro(arg):
    if not isinstance(arg, (list, tuple, dict)) or len(arg) != DIMENSOES:
        return False
    for linha in arg:
        if type(linha) != list or len(linha) != DIMENSOES:
            return False
        for casa in linha:
            if casa != '.' and casa not in LETRAS:
                return False
    return True


def eh_tabuleiro_vazio(arg):
    if not eh_tabuleiro(arg):
        return False
    for linha in arg:
        for casa in linha:
            if casa != '.':
                return False
    return True


def tabuleiros_iguais(t1,t2):
    if not eh_tabuleiro(t1) or not eh_tabuleiro(t2):
        return False
    for l in range(DIMENSOES):
        for c in range(DIMENSOES):
            if t1[l][c] != t2[l][c]:
                return False
    return True


#Transformadores

#Funções Auxiliares para tabuleiro_para_str DIMENSOES -> 15

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
    
    espaco = '     ' #Formatação
    #Criar as strings do cabeçalho
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
    #Criar uma string com o conteudo da linha em específico
    linha_conteudos = ' '.join(conteudo_linha)

    #Formatar o número da linha com largura 2 (à direita)
    indice_linha = f'{numero_linha:2}' 

    #Criar a linha final
    linha_str = f'{indice_linha} | {linha_conteudos} |'
    return linha_str
    

def tabuleiro_para_str(t): #3.2.7
    """
    Recebe a lista de listas da função cria_tabuleiro e representa o tabuleiro como uma string
    contínua, com os números de linha e coluna e com as bordas
    
    Argumentos:
        tab -> lista (tabuleiro)
    Return:
        tabuleiro -> string (tabuleiro formatado)
    """
    DIMENSOES = len(t)
    linhas = []

    #Adicionar os cabecalhos
    cabecalho_dezenas, cabecalho_unidades = cabecalho(DIMENSOES)
    linhas.append(cabecalho_dezenas)
    linhas.append(cabecalho_unidades)

    #Adicionar a borda superior
    borda_sup = borda_superior_inferior(DIMENSOES)
    linhas.append(borda_sup)

    #Adicionar a linhas do tabuleiro
    for i in range(1, DIMENSOES + 1):
        linhas.append((linha_para_str(i, t[i - 1]))) 

    #Adicionar a borda inferior
    borda_inf = borda_superior_inferior(DIMENSOES)
    linhas.append(borda_inf)

    #Criar o tabuleiro final
    tabuleiro = '\n'.join(linhas)

    return tabuleiro

#Funções de Alto Nível
def obtem_padrao(t, i, f):
    linha_i = i[0] - 1
    coluna_i = i[1] - 1
    linha_f = f[0] - 1
    coluna_f = f[1] - 1
    res = ''
    if linha_i == linha_f: #Direção Horizontal
        for i in range(coluna_i, coluna_f + 1):
            res += t[linha_i][i]

    if coluna_i == coluna_f: #Direção Vertical
        for i in range(linha_i, linha_f + 1):
            res += t[i][coluna_i]
    
    return res


def insere_palavra(t, c, d, p):
    linha, coluna = obtem_lin(c), obtem_col(c)
    if d == 'H':
        for i in range(len(p)):
            t = insere_letra(t, (linha, coluna + i), p[i])
    if d == 'V':
        for i in range(len(p)):
            t = insere_letra(t, (linha + i, coluna), p[i])

    return t


def obtem_subpadroes(t, i, f, l):
    """
    Função responsável por obter os subpadrões de um padrão específico do tabuleiro

    Args:
        t -> lista (tabuleiro) | i -> tuplo (casa inicial) | f -> tuplo (casa final) | l -> inteiro
    Return
        subpadrao_lst -> tuplo | casas_i_tup -> tuplo
    """
    #Obter o padrão
    padrao = obtem_padrao(t, i, f)
    comprimento = len(padrao)

    #Criar listas para armazenar o resultado final
    subpadrao_lst = list()
    casa_i_tup = list()

    #Percorre cada posição possível como início do subpadrão
    for inicio in range(comprimento):
        #Para cada posição inicial, gerar o maior subpadrão possível (encurtando depois da direita para a esquerda)
        for fim in range(comprimento, inicio, -1):
            #Obter o subpadrao
            subpadrao = padrao[inicio:fim]
            
            #Condição: Ter pelo menos um espaço livre e a sua quantidade ser menor ou igual a l
            espacos_livres = subpadrao.count('.')
            if '.' not in subpadrao or espacos_livres > l:
                continue
            
            #Condição: Garantir que há um espaço livre antes ou depois
            antes = '.'
            depois = '.'
            if inicio > 0:
                antes = padrao[inicio-1]
            if fim < comprimento:
                depois = padrao[fim]
            if antes != '.' or depois != '.':
                continue

            #Condição: Garantir que há pelo menos uma letra no subpadrão
            tem_letra = False
            for letra in subpadrao:
                if letra in LETRAS:
                    tem_letra = True
                    break
            if not tem_letra:
                continue
                
            #Obter a casa inicial do subpadrao
            if i[0] == f[0]: #Horizontal
                casa_inicio = (i[0], i[1] + inicio)
            else: #Vertical
                casa_inicio = (i[0] + inicio, i[1])
            
            subpadrao_lst.append(subpadrao)
            casa_i_tup.append(casa_inicio)

    return tuple(subpadrao_lst), tuple(casa_i_tup)


def gera_todos_padroes(t, l):
    """
    Devolve três tuplos (padroes, casas_inicio, direcoes).
    - padroes: tuplo de strings (sub-padrões) na ordem de geração (linhas completas, depois colunas).
    - casas_inicio: tuplo de coordenadas com a casa inicial correspondente para cada padrao.
    - direcoes: tuplo com 'H' ou 'V' para cada padrão, alinhado por índice com padroes.
    """
    padroes = []
    casas = []
    direcoes = []

    #Linhas -> Horizontal
    for linha in range(1, DIMENSOES + 1):
        i = (linha, 1)
        f = (linha, DIMENSOES)
        subpads, casas_sub = obtem_subpadroes(t, i, f, l)
        padroes.extend(subpads) #Colocar todos os subpadrões da linha
        casas.extend(casas_sub) #Colocar as casas iniciais correspondentes
        direcoes.extend(['H'] * len(subpads)) #Colocar 'H' tantas vezes quantos subpadrões foram gerados
    
    #Colunas -> Vertical
    for coluna in range(1, DIMENSOES + 1):
        i = (1, coluna)
        f = (DIMENSOES, coluna)
        subpads, casas_sub = obtem_subpadroes(t, i, f, l)
        padroes.extend(subpads) #Colocar todos os subpadrões da coluna
        casas.extend(casas_sub) #Colocar as casas iniciais correspondentes
        direcoes.extend(['V'] * len(subpads)) #Colocar 'V' tantas vezes quantos subpadrões foram gerados
    
    return tuple(padroes), tuple(casas), tuple(direcoes)

#---------------------------------------------------------
#Funções Adicionais
saco = {
    'A': 14, 'B': 3, 'C': 4, 'Ç': 2, 'D': 5, 'E': 11, 'F': 2, 'G': 2,
    'H': 2, 'I': 10, 'J': 2, 'L': 5, 'M': 6, 'N': 4, 'O': 10, 'P': 4,
    'Q': 1, 'R': 6, 'S': 8, 'T': 5, 'U': 7, 'V': 2, 'X': 1, 'Z': 1}

#Funções auxiliares ao baralha_saco
def gera_numero_aleatorio(estado): #Função Auxiliar
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


def permuta_letras(letras, estado): #Função Auxiliar 
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
    #Algoritmo Fisher-Yates
    for i in range(tamanho - 1, 0, -1):  
        estado = gera_numero_aleatorio(estado)
        n = estado % (i+1)
        letras[i], letras[n] = letras[n], letras[i]


def baralha_saco(seed):
    letras_saco = criar_lista_letras(saco)
    saco_ordenado = ordena_letras(letras_saco)
    permuta_letras(saco_ordenado, seed)

    return saco_ordenado


#Função Auxiliar à jogada
def joga_palavra(tab, palavra, casa, direcao, conj_letras, vocab, padrao): #3.4.1
    """
    Funçao Auxiliar ao funcionamento da jogada_humano e jogada_agente.
    Tem como função realizar a jogada retornando um tuplo com as letras usadas para a colocação da palavra no tabuleiro

    Argumentos: 
        tab -> tabuleiro |  palavra -> string | casa -> tuplo | direcao -> string |
        conj_letras -> conjunto de letras (tuplo) | vocab -> conjunto de letras válidas (dicionário) |
        primeira -> Bool
    Return:
        () -> tuplo (vazio) se a jogada for inválida | letras_usadas -> lista
    """
    #Atribuir valores às variáveis
    l, c = obtem_lin(casa) - 1, obtem_col(casa) - 1
    tamanho_palavra = len(palavra) 

    #Verificar se as palavras excedem os limites do tabuleiro
    if direcao == 'H':
        if c + tamanho_palavra > len(tab[0]):
            return()
    elif direcao == 'V':
        if l + tamanho_palavra > len(tab):
            return ()
    else:
        return ()
    
    #Verificar se a primeira palavra jogada interseta o centro do tabuleiro
    tabuleiro_vazio = eh_tabuleiro_vazio(tab)
    if tabuleiro_vazio:
        if tamanho_palavra < 2: #Testar se o comprimento da primeira palavra é maior do que 1
            return()
        centro = (len(tab[0]) + 1) // 2 
        coordenadas_centro = cria_casa(centro, centro) #Definir o par de coordenadas do centro
        passou_pelo_centro = False 
        #Coordenadas iniciais
        pos = casa

        for i in range(tamanho_palavra + 1):
            if pos == coordenadas_centro: #Se alguma letra da palavra passar pela coordenada centro
                passou_pelo_centro = True #
                break
            pos = incrementa_casa(casa, direcao, i)
            
        if not passou_pelo_centro: #Caso não tenha passado no centro do tabuleiro
            return ()
    
    #Verificar se a palavra pode ser formada com as letras do conjunto
    if isinstance(conj_letras, list):
        conj_temp = conj_letras.copy() #Criar um conjunto temporário para não alterar destrutivamente a lista original

    conj_temp = criar_lista_letras(conj_letras)
    letras_usadas = [] #Criar uma lista para armazenar as letras já utilizadas

    #Condição a executar se não for a primeira jogada
    if not tabuleiro_vazio:
        contador = 0
        for i in padrao:
            if i in LETRAS:
                break
            contador += 1
        # A partir da primeira jogada, as palavras introduzidas têm de intersetar alguma palavra existente no tabuleiro
        if contador == len(padrao):
            return ()

    #Se a palavra não puder ser introduzida
    """if not testa_palavra_padrao(vocab, palavra, padrao, conj_letras):
        return ()"""

    #Se a palavra corresponder ao padrao
    if padrao == palavra:
        return ()
    
    #Retirar as letras
    for p, l in zip(padrao, palavra):       
        if p == '.' and l in conj_temp:# or p == '.' and conj_temp[l] > 0:
            letras_usadas.append(l)
            #conj_temp[l] -= 1
            conj_temp.remove(l)

    letras_usadas = ordena_letras(letras_usadas) #Ordenar o baralho do jogador
    letras_usadas = tuple(letras_usadas) #Converter para tuplo

    return letras_usadas


def jogada_humano(tab, jog, vocab, pilha):
   while True:
        letras_troca = []
        #Pedir uma jogada ao utilizador
        entrada = input(f'Jogada {jogador_identidade(jog)}: ')
        #Separar os vários passos da jogada numa lista
        jogada = entrada.split(' ') 

        #Verificar a validade da jogada
        if len(jogada) < 1:
            continue
        
        #Opção Passar a vez
        if entrada.strip() == 'P':
            return False
            
        #Opção Trocar Letras
        elif jogada[0] == 'T':
            #Verificação
            letras_para_troca = jogada[1:]
        
            if len(pilha) == 0 or len(letras_para_troca) == 0 or len(letras_para_troca) > 7:
                continue
        
            validacao = True
            #Verificar se o jogador está a trocar letras que estão no seu baralho
            for letra in letras_para_troca:
                if letra not in jogador_letras(jog):
                        validacao = False
                        break
            
            if not validacao:
                continue

            #Retirar as letras do baralho do jogador         
            for l in letras_para_troca:
                usa_letra(jog, l)
                      
            #Adicionar as letras ao jogador
            distribui_letras(jog, pilha, len(letras_para_troca))
       
            return True
        
        #Opção Jogar
        elif jogada[0] == 'J':
            if len(jogada) != 5:
                continue

            #Obter as coordenadas do início da jogada
            linha = jogada[1] 
            coluna = jogada[2] 

            #Verificar se a casa introduzida pertence ao tabuleiro
            if not eh_casa((linha, coluna)):
                continue
            
            #Converter a linha e coluna para inteiro
            linha, coluna = int(linha), int(coluna)
            
            casa = (linha, coluna) #Criar o tuplo casa

            #Verificar a direção da jogada
            direcao = jogada[3]
            if direcao not in ('H', 'V'):
                continue

            palavra = jogada[4] #Obter a palavra
            tamanho_palavra = len(palavra)

            #Verificar se a palavra excede os limites do tabuleiro
            if direcao == 'H' and tamanho_palavra + coluna - 1 <= 15:
                padrao = obtem_padrao(tab, casa, (linha, coluna + tamanho_palavra - 1)) #Obter o padrão
            elif direcao == 'V' and tamanho_palavra + linha - 1 <= 15:
                padrao = obtem_padrao(tab, casa, (linha + tamanho_palavra - 1, coluna)) 
            else:
                continue
            
            #Testar a validade da jogada
            if not testa_palavra_padrao(vocab, palavra, padrao, jog['letras']):
                continue

            #Obter as letras usadas na palavra
            letras_usadas = joga_palavra(tab, palavra, casa, direcao, jog['letras'], vocab, padrao)
            if letras_usadas == ():
                continue

            #Atribuir os pontos pela jogada
            for letra in palavra:
                jog['pontos'] += PONTOS[letra]
            """pontuacao = obtem_pontos(vocab, palavra)
            #Se a palavra não for válida
            if pontuacao == 0:
                continue
            jog = soma_pontos(jog, pontuacao)"""
            
            #Inserir a palavra no tabuleiro
            insere_palavra(tab, casa, direcao, palavra)

            #Retirar as letras usadas (que não estavam no tabuleiro) do baralho do jogador
            for i in range(len(letras_usadas)):
                jog = usa_letra(jog, letras_usadas[i])                        

            #Distribuir as letras em falta no baralho do jogador
            distribui_letras(jog, pilha, len(letras_usadas))

            return True
        
        else:
            continue


def jogada_agente(tab, jog, vocab, pilha):
    min_pontos = 0
    #Passar a vez se o tabulerio estiver vazio
    if eh_tabuleiro_vazio(tab):
        print(f'Jogada {jogador_identidade(jog)}: P')
        return False

    letras_agente = criar_lista_letras(jogador_letras(jog))

    #Jogar
    padroes, casas, direcoes = gera_todos_padroes(tab, len(letras_agente))

    if jogador_identidade(jog) == 'FACIL':
        n = 100
    elif jogador_identidade(jog) == 'MEDIO':
        n = 50
    elif jogador_identidade(jog) == 'DIFICIL':
        n = 10

    padroes_s = padroes[::n]
    casas_s = casas[::n]
    direcoes_s = direcoes[::n]

    melhor_palavra = ''
    melhor_pontos = 0
    melhor_casa = None
    melhor_direcao = None
    melhor_letras_usadas = ()

    for i in range(0, len(padroes_s)):
        padrao = padroes_s[i]

        if '.' not in padrao or padrao.count('.') > len(letras_agente):
            continue

        casa = casas_s[i]
        direcao = direcoes_s[i]

        palavra, pontos_pal = procura_palavra_padrao(vocab, padrao, jogador_letras(jog), min_pontos)

        if palavra != '':
            letras_usadas = joga_palavra(tab, palavra, casa, direcao, jogador_letras(jog), vocab, padrao)

            if letras_usadas != ():
                if pontos_pal > melhor_pontos:
                    melhor_palavra = palavra
                    melhor_pontos = pontos_pal
                    melhor_casa = casa
                    melhor_direcao = direcao
                    melhor_letras_usadas = letras_usadas
        
    if melhor_palavra != '':
        insere_palavra(tab, melhor_casa, melhor_direcao, melhor_palavra)
        soma_pontos(jog, melhor_pontos)
        for letra in melhor_letras_usadas:
            usa_letra(jog, letra)
        distribui_letras(jog, pilha, len(melhor_letras_usadas))
        print(f'Jogada {jogador_identidade(jog)}: J {obtem_lin(melhor_casa)} {obtem_col(melhor_casa)} {melhor_direcao} {melhor_palavra}')
        return True

    #Verificar se é possível trocar as letras
    if len(pilha) >= 7:
        letras_troca = ''
        for let in jogador_letras(jog):
            letras_troca += ' ' + let
            #Retirar as letras do baralho do jogador
            usa_letra(jog, let)

        print(f'Jogada {jogador_identidade(jog)}: T{letras_troca}')
        #Acrescentar as letras novas
        distribui_letras(jog, pilha, 7)
        
        return True

    print(f'Jogada {jogador_identidade(jog)}: P')
    return False


def scrabble2(jogadores, nome_fich, seed): #tuplo, str, int
    #Validações
    if type(jogadores) != tuple or len(jogadores) > 4 or len(jogadores) < 1 or type(nome_fich) != str or type(seed) != int or seed <= 0 or type(saco) != dict:
        raise ValueError('scrabble2: argumentos inválidos')
    
    #Obter a pilha 
    pilha = baralha_saco(seed)

    #Criar os jogadores
    lista_jogadores = []
    for j in jogadores:
        if type(j) != str:
            raise ValueError('scrabble2: argumentos inválidos')
        if j[0] == '@':
            player = cria_agente(j[1:])
        else:
            player = cria_humano(j)
        distribui_letras(player, pilha, 7)
        lista_jogadores.append(player)

    #Criar vocabulário
    vocab = ficheiro_para_vocabulario(nome_fich)
    
    #Introdução
    print('Bem-vindo ao SCRABBLE2.')
    tab = cria_tabuleiro()

    passes = 0
    #Ciclo principal de jogo
    while True:
        for jogador in lista_jogadores:
            print(tabuleiro_para_str(tab))
            for j in lista_jogadores:
                print(jogador_para_str(j))
        
            res = None
            if eh_humano(jogador):
                res = jogada_humano(tab, jogador, vocab, pilha)
            
            elif eh_agente(jogador):
                res = jogada_agente(tab, jogador, vocab, pilha)
            
            if not res:
                passes += 1
            else: 
                passes = 0

            tuplo_final = ()
            if passes >= len(lista_jogadores):
                for jog in lista_jogadores:
                    tuplo_final = tuplo_final + (jogador_pontos(jog),) #Criar o tuplo com os pontos de cada jogador
                return tuplo_final
    
            baralho_jogador = criar_lista_letras(jogador_letras(jogador))
            if len(pilha) == 0 and len(baralho_jogador) == 0:
                for jog in lista_jogadores:
                    tuplo_final = tuplo_final + (jogador_pontos(jog),) #Criar o tuplo com os pontos de cada jogador
                return tuplo_final 