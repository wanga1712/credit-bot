"""Тесты для ядра кредитного калькулятора."""

import pytest

from .calculator import CreditCalculator
from .models import EarlyRepayment, EarlyRepaymentStrategy


@pytest.fixture()
def calculator() -> CreditCalculator:
    return CreditCalculator()


def test_calculate_annuity_payment_known_value(calculator: CreditCalculator) -> None:
    """Проверяет совпадение аннуитетного платежа с эталоном."""

    payment = calculator.calculate_annuity_payment(1_000_000, 60, 10.0)
    assert payment == pytest.approx(21247.05, abs=0.1)


def test_generate_payment_schedule_totals(calculator: CreditCalculator) -> None:
    """Проверяет корректность сумм в графике."""

    schedule = calculator.generate_payment_schedule(500_000, 24, 11.0)
    assert schedule.months == 24
    principal_total = sum(p.principal_amount for p in schedule.payments)
    assert principal_total == pytest.approx(500_000, abs=1.0)


def test_apply_early_repayment_reduce_term(calculator: CreditCalculator) -> None:
    """Проверяет сокращение срока при досрочке."""

    schedule = calculator.generate_payment_schedule(700_000, 36, 12.0)
    repayment = EarlyRepayment(
        amount=150_000,
        strategy=EarlyRepaymentStrategy.REDUCE_TERM,
        execute_after_payments=6,
    )
    recalculated = calculator.apply_early_repayment(schedule, repayment, 6)
    assert recalculated["months"] < schedule.months - 6


def test_apply_early_repayment_term_then_payment(calculator: CreditCalculator) -> None:
    """Проверяет комбинированную стратегию с двумя датами."""

    schedule = calculator.generate_payment_schedule(800_000, 48, 9.0)
    repayment = EarlyRepayment(
        amount=120_000,
        strategy=EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT,
        execute_after_payments=6,
        secondary_amount=80_000,
        secondary_execute_after_payments=12,
    )
    recalculated = calculator.apply_early_repayment(schedule, repayment, 6)
    assert recalculated["months"] < schedule.months - 6
    assert (
        recalculated["schedule"].payments[0].payment_amount
        < schedule.payments[0].payment_amount
    )


def test_find_optimal_strategy_by_overpayment(calculator: CreditCalculator) -> None:
    """Проверяет поиск суммы досрочки под целевую переплату."""

    repayment = EarlyRepayment(
        amount=0,
        strategy=EarlyRepaymentStrategy.REDUCE_PAYMENT,
        execute_after_payments=12,
    )
    result = calculator.find_optimal_strategy_by_overpayment(
        amount=900_000,
        term_months=48,
        annual_interest_rate=9.5,
        target_overpayment=150_000,
        repayment_strategy=repayment,
        tolerance=500.0,
    )
    assert abs(result["overpayment"] - 150_000) <= 500.0


def test_calculate_payment_by_target_overpayment(calculator: CreditCalculator) -> None:
    """Проверяет подбор платежа под заданную переплату."""

    result = calculator.calculate_payment_by_target_overpayment(
        amount=400_000,
        annual_interest_rate=12.0,
        target_overpayment=120_000,
        tolerance=1_000.0,
    )
    assert abs(result["overpayment"] - 120_000) <= 1_000.0
    assert result["payment"] > 0

