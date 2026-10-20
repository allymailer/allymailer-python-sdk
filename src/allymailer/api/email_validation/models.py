"""Models of the EmailValidation section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict

__all__ = ["EmailValidationSingleRequest", "EmailValidationSingleResponse"]


@dataclass
class EmailValidationSingleRequest:
    """EmailValidationSingleRequest"""

    email: str
    """Email-адреса, яку необхідно перевірити."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailValidationSingleRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EmailValidationSingleResponse:
    """EmailValidationSingleResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    email: Optional[str] = None
    """Email, що перевіряється."""

    result: Optional[str] = None
    """Можливі статуси:

    - "valid" - email-адреса дійсна,
    - "invalid" - email-адреса недійсна,
    - "suspicious" - email-адреса підозріла,
    - "unknown" - адресу не вдалося перевірити. Приймаючий сервер не відповів у межах припустимого часу перевірки.
    """

    cause: Optional[str] = None
    """Можливі статуси:

    - "no_mx_record" - у домену відсутні MX-записи,
    - "syntax_error" - адреса не відповідає стандартам email,
    - "possible_typo" - можливо, адресу введено з помилкою,
    - "mailbox_not_found" - адреса не існує,
    - "global_suppression" - адреса перманентно недоступна в сервісі через багаторазові недоставки,
    - "disposable" - одноразовий email, зазвичай такі адреси приймають пошту лише декілька хвилин,
    - "role" - загальна адреса електронної пошти, найчастіше використовується групою людей і не належить конкретній особі,
    - "abuse" - адреси, з яких надходить велика кількість скарг і натискань на "спам", іноді навіть в автоматичному режимі,
    - "spamtrap" - адреси-спам-пастки, зазвичай розміщуються поштовими провайдерами у відкритому доступі, але ніколи не використовуються для підписки. Надсилання листів на такі адреси сильно шкодить репутації відправника,
    - "smtp_connection_failed" - SMTP-сервер недоступний — можливо, адресу введено з помилкою.
    """

    validity: Optional[int] = None
    """Імовірність того, що адреса дійсна. Від 0 до 100 (100 - дійсна, 0 - недійсна)."""

    local_part: Optional[str] = None
    """Локальна частина email-адреси (усе, що перед знаком "@")."""

    domain: Optional[str] = None
    """Доменна частина email-адреси."""

    mx_found: Optional[bool] = None
    """Чи є у домену MX-запис? true якщо є, false якщо відсутній."""

    mx_record: Optional[str] = None
    """Бажана MX-запис домену."""

    did_you_mean: Optional[str] = None
    """Можлива адреса, отримана після виправлення помилки (для cause=possible_typo)."""

    processed_at: Optional[str] = None
    """Дата й час перевірки адреси у форматі РРРР-ММ-ДД гг:хх:сс у часовому поясі UTC."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailValidationSingleResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            email=data.get("email"),
            result=data.get("result"),
            cause=data.get("cause"),
            validity=data.get("validity"),
            local_part=data.get("local_part"),
            domain=data.get("domain"),
            mx_found=data.get("mx_found"),
            mx_record=data.get("mx_record"),
            did_you_mean=data.get("did_you_mean"),
            processed_at=data.get("processed_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "email": self.email,
            "result": self.result,
            "cause": self.cause,
            "validity": self.validity,
            "local_part": self.local_part,
            "domain": self.domain,
            "mx_found": self.mx_found,
            "mx_record": self.mx_record,
            "did_you_mean": self.did_you_mean,
            "processed_at": self.processed_at,
        }
        return {k: v for k, v in result.items() if v is not None}
