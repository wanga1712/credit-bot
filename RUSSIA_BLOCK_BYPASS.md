# Обход блокировки Telegram в России

## Проблема
Telegram заблокирован в России. Локальный прокси на сервере не поможет, так как он тоже находится в России и не может подключиться к Telegram API.

## Решения (от простого к сложному)

### Решение 1: Cloudflare WARP (БЕСПЛАТНО, РЕКОМЕНДУЕТСЯ)

Cloudflare WARP - бесплатный VPN, который может обойти блокировку Telegram.

**Установка:**
```bash
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list
sudo apt update
sudo apt install cloudflare-warp

# Регистрация (бесплатно)
warp-cli register

# Подключение
warp-cli connect

# Проверка
curl -I https://api.telegram.org
python check_telegram_connection.py
```

После подключения WARP, бот будет автоматически использовать VPN для всех соединений.

### Решение 2: SSH туннель через ноутбук (БЕСПЛАТНО)

Если ваш ноутбук не в России или использует VPN, можно использовать его как прокси.

**На ноутбуке (Windows PowerShell):**
```powershell
# Создайте SOCKS5 прокси
ssh -D 1080 -N wanga@100.122.104.106
```

**На сервере добавьте в `.env`:**
```bash
TELEGRAM_PROXY=socks5://127.0.0.1:1080
```

**Проблема:** Ноутбук должен быть включен и подключен.

### Решение 3: Бесплатные прокси (НЕНАДЕЖНО)

Можно попробовать бесплатные прокси из других стран:

1. Найдите бесплатный прокси (не из России):
   - https://www.proxy-list.download/
   - https://free-proxy-list.net/
   - Фильтруйте по странам: не Russia

2. Добавьте в `.env`:
   ```bash
   TELEGRAM_PROXY=http://proxy-ip:port
   ```

**Проблемы:** Ненадежно, медленно, могут перестать работать.

### Решение 4: Использование другого сервера (если есть)

Если у вас есть сервер за пределами России:

1. На том сервере настройте прокси
2. Используйте его IP в `.env`:
   ```bash
   TELEGRAM_PROXY=http://external-server-ip:port
   ```

## Рекомендация

**Для постоянной работы:** Используйте **Cloudflare WARP** - это бесплатно и надежно.

**Для тестирования:** Можно попробовать SSH туннель через ноутбук.

## Проверка после настройки

```bash
# 1. Проверьте подключение
curl -I https://api.telegram.org

# 2. Проверьте через Python
python check_telegram_connection.py

# 3. Если работает, запустите бота
python main.py
```

