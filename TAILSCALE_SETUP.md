# Решение проблемы с Telegram API для серверов в Tailscale

## Проблема
Сервер находится в сети Tailscale и не может подключиться к `api.telegram.org`.

## Решение 1: Настройка Tailscale для выхода в интернет

Tailscale может блокировать прямой доступ в интернет. Нужно настроить маршрутизацию.

### Проверка текущих настроек:

```bash
# Проверьте статус Tailscale
tailscale status

# Проверьте маршруты
ip route show

# Проверьте, может ли сервер выходить в интернет
curl -I https://www.google.com
```

### Настройка выхода в интернет через Tailscale:

Если сервер не может выходить в интернет, возможно нужно:

1. **Разрешить выход в интернет в настройках Tailscale:**
   - Зайдите на https://login.tailscale.com/admin/machines
   - Найдите ваш сервер
   - Включите "Allow local network access" или настройте маршруты

2. **Или используйте другой узел Tailscale как шлюз:**
   ```bash
   # Если у вас есть другой узел с доступом в интернет
   tailscale set --advertise-routes=0.0.0.0/0
   ```

## Решение 2: Использование Cloudflare WARP поверх Tailscale

WARP может работать поверх Tailscale:

```bash
# Установите WARP
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list
sudo apt update
sudo apt install cloudflare-warp

# Зарегистрируйтесь
warp-cli register

# Подключитесь
warp-cli connect

# Проверьте
curl -I https://api.telegram.org
```

## Решение 3: Использование прокси через другой узел Tailscale

Если у вас есть другой узел в Tailscale с доступом в интернет:

1. На том узле настройте прокси (например, через SSH туннель)
2. Используйте его Tailscale IP в `.env`:
   ```bash
   TELEGRAM_PROXY=http://100.x.x.x:8080
   ```

## Решение 4: Проверка DNS в Tailscale

Tailscale использует свой DNS (127.0.0.53). Попробуйте:

```bash
# Проверьте DNS
dig api.telegram.org
# или
host api.telegram.org

# Если не работает, попробуйте Google DNS
sudo systemd-resolve --set-dns=8.8.8.8 --interface=tailscale0
```

## Быстрая диагностика

```bash
# 1. Проверка интернета
curl -I https://www.google.com

# 2. Проверка Telegram API
curl -I https://api.telegram.org

# 3. Проверка DNS
dig api.telegram.org

# 4. Проверка маршрутов
ip route show

# 5. Проверка Tailscale
tailscale status
```

## Рекомендуемый порядок действий:

1. **Проверьте, может ли сервер вообще выходить в интернет:**
   ```bash
   curl -I https://www.google.com
   ```

2. **Если не может, настройте Tailscale** (см. выше)

3. **Если может, но Telegram не работает, попробуйте WARP**

4. **Если ничего не помогло, используйте прокси через другой узел Tailscale**

