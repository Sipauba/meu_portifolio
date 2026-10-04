"""Curated portfolio projects. Edit links and summaries here."""

PROJECTS = [
    dict(slug="glados-assitente-ti", name="Glados · Assistente de TI", category="IA & Automação", summary="Assistente de TI que conecta conversas, IA e sistemas internos para encaminhar solicitações e automatizar consultas.", problem="Centralizar solicitações operacionais e reduzir etapas manuais no atendimento.", stack=["n8n", "OpenAI", "GLPI", "Oracle", "Redis", "WhatsApp"], filters=["RPA", "IA", "GLPI", "Integrações"], featured=True, repo="https://github.com/Sipauba/glados-assitente-ti", symbol="✳"),
    dict(slug="notifica-status-gerador-energia", name="Monitor de energia e gerador", category="IoT & Monitoramento", summary="Monitoramento com ESP32 do fornecimento de energia, funcionamento do gerador e temperatura, com alertas remotos.", problem="Dar visibilidade rápida a mudanças no estado da energia e do gerador.", stack=["ESP32", "C++", "Arduino", "Telegram API"], filters=["IoT", "Integrações"], featured=True, repo="https://github.com/Sipauba/notifica-status-gerador-energia", symbol="⌁"),
    dict(slug="bot-cobranca", name="Bot de cobrança", category="RPA & Financeiro", summary="Fluxo que consulta títulos financeiros, prepara mensagens de cobrança e organiza notificações via WhatsApp.", problem="Agilizar consultas e comunicação em uma rotina financeira recorrente.", stack=["n8n", "Oracle", "PostgreSQL", "WhatsApp API"], filters=["RPA", "Integrações"], featured=True, repo="https://github.com/Sipauba/bot-cobranca", symbol="↗"),
    dict(slug="integra-glpi-ti-e-rh-admissao", name="Integração RH → TI · Admissão", category="Integrações & RH", summary="Automação que transforma solicitações de admissão do RH em demandas técnicas de criação de acessos no GLPI.", problem="Conectar RH e TI para iniciar a preparação de acessos sem redigitação.", stack=["n8n", "GLPI", "OpenAI", "REST API"], filters=["RPA", "IA", "GLPI", "Integrações"], repo="https://github.com/Sipauba/integra-glpi-ti-e-rh-admissao", symbol="↳"),
    dict(slug="integra-glpi-ti-e-rh-demissao", name="Integração RH → TI · Desligamento", category="Integrações & RH", summary="Fluxo de desligamento que converte solicitações do RH em tarefas técnicas para remoção de acessos.", problem="Organizar o repasse de desligamentos e apoiar a revogação de acessos.", stack=["n8n", "GLPI", "OpenAI", "REST API"], filters=["RPA", "IA", "GLPI", "Integrações"], repo="https://github.com/Sipauba/integra-glpi-ti-e-rh-demissao", symbol="↳"),
    dict(slug="notifica-solicitacao-de-validacao-glpi", name="Validações pendentes no GLPI", category="RPA & Service Desk", summary="Notificações via WhatsApp para responsáveis por validações de chamados pendentes no GLPI.", problem="Evitar que solicitações aguardem validação sem visibilidade.", stack=["n8n", "GLPI", "MySQL", "WhatsApp API"], filters=["RPA", "GLPI", "Integrações"], repo="https://github.com/Sipauba/notifica-solicitacao-de-validacao-glpi", symbol="◉"),
    dict(slug="notifica-chamados-vencendo", name="Alertas de SLA no GLPI", category="RPA & Service Desk", summary="Acompanhamento de chamados próximos do vencimento com alertas preventivos via WhatsApp.", problem="Antecipar a atenção da equipe a chamados com prazo de SLA próximo.", stack=["n8n", "GLPI", "MySQL", "WhatsApp API"], filters=["RPA", "GLPI", "Integrações"], repo="https://github.com/Sipauba/notifica-chamados-vencendo", symbol="◷"),
    dict(slug="glados-auto-atendimento-n8n", name="Glados · Autoatendimento", category="IA & Service Desk", summary="Assistente de TI que recebe texto, áudio e imagem pelo WhatsApp, consulta a base de conhecimento e encaminha casos quando necessário.", problem="Dar uma primeira resposta consistente e coletar contexto antes de acionar a equipe.", stack=["n8n", "OpenAI", "PostgreSQL", "GLPI", "Chatwoot", "WhatsApp"], filters=["RPA", "IA", "GLPI", "Integrações"], repo="https://github.com/Sipauba/glados-auto-atendimento-n8n", symbol="✳"),
    dict(slug="pinga_ni_mim", name="Pinga ni mim", category="Monitoramento & Infraestrutura", summary="Aplicativo desktop que monitora hosts e serviços web por ping ou HTTP e envia alertas de falha e recuperação via WhatsApp.", problem="Identificar indisponibilidades e acompanhar o estado de equipamentos e serviços em um painel único.", stack=["Python", "Tkinter", "Ping", "HTTP", "Evolution API"], filters=["RPA", "Integrações"], repo="https://github.com/Sipauba/pinga_ni_mim", symbol="↗"),
    dict(slug="relatorio-setor-compras", name="Follow up de compras", category="Dados & Compras", summary="Aplicativo desktop que consulta pedidos do WinThor e exporta um relatório de acompanhamento em Excel.", problem="Substituir a montagem manual de relatórios de pedidos e entregas.", stack=["Python", "Oracle", "Tkinter", "Pandas", "Excel"], filters=["RPA", "Integrações"], repo="https://github.com/Sipauba/relatorio-setor-compras", symbol="▥"),
]


# Short case-study content for the portfolio pages. Full technical docs stay in GitHub.
PROJECT_DETAILS = {
    "glados-assitente-ti": {
        "workflow": [
            "Recebe mensagens do WhatsApp pela Evolution API e identifica a intenção com OpenAI.",
            "Consulta ou atualiza dados em GLPI, MySQL e Oracle/WinThor conforme a solicitação.",
            "Usa Redis para manter o estado temporário de conversas que exigem confirmação.",
        ],
        "impact": "Reúne atendimentos e consultas operacionais em um fluxo conversacional, com menos troca manual entre sistemas.",
    },
    "notifica-status-gerador-energia": {
        "workflow": [
            "Lê sinais do gerador, da rede elétrica e de um sensor de temperatura com o ESP32.",
            "Exibe o estado em um LCD e permite configurar o Wi-Fi no dispositivo.",
            "Envia alertas de mudança e responde a consultas de status pelo Telegram.",
        ],
        "impact": "Torna o estado da energia e do gerador visível à distância para uma resposta mais rápida a mudanças.",
    },
    "bot-cobranca": {
        "workflow": [
            "Consulta títulos no Oracle conforme regras configuradas e normaliza os telefones.",
            "Valida os contatos pela API de WhatsApp e registra o controle operacional no PostgreSQL.",
            "Revalida os títulos antes do envio, gera mensagens e processa os avisos em lotes.",
        ],
        "impact": "Organiza uma rotina recorrente de cobrança e evita repetição de notificações por meio do controle de estado.",
    },
    "integra-glpi-ti-e-rh-admissao": {
        "workflow": [
            "Consulta solicitações de admissão do RH ainda não processadas.",
            "Usa IA para transformar o formulário em uma descrição objetiva para a equipe de TI.",
            "Abre o chamado no GLPI de suporte, notifica o responsável e marca a origem como processada.",
        ],
        "impact": "Reduz a transcrição manual entre RH e TI e organiza o início da criação de acessos.",
    },
    "integra-glpi-ti-e-rh-demissao": {
        "workflow": [
            "Identifica solicitações de desligamento do RH concluídas e ainda não processadas.",
            "Prepara com IA as tarefas técnicas de bloqueio e remoção de acessos.",
            "Cria um ticket no GLPI de suporte, notifica a equipe e atualiza o chamado de origem.",
        ],
        "impact": "Dá mais clareza ao repasse de desligamentos e às tarefas de revogação de acessos.",
    },
    "notifica-solicitacao-de-validacao-glpi": {
        "workflow": [
            "Consulta no GLPI as validações de chamados que ainda não receberam notificação.",
            "Verifica a disponibilidade do telefone do responsável e normaliza o número.",
            "Envia o aviso via API de WhatsApp e atualiza o estado de notificação.",
        ],
        "impact": "Dá visibilidade às validações pendentes para que o responsável possa agir mais cedo.",
    },
    "notifica-chamados-vencendo": {
        "workflow": [
            "Consulta periodicamente os prazos de resolução dos chamados no MySQL do GLPI.",
            "Identifica faixas próximas do vencimento, como 1 hora, 30 e 15 minutos.",
            "Monta o aviso com os dados do chamado e envia para um grupo no WhatsApp.",
        ],
        "impact": "Apoia o acompanhamento preventivo do SLA sem depender apenas de consulta manual ao GLPI.",
    },
    "glados-auto-atendimento-n8n": {
        "workflow": [
            "Recebe mensagens de texto, áudio ou imagem do WhatsApp por um webhook no n8n.",
            "Consulta o histórico e a base de conhecimento no PostgreSQL para orientar a conversa.",
            "Pode continuar o atendimento, encaminhar a uma pessoa via Chatwoot ou abrir chamado no GLPI.",
        ],
        "impact": "Estrutura a primeira etapa do atendimento e entrega mais contexto quando o caso segue para uma pessoa.",
    },
    "pinga_ni_mim": {
        "workflow": [
            "Monitora hosts por ping e URLs por requisições HTTP em intervalos configuráveis.",
            "Mostra status, latência, histórico, grupos e indicadores em uma interface Tkinter.",
            "Registra quedas e envia alertas de falha e recuperação via Evolution API, conforme as regras configuradas.",
        ],
        "impact": "Centraliza a visão de disponibilidade de equipamentos e serviços e antecipa a identificação de falhas.",
    },
    "relatorio-setor-compras": {
        "workflow": [
            "Permite filtrar pedidos por filial, período, comprador, fornecedor, tipo e status.",
            "Consulta dados do WinThor no Oracle e classifica a situação de faturamento e entrega.",
            "Mostra os resultados na interface desktop e exporta uma planilha Excel formatada.",
        ],
        "impact": "Substitui a montagem manual do acompanhamento de pedidos por uma consulta e exportação estruturadas.",
    },
}

for project in PROJECTS:
    project.update(PROJECT_DETAILS[project["slug"]])
