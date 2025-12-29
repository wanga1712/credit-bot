"""Форматирование ответов Telegram-бота."""

from __future__ import annotations

from credit_bot.core.models import PaymentSchedule


def format_schedule(schedule: PaymentSchedule) -> str:
    """Возвращает текст с ключевыми показателями графика."""

    if not schedule.payments:
        return "Кредит погашён полностью."
    payment = schedule.payments[0].payment_amount
    body = [
        "*График платежей*",
        f"• Платёж: `{payment:.2f}` ₽",
        f"• Переплата: `{schedule.total_interest:.2f}` ₽",
        f"• Срок: `{schedule.months}` мес.",
    ]
    return "\n".join(body)


def format_early_result(result: dict) -> str:
    """Описывает перерасчёт после досрочного платежа."""

    schedule = result["schedule"]
    body = ["*Досрочное погашение*", f"• Проценты до досрочки: `{result['interest_before']:.2f}` ₽"]
    if schedule.payments:
        body.append(f"• Новый платёж: `{schedule.payments[0].payment_amount:.2f}` ₽")
    body.append(f"• Новая переплата: `{result['total_interest']:.2f}` ₽")
    body.append(f"• Новый срок: `{schedule.months}` мес.")
    return "\n".join(body)


def format_payment_plan(plan: dict) -> str:
    """Формирует ответ для режима подбора платежа."""

    body = [
        "*Подбор платежа*",
        f"• Платёж: `{plan['payment']:.2f}` ₽",
        f"• Переплата: `{plan['overpayment']:.2f}` ₽",
        f"• Срок: `{int(plan['months'])}` мес.",
    ]
    return "\n".join(body)

