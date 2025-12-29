"""Обработчики для сценария досрочного погашения."""

from __future__ import annotations

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from credit_bot.core.models import EarlyRepaymentStrategy
from credit_bot.bot.calculation_helpers import calculate_and_send_early_result
from credit_bot.bot.keyboards import get_strategy_keyboard
from credit_bot.bot.session import sessions
from credit_bot.bot.states import (
    ENTER_EARLY_REPAYMENT_AMOUNT,
    ENTER_LOAN_AMOUNT,
    ENTER_PAYMENTS_MADE,
    ENTER_SECOND_AMOUNT,
    ENTER_STRATEGY,
)
from credit_bot.bot.utils import parse_float, parse_int


async def enter_payments_made(update: Update, context: CallbackContext) -> int:
    """Обрабатывает ввод количества сделанных платежей."""

    user_id = update.effective_user.id
    session = sessions.get(user_id)
    
    # Если базовые параметры не заданы, запрашиваем их
    if session.term_months is None:
        await update.message.reply_text(
            "Сначала нужно рассчитать базовый график.\n"
            "Введите сумму кредита (в рублях):"
        )
        return ENTER_LOAN_AMOUNT
    
    value = parse_int(update.message.text)
    if value is None or value < 0:
        await update.message.reply_text("Введите неотрицательное целое число.")
        return ENTER_PAYMENTS_MADE
    if value >= session.term_months:
        await update.message.reply_text("Это число должно быть меньше срока кредита.")
        return ENTER_PAYMENTS_MADE
    session.payments_made = value
    await update.message.reply_text("Введите сумму досрочного погашения (в рублях):")
    return ENTER_EARLY_REPAYMENT_AMOUNT


async def enter_early_repayment_amount(
    update: Update, context: CallbackContext
) -> int:
    """Обрабатывает ввод суммы досрочки."""

    user_id = update.effective_user.id
    session = sessions.get(user_id)
    value = parse_float(update.message.text)
    if value is None or value <= 0:
        await update.message.reply_text("Введите положительное число.")
        return ENTER_EARLY_REPAYMENT_AMOUNT
    session.early_repayment_amount = value
    
    # Если стратегия уже выбрана из главного меню, сразу выполняем расчёт
    if session.strategy == "reduce_payment":
        strategy = EarlyRepaymentStrategy.REDUCE_PAYMENT
        await calculate_and_send_early_result(update, strategy, session)
        return ConversationHandler.END
    elif session.strategy == "reduce_term":
        strategy = EarlyRepaymentStrategy.REDUCE_TERM
        await calculate_and_send_early_result(update, strategy, session)
        return ConversationHandler.END
    
    # Иначе показываем выбор стратегии (для совместимости)
    keyboard = get_strategy_keyboard()
    await update.message.reply_text("Выберите стратегию:", reply_markup=keyboard)
    return ENTER_STRATEGY


async def handle_strategy_callback(
    update: Update, context: CallbackContext
) -> int:
    """Обрабатывает выбор стратегии через inline-кнопку."""

    query = update.callback_query
    await query.answer()
    data = query.data
    if not data.startswith("strategy:"):
        await query.edit_message_text("Неверная команда.")
        return ConversationHandler.END
    strategy_name = data.split(":")[1]
    strategy_map = {
        "reduce_term": EarlyRepaymentStrategy.REDUCE_TERM,
        "reduce_payment": EarlyRepaymentStrategy.REDUCE_PAYMENT,
        "combo_pt": EarlyRepaymentStrategy.COMBINED_PAYMENT_THEN_TERM,
        "combo_tp": EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT,
    }
    strategy = strategy_map.get(strategy_name)
    if strategy is None:
        await query.edit_message_text("Неверная стратегия.")
        return ConversationHandler.END
    user_id = update.effective_user.id
    session = sessions.get(user_id)
    if strategy in (
        EarlyRepaymentStrategy.COMBINED_PAYMENT_THEN_TERM,
        EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT,
    ):
        await query.edit_message_text("Введите вторую сумму досрочного погашения:")
        session.strategy = strategy.value
        return ENTER_SECOND_AMOUNT
    await calculate_and_send_early_result(update, strategy, session)
    return ConversationHandler.END


async def enter_strategy(update: Update, context: CallbackContext) -> int:
    """Обрабатывает выбор стратегии через текст (legacy)."""

    user_id = update.effective_user.id
    session = sessions.get(user_id)
    text = update.message.text
    strategy_map = {
        "Сократить срок": EarlyRepaymentStrategy.REDUCE_TERM,
        "Сократить платёж": EarlyRepaymentStrategy.REDUCE_PAYMENT,
        "Платёж → срок": EarlyRepaymentStrategy.COMBINED_PAYMENT_THEN_TERM,
        "Срок → платёж": EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT,
    }
    strategy = strategy_map.get(text)
    if strategy is None:
        await update.message.reply_text("Выберите стратегию из предложенных.")
        return ENTER_STRATEGY
    if strategy in (
        EarlyRepaymentStrategy.COMBINED_PAYMENT_THEN_TERM,
        EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT,
    ):
        await update.message.reply_text("Введите вторую сумму досрочного погашения:")
        session.strategy = strategy.value
        return ENTER_SECOND_AMOUNT
    await calculate_and_send_early_result(update, strategy, session)
    return ConversationHandler.END
