"""Models of the Suppression section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of

__all__ = ["SuppressionSetRequest", "SuppressionGetRequest", "SuppressionGetResponse", "SuppressionGetObject", "SuppressionListRequest", "SuppressionListResponse", "SuppressionListObject", "SuppressionDeleteRequest"]


@dataclass
class SuppressionSetRequest:
    """SuppressionSetRequest"""

    email: str
    """Email-адреса, яку потрібно додати до списку недоступних."""

    cause: str
    """Причина, з якої надсилання на цей email блокується. Одна з таких:

    - __unsubscribed__ - зазначену адресу відписано;
    - __temporary_unavailable__ - адреса тимчасово недоступна. Це означає, що протягом наступних трьох діб надсилання на цю адресу повертатиме помилку. Email може бути тимчасово недоступним з різних причин, наприклад:

    - попереднє надсилання було відхилено сервером отримувача як спам;
    - поштова скринька отримувача переповнена або не використовується;
    - домен не приймає пошту через неправильне налаштування на боці отримувача або з інших причин;
    - сервер відправника було відхилено через блеклистинг;

    - __permanent_unavailable__ - адреса перманентно недоступна через багаторазові недоставки;
    - __complained__ - в одному з попередніх листів адресат натиснув “Це спам”.
    """

    created: Optional[str] = None
    """Коли було встановлено недоступність, у часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс"."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionSetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
            cause=data.get("cause"),
            created=data.get("created"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
            "cause": self.cause,
            "created": self.created,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionGetRequest:
    """SuppressionGetRequest"""

    email: str
    """Email-адреса, для якої потрібно отримати дані про недоступність."""

    all_projects: Optional[bool] = None
    """Якщо у користувача увімкнено проєкти, all_projects=true дозволить шукати за даними всіх проєктів.
    За замовчуванням: `False`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionGetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
            all_projects=data.get("all_projects"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
            "all_projects": self.all_projects,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionGetResponse:
    """SuppressionGetResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    email: Optional[str] = None
    """Email-адреса, для якої було запитано дані про недоступність."""

    suppressions: Optional[List[SuppressionGetObject]] = None
    """Масив об'єктів з інформацією про недоступність."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionGetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            email=data.get("email"),
            suppressions=list_of(data.get("suppressions"), lambda item0: model_of(SuppressionGetObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "email": self.email,
            "suppressions": [item0.to_dict() for item0 in self.suppressions] if self.suppressions is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionGetObject:
    """Об'єкт з даними про блокування email."""

    project_id: Optional[str] = None
    """Унікальний ідентифікатор проєкту, ASCII-рядок до 36 символів завдовжки."""

    cause: Optional[str] = None
    """Причина, з якої надсилання на цей email блокується. Одна з таких:

    - __unsubscribed__ - зазначену адресу відписано;
    - __temporary_unavailable__ - адреса тимчасово недоступна. Це означає, що протягом наступних трьох діб надсилання на цю адресу повертатиме помилку. Email може бути тимчасово недоступним з різних причин, наприклад:

    - попереднє надсилання було відхилено сервером отримувача як спам;
    - поштова скринька отримувача переповнена або не використовується;
    - домен не приймає пошту через неправильне налаштування на боці отримувача або з інших причин;
    - сервер відправника було відхилено через блеклистинг;

    - __permanent_unavailable__ - адреса перманентно недоступна через багаторазові недоставки;
    - __complained__ - в одному з попередніх листів адресат натиснув “Це спам”.
    - __blocked__ - надсилання на цю адресу заборонено адміністрацією AllyMailer.
    У майбутньому можуть з'явитися й інші причини.
    """

    source: Optional[str] = None
    """Джерело потрапляння до списку недоступних. Одне з таких:

    - __user__ - дії користувача за допомогою методу [suppression/set](https://docs.allymailer.com.ua/ua/web-api-ref#suppression-set);
    - __system__ - надсилання на цю адресу заборонено системою, наприклад через багаторазові недоставки;
    - __subscriber__ - у зв'язку з діями отримувача. В одному з попередніх листів адресат натиснув “Це спам” або відписався.
    """

    is_deletable: Optional[bool] = None
    """Чи можна видалити запис за допомогою виклику suppression/delete."""

    created: Optional[str] = None
    """Коли було встановлено недоступність, у часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс"."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionGetObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project_id=data.get("project_id"),
            cause=data.get("cause"),
            source=data.get("source"),
            is_deletable=data.get("is_deletable"),
            created=data.get("created"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project_id": self.project_id,
            "cause": self.cause,
            "source": self.source,
            "is_deletable": self.is_deletable,
            "created": self.created,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionListRequest:
    """SuppressionListRequest"""

    cause: Optional[str] = None
    """Причина, з якої надсилання на цей email блокується. Одна з таких:

    - __unsubscribed__ - зазначену адресу відписано;
    - __temporary_unavailable__ - адреса тимчасово недоступна. Це означає, що протягом наступних трьох діб надсилання на цю адресу повертатиме помилку. Email може бути тимчасово недоступним з різних причин, наприклад:

    - попереднє надсилання було відхилено сервером отримувача як спам;
    - поштова скринька отримувача переповнена або не використовується;
    - домен не приймає пошту через неправильне налаштування на боці отримувача або з інших причин;
    - сервер відправника було відхилено через блеклистинг;

    - __permanent_unavailable__ - адреса перманентно недоступна через багаторазові недоставки;
    - __complained__ - в одному з попередніх листів адресат натиснув “Це спам”.
    - __blocked__ - надсилання на цю адресу заборонено адміністрацією AllyMailer.
    У майбутньому можуть з'явитися й інші причини.
    """

    source: Optional[str] = None
    """Джерело потрапляння до списку недоступних. Одне з таких:

    - __user__ - дії користувача за допомогою методу [suppression/set](https://docs.allymailer.com.ua/ua/web-api-ref#suppression-set);
    - __system__ - надсилання на цю адресу заборонено системою, наприклад через багаторазові недоставки;
    - __subscriber__ - у зв'язку з діями отримувача. В одному з попередніх листів адресат натиснув “Це спам” або відписався.
    """

    start_time: Optional[str] = None
    """Дата у форматі РРРР-ММ-ДД гг:хх:сс, щоб отримати список блокування з "start_time" по сьогоднішній
    день. Ігнорується, якщо параметр “cursor” не порожній.
    """

    cursor: Optional[str] = None
    """Параметр указує, з якої позиції починати вибірку. Має бути порожнім або відсутнім для отримання
    першої порції даних; для отримання другої та наступних порцій його необхідно задавати, підставляючи
    значення поля "cursor" з попередньої порції.
    """

    limit: Optional[int] = None
    """Максимум записів, що видаються за один раз, за замовчуванням 50."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            cause=data.get("cause"),
            source=data.get("source"),
            start_time=data.get("start_time"),
            cursor=data.get("cursor"),
            limit=data.get("limit"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "cause": self.cause,
            "source": self.source,
            "start_time": self.start_time,
            "cursor": self.cursor,
            "limit": self.limit,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionListResponse:
    """SuppressionListResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    suppressions: Optional[List[SuppressionListObject]] = None
    """Масив об'єктів з інформацією про недоступність."""

    cursor: Optional[str] = None
    """Параметр указує, з якої позиції починати вибірку. Має бути порожнім або відсутнім для отримання
    першої порції даних; для отримання другої та наступних порцій його необхідно задавати, підставляючи
    значення поля "cursor" з попередньої порції.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            suppressions=list_of(data.get("suppressions"), lambda item0: model_of(SuppressionListObject, item0)),
            cursor=data.get("cursor"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "suppressions": [item0.to_dict() for item0 in self.suppressions] if self.suppressions is not None else None,
            "cursor": self.cursor,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionListObject:
    """Об'єкт з даними про блокування email."""

    email: Optional[str] = None
    """Email-адреса, яка знаходиться в списку недоступних."""

    cause: Optional[str] = None
    """Причина, з якої надсилання на цей email блокується. Одна з таких:

    - __unsubscribed__ - зазначену адресу відписано;
    - __temporary_unavailable__ - адреса тимчасово недоступна. Це означає, що протягом наступних трьох діб надсилання на цю адресу повертатиме помилку. Email може бути тимчасово недоступним з різних причин, наприклад:

    - попереднє надсилання було відхилено сервером отримувача як спам;
    - поштова скринька отримувача переповнена або не використовується;
    - домен не приймає пошту через неправильне налаштування на боці отримувача або з інших причин;
    - сервер відправника було відхилено через блеклистинг;

    - __permanent_unavailable__ - адреса перманентно недоступна через багаторазові недоставки;
    - __complained__ - в одному з попередніх листів адресат натиснув “Це спам”.
    - __blocked__ - надсилання на цю адресу заборонено адміністрацією AllyMailer.
    У майбутньому можуть з'явитися й інші причини.
    """

    source: Optional[str] = None
    """Джерело потрапляння до списку недоступних. Одне з таких:

    - __user__ - дії користувача за допомогою методу [suppression/set](https://docs.allymailer.com.ua/ua/web-api-ref#suppression-set);
    - __system__ - надсилання на цю адресу заборонено системою, наприклад через багаторазові недоставки;
    - __subscriber__ - у зв'язку з діями отримувача. В одному з попередніх листів адресат натиснув “Це спам” або відписався.
    """

    is_deletable: Optional[bool] = None
    """Чи можна видалити запис за допомогою виклику suppression/delete."""

    created: Optional[str] = None
    """Коли було встановлено недоступність, у часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс"."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionListObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
            cause=data.get("cause"),
            source=data.get("source"),
            is_deletable=data.get("is_deletable"),
            created=data.get("created"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
            "cause": self.cause,
            "source": self.source,
            "is_deletable": self.is_deletable,
            "created": self.created,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionDeleteRequest:
    """SuppressionDeleteRequest"""

    email: str
    """Email-адреса, яку потрібно видалити зі списку недоступних."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionDeleteRequest:
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
