"""Основной класс Telegram-бота."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from telegram import Update
from telegram.error import TimedOut
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    MessageHandler,
    filters,
)

from credit_bot.bot.registration import register_handlers

# Загружаем переменные из .env файла, если он существует
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class CreditBot:
    """Telegram-бот для расчёта кредитов."""

    def __init__(self, token: str) -> None:
        """Инициализирует бота с токеном."""

        self._token = token
        self._application: Application | None = None

    def _build_application(self) -> Application:
        """Создаёт и настраивает приложение Telegram."""

        # Настраиваем builder с увеличенными таймаутами для решения проблем с подключением
        builder = (
            ApplicationBuilder()
            .token(self._token)
            .get_updates_request(timeout=30)  # Увеличиваем таймаут для get_updates
            .connect_timeout(30)  # Таймаут подключения
            .read_timeout(30)  # Таймаут чтения
        )
        
        app = builder.build()
        register_handlers(app)
        
        # Добавляем обработчик ошибок
        async def error_handler(update: object, context: CallbackContext) -> None:
            """Обрабатывает ошибки при работе бота."""
            error = context.error
            if isinstance(error, TimedOut):
                logger.warning("Таймаут при отправке сообщения в Telegram.")
            else:
                logger.exception("Необработанная ошибка в боте.")
        
        app.add_error_handler(error_handler)
        
        return app

    async def _post_init(self, application: Application) -> None:
        """Вызывается после инициализации приложения."""

        logger.info("Telegram-бот инициализирован.")

    async def _post_shutdown(self, application: Application) -> None:
        """Вызывается при остановке бота."""

        logger.info("Telegram-бот остановлен.")

    def run(self) -> None:
        """Запускает бота в режиме polling."""

        try:
            self._application = self._build_application()
            
            logger.info("Запуск Telegram-бота...")
            # Используем стандартный run_polling с увеличенными таймаутами
            self._application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False
            )
        except KeyboardInterrupt:
            logger.info("Остановка бота по запросу пользователя.")
        except Exception as exc:
            logger.exception("Ошибка при запуске бота.")
            raise


def create_bot(token: str | None = None) -> CreditBot:
    """Создаёт экземпляр бота, используя токен из переменной окружения или аргумента."""

    bot_token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError(
            "Токен бота не найден. Установите переменную окружения "
            "TELEGRAM_BOT_TOKEN или передайте токен в функцию."
        )
    
    # Убираем пробелы и переносы строк
    bot_token = bot_token.strip()
    
    # Валидация формата токена (должен быть число:строка)
    if ":" not in bot_token:
        raise ValueError(
            f"Неверный формат токена. Токен должен быть в формате 'число:строка', "
            f"например '123456789:ABCdefGHIjklMNOpqrsTUVwxyz'.\n"
            f"Получен токен: '{bot_token[:20]}...' (показаны первые 20 символов)"
        )
    
    parts = bot_token.split(":", 1)
    if len(parts) != 2 or not parts[0].isdigit():
        raise ValueError(
            f"Неверный формат токена. Токен должен начинаться с числа, "
            f"затем двоеточие и строка.\n"
            f"Получен токен: '{bot_token[:20]}...' (показаны первые 20 символов)"
        )
    
    return CreditBot(bot_token)
