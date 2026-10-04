from flask import Flask, abort, redirect, render_template

from projects import PROJECTS

app = Flask(__name__)

PROFILE = {
    "name": "Mateus de Souza Sipaúba",
    "role": "RPA · Automation · Integration Developer",
    "location": "Fortaleza, CE",
    "email": "mateus.sipauba@yahoo.com.br",
    "github": "https://github.com/Sipauba",
    "linkedin": "https://www.linkedin.com/in/mateussipauba/",
}

AREAS = [
    ("01", "RPA & Automação", "Workflows e scripts para reduzir etapas manuais em processos operacionais."),
    ("02", "Integrações", "Conexão entre ERP, service desk, APIs, mensageria e bancos de dados."),
    ("03", "IA aplicada", "Uso de modelos de linguagem para classificação, extração e apoio a decisões."),
    ("04", "Dados & Infraestrutura", "Consultas, relatórios e serviços que sustentam automações confiáveis."),
]

STACK = [
    ("Automação", ["n8n", "Python", "JavaScript", "Webhooks"]),
    ("IA", ["OpenAI", "LLMs", "Prompt Engineering"]),
    ("Dados", ["Oracle", "MySQL", "PostgreSQL", "Redis"]),
    ("Integrações", ["REST APIs", "WhatsApp APIs", "Telegram API"]),
    ("Sistemas & Infra", ["GLPI", "WinThor", "Docker", "Linux"]),
    ("IoT", ["ESP32", "Arduino", "C++"]),
]


@app.get("/")
def home():
    return render_template("index.html", profile=PROFILE, projects=PROJECTS,
                           featured=[p for p in PROJECTS if p.get("featured")],
                           areas=AREAS, stack=STACK)


# Keep links from the previous portfolio useful. Detailed documentation lives in GitHub.
LEGACY_PROJECTS = {
    "giro-diario": "https://github.com/Sipauba/bot_atualiza_giro_dia",
    "follow-up-compras": "https://github.com/Sipauba/relatorio-setor-compras",
    "automacao-sped-fiscal": "https://github.com/Sipauba/automacao_txt_sped_contabil",
}


@app.get("/projetos/<slug>")
def project_detail(slug):
    project = next((item for item in PROJECTS if item["slug"] == slug), None)
    if project is not None:
        related = [item for item in PROJECTS if item["slug"] != slug and set(item["filters"]) & set(project["filters"])][:3]
        return render_template("project_detail.html", project=project, profile=PROFILE, related=related)
    repo = LEGACY_PROJECTS.get(slug)
    if repo is not None:
        return redirect(repo, code=302)
    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
