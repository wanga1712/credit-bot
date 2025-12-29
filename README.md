# Credit Bot

Telegram-бот для расчёта кредитов с поддержкой досрочного погашения и подбора платежа под целевую переплату.

## Возможности

- ✅ Расчёт аннуитетного графика платежей
- ✅ Досрочное погашение (сокращение срока или платежа)
- ✅ Комбинированные стратегии досрочки (две даты)
- ✅ Подбор ежемесячного платежа под целевую переплату

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Получение токена бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot` и следуйте инструкциям
3. Скопируйте полученный токен

### 3. Настройка токена бота

**Способ 1: Файл `.env` (рекомендуется)**

1. В корне проекта (там же, где `main.py`) создайте файл `.env`
2. Откройте его и вставьте:
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_здесь
   ```
3. Замените `ваш_токен_здесь` на реальный токен от @BotFather

**Способ 2: Переменная окружения**

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN="ваш_токен_здесь"
```

**Windows (CMD):**
```cmd
set TELEGRAM_BOT_TOKEN=ваш_токен_здесь
```

**Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN="ваш_токен_здесь"
```

> **Важно:** Файл `.env` уже создан в корне проекта. Просто откройте его и вставьте свой токен!

### 4. Запуск бота

```bash
python main.py
```

Или через PyCharm: просто запустите `main.py` (зелёная кнопка Run).

## Использование

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Используйте `/calculate` для начала расчёта
4. Следуйте инструкциям бота

## CLI-демо (для тестирования)

Для тестирования логики без Telegram:

```bash
python cli_demo.py
```

Или через `main.py` (если переключить на CLI-режим).

## Development Rules

- Follow PEP 8 for all Python code.
- Always guard critical operations with `try`/`except` and convert errors into helpful messages.
- Use `loguru` for logging; no `print`-based logging in production modules.
- Preserve modular design: if a module exceeds 150 lines, split it into smaller modules/classes.
- Писать комментарии и docstring только на русском языке.

These rules are duplicated in `pyproject.toml` under `[tool.credit_bot]` for programmatic consumption.

## Tooling & Checks

- `pyproject.toml` configures Black, isort, Flake8, and documents the house rules.
- `.pre-commit-config.yaml` runs Black, isort, Flake8, and the custom `scripts/check_module_lengths.py` to enforce the 150-line constraint.
- Install hooks with `pre-commit install` and run the full suite manually via `pre-commit run --all-files`.

