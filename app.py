from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from flask import Flask, Response, abort, redirect, render_template, request, url_for

from projects import PROJECTS

app = Flask(__name__)
SITE_URL = "https://mateus.sipauba.com.br"
ASSET_VERSIONS = {
    str(path.relative_to(app.static_folder)): sha256(path.read_bytes()).hexdigest()[:12]
    for path in Path(app.static_folder).rglob("*")
    if path.is_file()
}

PROFILE = {
    "name": "Mateus de Souza Sipaúba",
    "role": "RPA · Automation · Integration Developer",
    "location": "Fortaleza, CE",
    "email": "mateus.sipauba@yahoo.com.br",
    "github": "https://github.com/Sipauba",
    "linkedin": "https://www.linkedin.com/in/mateussipauba/",
}

AREAS = [
    (
        "01",
        "RPA & Automação",
        "Workflows e scripts para reduzir etapas manuais em processos operacionais.",
    ),
    ("02", "Integrações", "Conexão entre ERP, service desk, APIs, mensageria e bancos de dados."),
    (
        "03",
        "IA aplicada",
        "Uso de modelos de linguagem para classificação, extração e apoio a decisões.",
    ),
    (
        "04",
        "Dados & Infraestrutura",
        "Consultas, relatórios e serviços que sustentam automações confiáveis.",
    ),
]

STACK = [
    ("Desenvolvimento & automação", ["Python", "n8n", "JavaScript"]),
    ("Bancos de dados", ["SQL", "Oracle", "PostgreSQL", "MySQL", "Redis"]),
    (
        "Integrações & IA",
        [
            "REST APIs",
            "Webhooks",
            "OpenAI",
            "LLMs",
            "Prompt Engineering",
            "WhatsApp APIs",
            "Telegram API",
        ],
    ),
    ("Infraestrutura & monitoramento", ["Docker", "Linux", "Zabbix"]),
    ("Sistemas corporativos", ["GLPI", "WinThor"]),
    ("IoT", ["ESP32", "Arduino", "C++"]),
]


@app.get("/")
def home():
    return render_template(
        "index.html",
        projects=PROJECTS,
        areas=AREAS,
        stack=STACK,
        seo=metadata(
            "Mateus Sipaúba | Automação, Integrações e IA aplicada",
            "Soluções reais com Python, n8n, APIs e IA aplicada. Conheça os projetos "
            "de automação, integrações, dados e monitoramento de Mateus Sipaúba.",
            "/",
        ),
    )


def metadata(title, description, path, project=None):
    """Use the public domain, never an untrusted request Host, in metadata."""
    person = {
        "@type": "Person",
        "@id": f"{SITE_URL}/#person",
        "name": PROFILE["name"],
        "url": SITE_URL,
        "jobTitle": PROFILE["role"],
        "sameAs": [PROFILE["github"], PROFILE["linkedin"]],
    }
    page = {
        "@type": "WebPage" if project else "ProfilePage",
        "@id": SITE_URL + path,
        "url": SITE_URL + path,
        "name": title,
        "description": description,
        "inLanguage": "pt-BR",
        "mainEntity": {"@id": person["@id"]},
    }
    graph = [person, page]
    if project:
        software = {
            "@type": "SoftwareSourceCode",
            "@id": SITE_URL + path + "#project",
            "name": project["name"],
            "description": project["summary"],
            "codeRepository": project["repo"],
            "author": {"@id": person["@id"]},
            "keywords": project["stack"],
        }
        page["mainEntity"] = {"@id": software["@id"]}
        graph.extend(
            [
                software,
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Portfólio",
                            "item": SITE_URL + "/",
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": project["name"],
                            "item": SITE_URL + path,
                        },
                    ],
                },
            ]
        )
    return {
        "title": title,
        "description": description,
        "canonical": SITE_URL + path,
        "structured": {"@context": "https://schema.org", "@graph": graph},
    }


def asset(filename):
    return url_for("static", filename=filename, v=ASSET_VERSIONS.get(filename, "dev"))


@app.context_processor
def shared_context():
    return {
        "profile": PROFILE,
        "asset": asset,
        "site_url": SITE_URL,
        "year": datetime.now(timezone.utc).year,
    }


@app.after_request
def response_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self'; font-src 'self'; connect-src 'self'; "
        "object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'"
    )
    filename = (request.view_args or {}).get("filename")
    if (
        request.endpoint == "static"
        and response.status_code == 200
        and filename in ASSET_VERSIONS
        and request.args.get("v") == ASSET_VERSIONS[filename]
    ):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    elif request.endpoint == "static" and response.status_code == 200:
        response.headers["Cache-Control"] = "public, max-age=86400"
    return response


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
        related = [
            item
            for item in PROJECTS
            if item["slug"] != slug and set(item["filters"]) & set(project["filters"])
        ][:3]
        return render_template(
            "project_detail.html",
            project=project,
            related=related,
            seo=metadata(
                f"{project['name']} | Mateus Sipaúba",
                project["summary"],
                url_for("project_detail", slug=slug),
                project,
            ),
        )
    repo = LEGACY_PROJECTS.get(slug)
    if repo is not None:
        return redirect(repo, code=302)
    abort(404)


@app.get("/sitemap.xml")
def sitemap():
    paths = ["/"] + [url_for("project_detail", slug=p["slug"]) for p in PROJECTS]
    return Response(render_template("sitemap.xml", paths=paths), mimetype="application/xml")


@app.get("/robots.txt")
def robots():
    return Response(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", mimetype="text/plain"
    )


@app.get("/favicon.ico")
def favicon():
    return redirect(asset("favicon.ico"), code=302)


@app.errorhandler(404)
def not_found(error):
    return render_template(
        "404.html",
        seo=metadata(
            "Página não encontrada | Mateus Sipaúba",
            "Explore os projetos de automação e integração de Mateus Sipaúba.",
            "/",
        ),
        noindex=True,
    ), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
