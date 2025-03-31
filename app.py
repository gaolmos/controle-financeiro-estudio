
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

# Diagnóstico: listar planilhas visíveis
st.subheader("🔍 Diagnóstico de acesso ao Google Sheets")
try:
    sheets_list = client.openall()
    st.success("Autenticação bem-sucedida ✅")
    st.write("Planilhas disponíveis:")
    for s in sheets_list:
        st.write(f"📄 {s.title}")
except Exception as e:
    st.error("❌ Erro ao acessar as planilhas")
    st.exception(e)

# Tentar abrir a planilha esperada
st.subheader("📂 Tentando abrir: Controle Financeiro Estúdio")
try:
    sheet_name = "Controle Financeiro Estúdio"
    sheet = client.open(sheet_name).sheet1
    dados = pd.DataFrame(sheet.get_all_records())
    st.success("Planilha aberta com sucesso ✅")
    st.dataframe(dados)
except Exception as e:
    st.error("❌ Não foi possível abrir a planilha")
    st.exception(e)
