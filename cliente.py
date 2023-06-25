from auxiliares import *

nome_cliente = None
def alugar_jogo(lista_jogos, saldo):
    
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
    return saldo

def retornar_jogo(lista_jogos):
    encontrou = False
    clear()
    print("Opção 'Retornar jogo' selecionada.\n")
    exibir_jogos(lista_jogos)
    print("__________________________\n")
    nome_jogo = input("Digite o nome do jogo a ser retornado: ")
    for jogo in lista_jogos:
        if jogo["nome"] == nome_jogo:
            encontrou = True
            clear()
            print("__________________________")
            print("\nJogo retornado com sucesso!")
            jogo["qtd"] += 1 
            print("{}:  | Quantidade no estoque atualizada: {}".format(nome_jogo, jogo["qtd"]))
            print("__________________________\n")
            break
    if not encontrou:
        print("__________________________\n")
        print("Jogo não encontrado no estoque.")
        print("__________________________\n")
    return lista_jogos
        
def valida_cliente(lista_clientes, nome): # verifica se o cliente existe no cadastro tipo um login
    clear()
    for cliente in lista_clientes:
        if cliente['nome'] == nome:
            return True
    return False
