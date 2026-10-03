from flask import Flask, render_template

app = Flask(__name__)

PROFILE = {
    "name": "Mateus Sipaúba",
    "role": "Desenvolvedor de Software",
    "headline": "Transformo ideias em soluções digitais úteis.",
    "intro": "Sou desenvolvedor de software e gosto de criar produtos digitais simples, bem pensados e preparados para crescer. Aqui compartilho um pouco da minha trajetória e dos projetos que venho construindo.",
    "location": "Brasil",
    "email": "seu-email@exemplo.com",
    "github": "https://github.com/SEU-USUARIO",
    "linkedin": "https://www.linkedin.com/in/SEU-PERFIL",
}

EXPERIENCE = [
    {"period": "2023 — atual", "role": "Seu cargo atual", "company": "Nome da empresa", "description": "Conte em uma ou duas frases o que você faz, com quem trabalha e qual impacto gera.", "tags": ["Python", "Flask", "PostgreSQL"]},
    {"period": "2021 — 2023", "role": "Cargo anterior", "company": "Nome da empresa", "description": "Destaque uma responsabilidade importante ou uma entrega de que você se orgulha.", "tags": ["Desenvolvimento", "Colaboração"]},
]

PROJECTS = [
    {"number": "01", "name": "Relatório Follow Up de Compras", "description": "Aplicativo desktop que acompanha pedidos de compra no WinThor, consulta dados do Oracle e exporta relatórios formatados para Excel.", "stack": ["Python", "Tkinter", "Oracle", "Excel"], "url": "https://github.com/Sipauba/relatorio-setor-compras", "kind": "Automação · Compras"},
]


@app.get("/")
def home():
    return render_template("index.html", profile=PROFILE, experience=EXPERIENCE, projects=PROJECTS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
