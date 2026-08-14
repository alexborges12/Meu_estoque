import os
import json

LINK_APP = "https://meuestoque-c5rebryzdwvgtobe5shzw2.streamlit.app/"
estoque = []

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def salvar_estoque():
    with open("estoque.json", "w", encoding="utf-8") as f:
        json.dump(estoque, f, ensure_ascii=False, indent=4)

def carregar_estoque():
    global estoque
    try:
        with open("estoque.json","r", encoding="utf-8") as f:
            estoque = json.load(f)
    except FileNotFoundError:
        estoque = []

def perguntar_novamente(acao):
    limpar_tela()
    resp = input(f"\nDeseja {acao} novamente? [S/N]: ").strip().lower()
    return resp == 's'

carregar_estoque()

while True:
    limpar_tela()
    print("ALEX A.BORGES.LTDA".center(40))
    print("___________Meu estoque___________".center(35))
    print("_"*40)
    print("1.) Adicionar_produto\n2.) Checar_produto\n3.) Ver_estoque\n4.) Deletar_produto\n5.) Link_App\n6.) Sair")
    print("_"*40)

    entrada = input("Escolha uma das opções acima, ex: 1,2,3,4,5 ou 6: ").strip().lower()

    if entrada == "":
        print("Entrada não pode ser vazia!")
        input("Aperta ENTER ")
        continue

    # 1. ADICIONAR PRODUTO
    if entrada == "1" or entrada == "adicionar_produto":
        while True:
            limpar_tela()
            nome = input("Adicionar produto: ").strip().replace(",","")
            if nome == "":
                print("Entrada não pode ser vazia")
                input("Aperta ENTER ")
                continue

            qtd = input("Adicionar quantidade: ").strip()
            if qtd == "":
                print("entrada não pode ser vazia!")
                input("Aperta ENTER ")
                continue

            quant = input("kilos, unidade, caixa, fardo ou qualquer outra especificação: ").strip()
            if quant == "":
                print("Não pode ser vazio")
                input("Aperta ENTER ")
                continue

            while True:
                valor_str = input("Qual é o valor do produto: R$ ").strip()
                if valor_str == "":
                    print("Entrada não pode ser vazio")
                    continue
                numero = ""
                for letra in valor_str:
                    if letra.isdigit() or letra in ".,-":
                        numero += letra
                if "," in numero and "." in numero:
                    numero = numero.replace(".","")
                numero = numero.replace(",",".")
                try:
                    preco = float(numero)
                    if preco <= 0:
                        print("Entrada não pode ser 0 ou negativo!")
                        continue
                    break
                except ValueError:
                    print("Erro, entrada inválida!\nNão aceita número por extenso!")
                    continue

            estoque.append([nome, float(qtd), quant, preco])
            salvar_estoque()
            print(f"\nproduto cadastrado com sucesso!")

            if not perguntar_novamente("cadastrar"):
                break

    # 2. CHECAR PRODUTO
    elif entrada == "2" or entrada == "checar_produto":
        while True:
            limpar_tela()
            op = input("Checa estoque ou 'n' pra sair: ").strip().lower()
            if op == "n":
                break
            achou = False
            for p in estoque:
                if p[0].lower() == op:
                    print("="*40)
                    print(f"Achei : produto {p[0]} | quantidade {p[1]} {p[2]} | R$ {p[3]:.2f} |")
                    print("="*40)
                    achou = True
                    break
            if not achou:
                print("produto não cadastrado.")

            input("Aperta ENTER ")
            if not perguntar_novamente("checar"):
                break

    # 3. VER ESTOQUE
    elif entrada == "3" or entrada == "ver_estoque":
        while True:
            limpar_tela()
            ver_stq = input("Digite '1' para ver estoque completo: ").strip()
            if ver_stq == "1":
                print("========= estoque completo =============")
                if len(estoque) == 0:
                    print("Estoque vazio!")
                for item in estoque:
                    print(f"Produto : {item[0]}\nQuantidade : {item[1]} {item[2]}\nPreço : R$ {item[3]:.2f}")
                    print("="*40)
            else:
                print("Opção inválida")

            if not perguntar_novamente("ver estoque"):
                break

    # 4. DELETAR PRODUTO
    elif entrada == "4" or entrada == "deletar_produto":
        while True:
            limpar_tela()
            print("============= ESTOQUE ATUAL ============")
            if len(estoque) == 0:
                print("Estoque vazio!")
                input("Aperta ENTER ")
                break
            for a in estoque:
                print(f"|produto : {a[0]}\nquantidade : {a[1]} {a[2]}\npreço : R$ {a[3]:.2f}")
                print("-"*40)

            dlt = input("Deleta produto no estoque 'n' pra sair : ").strip().lower()
            if dlt == "n":
                break

            cont = 0
            for i,itens in enumerate(estoque):
                if itens[0].lower() == dlt:
                    guarda_deletado = itens[0]
                    estoque.pop(i)
                    cont += 1
                    salvar_estoque()
                    print(f"\n[{cont}] produtos deletado!")
                    print(f"Item [{guarda_deletado}] deletado com sucesso!")
                    print("\n========== ESTOQUE ATUALIZADO ==========")
                    for x in estoque:
                        print(f"|produto {x[0]}|quantidade {x[1]} {x[2]}|preço R$ {x[3]:.2f}|")
                    break
            else:
                print("Item produto não encontrado!")

            input("Aperta ENTER ")
            if not perguntar_novamente("deletar"):
                break

    # 5. LINK APP
    elif entrada == "5" or entrada == "app.web":
        limpar_tela()
        print("")
        print("########################################")
        print(" LINK DO MEU APP PRA COPIAR:")
        print(LINK_APP)
        print(" Segura em cima > Abrir link")
        print("########################################")
        print("")
        # volta direto pro menu sem perguntar

    # 6. SAIR
    elif entrada == "6" or entrada == "sair":
        salvar_estoque()
        print("tchau, volte sempre!")
        break

    else:
        print("Entrada inválida!")
        print("opçao de entrada:[1 ou adicionar_produto],[2 ou checar_produto],[3 ou ver_estoque],[4 ou deletar_produto],[5 ou app.web],[6 ou sair]")
        input("Aperta ENTER ")
