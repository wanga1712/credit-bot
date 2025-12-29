"""Реализация стратегий перерасчёта графика."""

from __future__ import annotations

from .helpers import (
    annual_from_monthly,
    build_schedule,
    ensure_positive,
    original_payment,
    remaining_principal,
    round_money,
)
from .models import EarlyRepayment, PaymentSchedule
from .payment_logic import calculate_annuity_payment


def reduce_term(
    balance: float,
    repayment_amount: float,
    monthly_percent: float,
    monthly_payment: float,
) -> PaymentSchedule:
    """Сохраняем платёж, сокращаем срок."""

    new_balance = round_money(max(balance - repayment_amount, 0.0))
    if new_balance == 0:
        return PaymentSchedule(payments=[])
    ensure_positive(monthly_payment, "monthly_payment")
    return build_schedule(new_balance, monthly_percent, monthly_payment)


def reduce_payment(
    balance: float,
    repayment_amount: float,
    monthly_percent: float,
    months_left: int,
) -> PaymentSchedule:
    """Сохраняем срок, уменьшаем платёж."""

    ensure_positive(months_left, "months_left")
    new_balance = round_money(max(balance - repayment_amount, 0.0))
    if new_balance == 0:
        return PaymentSchedule(payments=[])
    annual_rate = annual_from_monthly(monthly_percent)
    new_payment = calculate_annuity_payment(new_balance, months_left, annual_rate)
    return build_schedule(
        new_balance,
        monthly_percent,
        new_payment,
        months_limit=months_left,
    )


def payment_then_term(
    balance: float,
    repayment: EarlyRepayment,
    monthly_percent: float,
    months_left: int,
) -> PaymentSchedule:
    """Сначала уменьшаем платёж, затем срок."""

    if not repayment.secondary_amount:
        raise ValueError("Для комбинированной стратегии нужна вторая сумма.")

    intermediate = reduce_payment(
        balance,
        repayment.amount,
        monthly_percent,
        months_left,
    )
    if not intermediate.payments:
        return PaymentSchedule(payments=[])
    new_balance = remaining_principal(intermediate, 0)
    new_payment_value = original_payment(intermediate)
    return reduce_term(
        new_balance,
        repayment.secondary_amount,
        monthly_percent,
        monthly_payment=new_payment_value,
    )


def term_then_payment(
    balance: float,
    repayment: EarlyRepayment,
    monthly_percent: float,
    months_left: int,
    monthly_payment: float,
    payments_made: int,
) -> tuple[PaymentSchedule, float]:
    """Сначала уменьшаем срок, затем платёж (с двумя датами)."""

    if not repayment.secondary_amount:
        raise ValueError("Для комбинированной стратегии нужна вторая сумма.")
    if repayment.secondary_execute_after_payments is None:
        raise ValueError("Для комбинированной стратегии нужна вторая дата.")

    after_term = reduce_term(
        balance,
        repayment.amount,
        monthly_percent,
        monthly_payment,
    )
    delta = repayment.secondary_execute_after_payments - payments_made
    if delta < 0:
        raise ValueError("Вторая дата должна быть позже первой.")
    if not after_term.payments:
        return PaymentSchedule(payments=[]), 0.0
    if delta > after_term.months:
        raise ValueError("Вторая дата превышает длительность графика.")

    interest_between = 0.0
    if delta > 0:
        interest_between = sum(
            payment.interest_amount for payment in after_term.payments[:delta]
        )

    balance_after = remaining_principal(after_term, delta)
    months_after = after_term.months - delta
    if months_after <= 0:
        raise ValueError("Не осталось платежей для второй операции.")

    schedule = reduce_payment(
        balance_after,
        repayment.secondary_amount,
        monthly_percent,
        months_after,
    )
    return schedule, interest_between

