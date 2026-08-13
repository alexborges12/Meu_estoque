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
    with st.form("form_add"):
        nome = st.text_input("Nome do produto").strip().replace(",","")
        qtd = st.text_input("Quantidade")
        quant = st.text_input("Especificação: kilos, unidade, caixa, fardo...")
        valor_str = st.text_input("Valor do produto")
        submitted = st.form_submit_button("Cadastrar")

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
                except ValueError:
                    st.error("Erro: Entrada inválida! Não aceita número por extenso!")

# 2. CHECAR PRODUTO
elif menu.startswith("2"):
    st.subheader("🔍 Checar Produto")
    op = st.text_input("Digite o nome do produto pra checar ou 'n' pra sair")
    if op and op.lower()!= "n":
        encontrado = False
        for p in estoque:
            if p[0].lower() == op.lower():
                st.success(f"Achei: Produto {p[0]} | Quantidade {p[1]:.2f} {p[2]} | R$ {p[3]:.2f}")
                encontrado = True
                break
        if not encontrado:
            st.warning("Produto não cadastrado.")

# 3. VER ESTOQUE
elif menu.startswith("3"):
    st.subheader("📋 Estoque Completo")
    if estoque:
        for item in estoque:
            st.write("="*40)
            st.write(f"**Produto:** {item[0]}")
            st.write(f"**Quantidade:** {item[1]:.2f} {item[2]}")
            st.write(f"**Preço:** R$ {item[3]:.2f}")
            st.write("="*40)
    else:
        st.info("Estoque vazio.")

# 4. DELETAR PRODUTO
elif menu.startswith("4"):
    st.subheader("🗑️ Deletar Produto")
    st.write("============= ESTOQUE ATUAL ============")
    for a in estoque:
        st.write(f"- {a[0]} | {a[1]:.2f} {a[2]} | R$ {a[3]:.2f}")

    dlt = st.text_input("Digite o nome do produto pra deletar ou 'n' pra sair")
    if dlt and dlt.lower()!= "n":
        cont = 0
        guarda_deletado = ""
        for i, itens in enumerate(estoque):
            if itens[0].lower() == dlt.lower():
                guarda_deletado = itens[0]
                estoque.pop(i)
                cont += 1
                salvar_estoque(estoque)
                st.success(f"[{cont}] produto deletado!")
                st.success(f"Item [{guarda_deletado}] deletado com sucesso!")
                break
        else:
            st.error("Item produto não encontrado!")

    st.write("========== ESTOQUE ATUALIZADO ==========")
    for x in estoque:
        st.write(f"| produto {x[0]} | quantidade {x[1]:.2f} {x[2]} | preço R$ {x[3]:.2f} |")

# 5. SAIR
elif menu.startswith("5"):
    st.subheader("👋 Tchau, volte sempre!")
