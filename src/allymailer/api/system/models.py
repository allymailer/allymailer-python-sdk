"""Models of the System section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, model_of, to_enum

from allymailer.common import EmailCounterMode

__all__ = ["SystemPingResponse", "SystemInfoResponse", "ProjectAccountingObject", "SystemInfoResponseAccounting"]


@dataclass
class SystemPingResponse:
    """SystemPingResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    user_id: Optional[int] = None
    """Унікальний ідентифікатор користувача."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SystemPingResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            user_id=data.get("user_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "user_id": self.user_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SystemInfoResponse:
    """SystemInfoResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    user_id: Optional[int] = None
    """Унікальний ідентифікатор користувача."""

    email: Optional[str] = None
    """Email користувача."""

    project_id: Optional[str] = None
    """Унікальний ідентифікатор проєкту, ASCII-рядок до 36 символів завдовжки. Присутній лише якщо
    API-ключ, використаний для запиту, був API-ключем проєкту.
    """

    project_name: Optional[str] = None
    """Назва проєкту, унікальна в межах облікового запису користувача. Присутня лише якщо API-ключ,
    використаний для запиту, був API-ключем проєкту.
    """

    project_accounting: Optional[ProjectAccountingObject] = None
    """Об'єкт із властивостями лічильника листів. Присутній лише якщо API-ключ, використаний для запиту,
    був API-ключем проєкту.
    """

    accounting: Optional[SystemInfoResponseAccounting] = None
    """Об'єкт з властивостями періоду обліку. Присутній лише якщо API-ключ, використаний для запиту, був
    API-ключем користувача.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SystemInfoResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            user_id=data.get("user_id"),
            email=data.get("email"),
            project_id=data.get("project_id"),
            project_name=data.get("project_name"),
            project_accounting=model_of(ProjectAccountingObject, data.get("project_accounting")),
            accounting=model_of(SystemInfoResponseAccounting, data.get("accounting")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "user_id": self.user_id,
            "email": self.email,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "project_accounting": self.project_accounting.to_dict() if self.project_accounting is not None else None,
            "accounting": self.accounting.to_dict() if self.accounting is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectAccountingObject:
    """Об'єкт із властивостями лічильника листів. Присутній лише якщо API-ключ, використаний для запиту,
    був API-ключем проєкту.
    """

    email_counter: Optional[int] = None
    """Значення лічильника листів для проєкту, збільшується під час надсилання кожного листа."""

    email_counter_limit: Optional[int] = None
    """Дозволяє обмежити кількість надісланих проєктом листів. У разі досягнення цього ліміту надсилання
    припиняється. Значення 0 (за замовчуванням) означає відсутність ліміту.
    """

    email_counter_mode: Optional[EmailCounterMode] = None
    """'default' - лічильник автоматично скидається в нуль на початку кожного облікового періоду,
    'permanent' - лічильник ніколи не скидається автоматично.
    За замовчуванням: `default`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectAccountingObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email_counter=data.get("email_counter"),
            email_counter_limit=data.get("email_counter_limit"),
            email_counter_mode=to_enum(EmailCounterMode, data.get("email_counter_mode")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email_counter": self.email_counter,
            "email_counter_limit": self.email_counter_limit,
            "email_counter_mode": self.email_counter_mode,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SystemInfoResponseAccounting:
    """Об'єкт з властивостями періоду обліку. Присутній лише якщо API-ключ, використаний для запиту, був
    API-ключем користувача.
    """

    period_start: Optional[str] = None
    """Дата й час початку періоду обліку в часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс"."""

    period_end: Optional[str] = None
    """Дата й час кінця періоду обліку в часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс"."""

    emails_included: Optional[int] = None
    """Кількість листів, включених в обліковий період."""

    emails_sent: Optional[int] = None
    """Кількість листів, надісланих за обліковий період. Може бути більшою за emails_included у разі
    перевищення.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SystemInfoResponseAccounting:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            period_start=data.get("period_start"),
            period_end=data.get("period_end"),
            emails_included=data.get("emails_included"),
            emails_sent=data.get("emails_sent"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "period_start": self.period_start,
            "period_end": self.period_end,
            "emails_included": self.emails_included,
            "emails_sent": self.emails_sent,
        }
        return {k: v for k, v in result.items() if v is not None}
