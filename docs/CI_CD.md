# CI/CD do Equilibra

## CI

Arquivo: `.github/workflows/ci.yml`

Gatilhos:

- Pull Request para `develop`, `qa` ou `main`;
- push nessas branches;
- execução manual pela aba Actions.

Etapas:

1. checkout;
2. Python 3.12;
3. dependências;
4. validação estrutural;
5. testes unitários;
6. testes de integração;
7. suíte completa com cobertura de linhas e branches;
8. bloqueio se cobertura < 90%;
9. upload do relatório de cobertura.

## Proteção de branch

Em GitHub > Settings > Branches/Rulesets, exigir o check `Testes e cobertura` antes do merge nas branches que o grupo decidir proteger.

## CD

Arquivo: `.github/workflows/cd.yml`

O CD é executado somente depois de uma CI concluída com sucesso na `main`.

Ele:

1. cria a imagem do `Dockerfile`;
2. publica no GHCR;
3. publica as tags `latest` e `sha-XXXXXXX`.

A publicação no GHCR é automática. A implantação em servidor é opcional.

## Deploy opcional

Para ativar deploy externo:

- variável de repositório: `DEPLOY_ENABLED=true`;
- secrets: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`;
- servidor Linux com Docker e `curl`;
- `/opt/equilibra/.env` contendo `JWT_SECRET` e `GEMINI_API_KEY`;
- `/opt/equilibra/data` usado como volume persistente.

Se a imagem GHCR for privada, o servidor também precisa estar autenticado no GHCR.

## Persistência / atualização

Os bancos ficam fora do container em `/opt/equilibra/data`. Uma nova imagem não apaga os SQLite.

A aplicação cria tabelas ausentes com `CREATE TABLE IF NOT EXISTS` durante a inicialização. O projeto acadêmico não usa ferramenta externa de migrations.

## Rollback

`deploy/deploy.sh` guarda a imagem anterior. Se o health check falhar, remove a nova versão e tenta iniciar a imagem anterior.

## Health check

```text
GET /api/v1/health
```

O deploy só é considerado válido se o health check responder com sucesso.

## Secrets

Nunca colocar `JWT_SECRET`, `GEMINI_API_KEY`, chave SSH ou outras credenciais em fonte, Dockerfile, imagem ou logs.
