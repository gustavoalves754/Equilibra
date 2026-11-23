# Resultado dos testes

Comandos executados a partir da raiz do repositório:

```bash
cd backend
python -m compileall -q app tests run.py wsgi.py
python -m pytest -q
python -m pytest -q -m unit
python -m pytest -q -m integration
python -m pytest -q --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=90
```

## Resultado local

- Suíte completa: 101 testes aprovados.
- Cobertura de linhas e branches: 97,70%.
- Meta mínima configurada: 90%.
- Sintaxe dos arquivos JavaScript do frontend: validada com `node --check`.

A publicação GHCR só pode ser declarada concluída depois que o código chegar à `main` e o workflow `CD` terminar com sucesso.
