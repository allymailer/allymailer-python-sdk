"""Models of the Template section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, map_of, model_of, to_enum

from allymailer.common import AttachmentsArrayItem, BodyObject, HeadersObject, InlineAttachmentsArrayItem, TemplateEngine

__all__ = ["EditorType", "TemplateSetRequest", "TemplateObject", "TemplateSetResponse", "TemplateGetRequest", "TemplateGetResponse", "TemplateListRequest", "TemplateListResponse", "TemplateListObject", "TemplateDeleteRequest"]


class EditorType(str, Enum):
    """Тип редактора шаблону у вебінтерфейсі, "html" або "visual". За замовчуванням — "html". Створення
    шаблонів із типом редактора "visual" можливе лише через вебінтерфейс.
    """

    HTML = "html"
    VISUAL = "visual"


@dataclass
class TemplateSetRequest:
    """Об'єкт з усіма властивостями шаблону."""

    template: TemplateObject
    """Об'єкт, що містить властивості шаблону."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateSetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            template=model_of(TemplateObject, data.get("template")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "template": self.template.to_dict() if self.template is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateObject:
    """Об'єкт, що містить властивості шаблону."""

    name: str
    """Назва шаблону."""

    from_email: str
    """Email-адреса відправника."""

    id: Optional[str] = None
    """Унікальний ідентифікатор шаблону. Якщо вказано, система спробує знайти шаблон із указаним id і
    відредагувати його. Якщо не задано, буде створено новий шаблон.
    """

    editor_type: Optional[EditorType] = None
    """Тип редактора шаблону у вебінтерфейсі, "html" або "visual". За замовчуванням — "html". Створення
    шаблонів із типом редактора "visual" можливе лише через вебінтерфейс.
    """

    template_engine: Optional[TemplateEngine] = None
    """Параметр для вибору [шаблонізатора](https://docs.allymailer.com.ua/en/template-engines) — або
    "simple", або "velocity", або "liquid", або "none". За замовчуванням — "simple".
    """

    global_substitutions: Optional[Dict[str, str]] = None
    """Об'єкт для передачі глобальних підстановок (наприклад, назва компанії). Якщо назви змінних
    повторюються в об'єкті користувацьких підстановок "substitutions", значення змінних будуть взяті з
    об'єкта "substitutions". Підстановки працюють у параметрах:

    - body.html
    - body.plaintext
    - body.amp
    - subject
    - from_name
    - options.unsubscribe_url
    Назви змінних можуть містити літери латинського алфавіту, цифри, символ "_". Першим символом може
    бути лише літера, використання пробілів не допускається.
    """

    global_metadata: Optional[Dict[str, str]] = None
    """Об'єкт для передачі метаданих, спільних для всіх отримувачів, у форматі: "key": "value". Максимальна
    кількість ключів: 10; максимальна довжина ключа: 64 символи; максимальна довжина значення ключа:
    1024 символи. Метадані передаються під час виклику
    [webhook](https://docs.allymailer.com.ua/ua/web-api-ref#webhook). Для групування листів в одну
    розсилку може використовуватися системний ключ "campaign_id" зі значенням у вигляді невід'ємного
    десяткового цілого до 128 біт або UUID вигляду "c7703772-453e-4c77-a9ae-9a1b94051b5a". Неправильні
    значення будуть прирівняні до '0'
    """

    body: Optional[BodyObject] = None
    """Об'єкт, що містить у собі html-, plaintext- і amp-частини листа. Або html-, або plaintext-частина
    має бути присутня обов'язково.
    """

    subject: Optional[str] = None
    """Тема листа."""

    from_name: Optional[str] = None
    """Ім'я відправника."""

    reply_to: Optional[str] = None
    """Необов'язкова email-адреса для відповідей (на випадок, якщо відрізняється від адреси відправника)"""

    reply_to_name: Optional[str] = None
    """Необов'язкове ім'я для відповідей (якщо вказано email reply_to і ви хочете, щоб відображався не лише
    цей email, але й ім'я)
    """

    track_links: Optional[int] = None
    """1 = відстеження переходів за посиланнями увімкнено (значення за замовчуванням), 0=вимкнено. Для
    використання track_links = 0 вам потрібно [попросити
    техпідтримку](https://cp.allymailer.com/ua/support) увімкнути таку можливість.
    Допустимі значення: `0`, `1`.
    """

    track_read: Optional[int] = None
    """1 = відстеження прочитань листа увімкнено (значення за замовчуванням), 0 = вимкнено. Для
    використання track_read = 0 вам потрібно [попросити
    техпідтримку](https://cp.allymailer.com/ua/support) увімкнути таку можливість.
    Допустимі значення: `0`, `1`.
    """

    headers: Optional[HeadersObject] = None
    """Об'єкт, що містить додаткові заголовки листа, максимум 50 заголовків. Префікс “X-” в імені заголовка
    обов'язковий, заголовки без нього будуть проігноровані, наприклад X-ALLYMAILER-Global-Language,
    X-ALLYMAILER-Template-Engine. Стандартні заголовки "To", "CC", "BCC" передаються без префікса "X-",
    але обробляються спеціальним чином, тому мають низку обмежень, докладніше про це можна прочитати
    [тут](/cc-and-bcc). Також якщо [техпідтримка](https://cp.allymailer.com/ua/support) схвалила вам
    вимкнення посилання відписки, то ви також можете передавати заголовки List-Unsubscribe,
    List-Subscribe, List-Help, List-Owner, List-Archive, In-Reply-To і References.
    """

    attachments: Optional[List[AttachmentsArrayItem]] = None
    """Необов'язковий масив вкладень."""

    inline_attachments: Optional[List[InlineAttachmentsArrayItem]] = None
    """Масив для передачі inline-вкладень, наприклад, для включення зображень у лист замість завантаження
    їх за посиланням.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            name=data.get("name"),
            from_email=data.get("from_email"),
            id=data.get("id"),
            editor_type=to_enum(EditorType, data.get("editor_type")),
            template_engine=to_enum(TemplateEngine, data.get("template_engine")),
            global_substitutions=map_of(data.get("global_substitutions")),
            global_metadata=map_of(data.get("global_metadata")),
            body=model_of(BodyObject, data.get("body")),
            subject=data.get("subject"),
            from_name=data.get("from_name"),
            reply_to=data.get("reply_to"),
            reply_to_name=data.get("reply_to_name"),
            track_links=data.get("track_links"),
            track_read=data.get("track_read"),
            headers=model_of(HeadersObject, data.get("headers")),
            attachments=list_of(data.get("attachments"), lambda item0: model_of(AttachmentsArrayItem, item0)),
            inline_attachments=list_of(data.get("inline_attachments"), lambda item0: model_of(InlineAttachmentsArrayItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
            "name": self.name,
            "editor_type": self.editor_type,
            "template_engine": self.template_engine,
            "global_substitutions": self.global_substitutions,
            "global_metadata": self.global_metadata,
            "body": self.body.to_dict() if self.body is not None else None,
            "subject": self.subject,
            "from_email": self.from_email,
            "from_name": self.from_name,
            "reply_to": self.reply_to,
            "reply_to_name": self.reply_to_name,
            "track_links": self.track_links,
            "track_read": self.track_read,
            "headers": self.headers.to_dict() if self.headers is not None else None,
            "attachments": [item0.to_dict() for item0 in self.attachments] if self.attachments is not None else None,
            "inline_attachments": [item0.to_dict() for item0 in self.inline_attachments] if self.inline_attachments is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateSetResponse:
    """TemplateSetResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    template: Optional[TemplateObject] = None
    """Об'єкт, що містить властивості шаблону."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateSetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            template=model_of(TemplateObject, data.get("template")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "template": self.template.to_dict() if self.template is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateGetRequest:
    """TemplateGetRequest"""

    id: str
    """Ідентифікатор шаблону."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateGetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateGetResponse:
    """TemplateGetResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    template: Optional[TemplateObject] = None
    """Об'єкт, що містить властивості шаблону."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateGetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            template=model_of(TemplateObject, data.get("template")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "template": self.template.to_dict() if self.template is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateListRequest:
    """TemplateListRequest"""

    limit: Optional[int] = None
    """Максимальна кількість шаблонів, що повертаються, за замовчуванням 50.
    За замовчуванням: `50`.
    """

    offset: Optional[int] = None
    """Індекс першого шаблону зі списку, що повертається, рахуючи з нуля.
    За замовчуванням: `0`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            limit=data.get("limit"),
            offset=data.get("offset"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "limit": self.limit,
            "offset": self.offset,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateListResponse:
    """TemplateListResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    templates: Optional[List[TemplateListObject]] = None
    """Масив об'єктів-шаблонів."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            templates=list_of(data.get("templates"), lambda item0: model_of(TemplateListObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "templates": [item0.to_dict() for item0 in self.templates] if self.templates is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateListObject:
    """TemplateListObject"""

    id: Optional[str] = None
    """Унікальний ідентифікатор шаблону."""

    name: Optional[str] = None
    """Назва шаблону."""

    editor_type: Optional[EditorType] = None
    """Тип редактора шаблону у вебінтерфейсі, "html" або "visual". За замовчуванням — "html". Створення
    шаблонів із типом редактора "visual" можливе лише через вебінтерфейс.
    """

    template_engine: Optional[TemplateEngine] = None
    """Параметр для вибору [шаблонізатора](https://docs.allymailer.com.ua/en/template-engines) — або
    "simple", або "velocity", або "liquid", або "none". За замовчуванням — "simple".
    """

    global_substitutions: Optional[Dict[str, str]] = None
    """Об'єкт для передачі глобальних підстановок (наприклад, назва компанії). Якщо назви змінних
    повторюються в об'єкті користувацьких підстановок "substitutions", значення змінних будуть взяті з
    об'єкта "substitutions". Підстановки працюють у параметрах:

    - body.html
    - body.plaintext
    - body.amp
    - subject
    - from_name
    - options.unsubscribe_url
    Назви змінних можуть містити літери латинського алфавіту, цифри, символ "_". Першим символом може
    бути лише літера, використання пробілів не допускається.
    """

    global_metadata: Optional[Dict[str, str]] = None
    """Об'єкт для передачі метаданих, спільних для всіх отримувачів, у форматі: "key": "value". Максимальна
    кількість ключів: 10; максимальна довжина ключа: 64 символи; максимальна довжина значення ключа:
    1024 символи. Метадані передаються під час виклику
    [webhook](https://docs.allymailer.com.ua/ua/web-api-ref#webhook). Для групування листів в одну
    розсилку може використовуватися системний ключ "campaign_id" зі значенням у вигляді невід'ємного
    десяткового цілого до 128 біт або UUID вигляду "c7703772-453e-4c77-a9ae-9a1b94051b5a". Неправильні
    значення будуть прирівняні до '0'
    """

    body: Optional[BodyObject] = None
    """Об'єкт, що містить у собі html-, plaintext- і amp-частини листа. Або html-, або plaintext-частина
    має бути присутня обов'язково.
    """

    subject: Optional[str] = None
    """Тема листа."""

    from_email: Optional[str] = None
    """Email-адреса відправника."""

    from_name: Optional[str] = None
    """Ім'я відправника."""

    reply_to: Optional[str] = None
    """Необов'язкова email-адреса для відповідей (на випадок, якщо відрізняється від адреси відправника)"""

    reply_to_name: Optional[str] = None
    """Необов'язкове ім'я для відповідей (якщо вказано email reply_to і ви хочете, щоб відображався не лише
    цей email, але й ім'я)
    """

    track_links: Optional[int] = None
    """1 = відстеження переходів за посиланнями увімкнено (значення за замовчуванням), 0=вимкнено. Для
    використання track_links = 0 вам потрібно [попросити
    техпідтримку](https://cp.allymailer.com/ua/support) увімкнути таку можливість.
    Допустимі значення: `0`, `1`.
    """

    track_read: Optional[int] = None
    """1 = відстеження прочитань листа увімкнено (значення за замовчуванням), 0 = вимкнено. Для
    використання track_read = 0 вам потрібно [попросити
    техпідтримку](https://cp.allymailer.com/ua/support) увімкнути таку можливість.
    Допустимі значення: `0`, `1`.
    """

    headers: Optional[HeadersObject] = None
    """Об'єкт, що містить додаткові заголовки листа, максимум 50 заголовків. Префікс “X-” в імені заголовка
    обов'язковий, заголовки без нього будуть проігноровані, наприклад X-ALLYMAILER-Global-Language,
    X-ALLYMAILER-Template-Engine. Стандартні заголовки "To", "CC", "BCC" передаються без префікса "X-",
    але обробляються спеціальним чином, тому мають низку обмежень, докладніше про це можна прочитати
    [тут](/cc-and-bcc). Також якщо [техпідтримка](https://cp.allymailer.com/ua/support) схвалила вам
    вимкнення посилання відписки, то ви також можете передавати заголовки List-Unsubscribe,
    List-Subscribe, List-Help, List-Owner, List-Archive, In-Reply-To і References.
    """

    attachments: Optional[List[AttachmentsArrayItem]] = None
    """Необов'язковий масив вкладень."""

    inline_attachments: Optional[List[InlineAttachmentsArrayItem]] = None
    """Масив для передачі inline-вкладень, наприклад, для включення зображень у лист замість завантаження
    їх за посиланням.
    """

    created: Optional[str] = None
    """Час створення шаблону в часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс\""""

    user_id: Optional[int] = None
    """Унікальний ідентифікатор користувача."""

    project_id: Optional[str] = None
    """Унікальний ідентифікатор проєкту, ASCII-рядок до 36 символів завдовжки."""

    project_name: Optional[str] = None
    """Назва проєкту, унікальна в межах облікового запису користувача."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateListObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            editor_type=to_enum(EditorType, data.get("editor_type")),
            template_engine=to_enum(TemplateEngine, data.get("template_engine")),
            global_substitutions=map_of(data.get("global_substitutions")),
            global_metadata=map_of(data.get("global_metadata")),
            body=model_of(BodyObject, data.get("body")),
            subject=data.get("subject"),
            from_email=data.get("from_email"),
            from_name=data.get("from_name"),
            reply_to=data.get("reply_to"),
            reply_to_name=data.get("reply_to_name"),
            track_links=data.get("track_links"),
            track_read=data.get("track_read"),
            headers=model_of(HeadersObject, data.get("headers")),
            attachments=list_of(data.get("attachments"), lambda item0: model_of(AttachmentsArrayItem, item0)),
            inline_attachments=list_of(data.get("inline_attachments"), lambda item0: model_of(InlineAttachmentsArrayItem, item0)),
            created=data.get("created"),
            user_id=data.get("user_id"),
            project_id=data.get("project_id"),
            project_name=data.get("project_name"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
            "name": self.name,
            "editor_type": self.editor_type,
            "template_engine": self.template_engine,
            "global_substitutions": self.global_substitutions,
            "global_metadata": self.global_metadata,
            "body": self.body.to_dict() if self.body is not None else None,
            "subject": self.subject,
            "from_email": self.from_email,
            "from_name": self.from_name,
            "reply_to": self.reply_to,
            "reply_to_name": self.reply_to_name,
            "track_links": self.track_links,
            "track_read": self.track_read,
            "headers": self.headers.to_dict() if self.headers is not None else None,
            "attachments": [item0.to_dict() for item0 in self.attachments] if self.attachments is not None else None,
            "inline_attachments": [item0.to_dict() for item0 in self.inline_attachments] if self.inline_attachments is not None else None,
            "created": self.created,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "project_name": self.project_name,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateDeleteRequest:
    """TemplateDeleteRequest"""

    id: str
    """Ідентифікатор шаблону."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
        }
        return {k: v for k, v in result.items() if v is not None}
