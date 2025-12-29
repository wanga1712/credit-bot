"""Определения состояний диалога Telegram-бота."""

from __future__ import annotations


(
    ENTER_LOAN_AMOUNT,
    ENTER_LOAN_TERM,
    ENTER_INTEREST_RATE,
    CHOOSE_ACTION,
    ENTER_PAYMENTS_MADE,
    ENTER_EARLY_REPAYMENT_AMOUNT,
    ENTER_STRATEGY,
    ENTER_SECOND_AMOUNT,
    ENTER_SECOND_PAYMENTS,
    ENTER_TARGET_OVERPAYMENT,
    ENTER_TOLERANCE,
) = range(11)


ACTION_CALCULATE_SCHEDULE = "schedule"
ACTION_EARLY_REPAYMENT = "early"
ACTION_TARGET_OVERPAYMENT = "payment"


STRATEGY_LABELS = {
    "term": "Сократить срок",
    "payment": "Сократить платёж",
    "combo_pt": "Платёж -> срок",
    "combo_tp": "Срок -> платёж",
}

