from auxiliares import *

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
        return lista_jogos

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

