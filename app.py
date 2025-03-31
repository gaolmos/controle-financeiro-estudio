
import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Lê as credenciais do Streamlit Secrets
creds_dict = dict(st.secrets["gcp_service_account"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)


# Nome da planilha
sheet_name = "Controle Financeiro Estúdio"
sheet = client.open(sheet_name).sheet1

# Página
st.set_page_config(page_title="Controle Financeiro", layout="centered")
st.title("Controle Financeiro - Estúdio de Tatuagem")

# Formulário
with st.form("nova_movimentacao"):
    data = st.date_input("Data", value=datetime.today())
    tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
    descricao = st.text_input("Descrição")
    pagamento = st.selectbox("Forma de Pagamento", ["Pix", "Cartão", "Dinheiro"])
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    submit = st.form_submit_button("Adicionar")

    if submit:
        nova_linha = [str(data), tipo, descricao, pagamento, valor]
        sheet.append_row(nova_linha)
        st.success("Movimentação registrada com sucesso!")

# Carregar dados
dados = pd.DataFrame(sheet.get_all_records())
st.subheader("Histórico")
st.dataframe(dados)

# Resumo
entradas = dados[dados["Tipo"] == "Entrada"]["Valor"].sum()
saidas = dados[dados["Tipo"] == "Saída"]["Valor"].sum()
saldo = entradas - saidas

st.subheader("Resumo")
st.metric("Entradas", f"R$ {entradas:.2f}")
st.metric("Saídas", f"R$ {saidas:.2f}")
st.metric("Saldo Atual", f"R$ {saldo:.2f}")
