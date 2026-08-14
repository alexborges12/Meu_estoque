import streamlit as st
import json
import os

st.set_page_config(page_title="Meu Estoque", layout="centered")

LINK_APP = "https://meuestoque-c5rebryzdwvgtobe5shzw2.streamlit.app/"

# Carregar estoque
ARQUIVO = "estoque.json"
if "estoque" not in st.session_state:
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            st.session_state.estoque = json.load(f)
    else:
        st.session_state.estoque = []

def salvar_estoque():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(st.session_state.estoque, f, ensure_ascii=False, indent=4)

st.markdown("<h1 style='text-align: center;'>ALEX A.BORGES.LTDA</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>___________Meu estoque___________</h3>", unsafe_allow_html=True)
st.divider()

menu = st.radio(
    "Escolha uma das opções acima, ex: 1,2,3,4 ou 5:",
    ["1 - adcionar_produto", "2 - checar_produto", "3 - ver_estoque", "4 - deleta_produto", "5 - sair"],
    key="menu_opcao"
)

# 1 - ADICIONAR PRODUTO
if menu.startswith("1"):
    st.subheader("Adicionar produto")
    with st.form("form_add", clear_on_submit=True): # clear_on_submit limpa tudo ao enviar
        nome = st.text_input("Adicionar produto:").strip().replace(",", "")
        qtd = st.text_input("Adicionar quantidade:")
        quant = st.text_input("kilos, unidade, caixa, fardo ou qualquer outra especificação:")
        valor_str = st.text_input("Qual é o valor do produto:")
        opc = st.radio("Deseja cadastrar mais produto?", ["sim", "nao"], horizontal=True)
        enviar = st.form_submit_button("Cadastrar")

    if enviar:
        if nome == "" or qtd == "" or quant.strip().lower() == "" or valor_str == "":
            st.error("Entrada não pode ser vazia!")
        else:
            # trata quantidade
            numero_qtd = ""
            for letra in qtd:
                if letra.isdigit() or letra in ".,-":
                    numero_qtd += letra
            numero_qtd = numero_qtd.replace(".", "").replace(",", ".")
            try:
                preco_float = float(numero_qtd)
                if preco_float <= 0:
                    st.error("Entrada não pode ser 0 ou negativo!")
                    st.stop()
            except ValueError:
                st.error("Erro: entrada inválida! Não aceita número por extenso!")
                st.stop()

            # trata valor
            numero_valor = ""
            for letra in valor_str:
                if letra.isdigit() or letra in ".,-":
                    numero_valor += letra
            if "," in numero_valor and "." in numero_valor:
                numero_valor = numero_valor.replace(".", "")
            numero_valor = numero_valor.replace(",", ".")
            try:
                preco = float(numero_valor)
            except ValueError:
                st.error("Erro: entrada inválida! Não aceita número por extenso!")
                st.stop()

            st.session_state.estoque.append([nome, preco_float, quant, preco])
            salvar_estoque()
            st.success("Produto cadastrado com sucesso!")
            if opc == "nao":
                st.rerun()

# 2 - CHECAR PRODUTO
elif menu.startswith("2"):
    st.subheader("Checar produto")
    op = st.text_input("Checa estoque ou 'n' pra sair:", key="checar_input")
    if op:
        if op.strip().lower() == "n":
            st.rerun()
        encontrado = False
        for p in st.session_state.estoque:
            if p[0].strip().lower() == op.strip().lower():
                st.divider()
                st.write(f"**Achei:** produto {p[0]} | quantidade {p[1]:.2f} {p[2]} | R$ {p[3]:.2f}")
                st.divider()
                encontrado = True
                break
        if not encontrado:
            st.warning("Produto não cadastrado.")

# 3 - VER ESTOQUE
elif menu.startswith("3"):
    st.subheader("Ver estoque completo")
    ver_stq = st.text_input("Digite '1' para ver estoque completo:")
    if ver_stq.strip() == "1":
        st.divider()
        st.markdown("### ========= estoque completo =============")
        if not st.session_state.estoque:
            st.info("Estoque vazio")
        for item in st.session_state.estoque:
            st.write(f"**Produto:** {item[0]}")
            st.write(f"**Quantidade:** {item[1]:.2f} {item[2]}")
            st.write(f"**Preço:** R$ {item[3]:.2f}")
            st.divider()

# 4 - DELETAR PRODUTO
elif menu.startswith("4"):
    st.subheader("Deletar produto")
    st.markdown("### ============= ESTOQUE ATUAL ============")
    if not st.session_state.estoque:
        st.info("Estoque vazio")
    for a in st.session_state.estoque:
        st.write(f"|produto: {a[0]} | quantidade: {a[1]:.2f} {a[2]} | preço: R$ {a[3]:.2f}|")

    dlt = st.text_input("Deleta produto no estoque 'n' pra sair:", key="deleta_input")
    if dlt:
        if dlt.strip().lower() == "n":
            st.rerun()
        cont = 0
        guarda_deletado = ""
        for i, itens in enumerate(st.session_state.estoque):
            if itens[0].strip().lower() == dlt.strip().lower():
                guarda_deletado = itens[0]
                st.session_state.estoque.pop(i)
                cont += 1
                salvar_estoque()
                st.success(f"[{cont}] produto deletado!")
                st.success(f"Item [{guarda_deletado}] deletado com sucesso!")
                st.divider()
                st.markdown("### ========== ESTOQUE ATUALIZADO ==========")
                for x in st.session_state.estoque:
                    st.write(f"|produto {x[0]}|quantidade {x[1]:.2f} {x[2]}|preço R$ {x[3]:.2f}|")
                break
        else:
            st.error("Item produto não encontrado!")

# 5 - SAIR
elif menu.startswith("5"):
    st.success("tchau, volte sempre!")
