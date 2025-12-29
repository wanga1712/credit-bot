# Быстрое решение: Локальный прокси

## Проблема
Python не может подключиться к Telegram API из-за потери пакетов на стороне провайдера. Локальный прокси может помочь.

## Быстрая установка

```bash
cd ~/credit-bot
git pull origin main
chmod +x setup_local_proxy.sh
./setup_local_proxy.sh
```

## После установки

1. **Добавьте в `.env`:**
```bash
nano .env
```
Добавьте:
```
TELEGRAM_PROXY=http://127.0.0.1:8888
```

2. **Проверьте:**
```bash
curl --proxy http://127.0.0.1:8888 https://api.telegram.org
python check_telegram_connection.py
```

3. **Запустите бота:**
```bash
python main.py
```

## Если tinyproxy не работает

Попробуйте альтернативу - простой Python прокси:

```bash
pip install pproxy
pproxy -l http://127.0.0.1:8888 &
```

Затем в `.env`:
```
TELEGRAM_PROXY=http://127.0.0.1:8888
```

