"""Обработка комбинированных стратегий досрочного погашения."""

from __future__ import annotations

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from credit_bot.core.calculator import CreditCalculator
from credit_bot.core.models import EarlyRepayment, EarlyRepaymentStrategy
from credit_bot.bot.formatters import format_early_result
from credit_bot.bot.keyboards import get_main_menu_keyboard
from credit_bot.bot.session import sessions
from credit_bot.bot.states import ENTER_SECOND_AMOUNT, ENTER_SECOND_PAYMENTS
from credit_bot.bot.utils import parse_float, parse_int

calculator = CreditCalculator()


async def enter_second_amount(update: Update, context: CallbackContext) -> int:
    """Обрабатывает ввод второй суммы для комбинированной стратегии."""

    user_id = update.effective_user.id
    session = sessions.get(user_id)
    value = parse_float(update.message.text)
    if value is None or value <= 0:
        await update.message.reply_text("Введите положительное число.")
        return ENTER_SECOND_AMOUNT
    session.secondary_amount = value
    if session.strategy == EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT.value:
        await update.message.reply_text(
            "После скольких платежей сделать второе погашение?"
        )
        return ENTER_SECOND_PAYMENTS
    await _finish_combined(update, context)
    return ConversationHandler.END


async def enter_second_payments(update: Update, context: CallbackContext) -> int:
    """Обрабатывает ввод второй даты для стратегии срок→платёж."""

    user_id = update.effective_user.id
    session = sessions.get(user_id)
    value = parse_int(update.message.text)
    if value is None or value <= session.payments_made:
        await update.message.reply_text(
            "Введите число больше количества уже сделанных платежей."
        )
        return ENTER_SECOND_PAYMENTS
    session.secondary_payments = value
    await _finish_combined(update, context)
    return ConversationHandler.END


async def _finish_combined(update: Update, context: CallbackContext) -> None:
    """Завершает расчёт комбинированной стратегии."""

    user_id = update.effective_user.id
    session = sessions.get(user_id)
    base_schedule = calculator.generate_payment_schedule(
        session.loan_amount, session.term_months, session.annual_interest_rate
    )
    strategy = EarlyRepaymentStrategy(session.strategy)
    repayment = EarlyRepayment(
        amount=session.early_repayment_amount,
        strategy=strategy,
        execute_after_payments=session.payments_made,
        secondary_amount=session.secondary_amount,
        secondary_execute_after_payments=session.secondary_payments,
    )
    result = calculator.apply_early_repayment(
        base_schedule, repayment, session.payments_made
    )
    response = format_early_result(result)
    keyboard = get_main_menu_keyboard()
    await update.message.reply_text(
        response, parse_mode="Markdown", reply_markup=keyboard
    )

    # Полный рестарт после показа результата
    sessions.reset(user_id)

