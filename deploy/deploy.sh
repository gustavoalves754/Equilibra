#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:?Informe a imagem Docker.}"
APP_NAME="equilibra-backend"
APP_DIR="/opt/equilibra"
ENV_FILE="$APP_DIR/.env"
DATA_DIR="$APP_DIR/data"
PORT="${EQUILIBRA_PORT:-5000}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERRO: configure $ENV_FILE antes do deploy."
  exit 1
fi

mkdir -p "$DATA_DIR"
docker pull "$IMAGE"

PREVIOUS_IMAGE=""
if docker inspect "$APP_NAME" >/dev/null 2>&1; then
  PREVIOUS_IMAGE="$(docker inspect --format='{{.Config.Image}}' "$APP_NAME")"
  docker stop "$APP_NAME" >/dev/null
  docker rm "$APP_NAME" >/dev/null
fi

start_container() {
  local image="$1"
  docker run -d \
    --name "$APP_NAME" \
    --restart unless-stopped \
    --env-file "$ENV_FILE" \
    -p "$PORT:5000" \
    -v "$DATA_DIR:/app/data" \
    "$image" >/dev/null
}

start_container "$IMAGE"
HEALTH_URL="http://127.0.0.1:$PORT/api/v1/health"

for attempt in {1..12}; do
  if curl --fail --silent --show-error "$HEALTH_URL" >/dev/null; then
    echo "Deploy concluído. Health check OK."
    exit 0
  fi
  sleep 5
done

echo "ERRO: nova versão não ficou saudável."
docker logs --tail 100 "$APP_NAME" || true
docker stop "$APP_NAME" >/dev/null || true
docker rm "$APP_NAME" >/dev/null || true

if [[ -n "$PREVIOUS_IMAGE" ]]; then
  echo "Rollback para $PREVIOUS_IMAGE"
  start_container "$PREVIOUS_IMAGE"
  sleep 5
  curl --fail --silent --show-error "$HEALTH_URL" >/dev/null
  echo "Rollback concluído."
else
  echo "Não existe imagem anterior para rollback."
fi

exit 1
