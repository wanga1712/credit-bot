"""Фасад над расчётными функциями ядра."""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List

from .early_repayment import apply_early_repayment
from .models import EarlyRepayment, PaymentSchedule
from .payment_logic import calculate_annuity_payment, generate_payment_schedule
from .payment_search import find_payment_for_target_overpayment
from .strategy_search import find_optimal_strategy_by_overpayment


class CreditCalculator:
    """Сервисный класс, объединяющий расчётные функции."""

    def calculate_annuity_payment(
        self,
        amount: float,
        term_months: int,
        annual_interest_rate: float,
    ) -> float:
        """Возвращает аннуитетный платёж."""

        return calculate_annuity_payment(amount, term_months, annual_interest_rate)

    def generate_payment_schedule(
        self,
        amount: float,
        term_months: int,
        annual_interest_rate: float,
    ) -> PaymentSchedule:
        """Генерирует график платежей."""

        return generate_payment_schedule(amount, term_months, annual_interest_rate)

    def apply_early_repayment(
        self,
        current_schedule: PaymentSchedule,
        repayment: EarlyRepayment,
        payments_made: int,
    ) -> Dict[str, object]:
        """Перерасчитывает график после досрочного платежа."""

        return apply_early_repayment(current_schedule, repayment, payments_made)

    def find_optimal_strategy_by_overpayment(
        self,
        amount: float,
        term_months: int,
        annual_interest_rate: float,
        target_overpayment: float,
        repayment_strategy: EarlyRepayment,
        tolerance: float = 100.0,
    ) -> Dict[str, object]:
        """Находит сумму досрочки под заданную переплату."""

        return find_optimal_strategy_by_overpayment(
            amount=amount,
            term_months=term_months,
            annual_interest_rate=annual_interest_rate,
            target_overpayment=target_overpayment,
            repayment_strategy=repayment_strategy,
            tolerance=tolerance,
        )

    def calculate_payment_by_target_overpayment(
        self,
        amount: float,
        annual_interest_rate: float,
        target_overpayment: float,
        tolerance: float = 100.0,
    ) -> Dict[str, float]:
        """Подбирает размер платежа для заданной переплаты."""

        return find_payment_for_target_overpayment(
            amount=amount,
            annual_interest_rate=annual_interest_rate,
            target_overpayment=target_overpayment,
            tolerance=tolerance,
        )


def schedule_to_dict(schedule: PaymentSchedule) -> List[Dict[str, object]]:
    """Преобразует график платежей в список словарей."""

    return [asdict(payment) for payment in schedule.payments]

