"""Models of the Project section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of, to_enum

from allymailer.common import EmailCounterMode

__all__ = ["ProjectCreateRequest", "ProjectObject", "ProjectCreateResponse", "ProjectUpdateRequest", "ProjectUpdateObject", "ProjectUpdateResponse", "ProjectListRequest", "ProjectListResponse", "ProjectListObject", "ProjectDeleteRequest"]


@dataclass
class ProjectCreateRequest:
    """ProjectCreateRequest"""

    project: ProjectObject
    """Об'єкт із властивостями проєкту."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectCreateRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project=model_of(ProjectObject, data.get("project")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project": self.project.to_dict() if self.project is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectObject:
    """Об'єкт із властивостями проєкту."""

    name: str
    """Назва проєкту, унікальна в межах облікового запису користувача."""

    country: Optional[str] = None
    """Двобуквений код країни за правилами ISO-3166 alpha-2. Якщо задано, то AllyMailer обробляє
    персональні дані проєкту відповідно до законів заданої країни — наприклад, відповідно до GDPR для
    європейських країн.
    """

    send_enabled: Optional[bool] = None
    """Чи дозволено надсилання листів для проєкту.
    За замовчуванням: `True`.
    """

    custom_unsubscribe_url_enabled: Optional[bool] = None
    """Якщо false, то AllyMailer додає в кінець кожного листа системне посилання відписки. Значення true
    вимикає автоматичне додавання системою посилання відписки в кінець листа й дозволяє використовувати
    власне посилання відписки або надсилати листи зовсім без посилання відписки. Докладніше див.
    [тут](https://docs.allymailer.com.ua/en/unsubscribe-link). Якщо ви не вказуєте значення
    custom_unsubscribe_url_enabled під час створення проєкту — то це значення копіюється з головного
    облікового запису (якщо в головному обліковому записі було встановлено примусове вимкнення посилання
    відписки — то й у проєкту посилання відписки буде вимкнено).
    """

    backend_domain_id: Optional[int] = None
    """Унікальний ідентифікатор backend-домену, який визначає [домен посилань](/tracking-domains) або пул
    [виділених IP-адрес](/dedicated-ip) за замовчуванням. Якщо відсутній — обліковому запису/проєкту
    буде призначено дефолтний backend-домен за замовчуванням.
    """

    unsubscribe_page_id: Optional[int] = None
    """Унікальний ідентифікатор, який визначає сторінку відписки за замовчуванням. Якщо відсутній —
    обліковому запису/проєкту буде призначено системну сторінку відписки за замовчуванням.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            name=data.get("name"),
            country=data.get("country"),
            send_enabled=data.get("send_enabled"),
            custom_unsubscribe_url_enabled=data.get("custom_unsubscribe_url_enabled"),
            backend_domain_id=data.get("backend_domain_id"),
            unsubscribe_page_id=data.get("unsubscribe_page_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "name": self.name,
            "country": self.country,
            "send_enabled": self.send_enabled,
            "custom_unsubscribe_url_enabled": self.custom_unsubscribe_url_enabled,
            "backend_domain_id": self.backend_domain_id,
            "unsubscribe_page_id": self.unsubscribe_page_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectCreateResponse:
    """ProjectCreateResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    project_id: Optional[str] = None
    """Унікальний ідентифікатор проєкту, ASCII-рядок до 36 символів завдовжки."""

    project_api_key: Optional[str] = None
    """API-ключ проєкту. Ви можете використовувати цей ключ замість користувацького api_key у всіх методах,
    крім project-методів.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectCreateResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            project_id=data.get("project_id"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "project_id": self.project_id,
            "project_api_key": self.project_api_key,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectUpdateRequest:
    """ProjectUpdateRequest"""

    project: ProjectUpdateObject
    """Об'єкт із властивостями проєкту."""

    project_id: Optional[str] = None
    """Ідентифікатор проєкту, що оновлюється. Проєкт має бути ідентифіковано або цим полем project_id, або
    полем project_api_key. Ми рекомендуємо використовувати project_id, це безпечніше.
    """

    project_api_key: Optional[str] = None
    """Необов'язковий API-ключ проєкту, що оновлюється. Проєкт має бути ідентифіковано або полем
    project_id, або полем project_api_key. Ми рекомендуємо використовувати project_id, це безпечніше.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectUpdateRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project=model_of(ProjectUpdateObject, data.get("project")),
            project_id=data.get("project_id"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project_id": self.project_id,
            "project_api_key": self.project_api_key,
            "project": self.project.to_dict() if self.project is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectUpdateObject:
    """Об'єкт із властивостями проєкту."""

    name: str
    """Назва проєкту, унікальна в межах облікового запису користувача."""

    country: Optional[str] = None
    """Двобуквений код країни за правилами ISO-3166 alpha-2. Якщо задано, то AllyMailer обробляє
    персональні дані проєкту відповідно до законів заданої країни — наприклад, відповідно до GDPR для
    європейських країн.
    """

    send_enabled: Optional[bool] = None
    """Чи дозволено надсилання листів для проєкту.
    За замовчуванням: `True`.
    """

    custom_unsubscribe_url_enabled: Optional[bool] = None
    """Якщо false, то AllyMailer додає в кінець кожного листа системне посилання відписки. Значення true
    вимикає автоматичне додавання системою посилання відписки в кінець листа й дозволяє використовувати
    власне посилання відписки або надсилати листи зовсім без посилання відписки. Докладніше див.
    [тут](https://docs.allymailer.com.ua/en/unsubscribe-link). Якщо ви не вказуєте значення
    custom_unsubscribe_url_enabled під час створення проєкту — то це значення копіюється з головного
    облікового запису (якщо в головному обліковому записі було встановлено примусове вимкнення посилання
    відписки — то й у проєкту посилання відписки буде вимкнено).
    """

    backend_domain_id: Optional[int] = None
    """Унікальний ідентифікатор backend-домену, який визначає [домен посилань](/tracking-domains) або пул
    [виділених IP-адрес](/dedicated-ip) за замовчуванням. Якщо відсутній — обліковому запису/проєкту
    буде призначено дефолтний backend-домен за замовчуванням.
    """

    unsubscribe_page_id: Optional[int] = None
    """Унікальний ідентифікатор, який визначає сторінку відписки за замовчуванням. Якщо відсутній —
    обліковому запису/проєкту буде призначено системну сторінку відписки за замовчуванням.
    """

    email_counter: Optional[int] = None
    """Значення лічильника листів для проєкту, збільшується під час надсилання кожного листа. Приймає лише
    значення 0 (тобто скидання лічильника в нуль) або оновлюється автоматично, залежно від режиму роботи
    лічильника, заданого параметром 'email_counter_mode'. Якщо поле не передано в запиті або передано
    null, то значення лічильника не змінюється.
    """

    email_counter_limit: Optional[int] = None
    """Дозволяє обмежити кількість надісланих проєктом листів. У разі досягнення цього ліміту надсилання
    припиняється. Приймається будь-яке невід'ємне 64-бітне ціле число. Значення 0 означає відсутність
    ліміту. Якщо поле не передано в запиті або передано null, то значення ліміту не змінюється.
    За замовчуванням: `0`.
    """

    email_counter_mode: Optional[EmailCounterMode] = None
    """Встановлює режим роботи лічильника листів. Дозволяє вибрати, як має поводитися лічильник:
    автоматично скидатися чи залишатися постійним. Припустимі значення: default - лічильник автоматично
    скидається в нуль на початку кожного облікового періоду, permanent - лічильник ніколи не скидається
    автоматично. Скидання може бути виконане лише вручну користувачем, передавши значення 0 у полі
    'email_counter'. Якщо поле не передано в запиті або передано значення null, значення режиму не
    змінюється.
    За замовчуванням: `default`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectUpdateObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            name=data.get("name"),
            country=data.get("country"),
            send_enabled=data.get("send_enabled"),
            custom_unsubscribe_url_enabled=data.get("custom_unsubscribe_url_enabled"),
            backend_domain_id=data.get("backend_domain_id"),
            unsubscribe_page_id=data.get("unsubscribe_page_id"),
            email_counter=data.get("email_counter"),
            email_counter_limit=data.get("email_counter_limit"),
            email_counter_mode=to_enum(EmailCounterMode, data.get("email_counter_mode")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "name": self.name,
            "country": self.country,
            "send_enabled": self.send_enabled,
            "custom_unsubscribe_url_enabled": self.custom_unsubscribe_url_enabled,
            "backend_domain_id": self.backend_domain_id,
            "unsubscribe_page_id": self.unsubscribe_page_id,
            "email_counter": self.email_counter,
            "email_counter_limit": self.email_counter_limit,
            "email_counter_mode": self.email_counter_mode,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectUpdateResponse:
    """ProjectUpdateResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    project_api_key: Optional[str] = None
    """API-ключ проєкту. Повертається лише в разі, якщо в параметрі запиту був project_api_key. Якщо ж
    проєкт було ідентифіковано через project_id, то не повертається.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectUpdateResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "project_api_key": self.project_api_key,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectListRequest:
    """ProjectListRequest"""

    project_id: Optional[str] = None
    """Опціональна можливість указати project_id для включення до списку лише вказаного проєкту."""

    project_api_key: Optional[str] = None
    """Опціональна можливість указати project_api_key для включення до списку лише вказаного проєкту."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project_id=data.get("project_id"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project_id": self.project_id,
            "project_api_key": self.project_api_key,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectListResponse:
    """ProjectListResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    projects: Optional[List[ProjectListObject]] = None
    """Масив об'єктів, де кожен об'єкт відповідає окремому проєкту."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            projects=list_of(data.get("projects"), lambda item0: model_of(ProjectListObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "projects": [item0.to_dict() for item0 in self.projects] if self.projects is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectListObject:
    """ProjectListObject"""

    id: Optional[str] = None
    """Унікальний ідентифікатор проєкту, ASCII-рядок до 36 символів завдовжки."""

    api_key: Optional[str] = None
    """API-ключ проєкту. Ви можете використовувати цей ключ замість користувацького api_key у всіх методах,
    крім project-методів.
    """

    name: Optional[str] = None
    """Назва проєкту, унікальна в межах облікового запису користувача."""

    country: Optional[str] = None
    """Двобуквений код країни за правилами ISO-3166 alpha-2. Якщо задано, то AllyMailer обробляє
    персональні дані проєкту відповідно до законів заданої країни — наприклад, відповідно до GDPR для
    європейських країн.
    """

    reg_time: Optional[str] = None
    """Дата й час створення проєкту в часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс"."""

    send_enabled: Optional[bool] = None
    """Чи дозволено надсилання листів для проєкту.
    За замовчуванням: `True`.
    """

    custom_unsubscribe_url_enabled: Optional[bool] = None
    """Якщо false, то AllyMailer додає в кінець кожного листа системне посилання відписки. Значення true
    вимикає автоматичне додавання системою посилання відписки в кінець листа й дозволяє використовувати
    власне посилання відписки або надсилати листи зовсім без посилання відписки. Докладніше див.
    [тут](https://docs.allymailer.com.ua/en/unsubscribe-link). Якщо ви не вказуєте значення
    custom_unsubscribe_url_enabled під час створення проєкту — то це значення копіюється з головного
    облікового запису (якщо в головному обліковому записі було встановлено примусове вимкнення посилання
    відписки — то й у проєкту посилання відписки буде вимкнено).
    """

    backend_domain_id: Optional[int] = None
    """Унікальний ідентифікатор backend-домену, який визначає [домен посилань](/tracking-domains) або пул
    [виділених IP-адрес](/dedicated-ip) за замовчуванням. Якщо відсутній — обліковому запису/проєкту
    буде призначено дефолтний backend-домен за замовчуванням.
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

    unsubscribe_page_id: Optional[int] = None
    """Унікальний ідентифікатор, який визначає сторінку відписки за замовчуванням. Якщо відсутній —
    обліковому запису/проєкту буде призначено системну сторінку відписки за замовчуванням.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectListObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
            api_key=data.get("api_key"),
            name=data.get("name"),
            country=data.get("country"),
            reg_time=data.get("reg_time"),
            send_enabled=data.get("send_enabled"),
            custom_unsubscribe_url_enabled=data.get("custom_unsubscribe_url_enabled"),
            backend_domain_id=data.get("backend_domain_id"),
            email_counter=data.get("email_counter"),
            email_counter_limit=data.get("email_counter_limit"),
            email_counter_mode=to_enum(EmailCounterMode, data.get("email_counter_mode")),
            unsubscribe_page_id=data.get("unsubscribe_page_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
            "api_key": self.api_key,
            "name": self.name,
            "country": self.country,
            "reg_time": self.reg_time,
            "send_enabled": self.send_enabled,
            "custom_unsubscribe_url_enabled": self.custom_unsubscribe_url_enabled,
            "backend_domain_id": self.backend_domain_id,
            "email_counter": self.email_counter,
            "email_counter_limit": self.email_counter_limit,
            "email_counter_mode": self.email_counter_mode,
            "unsubscribe_page_id": self.unsubscribe_page_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectDeleteRequest:
    """ProjectDeleteRequest"""

    project_id: Optional[str] = None
    """Ідентифікатор проєкту, що видаляється. Проєкт має бути ідентифіковано або цим полем project_id, або
    полем project_api_key. Ми рекомендуємо використовувати project_id, це безпечніше.
    """

    project_api_key: Optional[str] = None
    """Необов'язковий API-ключ проєкту, що видаляється. Проєкт має бути ідентифіковано або полем
    project_id, або полем project_api_key. Ми рекомендуємо використовувати project_id, це безпечніше.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project_id=data.get("project_id"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project_id": self.project_id,
            "project_api_key": self.project_api_key,
        }
        return {k: v for k, v in result.items() if v is not None}
