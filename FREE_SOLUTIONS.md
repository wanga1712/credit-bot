# Бесплатные решения для доступа к Telegram API

## Проверка: действительно ли проблема в блокировке?

Сначала проверим, может ли сервер вообще выходить в интернет:

```bash
# Проверка общего доступа в интернет
curl -I https://www.google.com

# Проверка конкретно Telegram
curl -I https://api.telegram.org

# Проверка через другой порт
curl -I http://api.telegram.org
```

## Бесплатное решение 1: Cloudflare WARP (РЕКОМЕНДУЕТСЯ)

Cloudflare WARP - бесплатный VPN от Cloudflare, который может обойти блокировки.

### Установка на сервере:

```bash
# Для Ubuntu/Debian
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list
sudo apt update
sudo apt install cloudflare-warp

# Регистрация (бесплатно)
warp-cli register

# Подключение
warp-cli connect

# Проверка статуса
warp-cli status
```

После подключения WARP, бот должен автоматически использовать VPN для всех соединений.

**Проверка:**
```bash
curl -I https://api.telegram.org
```

Если работает, запустите бота - он будет использовать WARP автоматически.

## Бесплатное решение 2: Использование бесплатных прокси

### Где найти бесплатные прокси:

1. **Сайты со списками:**
   - https://www.proxy-list.download/
   - https://free-proxy-list.net/
   - https://www.proxyscrape.com/

2. **Как использовать:**

```bash
# На сервере отредактируйте .env
nano ~/credit-bot/.env

# Добавьте прокси (пример)
TELEGRAM_PROXY=http://123.45.67.89:8080
```

**Проблемы с бесплатными прокси:**
- Могут перестать работать в любой момент
- Медленные
- Могут быть небезопасными
- Нужно часто менять

**Автоматическое обновление прокси:**

Можно написать скрипт, который будет автоматически находить рабочие бесплатные прокси.

## Бесплатное решение 3: Использование Telegram MTProto прокси

Telegram предоставляет бесплатные MTProto прокси для обхода блокировок.

### Настройка:

1. **Найдите MTProto прокси:**
   - https://t.me/mtprotoproxy
   - https://github.com/TelegramMessenger/MTProxy

2. **Используйте через специальный клиент** (но это сложнее для бота)

## Бесплатное решение 4: Проверка настроек сервера

Возможно, проблема не в блокировке, а в настройках:

### Проверка файрвола:

```bash
# Проверьте статус файрвола
sudo ufw status

# Если файрвол активен, разрешите исходящие HTTPS соединения
sudo ufw allow out 443/tcp
```

### Проверка DNS:

```bash
# Проверьте DNS серверы
cat /etc/resolv.conf

# Попробуйте использовать Google DNS
sudo nano /etc/resolv.conf
# Добавьте:
nameserver 8.8.8.8
nameserver 8.8.4.4
```

### Проверка маршрутизации:

```bash
# Проверьте, может ли сервер достучаться до Telegram
traceroute api.telegram.org

# Или
mtr api.telegram.org
```

## Бесплатное решение 5: Использование другого DNS

Иногда проблема в DNS:

```bash
# Установите cloudflare-dns или используйте Google DNS
sudo systemd-resolve --set-dns=8.8.8.8 --interface=eth0
```

## Рекомендуемый порядок действий:

1. **Сначала проверьте настройки сервера** (файрвол, DNS)
2. **Попробуйте Cloudflare WARP** (самое простое и надежное бесплатное решение)
3. **Если не помогло, попробуйте бесплатные прокси** (но будьте готовы к проблемам)

## Быстрая проверка всех решений:

```bash
# 1. Проверка файрвола
sudo ufw status

# 2. Проверка DNS
nslookup api.telegram.org

# 3. Установка WARP
# (см. инструкцию выше)

# 4. После каждого шага проверяйте:
curl -I https://api.telegram.org
```

