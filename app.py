from flask import Flask, abort, render_template

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
    {
        "number": "01", "slug": "giro-diario", "name": "Automação do giro diário",
        "description": "Rotina Python que calcula e atualiza o giro diário de produtos no Oracle, com agendamento e registro da execução.",
        "stack": ["Python", "Oracle", "SQL", "schedule"], "kind": "Automação · Dados",
        "repo": "https://github.com/Sipauba/bot_atualiza_giro_dia",
        "context": "A atualização do giro era uma tarefa recorrente do setor de compras. O projeto automatiza o cálculo com base no histórico recente de vendas e nos dias úteis, reduzindo a dependência de uma execução manual diária.",
        "approach": "O script consulta o calendário de dias úteis no Oracle, calcula uma média diária a partir dos campos de venda dos últimos períodos e atualiza QTGIRODIA na tabela de estoque PCEST para as filiais configuradas.",
        "steps": ["Consulta no Oracle a quantidade de dias úteis considerada no cálculo.", "Soma as vendas mensais disponíveis e calcula o giro com arredondamento; a versão com log trata valores nulos como zero.", "Atualiza QTGIRODIA nas filiais definidas e confirma a transação.", "A versão com log prevê um arquivo datado com horários e contagens de itens com e sem giro; no código, o agendamento está configurado para dias úteis às 07h."],
        "technical": "O cálculo e a atualização ficam em SQL; Python organiza a conexão com cx_Oracle e o agendamento com schedule. O repositório prevê Oracle Client, acesso ao banco corporativo e configuração de credenciais e filiais no ambiente de execução.",
        "note": "É uma automação de back-office conectada ao ERP, não um aplicativo web. A configuração de conexão, o calendário, as filiais e o fluxo de agendamento precisam ser conferidos no ambiente de destino antes da execução.",
    },
    {
        "number": "02", "slug": "follow-up-compras", "name": "Relatório Follow Up de Compras",
        "description": "Aplicativo desktop para filtrar pedidos do WinThor, acompanhar faturamento e entregas e exportar um relatório Excel formatado.",
        "stack": ["Python", "Tkinter", "Oracle", "Pandas", "Excel"], "kind": "Automação · Compras",
        "repo": "https://github.com/Sipauba/relatorio-setor-compras",
        "context": "O acompanhamento semanal dos pedidos exigia consultar o WinThor e copiar os registros para uma planilha, linha por linha. O README do projeto relata que essa rotina manual consumia um turno de trabalho e estava sujeita a erros de digitação.",
        "approach": "Uma interface desktop reúne filtros para filial, período de emissão, comprador, fornecedor opcional, tipo de pedido e status. A consulta consolida pedidos, fornecedores e notas para mostrar a situação de cada entrega.",
        "steps": ["Seleciona filiais, datas, compradores e os tipos e status desejados; o fornecedor pode ser informado como filtro adicional.", "Consulta os dados do Oracle e classifica pedidos como entrega total ou parcial, aguardando entrega ou aguardando faturamento.", "Exibe os resultados em uma tabela na interface.", "Exporta os dados para XLSX com colunas formatadas e cores associadas aos status de entrega."],
        "technical": "A interface é construída com Tkinter. cx_Oracle conecta ao banco WinThor; SQL combina pedidos, fornecedores e pré-entradas/notas fiscais. Pandas e openpyxl geram e formatam o arquivo Excel. O código é dividido em módulos para separar filtros, consulta, tabela e exportação.",
        "note": "A conexão descrita no repositório depende do Oracle Client e da rede/domínio interno da empresa. A página apresenta o fluxo e a solução; ela não executa consultas nem expõe dados do ERP.",
    },
    {
        "number": "03", "slug": "automacao-sped-fiscal", "name": "Automação de arquivos SPED Fiscal",
        "description": "Ferramenta desktop para atualizar registros de arquivos TXT, remover exceções por planilha e ajustar valores de ICMS-ST.",
        "stack": ["Python", "Tkinter", "OpenPyXL", "SPED Fiscal"], "kind": "Automação · Fiscal",
        "repo": "https://github.com/Sipauba/automacao_txt_sped_contabil",
        "context": "O repositório organiza tarefas repetitivas de preparação de arquivos fiscais em uma interface com três abas: atualização do TXT, remoção de exceções e alteração do valor de substituição tributária (VL ST).",
        "approach": "O aplicativo permite selecionar um TXT e, quando necessário, uma planilha Excel. As rotinas percorrem registros delimitados por pipes e aplicam regras específicas aos blocos E220 e E240.",
        "steps": ["Atualizar TXT: analisa registros E220 e os registros seguintes para inserir o código fiscal correspondente.", "Remover exceções: usa os identificadores da primeira coluna da planilha para decidir quais blocos E220 preservar; mantém também os registros com o código CE100004.", "Alterar VL ST: relaciona campos da planilha com registros E240, substitui os valores correspondentes e recalcula o total do bloco E220.", "Apresenta o resultado ao usuário pela interface Tkinter."],
        "technical": "Python e Tkinter compõem a interface; openpyxl lê as planilhas. A lógica processa o conteúdo textual do arquivo fiscal sem banco de dados, aplicando regras pontuais aos registros selecionados.",
        "note": "O código trabalha nos caminhos de arquivo selecionados e regrava o TXT processado. É importante manter uma cópia de segurança antes de executar as rotinas. O título interno do aplicativo identifica o formato como SPED Fiscal.",
    },
]


@app.get("/")
def home():
    return render_template("index.html", profile=PROFILE, experience=EXPERIENCE, education=EDUCATION, skill_groups=SKILL_GROUPS, projects=PROJECTS, languages=["Inglês intermediário"])


@app.get("/projetos/<slug>")
def project_detail(slug):
    project = next((item for item in PROJECTS if item["slug"] == slug), None)
    if project is None:
        abort(404)
    return render_template("project_detail.html", project=project, profile=PROFILE, projects=PROJECTS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
