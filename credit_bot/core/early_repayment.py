"""Логика перерасчёта графика при досрочном погашении."""

from __future__ import annotations

from loguru import logger

from .helpers import (
    annual_from_monthly,
    ensure_positive,
    infer_monthly_percent,
    original_payment,
    remaining_principal,
)
from .models import EarlyRepayment, EarlyRepaymentStrategy, PaymentSchedule
from .repayment_strategies import (
    payment_then_term,
    reduce_payment,
    reduce_term,
    term_then_payment,
)


def apply_early_repayment(
    current_schedule: PaymentSchedule,
    repayment: EarlyRepayment,
    payments_made: int,
) -> dict[str, object]:
    """Пересчитывает график после досрочного платежа."""

    try:
        if not current_schedule.payments:
            raise ValueError("График платежей пуст.")
        if repayment.amount <= 0:
            raise ValueError("Сумма досрочного погашения должна быть положительной.")

        monthly_percent = infer_monthly_percent(current_schedule)
        annual_rate = annual_from_monthly(monthly_percent)
        balance = remaining_principal(current_schedule, payments_made)

        if balance <= 0:
            raise ValueError("Кредит уже погашён.")

        monthly_payment_value = original_payment(current_schedule)
        months_left = current_schedule.months - payments_made
        if months_left <= 0:
            raise ValueError("Не осталось платежей для пересчёта.")

        strategy = repayment.strategy
        interest_before = sum(
            payment.interest_amount for payment in current_schedule.payments[:payments_made]
        )

        extra_interest = 0.0

        if strategy == EarlyRepaymentStrategy.REDUCE_TERM:
            schedule = reduce_term(
                balance,
                repayment.amount,
                monthly_percent,
                monthly_payment_value,
            )
        elif strategy == EarlyRepaymentStrategy.REDUCE_PAYMENT:
            schedule = reduce_payment(
                balance,
                repayment.amount,
                monthly_percent,
                months_left,
            )
        elif strategy == EarlyRepaymentStrategy.COMBINED_PAYMENT_THEN_TERM:
            schedule = payment_then_term(
                balance,
                repayment,
                monthly_percent,
                months_left,
            )
        elif strategy == EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT:
            schedule, extra_interest = term_then_payment(
                balance,
                repayment,
                monthly_percent,
                months_left,
                monthly_payment_value,
                payments_made,
            )
        else:
            raise ValueError("Неизвестная стратегия досрочного погашения.")

        total_interest = interest_before + extra_interest + schedule.total_interest
        return {
            "schedule": schedule,
            "total_interest": total_interest,
            "interest_before": interest_before + extra_interest,
            "months": schedule.months,
            "annual_rate": annual_rate,
        }
    except ValueError:
        logger.exception("Ошибка при перерасчёте графика.")
        raise

