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
        
        # #region agent log
        import json
        log_path = Path(__file__).parent.parent.parent / ".cursor" / "debug.log"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "A",
                    "location": "bot.py:_build_application:entry",
                    "message": "Building application",
                    "data": {"token_length": len(self._token) if self._token else 0},
                    "timestamp": int(__import__("time").time() * 1000)
                }) + "\n")
        except Exception:
            pass
        # #endregion

        # Настраиваем builder с увеличенными таймаутами для решения проблем с подключением
        # В версии 22.5 нужно использовать правильные методы для настройки таймаутов
        builder = (
            ApplicationBuilder()
            .token(self._token)
            .connect_timeout(30.0)  # Таймаут подключения в секундах
            .read_timeout(30.0)  # Таймаут чтения в секундах
            .write_timeout(30.0)  # Таймаут записи в секундах
        )
        
        # Проверяем наличие прокси в переменных окружения
        proxy_url = os.getenv("TELEGRAM_PROXY")
        if proxy_url:
            builder = builder.proxy(proxy_url)
            logger.info("Используется прокси для подключения к Telegram API")
        
        # Проверяем наличие кастомного базового URL для Telegram API (для обхода блокировок)
        api_base_url = os.getenv("TELEGRAM_API_BASE_URL")
        if api_base_url:
            # Убираем /api/bot из URL, если есть (ApplicationBuilder добавит это сам)
            if api_base_url.endswith("/api/bot"):
                api_base_url = api_base_url[:-8]
            elif api_base_url.endswith("/api"):
                api_base_url = api_base_url[:-4]
            # Убираем завершающий слэш
            api_base_url = api_base_url.rstrip("/")
            builder = builder.base_url(api_base_url)
            logger.info(f"Используется кастомный базовый URL для Telegram API: {api_base_url}")
        
        # #region agent log
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "B",
                    "location": "bot.py:_build_application:before_build",
                    "message": "Before builder.build()",
                    "data": {},
                    "timestamp": int(__import__("time").time() * 1000)
                }) + "\n")
        except Exception:
            pass
        # #endregion
        
        app = builder.build()
        
        # #region agent log
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "C",
                    "location": "bot.py:_build_application:after_build",
                    "message": "After builder.build()",
                    "data": {"app_type": type(app).__name__, "has_bot": hasattr(app, "bot")},
                    "timestamp": int(__import__("time").time() * 1000)
                }) + "\n")
        except Exception:
            pass
        # #endregion
        
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
        
        # #region agent log
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "D",
                    "location": "bot.py:_build_application:exit",
                    "message": "Application built successfully",
                    "data": {},
                    "timestamp": int(__import__("time").time() * 1000)
                }) + "\n")
        except Exception:
            pass
        # #endregion
        
        return app

    async def _post_init(self, application: Application) -> None:
        """Вызывается после инициализации приложения."""

        logger.info("Telegram-бот инициализирован.")

    async def _post_shutdown(self, application: Application) -> None:
        """Вызывается при остановке бота."""

        logger.info("Telegram-бот остановлен.")

    def run(self) -> None:
        """Запускает бота в режиме polling."""
        
        import asyncio
        
        # #region agent log
        import json
        log_path = Path(__file__).parent.parent.parent / ".cursor" / "debug.log"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "E",
                    "location": "bot.py:run:entry",
                    "message": "Starting bot run",
                    "data": {},
                    "timestamp": int(__import__("time").time() * 1000)
                }) + "\n")
        except Exception:
            pass
        # #endregion

        async def _run_async() -> None:
            """Асинхронная функция для запуска бота с явной инициализацией."""
            max_retries = 3
            retry_delay = 5  # секунды
            
            for attempt in range(1, max_retries + 1):
                try:
                    self._application = self._build_application()
                    
                    # #region agent log
                    try:
                        with open(log_path, "a", encoding="utf-8") as f:
                            f.write(json.dumps({
                                "sessionId": "debug-session",
                                "runId": "run1",
                                "hypothesisId": "H",
                                "location": "bot.py:run:before_initialize",
                                "message": "Before initialize",
                                "data": {"app_created": self._application is not None, "attempt": attempt},
                                "timestamp": int(__import__("time").time() * 1000)
                            }) + "\n")
                    except Exception:
                        pass
                    # #endregion
                    
                    logger.info(f"Запуск Telegram-бота... (попытка {attempt}/{max_retries})")
                    
                    # Явная инициализация для версии 22.5
                    await self._application.initialize()
                
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({
                            "sessionId": "debug-session",
                            "runId": "run1",
                            "hypothesisId": "I",
                            "location": "bot.py:run:after_initialize",
                            "message": "After initialize",
                            "data": {"bot_id": getattr(self._application.bot, 'id', None) if hasattr(self._application, 'bot') else None},
                            "timestamp": int(__import__("time").time() * 1000)
                        }) + "\n")
                except Exception:
                    pass
                # #endregion
                
                await self._application.start()
                await self._application.updater.start_polling(
                    allowed_updates=Update.ALL_TYPES,
                    drop_pending_updates=True
                )
                
                    logger.info("Telegram-бот запущен и готов к работе.")
                    
                    # Ждем до отключения
                    await self._application.updater.stop()
                    await self._application.stop()
                    await self._application.shutdown()
                    break  # Успешно запустились, выходим из цикла повторов
                    
                except TimedOut as exc:
                    # #region agent log
                    try:
                        with open(log_path, "a", encoding="utf-8") as f:
                            f.write(json.dumps({
                                "sessionId": "debug-session",
                                "runId": "run1",
                                "hypothesisId": "J",
                                "location": "bot.py:run:timeout",
                                "message": "Connection timeout",
                                "data": {"attempt": attempt, "max_retries": max_retries},
                                "timestamp": int(__import__("time").time() * 1000)
                            }) + "\n")
                    except Exception:
                        pass
                    # #endregion
                    
                    if attempt < max_retries:
                        logger.warning(f"Таймаут подключения (попытка {attempt}/{max_retries}). Повтор через {retry_delay} сек...")
                        await asyncio.sleep(retry_delay)
                        # Закрываем приложение перед повторной попыткой
                        try:
                            if self._application:
                                await self._application.shutdown()
                        except Exception:
                            pass
                        continue
                    else:
                        logger.error("Не удалось подключиться к Telegram API после всех попыток.")
                        logger.error("Проверьте:")
                        logger.error("1. Доступность api.telegram.org с сервера")
                        logger.error("2. Настройки файрвола")
                        logger.error("3. Необходимость использования прокси (установите TELEGRAM_PROXY в .env)")
                        raise
                        
                except Exception as exc:
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({
                            "sessionId": "debug-session",
                            "runId": "run1",
                            "hypothesisId": "G",
                            "location": "bot.py:run:exception",
                            "message": "Exception caught in async",
                            "data": {"exception_type": type(exc).__name__, "exception_msg": str(exc)},
                            "timestamp": int(__import__("time").time() * 1000)
                        }) + "\n")
                except Exception:
                    pass
                # #endregion
                logger.exception("Ошибка при запуске бота.")
                raise
        
        try:
            asyncio.run(_run_async())
        except KeyboardInterrupt:
            logger.info("Остановка бота по запросу пользователя.")
        except Exception as exc:
            logger.exception("Сбой при запуске бота.")
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
