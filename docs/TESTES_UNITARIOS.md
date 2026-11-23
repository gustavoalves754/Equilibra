# Testes do Equilibra

## Modelos usados

- Fact equivalente: teste simples para um comportamento único.
- InlineData equivalente: `pytest.mark.parametrize` com dados diretamente no teste.
- MemberData equivalente: conjuntos reutilizáveis definidos em membros de classe em `backend/tests/data_providers.py`.
- ClassData equivalente: classe separada fornecendo cenários completos reutilizáveis.

Não são recursos idênticos do xUnit; são adaptações dos mesmos conceitos para pytest.

## Executar

Entre uma vez na pasta do backend:

```bash
cd backend
```

Todos:

```bash
python -m pytest -q
```

Unitários:

```bash
python -m pytest -q -m unit
```

Integração:

```bash
python -m pytest -q -m integration
```

Cobertura de linhas e branches:

```bash
python -m pytest -q --cov=app --cov-branch --cov-report=term-missing --cov-report=html --cov-fail-under=90
```

O relatório HTML fica em `htmlcov/index.html`.

Os testes usam SQLite temporário e mocks para o Gemini.
