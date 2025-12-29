"""Основные обработчики команд и сообщений Telegram-бота."""

from __future__ import annotations

from loguru import logger
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
)

from credit_bot.bot.keyboards import get_main_menu_keyboard
from credit_bot.bot.session import sessions
from credit_bot.bot.states import (
    ENTER_LOAN_AMOUNT,
    ENTER_PAYMENTS_MADE,
    ENTER_TARGET_OVERPAYMENT,
)
from credit_bot.bot.input_handlers import (
    calculate_start,
    enter_interest_rate,
    enter_loan_amount,
    enter_loan_term,
)


async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start."""

    user_id = update.effective_user.id
    logger.info(f"Пользователь {user_id} отправил команду /start")
    try:
        # Не сбрасываем сессию полностью, чтобы сохранить параметры кредита
        # если они уже были введены
        keyboard = get_main_menu_keyboard()
        message = await update.message.reply_text(
            "Привет! Я помогу рассчитать кредит.\n\n"
            "Выберите действие:",
            reply_markup=keyboard,
        )
        logger.info(f"Сообщение /start успешно отправлено пользователю {user_id}, message_id={message.message_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения /start пользователю {user_id}: {e}", exc_info=True)
        # Пытаемся отправить простое сообщение без клавиатуры
        try:
            await update.message.reply_text("Привет! Я помогу рассчитать кредит.")
        except Exception as e2:
            logger.error(f"Критическая ошибка при отправке сообщения: {e2}", exc_info=True)


async def handle_callback(update: Update, context: CallbackContext) -> int:
    """Обрабатывает нажатия на inline-кнопки."""

    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = update.effective_user.id
    logger.info(f"Пользователь {user_id} нажал на кнопку: {data}")
    
    if data.startswith("action:"):
        action = data.split(":")[1]
        session = sessions.get(user_id)
        logger.info(
            f"Обработка действия '{action}' для пользователя {user_id}. "
            f"Параметры сессии: term_months={session.term_months}, "
            f"loan_amount={session.loan_amount}, rate={session.annual_interest_rate}"
        )
        
        # Если базовые параметры не заданы, запрашиваем их
        if session.term_months is None:
            if action != "schedule":
                logger.info(
                    "Параметры кредита не заданы, "
                    f"запрашиваем их для пользователя {user_id}"
                )
                # Сохраняем выбранное действие, чтобы после ввода параметров перейти к нему
                session.strategy = action
                await query.edit_message_text(
                    "Сначала нужно рассчитать базовый график.\n"
                    "Введите сумму кредита (в рублях):"
                )
                return ENTER_LOAN_AMOUNT
        
        if action == "schedule":
            # Не сбрасываем сессию полностью, только очищаем для нового расчёта
            logger.info(f"Пользователь {user_id} выбрал 'Рассчитать график'")
            session.loan_amount = None
            session.term_months = None
            session.annual_interest_rate = None
            await query.edit_message_text("Введите сумму кредита (в рублях):")
            return ENTER_LOAN_AMOUNT
        elif action == "reduce_payment":
            # Сохраняем выбранную стратегию
            logger.info(f"Пользователь {user_id} выбрал 'Уменьшить платеж'")
            session.strategy = "reduce_payment"
            await query.edit_message_text("Сколько платежей уже сделано?")
            return ENTER_PAYMENTS_MADE
        elif action == "reduce_term":
            # Сохраняем выбранную стратегию
            logger.info(f"Пользователь {user_id} выбрал 'Уменьшить срок'")
            session.strategy = "reduce_term"
            await query.edit_message_text("Сколько платежей уже сделано?")
            return ENTER_PAYMENTS_MADE
        elif action == "combined":
            # Комбинированная стратегия: срок и платёж
            logger.info(
                f"Пользователь {user_id} выбрал 'Уменьшить срок и платёж' "
                "(комбинированная стратегия)"
            )
            session.strategy = "combined"
            await query.edit_message_text("Сколько платежей уже сделано?")
            return ENTER_PAYMENTS_MADE
        elif action == "payment":
            logger.info(f"Пользователь {user_id} выбрал 'Подобрать платеж для переплаты'")
            await query.edit_message_text("Введите желаемую переплату (в рублях):")
            return ENTER_TARGET_OVERPAYMENT

    logger.warning(f"Неизвестный callback_data от пользователя {user_id}: {data}")
    return ConversationHandler.END


async def choose_action(update: Update, context: CallbackContext) -> int:
    """Обрабатывает выбор действия пользователя (legacy, для совместимости)."""

    text = update.message.text
    if "Досрочное" in text:
        await update.message.reply_text("Сколько платежей уже сделано?")
        return ENTER_PAYMENTS_MADE
    if "Подобрать" in text:
        await update.message.reply_text("Введите желаемую переплату (в рублях):")
        return ENTER_TARGET_OVERPAYMENT
    await update.message.reply_text("График уже показан выше.")
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    """Отменяет текущий диалог."""

    user_id = update.effective_user.id
    sessions.reset(user_id)
    keyboard = get_main_menu_keyboard()
    await update.message.reply_text(
        "Операция отменена. Выберите действие:",
        reply_markup=keyboard,
    )
    return ConversationHandler.END
