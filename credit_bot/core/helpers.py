"""Вспомогательные функции для расчётов кредитного калькулятора."""

from __future__ import annotations

from typing import List, Optional

from loguru import logger

from .models import Payment, PaymentSchedule

MONTHS_IN_YEAR = 12
EPSILON = 1e-9


def ensure_positive(value: float, name: str) -> None:
    """Проверяет, что числовой параметр больше нуля."""

    if value <= 0:
        raise ValueError(f"Параметр '{name}' должен быть положительным.")


def monthly_rate(annual_percent: float) -> float:
    """Возвращает месячную ставку в долях единицы."""

    if annual_percent < 0:
        raise ValueError("Ставка не может быть отрицательной.")
    return annual_percent / 100 / MONTHS_IN_YEAR


def annual_from_monthly(monthly_percent: float) -> float:
    """Переводит месячную ставку в годовую (в процентах)."""

    if monthly_percent < 0:
        raise ValueError("Ставка не может быть отрицательной.")
    return monthly_percent * MONTHS_IN_YEAR * 100


def round_money(value: float) -> float:
    """Округляет денежное значение до копеек."""

    return round(value + EPSILON, 2)


def build_schedule(
    principal: float,
    monthly_percent: float,
    monthly_payment: float,
    months_limit: Optional[int] = None,
) -> PaymentSchedule:
    """Формирует график платежей при фиксированном платеже."""

    if principal <= EPSILON:
        return PaymentSchedule(payments=[])
    ensure_positive(monthly_payment, "monthly_payment")
    payments: List[Payment] = []
    balance = principal
    month = 1

    while balance > EPSILON:
        interest = round_money(balance * monthly_percent)
        principal_part = round_money(monthly_payment - interest)
        if principal_part <= 0:
            logger.error("Платёж не покрывает проценты, расчёт невозможен.")
            raise ValueError("Размер платежа должен покрывать проценты.")
        if principal_part > balance or (
            months_limit and month == months_limit and principal_part < balance
        ):
            principal_part = balance
            payment_value = round_money(principal_part + interest)
        else:
            payment_value = round_money(monthly_payment)
        balance = round_money(balance - principal_part)
        payments.append(
            Payment(
                number=month,
                date=None,
                payment_amount=payment_value,
                principal_amount=principal_part,
                interest_amount=interest,
                remaining_principal=max(balance, 0.0),
            )
        )
        month += 1
        if months_limit and month > months_limit and balance > EPSILON:
            raise ValueError("Не удалось погасить кредит за указанный срок.")

    return PaymentSchedule(payments=payments)


def remaining_principal(schedule: PaymentSchedule, payments_made: int) -> float:
    """Возвращает остаток долга после указанного количества платежей."""

    if not schedule.payments:
        return 0.0
    if payments_made <= 0:
        first = schedule.payments[0]
        return round_money(first.principal_amount + first.remaining_principal)
    if payments_made >= schedule.months:
        return 0.0
    prev_payment = schedule.payments[payments_made - 1]
    return round_money(prev_payment.remaining_principal)


def original_payment(schedule: PaymentSchedule) -> float:
    """Возвращает размер аннуитетного платежа из графика."""

    if not schedule.payments:
        raise ValueError("График пуст, платеж не задан.")
    first = schedule.payments[0]
    return round_money(first.payment_amount)


def infer_monthly_percent(schedule: PaymentSchedule) -> float:
    """Определяет месячную процентную ставку из графика."""

    first = schedule.payments[0]
    base = first.principal_amount + first.remaining_principal
    if base <= 0:
        raise ValueError("Невозможно вычислить ставку из графика.")
    if first.interest_amount == 0:
        return 0.0
    return first.interest_amount / base

