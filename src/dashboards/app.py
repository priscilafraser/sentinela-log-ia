from pathlib import Path
import sys

# Ajustando o PYTHONPATH
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]   # .../sentinela-log-ia/
SRC_DIR = PROJECT_ROOT / "src"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

#############################

import streamlit as st
import pandas as pd
import joblib
import json
from pathlib import Path

from ingestaoLogs.carregar_logs import carregar_logs_df
from preprocessamento.features import engenharia_features


# Mapeia o score de risco para um nível de severidade
def classificar_severidade(score: float) -> str:

    if score >= 0.70:
        return "Crítico 🔴"
    elif score >= 0.66:
        return "Alto 🟠"
    elif score >= 0.60:
        return "Médio 🟡"
    else:
        return "Baixo 🟢"


st.title("🔐 SentinelaLogIA")
st.markdown("### Detecção de Anomalias em Logs")
st.markdown("---")

upload_file = st.file_uploader("Envie um arquivo de log", type=["log", "txt"])

if upload_file is not None:
    path_temp = Path("data/arquivo_upload.log")
    path_temp.write_bytes(upload_file.read())

    df_logs = carregar_logs_df(str(path_temp))
    st.subheader("Prévia dos logs")
    st.dataframe(df_logs.head())

    modelo = joblib.load("modelos/sentinela_modelo.pkl")
    scaler = joblib.load("modelos/sentinela_scaler.pkl")
    feature_cols = json.load(open("modelos/feature_columns.json"))

    X = engenharia_features(df_logs)[feature_cols]
    X_scaled = scaler.transform(X)

    scores = modelo.score_samples(X_scaled)
    preds = modelo.predict(X_scaled)

    df_logs['anomalia'] = (preds == -1)
    df_logs['score_risco'] = -scores

    # nova coluna de severidade baseada no score
    df_logs['severidade'] = df_logs['score_risco'].apply(classificar_severidade)
    ###################################
    
    #st.subheader("Eventos suspeitos")
    suspeitos = df_logs[df_logs['anomalia']].sort_values('score_risco', ascending=False)

    #Cards com contagem de cada nível de severidade
    st.subheader("Resumo de severidade")

    total_suspeitos = len(suspeitos)
    criticos = (suspeitos['severidade'] == "Crítico 🔴").sum()
    altos = (suspeitos['severidade'] == "Alto 🟠").sum()
    medios = (suspeitos['severidade'] == "Médio 🟡").sum()
    baixos = (suspeitos['severidade'] == "Baixo 🟢").sum()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total suspeitos", total_suspeitos)
    col2.metric("Críticos 🔴", criticos)
    col3.metric("Altos 🟠", altos)
    col4.metric("Médios 🟡", medios)
    col5.metric("Baixos 🟢", baixos)

    st.dataframe(suspeitos)

    
