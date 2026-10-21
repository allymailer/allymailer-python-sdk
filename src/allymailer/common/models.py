"""Models of the Common section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ..client.enums import as_dict

__all__ = ["TemplateEngine", "EmailStatus", "VerificationRecordStatus", "EmailCounterMode", "BodyObject", "HeadersObject", "AttachmentsArrayItem", "InlineAttachmentsArrayItem", "SuccessResponse"]


class TemplateEngine(str, Enum):
    """Параметр для вибору [шаблонізатора](https://docs.allymailer.com.ua/ua/template-engines) — або
    "simple", або "velocity", або "liquid", або "none". За замовчуванням — "simple".
    """

    SIMPLE = "simple"
    VELOCITY = "velocity"
    LIQUID = "liquid"
    NONE = "none"


class EmailStatus(str, Enum):
    """EmailStatus"""

    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    UNSUBSCRIBED = "unsubscribed"
    SUBSCRIBED = "subscribed"
    SOFT_BOUNCED = "soft_bounced"
    HARD_BOUNCED = "hard_bounced"
    SPAM = "spam"


class VerificationRecordStatus(str, Enum):
    """Лише домени зі статусом "confirmed" запису про володіння доменом можуть використовуватися для
    надсилання листів.
    """

    CONFIRMED = "confirmed"
    UNCONFIRMED = "unconfirmed"


class EmailCounterMode(str, Enum):
    """Встановлює режим роботи лічильника листів. Дозволяє вибрати, як має поводитися лічильник:
    автоматично скидатися чи залишатися постійним. Припустимі значення: default - лічильник автоматично
    скидається в нуль на початку кожного облікового періоду, permanent - лічильник ніколи не скидається
    автоматично. Скидання може бути виконане лише вручну користувачем, передавши значення 0 у полі
    'email_counter'. Якщо поле не передано в запиті або передано значення null, значення режиму не
    змінюється.
    """

    DEFAULT = "default"
    PERMANENT = "permanent"


@dataclass
class BodyObject:
    """Об'єкт, що містить у собі html-, plaintext- і amp-частини листа. Або html-, або plaintext-частина
    має бути присутня обов'язково.
    """

    html: Optional[str] = None
    """HTML-частина листа"""

    plaintext: Optional[str] = None
    """Plaintext-частина листа."""

    amp: Optional[str] = None
    """Необов'язкова
    [AMP](http://amp.dev/documentation/guides-and-tutorials/learn/email_fundamentals/)-частина листа.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BodyObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            html=data.get("html"),
            plaintext=data.get("plaintext"),
            amp=data.get("amp"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "html": self.html,
            "plaintext": self.plaintext,
            "amp": self.amp,
        }
        return {k: v for k, v in result.items() if v is not None}

    @classmethod
    def from_html(cls, html: str, plaintext: Optional[str] = None) -> BodyObject:
        """An HTML body, with an optional plain-text part."""
        return cls(html=html, plaintext=plaintext)

    @classmethod
    def from_text(cls, plaintext: str) -> BodyObject:
        """A plain-text body."""
        return cls(plaintext=plaintext)


@dataclass
class HeadersObject:
    """Об'єкт, що містить додаткові заголовки листа, максимум 50 заголовків. Префікс “X-” в імені заголовка
    обов'язковий, заголовки без нього будуть проігноровані, наприклад X-ALLYMAILER-Global-Language,
    X-ALLYMAILER-Template-Engine. Стандартні заголовки "To", "CC", "BCC" передаються без префікса "X-",
    але обробляються спеціальним чином, тому мають низку обмежень, докладніше про це можна прочитати
    [тут](/cc-and-bcc). Також якщо [техпідтримка](https://cp.allymailer.com/ua/support) схвалила вам
    вимкнення посилання відписки, то ви також можете передавати заголовки List-Unsubscribe,
    List-Subscribe, List-Help, List-Owner, List-Archive, In-Reply-To і References.
    """

    x_allymailer_global_language: Optional[str] = None
    """Заголовок для вибору мови посилання та сторінки відписки. Припустимі значення "be", "de", "en",
    "es", "fr", "it", "pl", "pt", "ru", "ua", "kz".
    """

    x_allymailer_template_engine: Optional[str] = None
    """Заголовок для вибору шаблонізатора — або “simple”, або “velocity”, або “liquid”, або “none”. За
    замовчуванням — “simple”. Має пріоритет над значенням, що передається в параметрі “template_engine”.
    """

    extra: Dict[str, str] = field(default_factory=dict)
    """Поля понад іменовані, передаються як є поруч із ними (іменоване поле важливіше), наприклад будь-який
    заголовок X-*, "CC", "List-Unsubscribe": extra={"X-MyHeader": "some data"}. Сюди ж потрапляють
    невідомі ключі відповіді.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HeadersObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            x_allymailer_global_language=data.get("X-ALLYMAILER-Global-Language"),
            x_allymailer_template_engine=data.get("X-ALLYMAILER-Template-Engine"),
            extra={key: value for key, value in data.items() if key not in ("X-ALLYMAILER-Global-Language", "X-ALLYMAILER-Template-Engine", )},
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted. The keys of extra go next to the named fields (a named
        field wins).
        """
        result = {
            "X-ALLYMAILER-Global-Language": self.x_allymailer_global_language,
            "X-ALLYMAILER-Template-Engine": self.x_allymailer_template_engine,
        }
        extra = {key: value for key, value in (self.extra or {}).items() if key not in result and value is not None}
        return {**extra, **{k: v for k, v in result.items() if v is not None}}


@dataclass
class AttachmentsArrayItem:
    """AttachmentsArrayItem"""

    type: str
    """Тип вкладення, див. [MIME](https://en.wikipedia.org/wiki/MIME). Якщо не впевнені, використовуйте
    "application/octet-stream".
    """

    name: str
    """Назва вкладення у форматі: "ім'я.розширення". У разі передачі кількох вкладень їхні назви мають бути
    унікальними. У назві вкладень заборонено символ ‘/’.
    """

    content: str
    """Вміст файлу у [base64](https://en.wikipedia.org/wiki/Base64). Максимальний розмір файлу 7 Мб
    (9786710 байт у base64).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AttachmentsArrayItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            type=data.get("type"),
            name=data.get("name"),
            content=data.get("content"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "type": self.type,
            "name": self.name,
            "content": self.content,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class InlineAttachmentsArrayItem:
    """InlineAttachmentsArrayItem"""

    type: str
    """Тип вкладення, див. [MIME](https://en.wikipedia.org/wiki/MIME). Якщо не впевнені, використовуйте
    "application/octet-stream".
    """

    name: str
    """Ідентифікатор вкладення. Якщо, наприклад, "name"="IMAGECID", то для виведення картинки з цього
    вкладення в HTML-тексті листа потрібно вказати <img src="cid:IMAGECID">.
    """

    content: str
    """Вміст файлу у [base64](https://en.wikipedia.org/wiki/Base64). Максимальний розмір файлу 7 Мб
    (9786710 байт у base64).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> InlineAttachmentsArrayItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            type=data.get("type"),
            name=data.get("name"),
            content=data.get("content"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "type": self.type,
            "name": self.name,
            "content": self.content,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuccessResponse:
    """SuccessResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuccessResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
        }
        return {k: v for k, v in result.items() if v is not None}
