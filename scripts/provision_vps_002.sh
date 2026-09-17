#!/usr/bin/env bash
# Одноразовая подготовка vps-002 под деплой my_site через GitHub Actions.
# Запускать под root:  sudo bash scripts/provision_vps_002.sh [RUNNER_TOKEN]
# RUNNER_TOKEN — короткоживущий токен регистрации раннера (из GitHub UI репозитория:
#   Settings → Actions → Runners → New self-hosted runner), либо опционально.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "ОШИБКА: нужен root (sudo bash $0 [token])" >&2
  exit 1
fi

REPO="ts19830409/my_site"
RUNNER_DIR=/srv/actions-runner
APP_DIR=/srv/my_site
RUNNER_TOKEN="${1:-}"

echo "═══ 1. Обновляем apt и ставим Docker ═══"
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io docker-compose-v2 curl jq tar
systemctl enable --now docker
usermod -aG docker ts-admin
echo "docker: $(docker --version)"
echo "compose: $(docker compose version)"

echo "═══ 2. Директория приложения ═══"
mkdir -p "$APP_DIR"
chown ts-admin:ts-admin "$APP_DIR"

echo "═══ 3. GitHub Actions runner ═══"
VER=$(curl -fsSL https://api.github.com/repos/actions/runner/releases/latest \
  | jq -r '.tag_name' | sed 's/^v//')
mkdir -p "$RUNNER_DIR"
cd "$RUNNER_DIR"
curl -fsSL -o runner.tar.gz "https://github.com/actions/runner/releases/latest/download/actions-runner-linux-x64-${VER}.tar.gz"
tar xzf runner.tar.gz
rm -f runner.tar.gz
chown -R ts-admin:ts-admin "$RUNNER_DIR"

if [ -n "${RUNNER_TOKEN:-}" ]; then
  echo "═══ 4. Регистрируем раннер ═══"
  su ts-admin -c "cd $RUNNER_DIR && ./config.sh --url https://github.com/$REPO --token $RUNNER_TOKEN \
    --unattended --replace --name vps-002 --labels vps-002,linux,x64,self-hosted"
  echo "═══ 5. Сервис runner ═══"
  ./svc.sh install
  ./svc.sh start
else
  echo "═══ 4. Токен не передан — раннер НЕ зарегистрирован ═══"
  echo "    Дальше вручную:"
  echo "    cd $RUNNER_DIR"
  echo '    ./config.sh --url https://github.com/ts19830409/my_site --token <TOKEN> --unattended --replace --name vps-002 --labels vps-002,linux,x64,self-hosted'
  echo "    sudo ./svc.sh install && sudo ./svc.sh start"
fi

echo
echo "Готово. Проверка:"
echo "  1. docker run hello-world  (должен ответить)"
echo "  2. если раннер зарегистрирован — он будет виден в настройках репозитория GitHub"
echo "  3. Деплой запустится при push в main репозитория $REPO"
echo
echo "Если ufw активен — откройте порты: ufw allow OpenSSH && ufw allow 80"