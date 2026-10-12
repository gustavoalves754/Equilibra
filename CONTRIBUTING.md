# Contribuindo

Fluxo do projeto:

```text
feature/* -> develop -> qa -> main
```

Antes de abrir PR:

```bash
python -m pytest -q
python -m pytest -q --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=90
git status
```

Nunca versionar `.env`, bancos `.db`, tokens, senhas ou API Keys.
