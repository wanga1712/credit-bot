# Инструкция по развертыванию на Linux

## Требования

- Python 3.11 или выше
- pip
- git (для клонирования репозитория)

## Шаги развертывания

### 1. Клонирование репозитория

```bash
git clone <url_вашего_репозитория>
cd pythonProject93
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # Для bash/zsh
# или
. venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

```bash
cp .env.example .env
nano .env  # или используйте любой другой редактор
```

Отредактируйте файл `.env` и укажите ваш токен бота:
```
TELEGRAM_BOT_TOKEN=ваш_токен_здесь
```

### 5. Запуск бота

#### Вариант 1: Прямой запуск

```bash
python main.py
```

#### Вариант 2: Запуск в фоне (screen)

```bash
screen -S credit_bot
python main.py
# Нажмите Ctrl+A, затем D для отсоединения
# Для возврата: screen -r credit_bot
```

#### Вариант 3: Запуск в фоне (tmux)

```bash
tmux new -s credit_bot
python main.py
# Нажмите Ctrl+B, затем D для отсоединения
# Для возврата: tmux attach -t credit_bot
```

#### Вариант 4: Systemd service (рекомендуется для продакшена)

Создайте файл `/etc/systemd/system/credit-bot.service`:

```ini
[Unit]
Description=Credit Bot Telegram Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/pythonProject93
Environment="PATH=/path/to/pythonProject93/venv/bin"
ExecStart=/path/to/pythonProject93/venv/bin/python /path/to/pythonProject93/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Затем:

```bash
sudo systemctl daemon-reload
sudo systemctl enable credit-bot
sudo systemctl start credit-bot
sudo systemctl status credit-bot
```

Просмотр логов:
```bash
sudo journalctl -u credit-bot -f
```

## Обновление проекта

```bash
cd /path/to/pythonProject93
git pull
source venv/bin/activate
pip install -r requirements.txt
# Перезапустите сервис, если используете systemd
sudo systemctl restart credit-bot
```

## Проверка работы

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Проверьте, что бот отвечает

## Устранение проблем

### Бот не запускается

- Проверьте, что токен указан правильно в `.env`
- Проверьте логи: `sudo journalctl -u credit-bot -n 50`
- Убедитесь, что Python версии 3.11+

### Ошибки зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Проблемы с правами доступа

```bash
chmod +x main.py
chown -R your_username:your_username /path/to/pythonProject93
```

