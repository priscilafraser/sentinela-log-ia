import random
from datetime import datetime, timedelta
from pathlib import Path

NORMAL_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
]

ATTACK_USER_AGENTS = [
    "sqlmap/1.5.2#stable",
    "curl/7.68.0",
    "Mozilla/5.0 (compatible; Nmap Scripting Engine; http-enum)",
]

NORMAL_PATHS = ["/", "/produtos", "/contato", "/sobre", "/blog", "/blog/post1", "/assets/style.css", "/assets/app.js"]
ATTACK_PATHS = [
    "/login",
    "/wp-admin",
    "/wp-login.php",
    "/phpmyadmin",
    "/admin",
    "/../../../../etc/passwd",
    "/../etc/passwd",
    "/produtos?id=1%20OR%201=1",
    "/login?user=admin'%20OR%20'1'='1",
]

def random_ip(prefixo="192.168.0."):
    return prefixo + str(random.randint(1, 254))

def random_ataque_ip():
    return f"10.0.0.{random.randint(50, 200)}"

def formato_time(tempo_base, ajuste_segundos):
    t = tempo_base + timedelta(seconds=ajuste_segundos)
    return t.strftime("%d/%b/%Y:%H:%M:%S -0300")

def gerar_logs(n_normal=500, n_ataque=80, path_saida="data/dados_brutos_log/access.log"):
    tempo_base = datetime(2025, 11, 10, 14, 0, 0)
    linhas = []

    # acessos normais
    for i in range(n_normal):
        ip = random_ip()
        path = random.choice(NORMAL_PATHS)
        status = 200
        size = random.randint(2000, 8000)
        ua = random.choice(NORMAL_USER_AGENTS)
        ts = formato_time(tempo_base, i)
        line = f'{ip} - - [{ts}] "GET {path} HTTP/1.1" {status} {size} "-" "{ua}"'
        linhas.append(line)

    # ataques
    for i in range(n_ataque):
        ip = random_ataque_ip()
        path = random.choice(ATTACK_PATHS)

        if "login" in path and "?" not in path:
            method = "POST"
        else:
            method = "GET"

        if "etc/passwd" in path or "OR" in path or "admin" in path or "php" in path:
            status = random.choice([403, 404, 500])
        else:
            status = random.choice([401, 403, 404])

        size = random.randint(200, 1500)
        ua = random.choice(ATTACK_USER_AGENTS)
        ts = formato_time(tempo_base, n_normal + i)

        line = f'{ip} - - [{ts}] "{method} {path} HTTP/1.1" {status} {size} "-" "{ua}"'
        linhas.append(line)

    random.shuffle(linhas)
    arq_saida = Path(path_saida)
    arq_saida.parent.mkdir(parents=True, exist_ok=True)
    arq_saida.write_text("\n".join(linhas), encoding="utf-8")
    print(f"Gerado {len(linhas)} linhas em {arq_saida}")

if __name__ == "__main__":
    gerar_logs()
