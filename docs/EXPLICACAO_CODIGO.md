# Explicação resumida do projeto

- `backend/app/__init__.py`: cria a aplicação Flask e entrega o frontend.
- `backend/app/config.py`: lê configurações e variáveis de ambiente.
- `backend/app/auth.py`: cria/valida JWT e protege rotas.
- `backend/app/database.py`: acesso aos dois SQLite e criação das tabelas.
- `backend/app/validators.py`: valida credenciais e perfil.
- `backend/app/prompts.py`: monta o prompt enviado ao Gemini.
- `backend/app/gemini_service.py`: chama o SDK `google-genai` e trata erros/respostas inválidas.
- `backend/app/routes.py`: cadastro, login, perfil, orientação e histórico.
- `backend/run.py`: execução local de desenvolvimento.
- `backend/wsgi.py`: entrada utilizada pelo Gunicorn.
- `backend/tests/unit/`: funções isoladas.
- `backend/tests/integration/`: HTTP + Flask + SQLite temporário.
- `frontend/`: interface em HTML, CSS e JavaScript.
- `.github/workflows/ci.yml`: testes e cobertura.
- `.github/workflows/cd.yml`: Docker/GHCR e deploy opcional.
