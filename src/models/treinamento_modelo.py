from pathlib import Path
import joblib
import json
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from src.ingestaoLogs.carregar_logs import carregar_logs_df
from src.preprocessamento.features import engenharia_features


def treinamento_isolation_forest(X):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=200,
        contamination=0.15,
        random_state=42
    )
    model.fit(X_scaled)

    return model, scaler


if __name__ == "__main__":
    df_logs = carregar_logs_df("data/dados_brutos_log/access.log")
    X = engenharia_features(df_logs)

    model, scaler = treinamento_isolation_forest(X)

    Path("modelos").mkdir(exist_ok=True)

    joblib.dump(model, "modelos/sentinela_modelo.pkl")
    joblib.dump(scaler, "modelos/sentinela_scaler.pkl")

    with open("modelos/feature_columns.json", "w") as f:
        json.dump(list(X.columns), f, indent=2)

    print("Modelo treinado e salvo!")
