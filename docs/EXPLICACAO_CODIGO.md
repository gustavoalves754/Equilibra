# Explicação resumida do projeto

- `app/__init__.py`: cria e configura a aplicação Flask.
- `app/config.py`: lê configurações e variáveis de ambiente.
- `app/auth.py`: cria/valida JWT e protege rotas.
- `app/database.py`: acesso aos dois SQLite e criação das tabelas.
- `app/validators.py`: valida credenciais e perfil.
- `app/prompts.py`: monta o prompt enviado ao Gemini.
- `app/gemini_service.py`: chama o SDK `google-genai` e trata erros/respostas inválidas.
- `app/routes.py`: cadastro, login, perfil, orientação e histórico.
- `run.py`: execução local de desenvolvimento.
- `wsgi.py`: entrada utilizada pelo Gunicorn.
- `tests/unit/`: funções isoladas.
- `tests/integration/`: HTTP + Flask + SQLite temporário.
- `.github/workflows/ci.yml`: testes e cobertura.
- `.github/workflows/cd.yml`: Docker/GHCR e deploy opcional.
