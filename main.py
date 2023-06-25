import os
import platform
import sys
from time import sleep
import json

from cliente import *
from locadora import *
from auxiliares import *

# Definição de funções

#FUNCOES DA MAIN DE LEITURA E ESCRITA DE ARQUIVOS
def registra_json(lista, nome_arquivo):  # Escreve a lista no arquivo json 
    with open(nome_arquivo, "w") as arquivo:
        json.dump(lista, arquivo, ensure_ascii=False, indent=4)


def ler_json(nome_arquivo): # le o json e retorna-o como uma lista
    if os.path.isfile(nome_arquivo):  # Verifica se o arquivo existe
        try:
            with open(nome_arquivo, 'r') as arquivo:
                conteudo = json.load(arquivo)
                return conteudo
        except json.decoder.JSONDecodeError:
            print(f"O arquivo {nome_arquivo} está vazio ou possui uma formatação inválida.")
            return []
    else:
        print(f"O arquivo {nome_arquivo} não existe.")
        sys.exit()

def ler_saldo_arquivo(arquivo):
    with open(arquivo, 'r') as arquivo:
        linha = arquivo.readline()
        saldo_str = linha.split('R$ ')[1].strip()
        saldo = int(saldo_str)
        return saldo
    
def registra_saldo_arquivo(saldo):
    with open('caixa.txt', 'r+') as arquivo:
        linhas = arquivo.readlines()
        for i, linha in enumerate(linhas):
            if linha.startswith('Saldo: R$'):
                linhas[i] = 'Saldo: R$ ' + str(saldo) + '\n'
                break
        arquivo.seek(0)
        arquivo.writelines(linhas)
        arquivo.truncate()



def exibir_menu_principal():  # MENU PRINCIPAL
    clear()
    print("__________________________")
    print("MENU PRINCIPAL\n")
    print("1 - Cliente")
    print("2 - Locadora")

    print("\n0 - Encerrar programa")

    print("__________________________\n")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        exibir_menu_cliente()
    elif opcao == "2":
        exibir_menu_locadora()
    elif opcao == "0":
        animacao_espera(TEMPO_CARREGAMENTO, "ENCERRANDO PROGRAMA...")
        if lista_jogos:
            registra_json(lista_jogos, "estoque.json")
        if lista_clientes:
            registra_json(lista_clientes, "clientes.json")   
        if saldo:
            registra_saldo_arquivo(saldo)
        sys.exit()
    else:
        print("\nOpção inválida! Tente novamente.\n")
        animacao_espera(TEMPO_CARREGAMENTO, "REDIRECIONANDO PARA MENU PRINCIPAL")
        exibir_menu_principal()


def exibir_menu_cliente():  # MENU CLIENTE
    global lista_clientes
    global lista_jogos
    global LOGIN_FEITO
    global nome_cliente
    global saldo
    clear()
    
    if LOGIN_FEITO:
        print(f"Olá {nome_cliente}. Seja bem vindo à locadora!")
        print()
        print("__________________________")
        print("MENU CLIENTE\n")
        print("1 - Alugar jogo")
        print("2 - Retornar jogo")
        print("3 - Voltar")
        print("\n\n4 - Logout")
        print("__________________________\n")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            clear()
            saldo = alugar_jogo(lista_jogos, saldo)
        elif opcao == "2":
            lista_jogos = retornar_jogo(lista_jogos)
        elif opcao == "3":  # Voltar
            clear()
            animacao_espera(TEMPO_CARREGAMENTO, "REDIRECIONANDO PARA MENU PRINCIPAL")
            exibir_menu_principal()
        elif opcao == "4":  # Logout
            LOGIN_FEITO = False
            clear()
            print("Logout selecionado.\n")
            animacao_espera(TEMPO_CARREGAMENTO, "REDIRECIONANDO PARA MENU PRINCIPAL")
            exibir_menu_principal()
        else:
            print("\nOpção inválida! Tente novamente.\n")
            animacao_espera(TEMPO_CARREGAMENTO, "Aguarde um momento...")
            exibir_menu_cliente()
        continua("cliente")
        
    else:
        print("LOGIN:\n")
        nome = input("Para continuar, digite seu nome: ")
        
        if valida_cliente(lista_clientes, nome) == False:
            print("Cliente não cadastrado. Favor faça seu cadastro: \n")
            lista_clientes = cadastrar_cliente(lista_clientes)
            continua("cliente")
        else:
            nome_cliente = nome
            animacao_espera(TEMPO_CARREGAMENTO, "LOGIN REALIZADO COM SUCESSO! REDIRECIONANDO PARA O MENU CLIENTE...")
            LOGIN_FEITO = True
            exibir_menu_cliente()
            

def exibir_menu_locadora():  # MENU LOCADORA
    clear()
    global saldo
    global lista_jogos
    global lista_clientes
    # print("__________________________")
    # exibir_jogos(lista_jogos)
    print("Saldo da loja: R$ {}".format(saldo))
    print("__________________________")
    print("MENU LOCADORA\n")
    print("1 - Cadastrar cliente")
    print("2 - Cadastrar jogo")
    print("3 - Excluir jogo")
    print("4 - Consultar estoque")
    print("5 - Exibir clientes")
    print("6 - Voltar")
    print("__________________________\n")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        clear()
        lista_clientes = cadastrar_cliente(lista_clientes)
    elif opcao == "2":
        lista_jogos = cadastrar_jogo(lista_jogos)
        print("Lista jogos apos a chamada da função cadastrar jogo")
        print(lista_jogos)
        
    elif opcao == "3":
        lista_jogos = excluir_jogo(lista_jogos)
    elif opcao == "4":
        consultar_estoque(lista_jogos)
    elif opcao == "5":
        exibir_clientes(lista_clientes)
    elif opcao == "6":  # Voltar
        clear()
        animacao_espera(TEMPO_CARREGAMENTO, "REDIRECIONANDO PARA MENU PRINCIPAL")
        exibir_menu_principal()

    else:
        print("\nOpção inválida! Tente novamente.\n")
        animacao_espera(TEMPO_CARREGAMENTO, "Aguarde um momento...")
        exibir_menu_locadora()
        
    continua("locadora") #volta para o menu locadora


# FUNCOES CLIENTE 

# FUNCOES LOCADORA


# OUTRAS FUNÇOES
def continua(menu):
    print("\nDeseja continuar?\n")
    print("1 - SIM")
    print("2 - NAO")
    print("__________________________\n")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":  # SIM
        if menu == "cliente":
            exibir_menu_cliente()
        else:
            exibir_menu_locadora()
    elif opcao == "2":  # NAO
        animacao_espera(TEMPO_CARREGAMENTO, "ENCERRANDO PROGRAMA...")
        if lista_jogos:
            registra_json(lista_jogos, "estoque.json")
        if lista_clientes:
            registra_json(lista_clientes, "clientes.json")
        if saldo:
            registra_saldo_arquivo(saldo)
        sys.exit()
    else:
        print("\nOpção inválida! Tente novamente.\n")
        animacao_espera(TEMPO_CARREGAMENTO, "Aguarde um momento...")
        continua(menu)

# main
lista_jogos = ler_json("estoque.json")
lista_clientes = ler_json("clientes.json")
saldo = ler_saldo_arquivo("caixa.txt")
exibir_menu_principal()

