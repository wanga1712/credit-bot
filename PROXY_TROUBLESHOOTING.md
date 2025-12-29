# Решение проблем с прокси

## Проблема: `ConnectTimeout` при подключении к прокси

Если вы видите ошибку `httpcore.ConnectTimeout` при попытке подключиться к прокси, это означает, что Python не может установить TCP-соединение с прокси-сервером.

## Диагностика

### 1. Проверьте доступность прокси

```bash
# Проверка TCP подключения
python test_proxy_direct.py

# Или вручную
nc -zv 124.122.2.12 8080
# или
telnet 124.122.2.12 8080
```

### 2. Проверьте через curl

```bash
curl --proxy http://124.122.2.12:8080 https://api.telegram.org
```

Если `curl` работает, а Python нет - проблема в том, как Python подключается к прокси.

## Решения

### Решение 1: Попробуйте другой прокси

Публичные прокси часто нестабильны. Попробуйте найти другой:

1. **Бесплатные прокси-листы:**
   - https://www.proxy-list.download/
   - https://free-proxy-list.net/
   - Фильтруйте: страна != Russia, тип = HTTP

2. **Добавьте в `.env`:**
   ```bash
   TELEGRAM_PROXY=http://новый-прокси:порт
   ```

### Решение 2: Используйте SOCKS5 прокси

SOCKS5 прокси часто более надежны:

```bash
# В .env
TELEGRAM_PROXY=socks5://прокси:1080
```

### Решение 3: Cloudflare WARP (рекомендуется)

Cloudflare WARP - бесплатный VPN, который обходит блокировки:

```bash
# Установка на Ubuntu/Debian
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list
sudo apt update
sudo apt install -y cloudflare-warp

# Регистрация
warp-cli register

# Подключение
warp-cli connect

# Проверка
warp-cli status
```

После установки WARP, **удалите** `TELEGRAM_PROXY` из `.env` - WARP работает на уровне системы.

### Решение 4: Временно отключите прокси

Если прокси не работает, попробуйте запустить без него:

```bash
# В .env закомментируйте или удалите:
# TELEGRAM_PROXY=http://124.122.2.12:8080
```

Если бот не запустится без прокси (Telegram заблокирован), используйте WARP или другой прокси.

### Решение 5: Используйте SSH туннель

Если у вас есть другой сервер с доступом к Telegram:

**На сервере с доступом:**
```bash
ssh -D 1080 -N user@ваш-сервер
```

**На сервере с ботом в `.env`:**
```bash
TELEGRAM_PROXY=socks5://127.0.0.1:1080
```

## Рекомендации

1. **Для продакшена:** Используйте платный прокси или Cloudflare WARP
2. **Для тестирования:** Попробуйте несколько бесплатных прокси
3. **Для стабильности:** Используйте SOCKS5 вместо HTTP-прокси

## Проверка после настройки

```bash
# Проверка подключения
python check_telegram_connection.py

# Запуск бота
python main.py
```

