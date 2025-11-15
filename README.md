# SentinelaLogIA — Detecção Inteligente de Anomalias em Logs de Servidor

Machine Learning + Segurança Cibernética + Streamlit Dashboard

## Visão Geral

SentinelLogAI é uma ferramenta de segurança cibernética que utiliza Machine Learning (Isolation Forest) para identificar comportamentos anômalos em logs de servidor (Apache/Nginx).
O sistema analisa cada evento, calcula um Score de Risco, classifica a severidade (Crítico/Alto/Médio/Baixo) e exibe tudo em um dashboard interativo com Streamlit.

Este projeto simula a atuação de um analista de SOC (Security Operations Center), detectando:

- Directory Traversal

- SQL Injection (sqlmap)

- Força bruta em /login

- Scans de paths (curl)

- Varredura de serviços (Nmap)

- Acessos suspeitos por user-agent

- Comportamentos fora do padrão normal do servidor

O resultado é um mini-SIEM totalmente funcional para demonstração.

### Arquitetura do Projeto
````bash
sentinela-log-ia/
│
├── data/
│   ├── dados_brutos_log/
│   │   └── access.log             <-- Log de treino (normal + ataques)
│   └── arquivo_upload.log         <-- Log enviado pelo usuário no Streamlit
│
├── models/
│   ├── sentinela_modelo.pkl       <-- Modelo treinado
│   ├── sentinela_scaler.pkl       <-- Scaler (padronização)
│   └── feature_columns.json       <-- Ordem das features
│
├── src/
│   ├── ingestaoLogs/
│   │   ├── carregar_logs.py       <-- Leitura / carregamento e extração dos logs
│   │   └── gerar_logs_ataque.py   <-- Gerador de logs normais + ataques
│   │
│   ├── preprocessamento/
│   │   └── features.py            <-- Engenharia de atributos para o modelo
│   │
│   ├── models/
│   │   └── treinamento_modelo.py      <-- Treino do Isolation Forest
│   │
│   └── dashboards/
│       └── app.py                 <-- Dashboard Streamlit
│
└── README.md
````

### Fluxo Geral — Como Executar o Projeto
Para rodar o SentinelaLogIA, basta seguir os passos abaixo.

1️⃣ Preparar o ambiente

Clone o repositório e instale as dependências:
````bash
pip install -r requirements.txt
````

2️⃣ Preparar o arquivo de log para treino

O modelo precisa de um arquivo access.log contendo tráfego normal e/ou ataques simulados.

Você pode escolher:

✔️ Opção A — Usar um log real

Salve em:
````bash
data/dados_brutos_log/access.log
````

✔️ Opção B — Gerar um log automaticamente

O projeto inclui um gerador de logs com ataques simulados (Traversal, SQLi, Curl Scan, Brute Force etc.):
````bash
python -m src.ingestaoLogs.gerar_logs_ataque
````

Isso gera um log completo (normal + ataques) automaticamente. E cria automaticamente o arquivo:
````bash
data/dados_brutos_log/access.log
````

3️⃣ Treinar o modelo de Machine Learning

No terminal, na raiz do projeto, execute o script de treinamento:
````bash
python -m src.models.treinamento_modelo
````

Após finalizar, serão gerados:
````bash
modelos/sentinela_modelo.pkl
modelos/sentinela_scaler.pkl
modelos/feature_columns.json
````

O dashboard usará esses arquivos para analisar novos logs enviados pelo usuário.

4️⃣ Iniciar o Dashboard (Streamlit)

Agora basta rodar a interface de visualização:
````bash
streamlit run src/dashboards/app.py
````

A interface permite que você faça upload de qualquer arquivo .log ou .txt e receba análise em tempo real:

- Score de risco

- Classificação por severidade (Crítico/Alto/Médio/Baixo)

- Ranking ordenado de eventos suspeitos

- Cards de resumo de ataques

### Como o Score de Risco é Calculado?

O Isolation Forest fornece um score interno (score_samples) onde:

valores mais negativos → comportamento mais suspeito

valores próximos de zero → comportamento normal

Para facilitar a interpretação:
````bash
score_risco = -score_samples
````

Assim:

quanto maior o score_risco, maior o risco

facilita ordenar e visualizar no dashboard

### Classificação de Severidade

Com base no score normalizado:
| Severidade | Score     | Interpretação                                   |
| ---------- | --------- | ----------------------------------------------- |
| 🔴 Crítico | ≥ 0.70    | Ataques graves (SQLi, Traversal, scans pesados) |
| 🟠 Alto    | 0.66–0.69 | Força bruta, user-agents suspeitos              |
| 🟡 Médio   | 0.60–0.65 | Eventos fora do padrão                          |
| 🟢 Baixo   | < 0.60    | Suspeita leve / ruído normal                    |


### Exemplos de Ataques Detectados

- /../../../../etc/passwd → Directory Traversal

- /produtos?id=1 OR 1=1 → SQL Injection

- POST /login repetido → Brute Force

- /wp-admin / /phpmyadmin → Scan de paths

- User-agent sqlmap, curl, Nmap → Varredura

O modelo também prioriza eventos com:

- status HTTP incomuns (401,403,404,500)

- bytes fora do padrão

- URLs com entropia alta

- padrões raros aparecendo repentinamente

### Dashboard Interativo

O Streamlit mostra:

✔️ Cards com contagem por severidade

✔️ Filtro por severidade

✔️ Ranking ordenado por score

✔️ Prévia dos logs enviados

✔️ Tabela de eventos suspeitos

✔️ IP, URL, método, status, user-agent e score


É literalmente um mini-SIEM funcional.

### Tecnologias Utilizadas

- Python 3.11

- Pandas

- Scikit-Learn (Isolation Forest)

- Streamlit

- Joblib

- Regex (extração de logs)

### Status do Projeto

✅ Modelo treinado e funcional

✅ Dashboard pronto e interativo

✅ Para os dados utilizados detectou 100% dos ataques simulados

⚠️ Próximos passos possíveis:

- adicionar gráficos

- detecção por IP / geolocalização

- alertas por email

- logs em tempo real


### 🧑‍💻 Autor

Projeto desenvolvido para estudo e demonstração de estratégias de detecção de ameaças com Machine Learning e análise inteligente de logs, aplicando técnicas de Detecção de Anomalias e práticas de Segurança Cibernética (Blue Team).

