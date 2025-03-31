
import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Autenticar com Google via secrets
creds_dict = dict(st.secrets["gcp_service_account"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Nome da planilha
sheet_name = "Controle Financeiro Estúdio"
sheet = client.open(sheet_name).sheet1

# Verificar se a primeira linha tem os cabeçalhos corretos
HEADERS = ["Data", "Tipo", "Descrição", "Pagamento", "Valor"]
first_row = sheet.row_values(1)
if first_row != HEADERS:
    sheet.clear()
    sheet.append_row(HEADERS)

# Carregar os dados
dados = pd.DataFrame(sheet.get_all_records())

st.set_page_config(page_title="Controle Financeiro", layout="centered")
st.title("💸 Controle Financeiro - Estúdio de Tatuagem")

# Formulário
st.subheader("📥 Registrar movimentação")
with st.form("nova_movimentacao"):
    data = st.date_input("Data", value=datetime.today())
    tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
    descricao = st.text_input("Descrição")
    pagamento = st.selectbox("Forma de Pagamento", ["Pix", "Cartão", "Dinheiro"])
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    enviar = st.form_submit_button("Adicionar")

    if enviar:
        nova_linha = [str(data), tipo, descricao, pagamento, valor]
        sheet.append_row(nova_linha)
        st.success("Movimentação registrada com sucesso! ✅")

# Mostrar colunas carregadas (debug)
st.write("🧾 Colunas reconhecidas:", dados.columns.tolist())

# Tabela de dados
st.subheader("📜 Histórico de movimentações")
st.dataframe(dados)

# Resumo
st.subheader("📊 Resumo")
entradas = dados[dados["Tipo"] == "Entrada"]["Valor"].sum()
saidas = dados[dados["Tipo"] == "Saída"]["Valor"].sum()
saldo = entradas - saidas

col1, col2, col3 = st.columns(3)
col1.metric("Entradas", f"R$ {entradas:.2f}")
col2.metric("Saídas", f"R$ {saidas:.2f}")
col3.metric("Saldo Atual", f"R$ {saldo:.2f}")
