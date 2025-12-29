"""Точка входа в приложение."""

from __future__ import annotations

import sys

from loguru import logger

from credit_bot.bot.bot import create_bot


def main() -> None:
    """Запускает Telegram-бота."""

    try:
        bot = create_bot()
        bot.run()
    except ValueError as exc:
        logger.error("Ошибка конфигурации: {}", exc)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Остановка бота по запросу пользователя.")
    except Exception as exc:
        logger.exception("Сбой при запуске бота: {}", exc)
        raise


if __name__ == "__main__":
    main()
