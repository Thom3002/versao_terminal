import os
import platform
from time import sleep
import json



# Variáveis globais
TEMPO_CARREGAMENTO = 1 # tempo da animacao de carregamento
LOGIN_FEITO = False
CONTADOR = 0 # Conta quantas vezes um jogo que está sem estoque foi solicitado, se chegar a 3 dispara ao fornecedor a solicitação do jogo
REPOSICAO_QTD = 6 # Quantidade de jogos solicitados ao fornecedor quando acaba o estoque 


saldo = 0
lista_clientes = []
lista_jogos = []

def registra_pedidos(nome_jogo, quantidade): # é utilizada no modulo cliente pela funcao alugar_jogo()
    pedido = {"nome": nome_jogo, "qtd": quantidade}
    
    # Verifica se o arquivo já existe
    try:
        with open('pedidos.json', 'r') as arquivo:
            lista_pedidos = json.load(arquivo)
    except FileNotFoundError:
        lista_pedidos = []
    
    # Adiciona o novo pedido à lista
    lista_pedidos.append(pedido)
    
    with open('pedidos.json', 'w') as arquivo:
        json.dump(lista_pedidos, arquivo, ensure_ascii=False, indent=4)

def exibir_jogos(lista_jogos):  # Auxiliar para excluir jogos
    if not lista_jogos:
        print("A lista de jogos está vazia.")
    else:
        print("Jogos disponíveis:")
        i = 1
        for jogo in lista_jogos:
            print(f"{str(i).ljust(3)} | ID: {str(jogo['jogo_id']).ljust(4)} | Nome: {jogo['nome'].ljust(20)} | Quantidade: {str(jogo['qtd']).ljust(4)} | Preço de aluguel(diária): R$ {str(jogo['preco_aluguel']).ljust(5)}")

            i += 1


def animacao_espera(segundos, mensagem):
    animacao = "|/-\\"
    i = 0
    while segundos > 0:
        print(mensagem, animacao[i % len(animacao)], end="\r")
        i += 1
        sleep(0.1)
        segundos -= 0.1
    clear()


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
        