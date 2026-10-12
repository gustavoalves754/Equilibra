# Resultado dos testes — preenchimento final

Antes do merge da Issue 6, executar:

```bash
python -m compileall -q app tests run.py wsgi.py
python -m pytest -q
python -m pytest -q -m unit
python -m pytest -q -m integration
python -m pytest -q --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=90
```

Registrar aqui o resultado obtido no computador do grupo e confirmar também a CI verde no PR.

A publicação GHCR só pode ser declarada concluída depois que o código chegar à `main` e o workflow `CD` terminar com sucesso.
