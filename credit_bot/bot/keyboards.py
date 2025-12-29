"""Inline-кнопки для Telegram-бота."""

from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру главного меню."""

    keyboard = [
        [
            InlineKeyboardButton("📊 Рассчитать график", callback_data="action:schedule"),
        ],
        [
            InlineKeyboardButton("💰 Уменьшить платеж", callback_data="action:reduce_payment"),
        ],
        [
            InlineKeyboardButton("⏱️ Уменьшить срок", callback_data="action:reduce_term"),
        ],
        [
            InlineKeyboardButton(
                "🔁 Уменьшить срок и платёж", callback_data="action:combined"
            ),
        ],
        [
            InlineKeyboardButton(
                "🎯 Подобрать платеж для переплаты", callback_data="action:payment"
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_strategy_keyboard() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру выбора стратегии досрочного погашения."""

    keyboard = [
        [
            InlineKeyboardButton("Уменьшить срок", callback_data="strategy:reduce_term"),
        ],
        [
            InlineKeyboardButton("Уменьшить платеж", callback_data="strategy:reduce_payment"),
        ],
        [
            InlineKeyboardButton("Платёж → срок", callback_data="strategy:combo_pt"),
        ],
        [
            InlineKeyboardButton("Срок → платёж", callback_data="strategy:combo_tp"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

