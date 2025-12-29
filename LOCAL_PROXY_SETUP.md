# Настройка локального прокси на сервере

## Проблема
Пакеты теряются на стороне провайдера при прямом подключении к Telegram API. Локальный прокси может помочь, так как он может:
- Кэшировать соединения
- Переиспользовать TCP соединения
- Лучше обрабатывать потерю пакетов

## Решение: Установка tinyproxy

### Шаг 1: Установка

```bash
cd ~/credit-bot
git pull origin main
chmod +x setup_local_proxy.sh
./setup_local_proxy.sh
```

Или вручную:

```bash
sudo apt update
sudo apt install -y tinyproxy

# Настройка
sudo nano /etc/tinyproxy/tinyproxy.conf
```

Измените:
- `Port 8888` (или другой свободный порт)
- `Allow 127.0.0.1` (разрешить только локальные подключения)

### Шаг 2: Запуск

```bash
sudo systemctl enable tinyproxy
sudo systemctl restart tinyproxy
sudo systemctl status tinyproxy
```

### Шаг 3: Настройка бота

Добавьте в `.env`:
```bash
TELEGRAM_PROXY=http://127.0.0.1:8888
```

### Шаг 4: Проверка

```bash
# Проверка прокси
curl --proxy http://127.0.0.1:8888 https://api.telegram.org

# Проверка через скрипт
python check_telegram_connection.py
```

## Альтернатива: Python прокси (если tinyproxy не работает)

Если tinyproxy не помогает, можно использовать простой Python прокси:

```bash
pip install pproxy
```

Запуск:
```bash
pproxy -l http://127.0.0.1:8888
```

Затем в `.env`:
```bash
TELEGRAM_PROXY=http://127.0.0.1:8888
```

## Устранение проблем

### Прокси не запускается

```bash
# Проверьте логи
sudo journalctl -u tinyproxy -n 50

# Проверьте, не занят ли порт
sudo netstat -tuln | grep 8888
```

### Прокси не помогает

Попробуйте:
1. Увеличить таймауты в tinyproxy
2. Использовать другой прокси (squid, 3proxy)
3. Проверить, действительно ли проблема в потере пакетов

## Проверка работы

После настройки прокси:

```bash
# 1. Проверьте, что прокси работает
curl --proxy http://127.0.0.1:8888 https://www.google.com

# 2. Проверьте Telegram API
curl --proxy http://127.0.0.1:8888 https://api.telegram.org

# 3. Проверьте через Python
python check_telegram_connection.py

# 4. Запустите бота
python main.py
```

