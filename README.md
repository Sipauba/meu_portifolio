# Portfólio — Mateus Sipaúba

Site pessoal em Flask com apresentação, trajetória e projetos. O conteúdo fica no início de `app.py` para ser atualizado sem alterar o HTML.

## Personalizar

Edite `PROFILE`, `EXPERIENCE` e `PROJECTS` em `app.py`: troque cargo, apresentação, localização, e-mail e links; substitua os exemplos pelos seus dados reais. Copie um objeto existente para adicionar experiência ou projeto.

## Executar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app run --debug
```

Abra `http://127.0.0.1:5000`.

## Publicar no EasyPanel

1. Envie o projeto para um repositório GitHub.
2. No EasyPanel, crie um serviço **App** conectado ao repositório.
3. Selecione build por **Dockerfile**. A aplicação escuta na porta indicada por `PORT` (padrão `5000`).
4. Adicione `sipauba.com.br` e, se desejar, `www.sipauba.com.br` nos domínios do serviço.
5. No DNS do domínio, configure os registros que o EasyPanel solicitar para o IP público da VPS e ative HTTPS/Let's Encrypt.

Os registros exatos dependem do IP e da configuração do seu proxy EasyPanel; use os valores indicados pelo painel.
