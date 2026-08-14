import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Sistema de Estoque", layout="centered")
ARQUIVO = "estoque.csv"

# Carrega os dados
if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO)
else:
    df = pd.DataFrame(columns=["ID", "Produto", "Preço", "Qtd"])

def salvar():
    df.to_csv(ARQUIVO, index=False)

# Controle de tela pra "limpar"
if 'tela' not in st.session_state:
    st.session_state.tela = "menu"

# ========== CABEÇALHO FIXO ==========
st.title("========== SISTEMA DE ESTOQUE ==========")
st.subheader("ALEX S.BORGES.LTDA") # <- TEU NOME E EMPRESA AQUI
st.write("Meu Estoque")
st.divider()

# ========== MENU PRINCIPAL ==========
if st.session_state.tela == "menu":
    st.write("### MENU PRINCIPAL")

    if st.button("1. Cadastrar Produto", use_container_width=True):
        st.session_state.tela = "cadastrar"; st.rerun()
    if st.button("2. Listar Produtos", use_container_width=True):
        st.session_state.tela = "listar"; st.rerun()
    if st.button("3. Editar Produto", use_container_width=True):
        st.session_state.tela = "editar"; st.rerun()
    if st.button("4. Excluir Produto", use_container_width=True):
        st.session_state.tela = "excluir"; st.rerun()
    if st.button("5. Vender Produto", use_container_width=True):
        st.session_state.tela = "vender"; st.rerun()
    if st.button("6. Relatório", use_container_width=True):
        st.session_state.tela = "relatorio"; st.rerun()
    if st.button("7. Sair", use_container_width=True):
        st.write("Saindo...")

# ========== 1. CADASTRAR ==========
elif st.session_state.tela == "cadastrar":
    st.title("========== CADASTRAR PRODUTO ==========")
    nome = st.text_input("Digite o nome do produto:")
    preco = st.number_input("Digite o preço:", min_value=0.0, format="%.2f")
    qtd = st.number_input("Digite a quantidade:", min_value=0, step=1)

    if st.button("Salvar"):
        novo_id = 1 if df.empty else df["ID"].max() + 1
        df.loc[len(df)] = [novo_id, nome, preco, qtd]
        salvar()
        st.success("Produto cadastrado com sucesso!")
        st.session_state.tela = "menu"; st.rerun()

    if st.button("Voltar ao Menu"):
        st.session_state.tela = "menu"; st.rerun()

# ========== 2. LISTAR ==========
elif st.session_state.tela == "listar":
    st.title("========== LISTA DE PRODUTOS ==========")
    st.dataframe(df, use_container_width=True)
    if st.button("Voltar ao Menu"):
        st.session_state.tela = "menu"; st.rerun()

# ========== 3. EDITAR ==========
elif st.session_state.tela == "editar":
    st.title("========== EDITAR PRODUTO ==========")
    if not df.empty:
        id_edit = st.selectbox("Digite o ID do produto:", df["ID"])
        novo_nome = st.text_input("Novo nome:")
        novo_preco = st.number_input("Novo preço:", min_value=0.0, format="%.2f")
        nova_qtd = st.number_input("Nova quantidade:", min_value=0, step=1)
        if st.button("Salvar Alterações"):
            idx = df[df["ID"] == id_edit].index[0]
            df.loc[idx] = [id_edit, novo_nome, novo_preco, nova_qtd]
            salvar()
            st.success("Produto editado!")
            st.session_state.tela = "menu"; st.rerun()
    if st.button("Voltar ao Menu"):
        st.session_state.tela = "menu"; st.rerun()

# ========== 4. EXCLUIR ==========
elif st.session_state.tela == "excluir":
    st.title("========== EXCLUIR PRODUTO ==========")
    if not df.empty:
        id_del = st.selectbox("Digite o ID do produto:", df["ID"])
        if st.button("Confirmar Exclusão"):
            df = df[df["ID"]!= id_del]
            salvar()
            st.warning("Produto excluído!")
            st.session_state.tela = "menu"; st.rerun()
    if st.button("Voltar ao Menu"):
        st.session_state.tela = "menu"; st.rerun()

# ========== 5. VENDER ==========
elif st.session_state.tela == "vender":
    st.title("========== VENDER PRODUTO ==========")
    if not df.empty:
        produto = st.selectbox("Escolha o produto:", df["Produto"])
        qtd_venda = st.number_input("Quantidade para vender:", min_value=1, step=1)
        if st.button("Confirmar Venda"):
            idx = df[df["Produto"] == produto].index[0]
            if df.loc[idx, "Qtd"] >= qtd_venda:
                df.loc[idx, "Qtd"] -= qtd_venda
                salvar()
                st.success("Venda realizada!")
            else:
                st.error("Estoque insuficiente!")
            st.session_state.tela = "menu"; st.rerun()
    if st.button("Voltar ao Menu"):
        st.session_state.tela = "menu"; st.rerun()

# ========== 6. RELATÓRIO ==========
elif st.session_state.tela == "relatorio":
    st.title("========== RELATÓRIO ==========")
    if not df.empty:
        df["Total"] = df["Preço"] * df["Qtd"]
        st.metric("Valor Total em Estoque", f"R$ {df['Total'].sum():.2f}")
        st.dataframe(df)
    if st.button("Voltar ao Menu"):
        st.session_state.tela = "menu"; st.rerun()                
