# Portfólio — Mateus Sipaúba

Portfólio em Flask focado em RPA, automação e integrações. A página principal apresenta projetos de forma breve, com filtros no navegador. Cada card abre um resumo do projeto, com acesso direto ao repositório no GitHub.

## Atualizar conteúdo

- Edite `projects.py` para alterar projetos, categorias, tecnologias, destaques, conteúdo das páginas de resumo e URLs.
- Edite `PROFILE`, `AREAS` e `STACK` em `app.py` para atualizar dados profissionais e competências.
- O HTML fica em `templates/index.html`; estilos e interações ficam em `static/`.

## Executar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Abra `http://127.0.0.1:5000`.

## Publicar no EasyPanel

Use o `Dockerfile` existente. A aplicação escuta na porta indicada por `PORT` (padrão `5000`). Configure o domínio e HTTPS no painel conforme a instalação.
