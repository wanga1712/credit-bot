"""Поиск суммы досрочного платежа под целевую переплату."""

from __future__ import annotations

from loguru import logger

from .early_repayment import apply_early_repayment
from .helpers import ensure_positive
from .models import EarlyRepayment
from .payment_logic import generate_payment_schedule


def find_optimal_strategy_by_overpayment(
    amount: float,
    term_months: int,
    annual_interest_rate: float,
    target_overpayment: float,
    repayment_strategy: EarlyRepayment,
    tolerance: float,
) -> dict[str, object]:
    """Выполняет бинарный поиск по сумме досрочного платежа."""

    try:
        ensure_positive(target_overpayment, "target_overpayment")
        base_schedule = generate_payment_schedule(amount, term_months, annual_interest_rate)
        base_interest = base_schedule.total_interest
        if base_interest <= target_overpayment:
            return {
                "early_repayment": 0.0,
                "overpayment": base_interest,
                "schedule": base_schedule,
            }

        low, high = 0.0, amount
        best_result: dict[str, object] | None = None
        best_diff = float("inf")

        while high - low > 1:
            mid = (low + high) / 2
            candidate = EarlyRepayment(
                amount=mid,
                strategy=repayment_strategy.strategy,
                execute_after_payments=repayment_strategy.execute_after_payments,
                secondary_amount=repayment_strategy.secondary_amount,
            )
            recalculated = apply_early_repayment(
                current_schedule=base_schedule,
                repayment=candidate,
                payments_made=repayment_strategy.execute_after_payments,
            )
            overpayment = recalculated["total_interest"]
            diff = overpayment - target_overpayment
            abs_diff = abs(diff)
            if abs_diff < best_diff:
                best_diff = abs_diff
                best_result = {
                    "early_repayment": mid,
                    "overpayment": overpayment,
                    "schedule": recalculated["schedule"],
                }
            if abs_diff <= tolerance:
                break
            if diff > 0:
                low = mid
            else:
                high = mid

        return best_result or {
            "early_repayment": 0.0,
            "overpayment": base_interest,
            "schedule": base_schedule,
        }
    except ValueError:
        logger.exception("Ошибка при поиске оптимальной стратегии.")
        raise

