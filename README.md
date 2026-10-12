# 🥗 Equilibra

Backend acadêmico em Python para a disciplina de Gestão e Qualidade de Software (GQS), relacionado à ODS 3 — Saúde e Bem-Estar.

## Fluxo principal

```text
Cadastro -> Login/JWT -> Perfil -> Gemini -> Histórico
```

## Tecnologias

- Python 3.12
- Flask
- SQLite (`users.db` e `equilibra.db` separados)
- PyJWT
- google-genai
- pytest / pytest-cov
- GitHub Actions
- Docker + Gunicorn

## Regras de perfil

- idade entre 0 e 120;
- altura entre 1,00 e 2,60 m;
- peso > 1 kg e <= 500 kg;
- objetivo obrigatório, até 200 caracteres.

## Configuração local

Crie `.env` na raiz a partir de `.env.example`:

```env
JWT_SECRET=coloque-uma-chave-com-pelo-menos-32-caracteres
TOKEN_EXP_HOURS=8
GEMINI_API_KEY=COLE_SUA_CHAVE_REAL_AQUI
GEMINI_MODEL=gemini-3.8-flash
AUTH_DB_PATH=data/users.db
APP_DB_PATH=data/equilibra.db
```

O `.env` não deve ser versionado.

## Instalação

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
```

No Windows PowerShell, ative com:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Executar localmente

```bash
python run.py
```

Health check:

```text
GET /api/v1/health
```

## Rotas principais

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/me
PUT  /api/v1/profile
GET  /api/v1/profile
POST /api/v1/guidance
GET  /api/v1/guidance/history
```

## Testes

```bash
python -m pytest -q
python -m pytest -q -m unit
python -m pytest -q -m integration
python -m pytest -q --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=90
```

Os testes não fazem chamadas reais ao Gemini e usam bancos SQLite temporários.

## CI/CD

A CI executa em PRs/pushes para `develop`, `qa` e `main`, exigindo cobertura mínima de 90%.

Após uma CI verde na `main`, o CD cria a imagem Docker e publica no GitHub Container Registry (GHCR).

A implantação em servidor é opcional e só ocorre quando `DEPLOY_ENABLED=true` e os secrets do servidor estiverem configurados.

Detalhes em `docs/CI_CD.md`.
