import streamlit as st
import json
import os

ARQUIVO = "estoque.json"

# Carregar estoque
def carregar_estoque():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Salvar estoque
def salvar_estoque(estoque):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(estoque, f, ensure_ascii=False, indent=4)

# Função pra limpar numero igual no teu código
def limpar_numero(texto):
    numero = ""
    for letra in texto:
        if letra.isdigit() or letra in ".,-":
            numero += letra
    if "," in numero and "." in numero:
        numero = numero.replace(".","")
        numero = numero.replace(",",".")
    elif "," in numero:
        numero = numero.replace(",",".")
    return numero

st.set_page_config(page_title="Sistema de Estoque", layout="centered")

st.title("ALEX S.BORGES.LTDA")
st.title("______Menu estoque______")
st.write("_"*40)

estoque = carregar_estoque()

menu = st.radio(
    "Escolha uma opção:",
    ["1. Adicionar Produto", "2. Checar Produto", "3. Ver Estoque", "4. Deletar Produto", "5. Sair"]
)

# 1. ADICIONAR PRODUTO
if menu.startswith("1"):
    st.subheader("➕ Adicionar Produto")
    with st.form("form_add", clear_on_submit=True): # <- só adicionei isso aqui
        nome = st.text_input("Nome do produto").strip().replace(",","")
        qtd = st.text_input("Quantidade")
        quant = st.text_input("Especificação: kilos, unidade, caixa, fardo...")
        valor_str = st.text_input("Valor do produto").replace(",",".") # <- tratei a vírgula
        
        submitted = st.form_submit_button("Cadastrar")

        if submitted: # <- mudei pra dentro do form
            try:
                preco_float = float(valor_str)
                preco = f"R$ {preco_float:.2f}"
                
                estoque.append([nome, preco_float, quant, preco])
                salvar_estoque(estoque)
                st.success(f"Produto '{nome}' cadastrado com sucesso!")
                st.rerun() # <- isso aqui faz limpar e perguntar de novo
                
            except ValueError:
                st.error("Valor inválido. Use apenas números. Ex: 10.50")

        if submitted:
            if not nome or not qtd or not quant or not valor_str:
                st.error("Nenhum campo pode ser vazio!")
            else:
                try:
                    numero_qtd = limpar_numero(qtd)
                    preco_float = float(numero_qtd)
                    if preco_float <= 0:
                        st.error("Quantidade não pode ser 0 ou negativo!")
                        
                    else:
                        numero_valor = limpar_numero(valor_str)
                        preco = float(numero_valor)

                        estoque.append([nome, preco_float, quant, preco])
                        salvar_estoque(estoque)
                        st.success(f"Produto '{nome}' cadastrado com sucesso!")
                        st.rerun()
                except ValueError:
                    st.error("Erro: Entrada inválida! Não aceita número por extenso!")

# 2. CHECAR PRODUTO
elif menu.startswith("2"): # 2. CHECAR PRODUTO
    st.subheader("🔍 Checar Produto")

    with st.form("form_checar", clear_on_submit=True):
        checar = st.text_input("Digite o nome do produto pra checar").strip().replace(",","")
        buscar = st.form_submit_button("Pesquisar")

        if buscar:
            if not checar:
                st.warning("Digite um nome para pesquisar")
            else:
                achou = False
                for p in estoque:
                    if p[0].lower() == checar.lower():
                        st.success(f"Achei: Produto {p[0]} | Quantidade {p[1]:.2f} {p[2]} | R$ {p[3]:.2f}")
                        achou = True
                        break

                if not achou:
                    st.warning("Produto não cadastrado.")

                st.rerun() # <- limpa e já fica pronto pra pesquisar outro        

# 3. VER ESTOQUE
elif menu.startswith("3"): # 3. VER ESTOQUE
    st.subheader("📋 Estoque Completo")

    if not estoque:
        st.warning("Estoque vazio! Cadastre um produto primeiro.")
    else:
        st.write(f"**Total de produtos:** {len(estoque)}")
        for item in estoque:
            st.write("="*40)
            st.write(f"**Produto:** {item[0]}")
            st.write(f"**Quantidade:** {item[1]:.2f} {item[2]}")
            st.write(f"**Preço:** R$ {item[3]}")
            st.write("="*40)

# 4. DELETAR PRODUTO
elif menu.startswith("4"): # 4. DELETAR PRODUTO
    st.subheader("🗑️ Deletar Produto")

    if not estoque:
        st.warning("Estoque vazio!")
    else:
        st.write("============= ESTOQUE ATUAL ============")
        for a in estoque:
            st.write(f"- {a[0]} | Qtd: {a[1]:.2f} {a[2]} | Valor: R$ {a[3]}")
        st.write("=========================================")

        with st.form("form_delete", clear_on_submit=True):
            # Faz a lista pra tu escolher em vez de digitar
            nomes_produtos = [item[0] for item in estoque]
            produto_deletar = st.selectbox("Escolha o produto para deletar:", nomes_produtos)
            confirmar = st.form_submit_button("Deletar")

            if confirmar:
                # Deleta o produto escolhido
                estoque[:] = [item for item in estoque if item[0]!= produto_deletar]
                salvar_estoque(estoque)
                st.success(f"Item '{produto_deletar}' deletado com sucesso!")
                st.rerun() # <- atualiza a lista e já fica pronto pra deletar outro

    st.write("========== ESTOQUE ATUALIZADO ==========")
    for x in estoque:
        st.write(f"| produto {x[0]} | quantidade {x[1]:.2f} {x[2]} | preço R$ {x[3]} |")

# 5. SAIR
elif menu.startswith("5"):
    st.subheader("👋 Tchau, volte sempre!")
