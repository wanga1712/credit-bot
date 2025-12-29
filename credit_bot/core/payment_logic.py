"""Расчёты аннуитетного платежа и базового графика."""

from __future__ import annotations

from loguru import logger

from .helpers import build_schedule, ensure_positive, monthly_rate, round_money
from .models import PaymentSchedule


def calculate_annuity_payment(
    amount: float,
    term_months: int,
    annual_interest_rate: float,
) -> float:
    """Возвращает аннуитетный платёж для заданных параметров."""

    try:
        ensure_positive(amount, "amount")
        ensure_positive(term_months, "term_months")
        if annual_interest_rate < 0:
            raise ValueError("Ставка не может быть отрицательной.")

        monthly_percent = monthly_rate(annual_interest_rate)
        if monthly_percent == 0:
            payment = amount / term_months
        else:
            factor = (1 + monthly_percent) ** term_months
            coefficient = monthly_percent * factor / (factor - 1)
            payment = amount * coefficient
        return round_money(payment)
    except ValueError:
        logger.exception("Ошибка при расчёте аннуитетного платежа.")
        raise
    except ZeroDivisionError as exc:
        logger.exception("Не удалось вычислить коэффициент аннуитета.")
        raise ValueError("Некорректные параметры для расчёта платежа.") from exc


def generate_payment_schedule(
    amount: float,
    term_months: int,
    annual_interest_rate: float,
) -> PaymentSchedule:
    """Формирует график платежей на основе аннуитетной схемы."""

    try:
        monthly_payment = calculate_annuity_payment(amount, term_months, annual_interest_rate)
        monthly_percent = monthly_rate(annual_interest_rate)
        return build_schedule(
            principal=amount,
            monthly_percent=monthly_percent,
            monthly_payment=monthly_payment,
            months_limit=term_months,
        )
    except ValueError:
        logger.exception("Ошибка при генерации графика платежей.")
        raise

