
import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import altair as alt

# Config inicial do Streamlit
st.set_page_config(page_title="Controle Financeiro", layout="centered")

# Autenticação
creds_dict = dict(st.secrets["gcp_service_account"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Nome da planilha
sheet_name = "Controle Financeiro Estúdio"
sheet = client.open(sheet_name).sheet1

# Cabeçalhos padrão
HEADERS = ["Data", "Tipo", "Descrição", "Pagamento", "Valor"]
first_row = sheet.row_values(1)
if first_row != HEADERS:
    sheet.clear()
    sheet.append_row(HEADERS)

# Carregar dados
dados = pd.DataFrame(sheet.get_all_records())
dados["Data"] = pd.to_datetime(dados["Data"], errors="coerce")

st.title("💸 Controle Financeiro - Estúdio de Tatuagem")

# Filtros
st.subheader("🔎 Filtros")
with st.expander("Filtrar dados"):
    tipo_filtro = st.multiselect("Tipo", options=dados["Tipo"].unique(), default=dados["Tipo"].unique())
    pagamento_filtro = st.multiselect("Forma de Pagamento", options=dados["Pagamento"].unique(), default=dados["Pagamento"].unique())
    data_inicio = st.date_input("Data início", value=dados["Data"].min() if not dados.empty else datetime.today())
    data_fim = st.date_input("Data fim", value=dados["Data"].max() if not dados.empty else datetime.today())

# Aplicar filtros
dados_filtrados = dados[
    (dados["Tipo"].isin(tipo_filtro)) &
    (dados["Pagamento"].isin(pagamento_filtro)) &
    (dados["Data"] >= pd.to_datetime(data_inicio)) &
    (dados["Data"] <= pd.to_datetime(data_fim))
]

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

# Histórico
st.subheader("📜 Histórico de movimentações")
st.dataframe(dados_filtrados)

# Resumo
st.subheader("📊 Resumo")
if not dados_filtrados.empty and "Tipo" in dados.columns and "Valor" in dados.columns:
    entradas = dados_filtrados[dados_filtrados["Tipo"] == "Entrada"]["Valor"].sum()
    saidas = dados_filtrados[dados_filtrados["Tipo"] == "Saída"]["Valor"].sum()
    saldo = entradas - saidas

    col1, col2, col3 = st.columns(3)
    col1.metric("Entradas", f"R$ {entradas:.2f}")
    col2.metric("Saídas", f"R$ {saidas:.2f}")
    col3.metric("Saldo Atual", f"R$ {saldo:.2f}")
else:
    st.info("Sem dados suficientes para calcular o resumo.")

# Gráficos
if not dados_filtrados.empty:
    st.subheader("📈 Gráficos")

    graf_linha = alt.Chart(dados_filtrados).mark_line(point=True).encode(
        x="Data:T",
        y="Valor:Q",
        color="Tipo:N",
        tooltip=["Data", "Tipo", "Valor", "Descrição"]
    ).properties(width=700, height=300).interactive()

    st.altair_chart(graf_linha, use_container_width=True)

    graf_pizza = dados_filtrados.groupby("Tipo")["Valor"].sum().reset_index()
    st.write("Distribuição por Tipo")
    st.altair_chart(
        alt.Chart(graf_pizza).mark_arc().encode(
            theta="Valor:Q",
            color="Tipo:N",
            tooltip=["Tipo", "Valor"]
        ).properties(height=300),
        use_container_width=True
    )
