"""Models of the Obsolete section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of, to_enum

__all__ = ["ObsoleteUnsubscribedSetMessage", "ObsoleteUnsubscribedSetRequest", "ObsoleteUnsubscribedSetResponse", "ObsoleteUnsubscribedCheckRequest", "ObsoleteUnsubscribedCheckResponse", "ObsoleteUnsubscribedListRequest", "ObsoleteUnsubscribedListResponse", "ObsoleteUnsubscribedListResponseUnsubscribedItem"]


class ObsoleteUnsubscribedSetMessage(str, Enum):
    """Подробиці відписки:

    - "unsubscribed" якщо email було щойно відписано,
    - "was inactive" якщо він уже був позначений як неактивний і немає сенсу відписувати,
    - "was unsubscribed" якщо email уже було відписано раніше,
    - "added and unsubscribed" якщо для цього email не зберігалося жодного більш раннього статусу, тому його було додано й одразу ж відписано.
    """

    UNSUBSCRIBED = "unsubscribed"
    WAS_INACTIVE = "was inactive"
    WAS_UNSUBSCRIBED = "was unsubscribed"
    ADDED_AND_UNSUBSCRIBED = "added and unsubscribed"


@dataclass
class ObsoleteUnsubscribedSetRequest:
    """ObsoleteUnsubscribedSetRequest"""

    address: str
    """Email, який має бути відписано."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedSetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            address=data.get("address"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "address": self.address,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedSetResponse:
    """ObsoleteUnsubscribedSetResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    address: Optional[str] = None
    """Відписаний email."""

    message: Optional[ObsoleteUnsubscribedSetMessage] = None
    """Подробиці відписки:

    - "unsubscribed" якщо email було щойно відписано,
    - "was inactive" якщо він уже був позначений як неактивний і немає сенсу відписувати,
    - "was unsubscribed" якщо email уже було відписано раніше,
    - "added and unsubscribed" якщо для цього email не зберігалося жодного більш раннього статусу, тому його було додано й одразу ж відписано.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedSetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            address=data.get("address"),
            message=to_enum(ObsoleteUnsubscribedSetMessage, data.get("message")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "address": self.address,
            "message": self.message,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedCheckRequest:
    """ObsoleteUnsubscribedCheckRequest"""

    address: str
    """Email, який необхідно перевірити."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedCheckRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            address=data.get("address"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "address": self.address,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedCheckResponse:
    """ObsoleteUnsubscribedCheckResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    address: Optional[str] = None
    """Email, який було перевірено."""

    is_unsubscribed: Optional[bool] = None
    """true якщо відписано, false якщо ні."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedCheckResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            address=data.get("address"),
            is_unsubscribed=data.get("is_unsubscribed"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "address": self.address,
            "is_unsubscribed": self.is_unsubscribed,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedListRequest:
    """ObsoleteUnsubscribedListRequest"""

    date_from: Optional[str] = None
    """Дата у форматі РРРР-ММ-ДД, щоб отримати всі відписані адреси з "date_from" по сьогоднішній день.
    Якщо параметр не вказати, період за замовчуванням буде з 00:00 сьогоднішнього дня за UTC.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            date_from=data.get("date_from"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "date_from": self.date_from,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedListResponse:
    """ObsoleteUnsubscribedListResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    unsubscribed: Optional[List[ObsoleteUnsubscribedListResponseUnsubscribedItem]] = None
    """Масив об'єктів з даними відписаних."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            unsubscribed=list_of(data.get("unsubscribed"), lambda item0: model_of(ObsoleteUnsubscribedListResponseUnsubscribedItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "unsubscribed": [item0.to_dict() for item0 in self.unsubscribed] if self.unsubscribed is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedListResponseUnsubscribedItem:
    """ObsoleteUnsubscribedListResponseUnsubscribedItem"""

    address: Optional[str] = None
    """Відписаний email."""

    unsubscribed_on: Optional[str] = None
    """Дата й час відписки адреси у форматі РРРР-ММ-ДД гг:хх:сс у часовому поясі UTC."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedListResponseUnsubscribedItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            address=data.get("address"),
            unsubscribed_on=data.get("unsubscribed_on"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "address": self.address,
            "unsubscribed_on": self.unsubscribed_on,
        }
        return {k: v for k, v in result.items() if v is not None}
