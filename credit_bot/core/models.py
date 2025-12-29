"""Доменные модели, используемые в ядре кредитного калькулятора."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List, Optional


class PaymentType(str, Enum):
    """Типы расчёта платежей."""

    ANNUITY = "annuity"
    DIFFERENTIATED = "differentiated"


class EarlyRepaymentStrategy(str, Enum):
    """Стратегии досрочного погашения."""

    REDUCE_TERM = "reduce_term"
    REDUCE_PAYMENT = "reduce_payment"
    COMBINED_PAYMENT_THEN_TERM = "combined_payment_then_term"
    COMBINED_TERM_THEN_PAYMENT = "combined_term_then_payment"


@dataclass(frozen=True, slots=True)
class Loan:
    """Входные параметры кредитного продукта."""

    amount: float
    term_months: int
    annual_interest_rate: float
    payment_type: PaymentType = PaymentType.ANNUITY


@dataclass(frozen=True, slots=True)
class Payment:
    """Строка графика платежей."""

    number: int
    date: Optional[date]
    payment_amount: float
    principal_amount: float
    interest_amount: float
    remaining_principal: float


@dataclass(frozen=True, slots=True)
class PaymentSchedule:
    """Полный график платежей с агрегирующими свойствами."""

    payments: List[Payment]

    @property
    def total_paid(self) -> float:
        """Возвращает общую сумму выплат."""

        return sum(p.payment_amount for p in self.payments)

    @property
    def total_interest(self) -> float:
        """Возвращает суммарные проценты."""

        return sum(p.interest_amount for p in self.payments)

    @property
    def months(self) -> int:
        """Возвращает количество месяцев в графике."""

        return len(self.payments)


@dataclass(frozen=True, slots=True)
class EarlyRepayment:
    """Данные о досрочном погашении."""

    amount: float
    strategy: EarlyRepaymentStrategy
    execute_after_payments: int
    secondary_amount: Optional[float] = None
    secondary_execute_after_payments: Optional[int] = None

