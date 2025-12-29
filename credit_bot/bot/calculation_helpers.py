"""Вспомогательные функции для расчётов в боте."""

from __future__ import annotations

from telegram import Update

from credit_bot.core.calculator import CreditCalculator
from credit_bot.core.models import EarlyRepayment, EarlyRepaymentStrategy
from credit_bot.bot.formatters import format_early_result
from credit_bot.bot.keyboards import get_main_menu_keyboard
from credit_bot.bot.session import sessions

calculator = CreditCalculator()


async def calculate_and_send_early_result(
    update: Update, strategy: EarlyRepaymentStrategy, session
) -> None:
    """Выполняет расчёт досрочного погашения и отправляет результат.

    После отправки результата сценарий считается завершённым,
    временные поля сессии очищаются.
    """

    base_schedule = calculator.generate_payment_schedule(
        session.loan_amount,
        session.term_months,
        session.annual_interest_rate,
    )

    # Считаем, что пользователь вводит ОБЩУЮ сумму платежа в этот месяц:
    # банк сначала спишет обычный ежемесячный платёж,
    # остаток пойдёт на досрочное погашение основного долга.
    if not base_schedule.payments:
        return
    index = session.payments_made or 0
    index = min(max(index, 0), base_schedule.months - 1)
    regular_payment = base_schedule.payments[index].payment_amount

    total_amount = session.early_repayment_amount
    extra_amount = total_amount - regular_payment
    if extra_amount <= 0:
        # Если пользователь ввёл сумму, не превышающую обычный платёж,
        # досрочного погашения по сути нет.
        if hasattr(update, "message"):
            await update.message.reply_text(
                "Сумма должна быть больше обычного ежемесячного платежа, "
                "чтобы было досрочное погашение."
            )
        else:
            await update.callback_query.edit_message_text(
                "Сумма должна быть больше обычного ежемесячного платежа, "
                "чтобы было досрочное погашение."
            )
        return

    repayment = EarlyRepayment(
        amount=extra_amount,
        strategy=strategy,
        execute_after_payments=session.payments_made,
    )
    result = calculator.apply_early_repayment(
        base_schedule, repayment, session.payments_made
    )
    response = format_early_result(result)
    keyboard = get_main_menu_keyboard()
    if hasattr(update, "message"):
        await update.message.reply_text(
            response, parse_mode="Markdown", reply_markup=keyboard
        )
        user_id = update.effective_user.id
    else:
        await update.callback_query.edit_message_text(
            response, parse_mode="Markdown", reply_markup=keyboard
        )
        user_id = update.effective_user.id

    # Полный рестарт после показа результата
    sessions.reset(user_id)

