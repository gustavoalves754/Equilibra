# Issue 6 — CI/CD final, Docker e documentação

## Objetivo

Finalizar o backend do Equilibra com CI de cobertura mínima, empacotamento Docker, publicação automática no GHCR após CI verde na `main` e documentação final.

## Funcionalidades

- CI para `develop`, `qa` e `main`;
- testes unitários e de integração;
- cobertura de linhas e branches >= 90%;
- relatório de cobertura como artefato;
- Gunicorn para execução no container;
- Dockerfile e `.dockerignore`;
- CD após CI verde na `main`;
- publicação no GHCR com `latest` e `sha-*`;
- deploy em servidor opcional;
- health check e rollback;
- documentação final.

## Critérios de aceite

- [ ] suíte completa passa;
- [ ] cobertura >= 90%;
- [ ] CI verde;
- [ ] `.env` e `.db` não versionados;
- [ ] Docker usa Gunicorn;
- [ ] imagem é publicada no GHCR após promoção para `main`;
- [ ] deploy externo fica condicionado à infraestrutura;
- [ ] documentação final atualizada.

**Branch:** `feature/06-cicd-docs`
**PR:** `feature/06-cicd-docs` → `develop`
