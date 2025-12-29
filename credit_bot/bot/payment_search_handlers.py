"""Обработчики для сценария подбора платежа."""

from __future__ import annotations

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from credit_bot.core.calculator import CreditCalculator
from credit_bot.bot.formatters import format_payment_plan
from credit_bot.bot.keyboards import get_main_menu_keyboard
from credit_bot.bot.session import sessions
from credit_bot.bot.states import ENTER_TARGET_OVERPAYMENT, ENTER_TOLERANCE
from credit_bot.bot.utils import parse_float

calculator = CreditCalculator()


async def enter_target_overpayment(
    update: Update, context: CallbackContext
) -> int:
    """Обрабатывает ввод целевой переплаты."""

    user_id = update.effective_user.id
    session = sessions.get(user_id)
    
    # Если базовые параметры не заданы, запрашиваем их
    if session.term_months is None:
        from credit_bot.bot.states import ENTER_LOAN_AMOUNT
        
        await update.message.reply_text(
            "Сначала нужно рассчитать базовый график.\n"
            "Введите сумму кредита (в рублях):"
        )
        return ENTER_LOAN_AMOUNT
    
    value = parse_float(update.message.text)
    if value is None or value <= 0:
        await update.message.reply_text("Введите положительное число.")
        return ENTER_TARGET_OVERPAYMENT
    session.target_overpayment = value
    await update.message.reply_text("Введите допуск (в рублях, например 100):")
    return ENTER_TOLERANCE


async def enter_tolerance(update: Update, context: CallbackContext) -> int:
    """Обрабатывает ввод допуска и выполняет подбор платежа."""

    user_id = update.effective_user.id
    session = sessions.get(user_id)
    value = parse_float(update.message.text)
    if value is None or value <= 0:
        await update.message.reply_text("Введите положительное число.")
        return ENTER_TOLERANCE
    session.tolerance = value

    plan = calculator.calculate_payment_by_target_overpayment(
        amount=session.loan_amount,
        annual_interest_rate=session.annual_interest_rate,
        target_overpayment=session.target_overpayment,
        tolerance=session.tolerance,
    )
    response = format_payment_plan(plan)
    keyboard = get_main_menu_keyboard()
    await update.message.reply_text(
        response, parse_mode="Markdown", reply_markup=keyboard
    )

    # Полный рестарт после показа результата
    sessions.reset(user_id)
    return ConversationHandler.END

