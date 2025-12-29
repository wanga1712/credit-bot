"""Обработчики ввода базовых параметров кредита."""

from __future__ import annotations

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from credit_bot.core.calculator import CreditCalculator
from credit_bot.bot.formatters import format_schedule
from credit_bot.bot.keyboards import get_main_menu_keyboard
from credit_bot.bot.session import sessions
from credit_bot.bot.states import (
    CHOOSE_ACTION,
    ENTER_INTEREST_RATE,
    ENTER_LOAN_AMOUNT,
    ENTER_LOAN_TERM,
    ENTER_PAYMENTS_MADE,
    ENTER_TARGET_OVERPAYMENT,
)
from credit_bot.bot.utils import parse_float, parse_int

calculator = CreditCalculator()


async def calculate_start(update: Update, context: CallbackContext) -> int:
    """Начинает сценарий расчёта."""

    user_id = update.effective_user.id
    logger.info(f"Пользователь {user_id} начал расчёт кредита")
    sessions.reset(user_id)
    await update.message.reply_text("Введите сумму кредита (в рублях):")
    return ENTER_LOAN_AMOUNT


async def enter_loan_amount(update: Update, context: CallbackContext) -> int:
    """Обрабатывает ввод суммы кредита."""

    user_id = update.effective_user.id
    logger.info(f"Пользователь {user_id} ввёл сумму кредита: {update.message.text}")
    session = sessions.get(user_id)
    value = parse_float(update.message.text)
    if value is None or value <= 0:
        logger.warning(f"Неверный ввод суммы кредита от пользователя {user_id}: {update.message.text}")
        await update.message.reply_text("Введите положительное число.")
        return ENTER_LOAN_AMOUNT
    session.loan_amount = value
    logger.info(f"Сумма кредита сохранена: {value} для пользователя {user_id}")
    await update.message.reply_text("Введите срок кредита (в месяцах):")
    return ENTER_LOAN_TERM


async def enter_loan_term(update: Update, context: CallbackContext) -> int:
    """Обрабатывает ввод срока."""

    user_id = update.effective_user.id
    logger.info(f"Пользователь {user_id} ввёл срок кредита: {update.message.text}")
    session = sessions.get(user_id)
    value = parse_int(update.message.text)
    if value is None or value <= 0:
        logger.warning(f"Неверный ввод срока кредита от пользователя {user_id}: {update.message.text}")
        await update.message.reply_text("Введите положительное целое число.")
        return ENTER_LOAN_TERM
    session.term_months = value
    logger.info(f"Срок кредита сохранён: {value} для пользователя {user_id}")
    await update.message.reply_text("Введите годовую процентную ставку (%):")
    return ENTER_INTEREST_RATE


async def enter_interest_rate(update: Update, context: CallbackContext) -> int:
    """Обрабатывает ввод ставки и показывает базовый график."""

    user_id = update.effective_user.id
    logger.info(f"Пользователь {user_id} ввёл процентную ставку: {update.message.text}")
    session = sessions.get(user_id)
    value = parse_float(update.message.text)
    if value is None or value < 0:
        logger.warning(f"Неверный ввод ставки от пользователя {user_id}: {update.message.text}")
        await update.message.reply_text("Введите неотрицательное число.")
        return ENTER_INTEREST_RATE
    session.annual_interest_rate = value
    logger.info(
        f"Параметры кредита сохранены для пользователя {user_id}: "
        f"сумма={session.loan_amount}, срок={session.term_months}, ставка={value}"
    )

    schedule = calculator.generate_payment_schedule(
        session.loan_amount, session.term_months, session.annual_interest_rate
    )
    text = format_schedule(schedule)
    await update.message.reply_text(text, parse_mode="Markdown")

    # Проверяем, было ли выбрано действие до ввода параметров
    logger.info(
        f"Проверка сохранённого действия для пользователя {user_id}: "
        f"strategy={session.strategy}"
    )
    
    # Если было выбрано действие до ввода параметров, переходим к нему
    if session.strategy == "reduce_payment":
        logger.info(
            f"У пользователя {user_id} было выбрано действие 'reduce_payment', "
            f"переходим к запросу количества платежей"
        )
        await update.message.reply_text("Сколько платежей уже сделано?")
        return ENTER_PAYMENTS_MADE
    if session.strategy == "reduce_term":
        logger.info(
            f"У пользователя {user_id} было выбрано действие 'reduce_term', "
            f"переходим к запросу количества платежей"
        )
        await update.message.reply_text("Сколько платежей уже сделано?")
        return ENTER_PAYMENTS_MADE
    if session.strategy == "combined":
        logger.info(
            f"У пользователя {user_id} было выбрано действие 'combined', "
            f"переходим к запросу количества платежей (комбинированная стратегия)"
        )
        await update.message.reply_text("Сколько платежей уже сделано?")
        return ENTER_PAYMENTS_MADE
    if session.strategy == "payment":
        logger.info(
            f"У пользователя {user_id} было выбрано действие 'payment', "
            f"переходим к запросу переплаты"
        )
        await update.message.reply_text("Введите желаемую переплату (в рублях):")
        return ENTER_TARGET_OVERPAYMENT

    # Иначе показываем меню выбора действий
    logger.info(
        f"У пользователя {user_id} не было выбрано действие заранее, "
        f"показываем меню выбора"
    )
    keyboard = get_main_menu_keyboard()
    await update.message.reply_text("Выберите действие:", reply_markup=keyboard)
    logger.info(f"График платежей показан пользователю {user_id}, разговор завершён")
    return ConversationHandler.END
