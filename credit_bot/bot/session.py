"""Хранение временных данных диалога пользователя."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserSession:
    """Временные данные сессии пользователя."""

    loan_amount: Optional[float] = None
    term_months: Optional[int] = None
    annual_interest_rate: Optional[float] = None
    payments_made: Optional[int] = None
    early_repayment_amount: Optional[float] = None
    strategy: Optional[str] = None
    secondary_amount: Optional[float] = None
    secondary_payments: Optional[int] = None
    target_overpayment: Optional[float] = None
    tolerance: Optional[float] = None

    def reset(self) -> None:
        """Сбрасывает все поля сессии."""

        self.loan_amount = None
        self.term_months = None
        self.annual_interest_rate = None
        self.payments_made = None
        self.early_repayment_amount = None
        self.strategy = None
        self.secondary_amount = None
        self.secondary_payments = None
        self.target_overpayment = None
        self.tolerance = None


class SessionStorage:
    """Простое хранилище сессий в памяти."""

    def __init__(self) -> None:
        self._sessions: dict[int, UserSession] = {}

    def get(self, user_id: int) -> UserSession:
        """Возвращает сессию пользователя, создавая новую при необходимости."""

        if user_id not in self._sessions:
            self._sessions[user_id] = UserSession()
        return self._sessions[user_id]

    def reset(self, user_id: int) -> None:
        """Сбрасывает сессию пользователя."""

        if user_id in self._sessions:
            self._sessions[user_id].reset()


# Глобальное хранилище сессий, общее для всех модулей бота
sessions = SessionStorage()
