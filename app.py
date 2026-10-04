from flask import Flask, render_template

app = Flask(__name__)

PROFILE = {
    "name": "Mateus de Souza Sipaúba",
    "role": "Analista de Sistemas",
    "headline": "Tecnologia que simplifica processos.",
    "intro": "Atuo com suporte e administração do ERP WinThor, consultas Oracle com SQL, automação de processos em Python e gestão de infraestrutura. Também desenvolvo integrações, chatbots e agentes de IA para resolver necessidades do dia a dia.",
    "location": "Fortaleza — CE",
    "email": "mateus.sipauba@yahoo.com.br",
    "phone": "+5585985690139",
    "github": "https://github.com/Sipauba",
    "linkedin": "https://www.linkedin.com/in/mateussipauba/",
}

EXPERIENCE = [
    {"period": "05/2022 — atual", "role": "Analista de Sistemas", "company": "SODINE · Fortaleza, CE", "description": "Atendimento e administração do ERP WinThor e da plataforma GLPI; gestão de Active Directory, VPS, contêineres Docker, monitoramento Zabbix, inventário OCS e regras de firewall pfSense. Crio consultas e relatórios em Oracle/SQL, automações em Python, integrações N8N e chatbots e agentes de IA.", "tags": ["WinThor", "Oracle", "SQL", "Python", "Docker", "N8N"]},
    {"period": "09/2021 — 05/2022", "role": "Estagiário de Suporte de TI", "company": "SODINE · Fortaleza, CE", "description": "Suporte remoto e presencial aos usuários, manutenção de hardware e software, configuração de ramais e e-mails e requisição de materiais e serviços.", "tags": ["Suporte", "Windows", "Hardware"]},
]

EDUCATION = [
    {"period": "08/2023 — cursando", "course": "Análise e Desenvolvimento de Sistemas", "institution": "Uniateneu · previsão de conclusão: 01/2027"},
]

SKILL_GROUPS = [
    {"name": "Linguagens e dados", "items": ["Python", "JavaScript", "C++", "Oracle", "MySQL", "SQL Server", "SQL"]},
    {"name": "Infraestrutura", "items": ["Windows", "Linux", "Docker", "VPS", "Zabbix", "pfSense", "Active Directory", "OCS Inventory"]},
    {"name": "Automação e integrações", "items": ["N8N", "Supabase", "APIs REST", "Webhooks", "GLPI", "Chatbots", "Agentes de IA"]},
    {"name": "Métodos e qualidade", "items": ["Scrum", "Kanban", "5S", "5W2H", "PDCA", "Diagrama de Ishikawa"]},
    {"name": "Ferramentas", "items": ["Git"]},
]

PROJECTS = [
    {"number": "01", "name": "Automação do giro diário", "description": "Automatização de tarefas relacionadas à atualização do giro diário usando Python e banco de dados Oracle.", "stack": ["Python", "Oracle", "SQL"], "url": "https://github.com/Sipauba/bot_atualiza_giro_dia", "kind": "Automação · Dados"},
    {"number": "02", "name": "Relatório Follow Up de Compras", "description": "Aplicativo desktop que acompanha pedidos de compra no WinThor, consulta dados do Oracle e exporta relatórios formatados para Excel.", "stack": ["Python", "Tkinter", "Oracle", "Excel"], "url": "https://github.com/Sipauba/relatorio-setor-compras", "kind": "Automação · Compras"},
    {"number": "03", "name": "Automação do SPED contábil", "description": "Projeto de automação de tarefas relacionadas a arquivos TXT do SPED contábil.", "stack": ["Python", "Automação", "SPED"], "url": "https://github.com/Sipauba/automacao_txt_sped_contabil", "kind": "Automação · Contábil"},
]


@app.get("/")
def home():
    return render_template("index.html", profile=PROFILE, experience=EXPERIENCE, education=EDUCATION, skill_groups=SKILL_GROUPS, projects=PROJECTS, languages=["Inglês intermediário"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
