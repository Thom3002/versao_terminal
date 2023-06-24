import os
import platform
import sys
from time import sleep
import json

# Variáveis globais
TEMPO_CARREGAMENTO = 1 # tempo da animacao de carregamento
LOGIN_FEITO = False
CONTADOR = 0 # Conta quantas vezes um jogo que está sem estoque foi solicitado, se chegar a 3 dispara ao fornecedor a solicitação do jogo
REPOSICAO_QTD = 6 # Quantidade de jogos solicitados ao fornecedor quando acaba o estoque

lista_clientes = []
lista_jogos = [] 

global nome_cliente
global saldo

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

def registra_pedidos(nome_jogo, quantidade):
    pedido = {"nome": nome_jogo, "qtd": quantidade}
    with open('pedidos.json', 'a') as arquivo:
        json.dump(pedido, arquivo, ensure_ascii=False, indent=4)
        arquivo.write('\n')

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
            alugar_jogo(lista_jogos)
        elif opcao == "2":
            retornar_jogo()
        elif opcao == "3":  # Voltar
            clear()
            animacao_espera(TEMPO_CARREGAMENTO, "REDIRECIONANDO PARA MENU PRINCIPAL")
            exibir_menu_principal()
        elif opcao == "4": # Logout
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
        if valida_cliente(lista_clientes) == False:
            print("Cliente não cadastrado. Favor faça seu cadastro: \n")
            lista_clientes = cadastrar_cliente(lista_clientes)
            continua("cliente")
        else:
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
    print("\nSaldo da loja: R$ {}".format(saldo))
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
        excluir_jogo(lista_jogos)
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
def alugar_jogo(lista_jogos):
    global saldo
    encontrou = False
    print("Opção 'Alugar jogo' selecionada.\n")
    exibir_jogos(lista_jogos)
    print("__________________________\n")
    nome_jogo = input("Digite o nome do jogo a ser alugado: ")
    for jogo in lista_jogos:
        if jogo["nome"] == nome_jogo:
            print("\n__________________________\n")
            encontrou = True
            opcao_valida = False
            if jogo["qtd"] > 0:
                print("Período de aluguel:\n")
                print("1 - Um dia")
                print("2 - Uma semana")
                print("__________________________\n")
                opcao = int(input("Escolha uma opção: "))
                if opcao == 1:
                    opcao_valida = True
                    clear()
                    pagamento = 1 * jogo["preco_aluguel"]
                    novo_saldo = saldo + pagamento
                    print("{} alugado com sucesso por 1 dia! Valor a pagar: R$ {} (1 dia x R$ {})\nNovo saldo: R$ {} + (R$ {}) = R$ {}".format(nome_jogo, pagamento, jogo["preco_aluguel"], saldo, pagamento, novo_saldo))
                    saldo = novo_saldo
                    
                elif opcao == 2:
                    opcao_valida = True
                    clear()
                    pagamento = 7 * jogo["preco_aluguel"]
                    novo_saldo = saldo + pagamento
                    print("{} alugado com sucesso por 1 semana! Valor a pagar: R$ {} (7 dias x R$ {})\nNovo saldo: R$ {} + (R$ {}) = R$ {}".format(nome_jogo, pagamento, jogo["preco_aluguel"], saldo, pagamento, novo_saldo))
                    saldo = novo_saldo
                else: 
                    print("Opção inválida.")
                    alugar_jogo()
                if opcao_valida:
                    jogo["qtd"] -= 1 
                    print("\n{}:  | Quantidade no estoque atualizada: {}\n".format(nome_jogo, jogo["qtd"]))
                
            else:
                jogo["cont"] += 1
                print("Sem estoque. {}° solicitação.".format(jogo["cont"]))
                if jogo["cont"] == 3:
                    print("\nMandando reposicao de estoque do jogo {} ao fornecedor.".format(jogo["nome"]))# dispara ao fornecedor solicitacao para repor o estoque do jogo]
                    registra_pedidos(jogo["nome"], REPOSICAO_QTD)
                    jogo["cont"] = 0
            break
    if not encontrou:
        print("Jogo não encontrado no estoque.")
        # aumenta o contador, se chegar a 3 dispara ao fornecedor a solicitacao para comprar esse jogo
    
def retornar_jogo():
    global lista_jogos
    encontrou = False
    clear()
    print("Opção 'Retornar jogo' selecionada.\n")
    exibir_jogos(lista_jogos)
    print("__________________________\n")
    nome_jogo = input("Digite o nome do jogo a ser retornado: ")
    for jogo in lista_jogos:
        if jogo["nome"] == nome_jogo:
            encontrou = True
            print("\nJogo retornado com sucesso!")
            jogo["qtd"] += 1 
            print("\n{}:  | Quantidade no estoque atualizada: {}\n".format(nome_jogo, jogo["qtd"]))
            break
    if not encontrou:
        print("Jogo não encontrado no estoque.")
  
def valida_cliente(lista_clientes): # verifica se o cliente existe no cadastro tipo um login
    global nome_cliente
    clear()
    print("LOGIN:\n")
    nome_cliente = input("Para continuar, digite seu nome: ")
    for cliente in lista_clientes:
        if cliente['nome'] == nome_cliente:
            return True
    return False

# FUNCOES LOCADORA
def cadastrar_cliente(lista_clientes):
    nome = input("Digite o nome do cliente: ")
    cpf = input("Digite o CPF do cliente: ")
    email = input("Digite o e-mail do cliente: ")

    clientes = {'nome': nome, 'cpf': cpf, 'email': email}
    lista_clientes.append(clientes)
    print("Cliente cadastrado com sucesso!")
    # print(lista_clientes)
    return lista_clientes


def cadastrar_jogo(lista_jogos):
    print("Opção 'Cadastrar jogo' selecionada.\n")
    clear()
    jogo_id = input("Digite o id do jogo: ")
    nome = input("Digite o nome do jogo: ")
    qtd = int(input("Numero de unidades: "))
    preco_aluguel = int(input("Preço de aluguel(diária): R$ "))
    jogo = {'jogo_id': jogo_id, 'nome': nome, 'qtd': qtd, 'preco_aluguel': preco_aluguel, 'cont': 0}
    lista_jogos.append(jogo)
    return lista_jogos


def excluir_jogo(lista_jogos):
    clear()
    print("Opção 'Excluir jogo' selecionada.\n")
    if not lista_jogos:
        print("A lista de jogos está vazia.")
    else:
        exibir_jogos(lista_jogos)

        jogo_id = input("\nDigite o ID do jogo que você deseja excluir: ")

        for jogo in lista_jogos:
            if jogo['jogo_id'] == jogo_id:
                lista_jogos.remove(jogo)
                print("Jogo removido com sucesso!")
                break
        else:
            print("Jogo não encontrado no estoque.")

        exibir_jogos(lista_jogos)


def exibir_jogos(lista_jogos):  # Auxiliar para excluir jogos
    if not lista_jogos:
        print("A lista de jogos está vazia.")
    else:
        print("Jogos disponíveis:")
        i = 1
        for jogo in lista_jogos:
            print(f"{str(i).ljust(3)} | ID: {str(jogo['jogo_id']).ljust(4)} | Nome: {jogo['nome'].ljust(20)} | Quantidade: {str(jogo['qtd']).ljust(4)} | Preço de aluguel(diária): R$ {str(jogo['preco_aluguel']).ljust(5)}")

            i += 1

def exibir_clientes(lista_clientes):  
    clear()
    print("Opção 'Exibir clientes' selecionada.\n")
    if not lista_clientes:
        print("A lista de clientes está vazia.")
    else:
        print("Lista de clientes cadastrados:")
        i = 1
        for cliente in lista_clientes:
            print(f"{str(i).ljust(3)} | Nome: {cliente['nome'].ljust(25)} | CPF: {cliente['cpf'].ljust(14)} | E-mail: {cliente['email']}")

            i += 1
                        
def consultar_estoque(jogos):
    global lista_clientes
    clear()
    print("Opção 'Consultar estoque' selecionada.\n")
    if not jogos:
        print("Estoque vazio.")
    else:
        exibir_jogos(jogos)



# OUTRAS FUNÇOES
def animacao_espera(segundos, mensagem):
    animacao = "|/-\\"
    i = 0
    while segundos > 0:
        print(mensagem, animacao[i % len(animacao)], end="\r")
        i += 1
        sleep(0.1)
        segundos -= 0.1
    clear()


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


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# main
lista_jogos = ler_json("estoque.json")
lista_clientes = ler_json("clientes.json")
saldo = ler_saldo_arquivo("caixa.txt")
exibir_menu_principal()

