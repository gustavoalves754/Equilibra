# 🥗 Equilibra

Aplicação acadêmica da disciplina de Gestão e Qualidade de Software (GQS), relacionada à ODS 3 — Saúde e Bem-Estar.

O projeto está organizado como um monorepositório com frontend e backend separados:

```text
Equilibra/
├── backend/
│   ├── app/                  # API Flask
│   ├── tests/                # testes unitários e de integração
│   ├── data/                 # bancos SQLite locais (não versionados)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── run.py
│   └── wsgi.py
├── frontend/
│   ├── js/
│   ├── index.html
│   └── style.css
├── deploy/
├── docs/
└── .github/workflows/
```

## Fluxo principal

```text
Cadastro -> Login/JWT -> Perfil -> Gemini -> Histórico
```

## Tecnologias

- Python 3.12
- Flask
- HTML, CSS e JavaScript
- SQLite (`users.db` e `equilibra.db` separados)
- PyJWT
- Google Gen AI
- pytest / pytest-cov
- GitHub Actions
- Docker + Gunicorn

## Configuração local

Entre na pasta do backend e crie o arquivo `.env` a partir do exemplo:

```powershell
cd backend
Copy-Item .env.example .env
```

Preencha as variáveis necessárias no arquivo criado:

```env
JWT_SECRET=coloque-uma-chave-com-pelo-menos-32-caracteres
TOKEN_EXP_HOURS=8
GEMINI_API_KEY=COLE_SUA_CHAVE_REAL_AQUI
GEMINI_MODELS=gemini-3.8-flash,gemini-3.6-flash,gemini-3.5-flash-lite
AUTH_DB_PATH=data/users.db
APP_DB_PATH=data/equilibra.db
```

O `.env` e os bancos SQLite locais não devem ser versionados.

## Instalação

Execute os comandos dentro de `backend/`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

## Executar localmente

Ainda dentro de `backend/`:

```powershell
python run.py
```

A aplicação completa fica disponível em:

```text
http://127.0.0.1:5000
```

O Flask entrega o frontend da pasta `frontend/` e mantém a API em `/api/v1`.

## Rotas principais

```text
GET  /api/v1/health
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/me
PUT  /api/v1/profile
GET  /api/v1/profile
POST /api/v1/guidance
GET  /api/v1/guidance/history
```

## Testes

Na pasta `backend/`:

```powershell
python -m pytest -q
python -m pytest -q -m unit
python -m pytest -q -m integration
python -m pytest -q --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=90
```

Os testes não fazem chamadas reais ao Gemini e usam bancos SQLite temporários.

## Branches principais

- `develop`: desenvolvimento e integração das alterações;
- `qa`: validação e homologação;
- `main`: versão estável.

## CI/CD

A CI executa em pushes e pull requests para `develop`, `qa` e `main`, com cobertura mínima de 90%.

Após uma CI verde na `main`, o CD cria a imagem usando `backend/Dockerfile` e publica no GitHub Container Registry. A implantação em servidor continua opcional.

Mais detalhes em [docs/CI_CD.md](docs/CI_CD.md).
