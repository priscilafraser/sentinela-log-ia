import re
import pandas as pd
from pathlib import Path

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) (?P<bytes>\S+) '
    r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

def extrair_dados_log(linha: str):
    resultado_regex = LOG_PATTERN.match(linha)
    if resultado_regex:
        return resultado_regex.groupdict()
    return None

def carregar_logs_df(log_path: str) -> pd.DataFrame:
    log_file = Path(log_path)
    registros = []

    with log_file.open('r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            resultado = extrair_dados_log(linha.strip())
            if resultado:
                registros.append(resultado)

    df = pd.DataFrame(registros)

    if not df.empty:
        df['status'] = df['status'].astype(int)
        df['bytes'] = df['bytes'].replace('-', 0).astype(int)

    return df
