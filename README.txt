
# Controle Financeiro com Google Sheets + Streamlit Cloud

Este app agora usa `secrets.toml` para armazenar suas credenciais do Google de forma segura no Streamlit Cloud.

## Como usar

1. Crie a planilha no Google Sheets chamada **"Controle Financeiro Estúdio"**
   - Colunas obrigatórias: Data | Tipo | Descrição | Pagamento | Valor
   - Compartilhe com o e-mail da conta de serviço do seu JSON

2. No seu projeto Streamlit Cloud:
   - Vá em **Settings > Secrets**
   - Cole o conteúdo do `credentials.json` assim:

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
...

⚠️ Atenção: **as quebras de linha do `private_key` precisam ser \n, não reais**

3. Rode o app com `streamlit run app.py` localmente ou publique no Streamlit Cloud

## Requisitos
pip install streamlit gspread oauth2client pandas
