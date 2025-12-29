# Настройка прокси для Telegram бота

## Проблема
Сервер не может подключиться к `api.telegram.org` напрямую (блокировка, файрвол, сетевые ограничения).

## Решение: Использование прокси

### Вариант 1: HTTP/HTTPS прокси

1. **Добавьте прокси в файл `.env`:**

```bash
TELEGRAM_BOT_TOKEN=ваш_токен_здесь
TELEGRAM_PROXY=http://proxy.example.com:8080
```

Или для HTTPS прокси:
```bash
TELEGRAM_PROXY=https://proxy.example.com:8080
```

### Вариант 2: SOCKS5 прокси

```bash
TELEGRAM_PROXY=socks5://proxy.example.com:1080
```

Или с аутентификацией:
```bash
TELEGRAM_PROXY=socks5://username:password@proxy.example.com:1080
```

### Вариант 3: SOCKS4 прокси

```bash
TELEGRAM_PROXY=socks4://proxy.example.com:1080
```

## Где взять прокси?

### 1. Публичные прокси (не рекомендуется для продакшена)
- https://www.proxy-list.download/
- https://free-proxy-list.net/

### 2. Платные прокси-сервисы (рекомендуется)
- ProxyMesh
- Bright Data (бывший Luminati)
- Smartproxy
- Oxylabs

### 3. Собственный прокси-сервер
Если у вас есть другой сервер с доступом к Telegram, можете настроить прокси там.

### 4. VPN с прокси-выходом
Если у вас есть VPN, можно использовать его прокси-выход.

## Проверка работы прокси

После настройки прокси в `.env`, запустите:

```bash
python check_telegram_connection.py
```

Скрипт проверит работу прокси автоматически.

## Примеры конфигурации

### Пример 1: HTTP прокси без аутентификации
```bash
TELEGRAM_PROXY=http://192.168.1.100:3128
```

### Пример 2: HTTP прокси с аутентификацией
```bash
TELEGRAM_PROXY=http://user:pass@proxy.example.com:8080
```

### Пример 3: SOCKS5 прокси
```bash
TELEGRAM_PROXY=socks5://127.0.0.1:1080
```

## Важно

- Прокси должен поддерживать HTTPS соединения
- Прокси должен иметь доступ к `api.telegram.org`
- Для продакшена используйте надежные прокси-сервисы
- Не храните пароли прокси в открытом виде (используйте переменные окружения)

## Альтернативные решения

Если прокси недоступен:

1. **Использование VPN на сервере:**
   - Установите OpenVPN или WireGuard
   - Настройте маршрутизацию через VPN

2. **Использование SSH туннеля:**
   ```bash
   ssh -D 1080 user@server-with-access
   ```
   Затем используйте `TELEGRAM_PROXY=socks5://127.0.0.1:1080`

3. **Запуск бота на другом сервере:**
   - Если у вас есть сервер с доступом к Telegram, запустите бота там

