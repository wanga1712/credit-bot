"""Регистрация обработчиков для Telegram-бота."""

from __future__ import annotations

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from credit_bot.bot.handlers import cancel, choose_action, handle_callback, start
from credit_bot.bot.input_handlers import (
    calculate_start,
    enter_interest_rate,
    enter_loan_amount,
    enter_loan_term,
)
from credit_bot.bot.early_repayment_handlers import (
    enter_early_repayment_amount,
    enter_payments_made,
    enter_strategy,
    handle_strategy_callback,
)
from credit_bot.bot.combined_strategy import enter_second_amount, enter_second_payments
from credit_bot.bot.payment_search_handlers import (
    enter_target_overpayment,
    enter_tolerance,
)
from credit_bot.bot.states import (
    CHOOSE_ACTION,
    ENTER_EARLY_REPAYMENT_AMOUNT,
    ENTER_INTEREST_RATE,
    ENTER_LOAN_AMOUNT,
    ENTER_LOAN_TERM,
    ENTER_PAYMENTS_MADE,
    ENTER_SECOND_AMOUNT,
    ENTER_SECOND_PAYMENTS,
    ENTER_STRATEGY,
    ENTER_TARGET_OVERPAYMENT,
    ENTER_TOLERANCE,
)


def register_handlers(application: Application) -> None:
    """Регистрирует все обработчики команд и сообщений."""

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("calculate", calculate_start),
            CallbackQueryHandler(handle_callback, pattern="^action:"),
        ],
        per_message=False,
        per_chat=True,
        per_user=True,
        states={
            ENTER_LOAN_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_loan_amount)
            ],
            ENTER_LOAN_TERM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_loan_term)
            ],
            ENTER_INTEREST_RATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_interest_rate)
            ],
            CHOOSE_ACTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, choose_action),
                CallbackQueryHandler(handle_callback, pattern="^action:"),
            ],
            ENTER_PAYMENTS_MADE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_payments_made)
            ],
            ENTER_EARLY_REPAYMENT_AMOUNT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, enter_early_repayment_amount
                )
            ],
            ENTER_STRATEGY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_strategy),
                CallbackQueryHandler(handle_strategy_callback, pattern="^strategy:"),
            ],
            ENTER_SECOND_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_second_amount)
            ],
            ENTER_SECOND_PAYMENTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_second_payments)
            ],
            ENTER_TARGET_OVERPAYMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_target_overpayment)
            ],
            ENTER_TOLERANCE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_tolerance)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
