"""Консольная песочница для проверки логики CreditCalculator."""

from __future__ import annotations

from loguru import logger

from credit_bot import CreditCalculator
from credit_bot.core.models import EarlyRepayment, EarlyRepaymentStrategy


def ask_float(prompt: str) -> float:
    """Запрашивает у пользователя число с плавающей точкой."""

    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Введите корректное число.")


def ask_int(prompt: str) -> int:
    """Запрашивает целое число."""

    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def main() -> None:
    """Точка входа CLI."""

    calculator = CreditCalculator()
    print("=== Демонстрация кредитного калькулятора ===")
    try:
        amount = ask_float("Сумма кредита: ")
        term = ask_int("Срок в месяцах: ")
        rate = ask_float("Годовая ставка (%): ")

        schedule = calculator.generate_payment_schedule(amount, term, rate)
        print(f"Ежемесячный платёж: {schedule.payments[0].payment_amount:.2f} ₽")
        print(f"Переплата за весь срок: {schedule.total_interest:.2f} ₽")

        payment_option = input("Подобрать платёж под переплату? (y/n): ").lower()
        if payment_option == "y":
            target_overpayment = ask_float("Желаемая переплата: ")
            tolerance_raw = input("Допустимое отклонение (по умолчанию 100): ").strip()
            tolerance = float(tolerance_raw.replace(",", ".")) if tolerance_raw else 100.0
            payment_plan = calculator.calculate_payment_by_target_overpayment(
                amount=amount,
                annual_interest_rate=rate,
                target_overpayment=target_overpayment,
                tolerance=tolerance,
            )
            print("--- Подбор платежа ---")
            print(f"Платёж: {payment_plan['payment']:.2f} ₽")
            print(f"Переплата: {payment_plan['overpayment']:.2f} ₽")
            print(f"Срок (мес.): {int(payment_plan['months'])}")

        choice = input("Рассчитать досрочное погашение? (y/n): ").lower()
        if choice == "y":
            repayments_done = ask_int("Сколько платежей уже сделано?: ")
            repay_sum = ask_float("Сумма досрочного платежа: ")
            strategy_input = input(
                "Стратегия (term/payment/combo_pt/combo_tp): "
            ).strip().lower()
            strategy_map = {
                "term": EarlyRepaymentStrategy.REDUCE_TERM,
                "payment": EarlyRepaymentStrategy.REDUCE_PAYMENT,
                "combo_pt": EarlyRepaymentStrategy.COMBINED_PAYMENT_THEN_TERM,
                "combo_tp": EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT,
            }
            strategy = strategy_map.get(strategy_input)
            if not strategy:
                print("Неизвестная стратегия, пропуск.")
                return
            second_amount = None
            second_payments = None
            if strategy in (
                EarlyRepaymentStrategy.COMBINED_PAYMENT_THEN_TERM,
                EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT,
            ):
                second_amount = ask_float("Вторая сумма досрочного платежа: ")
            if strategy == EarlyRepaymentStrategy.COMBINED_TERM_THEN_PAYMENT:
                second_payments = ask_int(
                    "Сколько платежей будет сделано ко второму погашению?: "
                )
            repayment = EarlyRepayment(
                amount=repay_sum,
                strategy=strategy,
                execute_after_payments=repayments_done,
                secondary_amount=second_amount,
                secondary_execute_after_payments=second_payments,
            )
            result = calculator.apply_early_repayment(schedule, repayment, repayments_done)
            new_schedule = result["schedule"]
            print("--- Новый график ---")
            if new_schedule.payments:
                print(f"Новый платёж: {new_schedule.payments[0].payment_amount:.2f} ₽")
            print(f"Переплата после досрочки: {result['total_interest']:.2f} ₽")
            print(f"Проценты до досрочки: {result['interest_before']:.2f} ₽")
            print(f"Новый срок (мес.): {new_schedule.months}")
    except ValueError as exc:
        logger.error("Ошибка ввода: {}", exc)
        print("Не удалось выполнить расчёт, проверьте введённые данные.")


if __name__ == "__main__":
    main()

