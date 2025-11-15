import pandas as pd
import numpy as np

def engenharia_features(df: pd.DataFrame) -> pd.DataFrame:
    df_feat = df.copy()

    df_feat['url_login'] = df_feat['url'].str.contains('login', case=False, na=False).astype(int)
    df_feat['url_admin'] = df_feat['url'].str.contains('admin', case=False, na=False).astype(int)
    df_feat['caminho_suspeito'] = df_feat['url'].str.contains(r'\.\./|\.(php|asp|aspx)', regex=True, na=False).astype(int)

    df_feat = pd.get_dummies(df_feat, columns=['method'], prefix='metodo')

    df_feat['erro_4xx'] = df_feat['status'].between(400, 499).astype(int)
    df_feat['erro_5xx'] = df_feat['status'].between(500, 599).astype(int)

    df_feat['bytes_log'] = np.log1p(df_feat['bytes'])

    colun_numericas = df_feat.select_dtypes(include=[np.number]).columns
    return df_feat[colun_numericas]
