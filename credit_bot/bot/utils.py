"""Вспомогательные функции для обработчиков."""

from __future__ import annotations


def parse_float(text: str) -> float | None:
    """Парсит число с плавающей точкой."""

    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def parse_int(text: str) -> int | None:
    """Парсит целое число."""

    try:
        return int(text)
    except ValueError:
        return None

