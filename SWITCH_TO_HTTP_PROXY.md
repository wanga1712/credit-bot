# Переход с Tor на HTTP-прокси

## Удаление Tor

```bash
cd ~/credit-bot
git pull origin main
chmod +x remove_tor.sh
sudo bash remove_tor.sh
```

## Настройка HTTP-прокси

### Шаг 1: Найдите HTTP-прокси

Откройте один из сайтов:
- https://www.proxy-list.download/ (выберите HTTP, страна не Россия)
- https://free-proxy-list.net/ (аналогично)
- https://spys.one/en/http-proxy-list/

**Критерии:**
- Тип: **HTTP** (не SOCKS)
- Страна: **не Россия**
- Анонимность: лучше Elite или Anonymous
- Скорость: чем выше, тем лучше

### Шаг 2: Протестируйте прокси

```bash
# Проверка через curl
curl --proxy http://новый-ip:порт https://api.telegram.org

# Если видите ответ (даже 302 или HTML) - прокси работает
```

### Шаг 3: Обновите .env

```bash
cd ~/credit-bot
nano .env
```

Замените строку:
```bash
TELEGRAM_PROXY=http://новый-ip:порт
```

Например:
```bash
TELEGRAM_PROXY=http://123.45.67.89:8080
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

### Шаг 4: Проверьте прокси

```bash
python test_proxy_direct.py
```

Должно показать: `✅ TCP подключение успешно` и `✅ httpx подключение успешно`

### Шаг 5: Запустите бота

```bash
python main.py
```

## Важно

- Бесплатные прокси часто нестабильны - могут перестать работать
- Если прокси перестанет работать - найдите новый и обновите `.env`
- Для стабильности рассмотрите платные прокси (ProxyMesh, Smartproxy и др.)

## Если прокси не работает

1. Попробуйте другой прокси из списка
2. Проверьте формат: `http://ip:порт` (без пробелов)
3. Убедитесь, что прокси не из России

