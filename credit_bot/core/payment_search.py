"""Подбор ежемесячного платежа под целевую переплату."""

from __future__ import annotations

from loguru import logger

from .helpers import build_schedule, ensure_positive, monthly_rate
from .payment_logic import calculate_annuity_payment


def find_payment_for_target_overpayment(
    amount: float,
    annual_interest_rate: float,
    target_overpayment: float,
    tolerance: float,
) -> dict[str, float]:
    """Бинарный поиск платежа, обеспечивающего заданную переплату."""

    try:
        ensure_positive(amount, "amount")
        ensure_positive(target_overpayment, "target_overpayment")
        if tolerance <= 0:
            raise ValueError("Допуск должен быть положительным.")

        monthly_percent = monthly_rate(annual_interest_rate)
        base_payment = calculate_annuity_payment(amount, 360, annual_interest_rate)
        low = max(base_payment, amount * monthly_percent + 1.0)
        high = max(low * 2, amount)

        def simulate(payment_value: float) -> tuple[float, int]:
            schedule = build_schedule(amount, monthly_percent, payment_value)
            return schedule.total_interest, schedule.months

        high_interest, high_months = simulate(high)
        while high_interest > target_overpayment and high < amount * 5:
            high *= 1.5
            high_interest, high_months = simulate(high)

        best = {"payment": high, "overpayment": high_interest, "months": high_months}
        best_diff = abs(high_interest - target_overpayment)

        for _ in range(60):
            mid = (low + high) / 2
            overpayment, months = simulate(mid)
            diff = overpayment - target_overpayment
            abs_diff = abs(diff)
            if abs_diff < best_diff:
                best = {"payment": mid, "overpayment": overpayment, "months": months}
                best_diff = abs_diff
            if abs_diff <= tolerance:
                break
            if diff > 0:
                low = mid
            else:
                high = mid

        return best
    except ValueError:
        logger.exception("Ошибка при подборе платежа под переплату.")
        raise

