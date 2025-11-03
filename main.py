import random
import os
import time
from operator import attrgetter

# ------------------------------------------------------------------------------------------------
#                                          Constantes                                        
# ------------------------------------------------------------------------------------------------
VELOCIDADE_DO_JOGO = 2
CORAGEM            = 1


# ------------------------------------------------------------------------------------------------
#                                          Classes                                        
# ------------------------------------------------------------------------------------------------
class Naipe:
    def __init__(self, nome, simbolo):
        self.nome    = nome
        self.simbolo = simbolo

class Carta:
    def __init__(self, numero, naipe, peso):
        self.numero = numero
        self.naipe  = naipe
        self.peso   = peso

    def __str__(self):
        coresPadrao = "\033[0m"
        if self.naipe.nome == "copas" or self.naipe.nome == "ouros":
            corTexto = "\033[0;31m" # vermelho
            corFundo = "\033[47m" # branco
            return f"{corTexto}{corFundo}[{self.numero}{self.naipe.simbolo}]{coresPadrao}"
        else:
            corTexto = "\033[30m" # preto
            corFundo = "\033[47m" # branco
            return f"{corTexto}{corFundo}[{self.numero}{self.naipe.simbolo}]{coresPadrao}"

class Baralho:
    def __init__(self):
        self.cartas = []
        self.naipes = {
            Naipe("copas",   "\U00002665"),
            Naipe("ouros",   "\U00002666"),
            Naipe("espadas", "\U00002660"),
            Naipe("paus",    "\U00002663")
        }
        self.criaBaralho()

    def __str__(self):
        cartasOrdenadas = sorted(self.cartas, key=attrgetter('peso'))
        baralhoString   = ""
        for carta in cartasOrdenadas:
            # baralhoString += carta.__str__() + " "
            baralhoString += f"{carta.__str__()} -> {carta.peso}\n"
        return baralhoString

    def criaBaralho(self):
        # criando o baralho
        for naipe in self.naipes:

            if naipe.nome == "paus": # zap
                self.adicionaCarta(Carta("4", naipe, 14))
            else:
                self.adicionaCarta(Carta("4", naipe, 1))

            self.adicionaCarta(Carta("5", naipe, 2))
            self.adicionaCarta(Carta("6", naipe, 3))

            if naipe.nome == "copas": # setão
                self.adicionaCarta(Carta("7", naipe, 13))
            elif naipe.nome == "ouros": # mole
                self.adicionaCarta(Carta("7", naipe, 11))
            else:
                self.adicionaCarta(Carta("7", naipe, 4))

            self.adicionaCarta(Carta("Q", naipe, 5))
            self.adicionaCarta(Carta("J", naipe, 6))
            self.adicionaCarta(Carta("K", naipe, 7))

            if naipe.nome == "espadas": # espadilha
                self.adicionaCarta(Carta("A", naipe, 12))
            else:
                self.adicionaCarta(Carta("A", naipe, 8))

            self.adicionaCarta(Carta("2", naipe, 9))
            self.adicionaCarta(Carta("3", naipe, 10))

    def sorteaCartaTiraDoBaralho(self):
        cartaSorteada = random.choice(self.cartas)
        self.cartas.remove(cartaSorteada)
        return cartaSorteada

    def sorteaUmaMao(self):
        cartas = []
        for i in range (0,3):
            cartas.append(self.sorteaCartaTiraDoBaralho())
        return Mao(cartas)
    
    def removeCartaDoBaralho(self, cartaParaRemover):
        for cartaBaralho in self.cartas:
            if (cartaBaralho.numero == cartaParaRemover.numero) and (cartaBaralho.naipe.nome == cartaParaRemover.naipe.nome):
                self.cartas.remove(cartaBaralho)    

    def removeCartasDoBaralho(self, cartasParaRemover):
        for cartaParaRemover in cartasParaRemover:
            self.removeCartaDoBaralho(cartaParaRemover)
        # self.cartas = np.setdiff1d(self.cartas, cartas)

    def adicionaCarta(self, carta):
        self.cartas.append(carta)



class Mao:
    def __init__(self, cartas):
        self.cartas = cartas

    def __str__(self):
        cartasString = ""
        for carta in self.cartas:
            cartasString += carta.__str__() + " "
        return cartasString
    
    def printaCartas(self, podeTrucar):
        if podeTrucar:
            print(self.__str__() + "[truco]")
        else:
            print(self.__str__())
            
        opcoes = []
        for i in range (1, len(self.cartas)+1):
            opcao = i
            opcoes.append(opcao)

        if podeTrucar:
            opcao = 4
            opcoes.append(opcao)

        return opcoes
    
    def printaCartasEOpcoes(self, podeTrucar):
        if podeTrucar:
            print(self.__str__() + "[truco]")
        else:
            print(self.__str__())
            
        mensagemOpcoes = ""
        opcoes = []
        for i in range (1, len(self.cartas)+1):
            opcao           = i
            mensagemOpcoes += f" {opcao}   "
            opcoes.append(opcao)

        if podeTrucar:
            opcao = 4
            mensagemOpcoes += f"   {opcao}"
            opcoes.append(opcao)

        print(mensagemOpcoes)
        return opcoes

    def removeDaMao(self, posicaoCarta):
        return self.cartas.pop(posicaoCarta)


class Jogador:
    def __init__(self, nome, mao, npc):
        self.nome              = nome
        self.mao               = mao
        self.npc               = npc
        self.podeTrucar        = True
        self.cartasDescobertas = [] # cartas que o jogador já viu na mesa
        self.adicionaArrayCartasDescobertas(mao.cartas) # já conheço as cartas da mão inicial

    def __str__(self):
        return f"{self.nome}: " + self.mao.__str__() + "\n"

    # aqui faço a lógica de qual carta jogar
    def decideQualCartaJogar(self):
        # por enquanto, só jogo a mais forte
        maiorCartaDaMao   = Carta("4", Naipe("ouros", "\U00002666"), 1)
        i                 = 0
        posicaoMaiorCarta = i
        for carta in self.mao.cartas:
            i += 1
            if carta.peso >= maiorCartaDaMao.peso:
                maiorCartaDaMao   = carta
                posicaoMaiorCarta = i

        porcentagemCartasMaiores = self.porcentagemDeCartasMaiores(maiorCartaDaMao)
        if porcentagemCartasMaiores < (5 * CORAGEM) and self.podeTrucar:
            return 4 # tô forte, vou trucar

        return posicaoMaiorCarta
    

    # aqui é a decisão de aceitar ou não o truco
    def decideSeAceitaTruco(self):
        maiorCartaDaMao = Carta("4", Naipe("ouros", "\U00002666"), 1)
        for carta in self.mao.cartas:
            if carta.peso >= maiorCartaDaMao.peso:
                maiorCartaDaMao = carta
        
        # vamos calcular a porcentagem de cartas desconhecidas que são maiores que a minha mais forte
        porcentagemCartasMaiores = self.porcentagemDeCartasMaiores(maiorCartaDaMao)

        # quanto menor a porcentagem, melhor
        if porcentagemCartasMaiores < (5 * CORAGEM):
            return 3 # truco por cima
        elif porcentagemCartasMaiores < (10 * CORAGEM):
            return 1 # aceito o truco
        else:
            return 2 # corro
        
    def adicionaCartaDescoberta(self, carta):
        self.cartasDescobertas.append(carta)

    def adicionaArrayCartasDescobertas(self, cartas):
        self.cartasDescobertas += cartas

    def printaCartasDescobertas(self):
        textoCartas = ""
        for carta in self.cartasDescobertas:
            textoCartas += f" {carta.__str__()}"
        print(f"cartasDescobertas: {textoCartas}")

    def porcentagemDeCartasMaiores(self, carta):
        # vou criar um novo baralho completo e remover as cartas que já conheço.
        # dessa forma, tenho as cartas que ainda não conheço e posso calcular minha chance contra elas
        baralhoCompleto = Baralho()
        baralhoCompleto.removeCartasDoBaralho(self.cartasDescobertas)

        cartasDesconhecidas           = baralhoCompleto.cartas
        quantidadeCartasDesconhecidas = len(cartasDesconhecidas)
        cartasMaioresQueAMinha        = 0

        for cartaDesconhecida in cartasDesconhecidas:
            if cartaDesconhecida.peso > carta.peso:
                cartasMaioresQueAMinha += 1

        porcentagemCartasMaiores = (cartasMaioresQueAMinha * 100) / quantidadeCartasDesconhecidas
        return porcentagemCartasMaiores


class Dupla:
    def __init__(self, jogadores, pontos, rodadas):
        self.jogadores   = jogadores
        self.pontos      = pontos
        self.rodadas     = rodadas
        self.nomeDaDupla = f"{jogadores[0].nome} e {jogadores[1].nome}" 

    def __str__(self):
        duplaString  = "Dupla: "   + self.nomeDaDupla  + "\n"
        duplaString += "Pontos: "  + str(self.pontos)  + "\n"
        duplaString += "Rodadas: " + str(self.rodadas) + "\n"
        return duplaString
        

# ------------------------------------------------------------------------------------------------
#                                          Funções gerais                                        
# ------------------------------------------------------------------------------------------------
def buscaProximoJogadorDaFila(jogadorAtual, filaDeJogadores):
    quantidadeJogadores = len(filaDeJogadores)
    i                   = 0
    for jogador in filaDeJogadores:
        if jogador.nome == jogadorAtual.nome:  
            posicaoJogadorAtual = i
            if posicaoJogadorAtual == (quantidadeJogadores - 1):
                proximoJogador = filaDeJogadores[0]
            else: 
                proximoJogador = filaDeJogadores[posicaoJogadorAtual + 1]
        i += 1
    return proximoJogador

def adicionaCartaDescobertaAosOutrosJogadores(carta, jogadores, quemJogou):
    for jogador in jogadores:
        if jogador.nome != quemJogou.nome:
            jogador.adicionaCartaDescoberta(carta)




# ------------------------------------------------------------------------------------------------
#                                          Iniciando o programa                                        
# ------------------------------------------------------------------------------------------------
os.system("clear")
baralho = Baralho()

print("---------------- SEJA BEM-VINDO AO TRUCO! ----------------\n")
quantidadeDuplas = int(input("Quantas duplas vão jogar? "))

if quantidadeDuplas < 2:
    print("Ops... O truco deve ser jogado com pelo menos 2 duplas")
    exit()

duplas          = []
filaDeJogadores = []
for indexDupla in range(0, quantidadeDuplas):
    dupla = []
    print(f"\n\n---> Dupla {indexDupla + 1}")
    for indexJogadorDupla in range(0, 2):
        nome = input("\nNome: ")
        npc  = input("Será um jogador real (sim/nao): ")
        if npc == "sim":
            npc = False
        else:
            npc = True
        dupla.append(Jogador(nome, baralho.sorteaUmaMao(), npc))
    
    # coloco os jogadores em uma dupla
    duplas.append(Dupla([dupla[0], dupla[1]], 0, 0))

# coloco os jogadores na fila, de forma que as duplas fiquem alternadas
for cadaDupla in duplas:
    filaDeJogadores.append(cadaDupla.jogadores[0])
for cadaDupla in duplas:
    filaDeJogadores.append(cadaDupla.jogadores[1])


# loop para cada partida, roda pela ordem dos jogadores
# uma mão só acaba quando todos os jogadores jogarem todas as suas cartas
# uma rodada acaba quando chegamos ao fim da fila de jogadores
# cada mão possui 3 rodadas
i              = 0
cartasDaMao    = [] 
cartasDaRodada = [] 
numeroDaMao    = 1
duplaVencedora = 0

while not duplaVencedora: # loop de mãos
    valorDaRodada = 2 # valor padrão, reseto a cada mão
    
    # loop de rodadas
    numeroDaRodada = 1
    while numeroDaRodada <= 3: 
        os.system("clear")
        print(duplas[0])
        print(duplas[1])

        jogadorDaVez  = filaDeJogadores[i]
        correuDoTruco = False
        rodadaTrucada = False

        print(f"Mão: {numeroDaMao}")
        print(f"Rodada: {numeroDaRodada}")
        print(f"Valor da rodada: {valorDaRodada}\n")

        if len(cartasDaRodada) > 0:
            for carta in cartasDaRodada:
                print(f"{carta['jogador'].nome}: {carta['carta'].__str__()}")

        print("\n" + jogadorDaVez.nome)
        
        # para que o jogador não consiga trucar 2 vezes na mesma hora
        if rodadaTrucada:
            podeTrucar = False
        else: 
            podeTrucar = True

        opcaoErrada = True # só pra entrar no while. é gambiarra... eu sei
        while opcaoErrada:
            opcaoErrada = False
            
            if jogadorDaVez.npc:
                opcoes = jogadorDaVez.mao.printaCartas(jogadorDaVez.podeTrucar)
                print("Decidindo qual carta jogar... [computador]")
                escolha = jogadorDaVez.decideQualCartaJogar()
                time.sleep(2 / VELOCIDADE_DO_JOGO)
            else:
                opcoes  = jogadorDaVez.mao.printaCartasEOpcoes(jogadorDaVez.podeTrucar)
                escolha = input("Qual carta vai jogar? ").strip()
                if escolha == "": 
                    escolha = 0
                else:
                    escolha = int(escolha)

            # verifica se a resposta é válida
            if escolha not in opcoes:
                opcaoErrada = True
                print(f"\nOps... você tem as seguintes opções: ")
                continue

            elif escolha == 4: # truco ladrao
                respostaTruco             = 0
                quemPediuTruco            = jogadorDaVez
                quemPediuTruco.podeTrucar = False # esse jogador não pode trucar de novo nessa mão

                while (respostaTruco != 1) and (respostaTruco != 2):
                    proximoJogador = buscaProximoJogadorDaFila(quemPediuTruco, filaDeJogadores)
                    
                    print(f"\n\n{quemPediuTruco.nome} pediu truco ({valorDaRodada + 2} pontos)!")

                    if proximoJogador.npc:
                        print(f"{proximoJogador.nome} está decidindo se aceita ou não... [computador]")
                        respostaTruco = proximoJogador.decideSeAceitaTruco()
                        time.sleep(2 / VELOCIDADE_DO_JOGO)
                    else:
                        print(f"\n{proximoJogador.nome}, você aceita?")
                        proximoJogador.mao.printaCartas(False)
                        print(f"\n[Sim] [Não] [Quero {valorDaRodada + 2 + 2}!]")
                        print(f"  1     2        3")
                        respostaTruco = input("Opção: ")

                    respostaTruco = int(respostaTruco)

                    if respostaTruco == 1:
                        rodadaTrucada  = True
                        valorDaRodada += 2
                        print(f"{proximoJogador.nome} aceitou! A rodada agora vale {valorDaRodada} pontos!")
                        time.sleep(2 / VELOCIDADE_DO_JOGO)

                    elif respostaTruco == 2:
                        correuDoTruco = True
                        vencedorTruco = quemPediuTruco
                        print(f"{proximoJogador.nome} correu... A dupla de {quemPediuTruco.nome} ganhou {valorDaRodada} pontos!")
                        time.sleep(2 / VELOCIDADE_DO_JOGO)

                    elif respostaTruco == 3:
                        valorDaRodada += 2
                        quemPediuTruco = proximoJogador
                        print(f"\n{quemPediuTruco.nome} aumentou!")
                        time.sleep(2 / VELOCIDADE_DO_JOGO)

                    else: 
                        print("Opção inválida... Tente novamente")

            else: 
                cartaJogada = jogadorDaVez.mao.removeDaMao(escolha-1)
                cartasDaRodada.append({
                    "jogador": jogadorDaVez,
                    "carta":   cartaJogada
                })
                adicionaCartaDescobertaAosOutrosJogadores(cartaJogada, filaDeJogadores, jogadorDaVez)

        # se for trucada, preciso passar pelo mesmo jogador de novo pra ele jogar, então não incremento
        if not rodadaTrucada: 
            i += 1

        # todos já jogaram ou alguém correu do truco, rodada acabou
        if (i == len(filaDeJogadores)) or correuDoTruco: 
            os.system("clear")
            # cálculos pra definir a dupla vencedora

            if not correuDoTruco:
                # iniciamos com a primeira e vamos comparar com as outras
                cartaMaisForte = cartasDaRodada[0]
                for cadaCarta in cartasDaRodada:
                    if cadaCarta["carta"].peso >= cartaMaisForte["carta"].peso:
                        cartaMaisForte = cadaCarta

            else:
                # se correu do truco, a mão é finalizada
                numeroDaRodada = 4 # para finalizar o look da mão
                cartaMaisForte = {
                    "jogador": vencedorTruco,
                    "carta":   "A outra dupla correu do truco..."
                }

            # procuro a dupla do jogador vencedor
            for dupla in duplas:
                for jogador in dupla.jogadores:
                    if jogador.nome == cartaMaisForte["jogador"].nome:
                        # incrementando as vitorias na mão
                        dupla.rodadas += 1


            print("\n\nE quem levou a rodada foi...")
            print(cartaMaisForte["jogador"].nome)
            print(f"Com a carta: {cartaMaisForte['carta']}")
            time.sleep(3 / VELOCIDADE_DO_JOGO)

            # resetando os contadores
            for cartaJogada in cartasDaRodada:
                cartasDaMao.append(cartaJogada)
            cartasDaRodada  = []
            numeroDaRodada += 1
            i = 0

    # a mão acabou
    os.system("clear")
    numeroDaMao += 1

    # procurando a dupla vencedora
    duplaVencedoraMao = duplas[0] # só pra iniciar
    for dupla in duplas: 
        if dupla.rodadas > duplaVencedoraMao.rodadas:
            duplaVencedoraMao = dupla

    duplaVencedoraMao.pontos += valorDaRodada
    print("Dupla vencedora dessa mão:")
    print(duplaVencedoraMao)

    # resetando contador de rodadas
    for dupla in duplas: 
        dupla.rodadas = 0

    # verificando se alguma dupla já completou 12 pontos e ganhou
    for dupla in duplas:
        if dupla.pontos >= 12:
            duplaVencedora = dupla
    
    if not duplaVencedora:
        # embaralhando e distribuindo as cartas 
        print("\n\nEmbaralhando e distribuindo as cartas...")
        baralho.criaBaralho()
        for jogador in filaDeJogadores:
            jogador.podeTrucar        = True
            jogador.cartasDescobertas = []
            jogador.mao               = baralho.sorteaUmaMao()
            jogador.adicionaArrayCartasDescobertas(jogador.mao.cartas)
        time.sleep(5 / VELOCIDADE_DO_JOGO)

    # aqui eu altero a ordem da fila, para que o dealer seja o próximo jogador
    # passando o antigo dealer pro fim da fila
    antigoDealer = filaDeJogadores.pop(0)
    filaDeJogadores.append(antigoDealer)

os.system("clear")
print("E a dupla vencedora foi...")
time.sleep(1 / VELOCIDADE_DO_JOGO)
print(duplaVencedora.nomeDaDupla)
print(f"Com {duplaVencedora.pontos} pontos!")

time.sleep(10 / VELOCIDADE_DO_JOGO)