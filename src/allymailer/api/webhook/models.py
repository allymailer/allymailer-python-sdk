"""Models of the Webhook section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, map_of, model_of, to_enum

from allymailer.common import EmailStatus

__all__ = ["WebhookStatus", "WebhookEventFormat", "EventName", "DeviceType", "TrafficType", "BlockType", "DomainStatus", "WebhookSetRequest", "WebhookEventsObject", "WebhookSetResponse", "WebhookObject", "WebhookCallback", "WebhookCallbackEventsByUserItem", "WebhookCallbackEventsByUserItemEventsItem", "WebhookCallbackEventsByUserItemEventsItemEventData", "WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo", "WebhookGetRequest", "WebhookGetResponse", "WebhookListRequest", "WebhookListResponse", "WebhookDeleteRequest"]


class WebhookStatus(str, Enum):
    """Статус webhook, за замовчуванням "active". Статус "disabled" означає, що webhook було вимкнено
    користувачем, "stopped" означає, що webhook було зупинено системою після 24 годин невдалих викликів
    (мінімум за 10 різними подіями).
    """

    ACTIVE = "active"
    DISABLED = "disabled"
    STOPPED = "stopped"


class WebhookEventFormat(str, Enum):
    """Формат сповіщень. "json_post"(за замовчуванням) або "json_post_gzip"."""

    JSON_POST = "json_post"
    JSON_POST_GZIP = "json_post_gzip"


class EventName(str, Enum):
    """Тип даних, що містяться в об'єкті event_data. Або "transactional_email_status", або
    "transactional_spam_block".
    """

    TRANSACTIONAL_EMAIL_STATUS = "transactional_email_status"
    TRANSACTIONAL_SPAM_BLOCK = "transactional_spam_block"


class DeviceType(str, Enum):
    """Тип пристрою отримувача, визначений за user agent. Присутній для статусів "clicked" і "opened";
    дорівнює "unknown", якщо тип пристрою визначити не вдалося.
    """

    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    OTHER = "other"
    UNKNOWN = "unknown"


class TrafficType(str, Enum):
    """Якість трафіку для статусів "opened" і "clicked". "human" — розпізнано звичайний браузер або
    поштовий клієнт без машинних ознак; "machine" — бот, сканер посилань або проксі безпеки; "protected"
    — механізм приватності скриньки/ОС, участь людини підтвердити не можна (Apple Mail Privacy
    Protection / iCloud Private Relay, Gmail Image Proxy; Apple MPP — це protected, не machine);
    "unknown" — User-Agent відсутній, пошкоджений або не розпізнаний.
    """

    HUMAN = "human"
    MACHINE = "machine"
    PROTECTED = "protected"
    UNKNOWN = "unknown"


class BlockType(str, Enum):
    """Тип спам-блока — заблоковано або один відправляючий SMTP, або одразу багато. У разі блокування
    одиночного SMTP із загального пулу AllyMailer пробуватиме ще декілька. Властивість присутня лише
    якщо event_name="transactional_spam_block".
    """

    ONE_SMTP = "one_smtp"
    ALL_SMTP = "all_smtp"


class DomainStatus(str, Enum):
    """Це подія блокування чи розблокування. Властивість присутня лише якщо
    event_name="transactional_spam_block".
    """

    BLOCKED = "blocked"
    UNBLOCKED = "unblocked"


@dataclass
class WebhookSetRequest:
    """WebhookSetRequest"""

    url: str
    """Рядок з URL, на який надсилатиметься запит у разі виникнення події (ідентифікатор обробника). В URL
    поки що підтримуються лише ASCII-символи. Якщо вам потрібно використати не-ASCII, сконвертуйте URL у
    [Punycode](https://en.wikipedia.org/wiki/Punycode).
    """

    status: Optional[WebhookStatus] = None
    """Статус webhook, за замовчуванням "active". Статус "disabled" означає, що webhook було вимкнено
    користувачем, "stopped" означає, що webhook було зупинено системою після 24 годин невдалих викликів
    (мінімум за 10 різними подіями).
    За замовчуванням: `active`.
    """

    event_format: Optional[WebhookEventFormat] = None
    """Формат сповіщень. "json_post"(за замовчуванням) або "json_post_gzip".
    За замовчуванням: `json_post`.
    """

    delivery_info: Optional[int] = None
    """Повертати (1) чи ні (0) докладну інформацію про доставку. Якщо delivery_info=1, повертається
    додаткова інформація про відповідь сервера та внутрішній статус доставки в разі статусів доставки
    "hard_bounced" і "soft_bounced"; user agent, IP-адреса отримувача, геодані, визначена за user agent
    інформація про пристрій (тип і марка пристрою, назва ОС, браузера або поштового клієнта) і
    traffic_type (human, machine, protected або unknown) в разі статусів "opened" і "clicked"; URL для
    статусу "clicked". Для статусів "delivered", "soft_bounced" і "hard_bounced" AllyMailer також може
    повернути sender_ip — IP-адресу SMTP-сервера, з якого було надіслано лист, якщо він доступний.
    Допустимі значення: `0`, `1`.
    За замовчуванням: `0`.
    """

    single_event: Optional[int] = None
    """0=в одному виклику може надійти декілька подій, 1=лише одна подія на виклик (не рекомендується).
    Допустимі значення: `0`, `1`.
    За замовчуванням: `0`.
    """

    max_parallel: Optional[int] = None
    """Максимальна кількість дозволених паралельних запитів до вашого сервера. Чим більше ваш сервер може
    обробити — тим краще.
    За замовчуванням: `10`.
    """

    events: Optional[WebhookEventsObject] = None
    """Об'єкт, що описує події, про які потрібно сповіщати."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookSetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            url=data.get("url"),
            status=to_enum(WebhookStatus, data.get("status")),
            event_format=to_enum(WebhookEventFormat, data.get("event_format")),
            delivery_info=data.get("delivery_info"),
            single_event=data.get("single_event"),
            max_parallel=data.get("max_parallel"),
            events=model_of(WebhookEventsObject, data.get("events")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "url": self.url,
            "status": self.status,
            "event_format": self.event_format,
            "delivery_info": self.delivery_info,
            "single_event": self.single_event,
            "max_parallel": self.max_parallel,
            "events": self.events.to_dict() if self.events is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookEventsObject:
    """Об'єкт, що описує події, про які потрібно сповіщати."""

    spam_block: Optional[List[str]] = None
    """Якщо присутній, то надсилатимуться сповіщення про спам-блокування. У масиві має бути єдиний елемент
    із рядком "*".
    """

    email_status: Optional[List[EmailStatus]] = None
    """Якщо присутній, то надсилатимуться сповіщення про зміну статусу email. У масиві перелічуються ті
    статуси, про які надсилатимуться сповіщення.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookEventsObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            spam_block=list_of(data.get("spam_block")),
            email_status=list_of(data.get("email_status"), lambda item0: to_enum(EmailStatus, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "spam_block": self.spam_block,
            "email_status": self.email_status,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookSetResponse:
    """WebhookSetResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    object: Optional[WebhookObject] = None
    """Об'єкт з усіма властивостями webhook."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookSetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            object=model_of(WebhookObject, data.get("object")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "object": self.object.to_dict() if self.object is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookObject:
    """Об'єкт з усіма властивостями webhook."""

    id: Optional[int] = None
    """Унікальний ідентифікатор webhook."""

    url: Optional[str] = None
    """URL webhook."""

    status: Optional[WebhookStatus] = None
    """Статус webhook, за замовчуванням "active". Статус "disabled" означає, що webhook було вимкнено
    користувачем, "stopped" означає, що webhook було зупинено системою після 24 годин невдалих викликів
    (мінімум за 10 різними подіями).
    За замовчуванням: `active`.
    """

    event_format: Optional[WebhookEventFormat] = None
    """Формат сповіщень. "json_post"(за замовчуванням) або "json_post_gzip".
    За замовчуванням: `json_post`.
    """

    delivery_info: Optional[int] = None
    """Повертати (1) чи ні (0) докладну інформацію про доставку. Якщо delivery_info=1, повертається
    додаткова інформація про відповідь сервера та внутрішній статус доставки в разі статусів доставки
    "hard_bounced" і "soft_bounced"; user agent, IP-адреса отримувача, геодані, визначена за user agent
    інформація про пристрій (тип і марка пристрою, назва ОС, браузера або поштового клієнта) і
    traffic_type (human, machine, protected або unknown) в разі статусів "opened" і "clicked"; URL для
    статусу "clicked". Для статусів "delivered", "soft_bounced" і "hard_bounced" AllyMailer також може
    повернути sender_ip — IP-адресу SMTP-сервера, з якого було надіслано лист, якщо він доступний.
    Допустимі значення: `0`, `1`.
    За замовчуванням: `0`.
    """

    single_event: Optional[int] = None
    """0=в одному виклику може надійти декілька подій, 1=лише одна подія на виклик (не рекомендується).
    Допустимі значення: `0`, `1`.
    За замовчуванням: `0`.
    """

    max_parallel: Optional[int] = None
    """Максимальна кількість дозволених паралельних запитів до вашого сервера. Чим більше ваш сервер може
    обробити — тим краще.
    За замовчуванням: `10`.
    """

    updated_at: Optional[str] = None
    """Час останнього оновлення властивостей webhook у часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс"."""

    events: Optional[WebhookEventsObject] = None
    """Об'єкт, що описує події, про які потрібно сповіщати."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
            url=data.get("url"),
            status=to_enum(WebhookStatus, data.get("status")),
            event_format=to_enum(WebhookEventFormat, data.get("event_format")),
            delivery_info=data.get("delivery_info"),
            single_event=data.get("single_event"),
            max_parallel=data.get("max_parallel"),
            updated_at=data.get("updated_at"),
            events=model_of(WebhookEventsObject, data.get("events")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
            "url": self.url,
            "status": self.status,
            "event_format": self.event_format,
            "delivery_info": self.delivery_info,
            "single_event": self.single_event,
            "max_parallel": self.max_parallel,
            "updated_at": self.updated_at,
            "events": self.events.to_dict() if self.events is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallback:
    """Опис формату webhook."""

    auth: Optional[str] = None
    """MD5-хеш рядкового тіла повідомлення, у якому значення auth замінено на api_key користувача/проєкту,
    чий обробник викликається. За допомогою цього отримувач сповіщення може як провести автентифікацію,
    так і перевірити цілісність сповіщення.
    """

    events_by_user: Optional[List[WebhookCallbackEventsByUserItem]] = None
    """Масив з одним елементом, що містить дані про події користувача/проєкту."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallback:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            auth=data.get("auth"),
            events_by_user=list_of(data.get("events_by_user"), lambda item0: model_of(WebhookCallbackEventsByUserItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "auth": self.auth,
            "events_by_user": [item0.to_dict() for item0 in self.events_by_user] if self.events_by_user is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallbackEventsByUserItem:
    """WebhookCallbackEventsByUserItem"""

    user_id: Optional[int] = None
    """Унікальний ідентифікатор користувача."""

    project_id: Optional[str] = None
    """Ідентифікатор проєкту, присутній, якщо webhook було зареєстровано за допомогою API-ключа проєкту."""

    project_name: Optional[str] = None
    """Назва проєкту, присутня, якщо webhook було зареєстровано за допомогою API-ключа проєкту."""

    events: Optional[List[WebhookCallbackEventsByUserItemEventsItem]] = None
    """Масив подій, про які сповіщає виклик webhook."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallbackEventsByUserItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            user_id=data.get("user_id"),
            project_id=data.get("project_id"),
            project_name=data.get("project_name"),
            events=list_of(data.get("events"), lambda item0: model_of(WebhookCallbackEventsByUserItemEventsItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "user_id": self.user_id,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "events": [item0.to_dict() for item0 in self.events] if self.events is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallbackEventsByUserItemEventsItem:
    """WebhookCallbackEventsByUserItemEventsItem"""

    event_name: Optional[EventName] = None
    """Тип даних, що містяться в об'єкті event_data. Або "transactional_email_status", або
    "transactional_spam_block".
    """

    event_data: Optional[WebhookCallbackEventsByUserItemEventsItemEventData] = None
    """Об'єкт з різними властивостями події, що залежать від поля "event_name". Нижче перелічено всі
    можливі властивості, спочатку для події "transactional_email_status", потім для події
    "transactional_spam_block".
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallbackEventsByUserItemEventsItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            event_name=to_enum(EventName, data.get("event_name")),
            event_data=model_of(WebhookCallbackEventsByUserItemEventsItemEventData, data.get("event_data")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "event_name": self.event_name,
            "event_data": self.event_data.to_dict() if self.event_data is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallbackEventsByUserItemEventsItemEventData:
    """Об'єкт з різними властивостями події, що залежать від поля "event_name". Нижче перелічено всі
    можливі властивості, спочатку для події "transactional_email_status", потім для події
    "transactional_spam_block".
    """

    job_id: Optional[str] = None
    """Ідентифікатор завдання, раніше повернутий методом
    [email/send](https://docs.allymailer.com.ua/ua/web-api-ref#email-send). Присутній лише якщо
    event_name="transactional_email_status".
    """

    metadata: Optional[Dict[str, str]] = None
    """Метадані, раніше передані методом
    [email/send](https://docs.allymailer.com.ua/ua/web-api-ref#email-send) у полі recipients.metadata
    або global_metadata. Присутні лише якщо event_name="transactional_email_status".
    """

    email: Optional[str] = None
    """Email, на який було здійснено надсилання. Присутній лише якщо
    event_name="transactional_email_status".
    """

    status: Optional[EmailStatus] = None
    """Статус доставки листа. Присутній лише якщо event_name="transactional_email_status". Набуває одного з
    таких значень:

    __accepted__ — повідомлення прийнято, але ще не надіслано.

    __sent__ — повідомлення надіслано, але ще не доставлено.

    __delivered__ — повідомлення доставлено. Може змінитися на “opened”, “clicked”, “unsubscribed”,
    “subscribed” або “spam”.

    __opened__ — повідомлення доставлено й зареєстровано його прочитання. Може змінитися на “clicked”,
    “unsubscribed”, “subscribed” або “spam”.

    __clicked__ — повідомлення доставлено, прочитано, було зареєстровано перехід за одним з посилань у
    листі. Може змінитися на “unsubscribed”, “subscribed” або “spam”.

    __unsubscribed__ — повідомлення було доставлено отримувачу й прочитано ним, але користувач
    відписався за посиланням у листі. Може змінитися на “subscribed”.

    __subscribed__ — повідомлення було доставлено отримувачу й прочитано ним, але користувач відписався,
    а потім знову підписався за посиланням у листі. Може змінитися на “unsubscribed”.

    __soft_bounced__ — тимчасова недоставка повідомлення. AllyMailer продовжує спроби доставки протягом
    2 діб. У разі успішної доставки лист перейде у статус “delivered”, у разі неуспішної — у
    “hard_bounced”.

    __hard_bounced__ — доставка не вдалася, спроб доставки більше не буде. Статус остаточний. Можливих
    причин невдалої доставки безліч, для їх аналізу можна використати текст відповіді SMTP-сервера з
    поля delivery_info.destination_response або нашу внутрішню класифікацію помилок з поля
    delivery_info.delivery_status.

    __spam__ — повідомлення доставлено, але позначено як “спам” отримувачем. Статус остаточний. Ось
    деякі домени, від яких AllyMailer може отримати й обробити скаргу про спам (використовуючи
    технологію FBL): mail.ru, msn.com, outlook.com, hotmail.com, live.com, ukr.net, yahoo.com, aol.com.
    """

    event_time: Optional[str] = None
    """Дата й час події в часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс". Присутній лише якщо
    event_name="transactional_email_status".
    """

    url: Optional[str] = None
    """URL у разі статусів "opened" і "clicked". Присутній лише якщо
    event_name="transactional_email_status".
    """

    delivery_info: Optional[WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo] = None
    """Об'єкт з додатковою інформацією про доставку. Присутній лише якщо властивість delivery_info під час
    встановлення webhook дорівнювала 1 і якщо event_name="transactional_email_status".
    """

    block_time: Optional[str] = None
    """Дата й час спам-блока в часовому поясі UTC у форматі "РРРР-ММ-ДД гг:хх:сс". Присутній лише якщо
    event_name="transactional_spam_block".
    """

    block_type: Optional[BlockType] = None
    """Тип спам-блока — заблоковано або один відправляючий SMTP, або одразу багато. У разі блокування
    одиночного SMTP із загального пулу AllyMailer пробуватиме ще декілька. Властивість присутня лише
    якщо event_name="transactional_spam_block".
    """

    domain: Optional[str] = None
    """Домен, що заблокував надсилання. Властивість присутня лише якщо
    event_name="transactional_spam_block".
    """

    smtp_blocks_count: Optional[int] = None
    """Кількість заблокованих вихідних SMTP. Властивість присутня лише якщо
    event_name="transactional_spam_block".
    """

    domain_status: Optional[DomainStatus] = None
    """Це подія блокування чи розблокування. Властивість присутня лише якщо
    event_name="transactional_spam_block".
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallbackEventsByUserItemEventsItemEventData:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            job_id=data.get("job_id"),
            metadata=map_of(data.get("metadata")),
            email=data.get("email"),
            status=to_enum(EmailStatus, data.get("status")),
            event_time=data.get("event_time"),
            url=data.get("url"),
            delivery_info=model_of(WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo, data.get("delivery_info")),
            block_time=data.get("block_time"),
            block_type=to_enum(BlockType, data.get("block_type")),
            domain=data.get("domain"),
            smtp_blocks_count=data.get("SMTP_blocks_count"),
            domain_status=to_enum(DomainStatus, data.get("domain_status")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "job_id": self.job_id,
            "metadata": self.metadata,
            "email": self.email,
            "status": self.status,
            "event_time": self.event_time,
            "url": self.url,
            "delivery_info": self.delivery_info.to_dict() if self.delivery_info is not None else None,
            "block_time": self.block_time,
            "block_type": self.block_type,
            "domain": self.domain,
            "SMTP_blocks_count": self.smtp_blocks_count,
            "domain_status": self.domain_status,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo:
    """Об'єкт з додатковою інформацією про доставку. Присутній лише якщо властивість delivery_info під час
    встановлення webhook дорівнювала 1 і якщо event_name="transactional_email_status".
    """

    delivery_status: Optional[str] = None
    """Внутрішній детальний статус доставки AllyMailer. Ось деякі з можливих статусів:

    __err_user_unknown__ -- адреса не існує (і невідомо, чи існувала колись);

    __err_user_inactive__ -- адреса не використовується;

    __err_will_retry__ -- лист було тимчасово відхилено, пізніше буде здійснено повторну спробу
    доставки;

    __err_mailbox_discarded__ -- адресу видалено (тобто колись існувала, але тепер її немає);

    __err_mailbox_full__ -- поштова скринька переповнена;

    __err_spam_rejected__ -- лист відхилено як спам;

    __err_blacklisted__ -- лист було відхилено через наявність IP-адреси або домену відправника в
    якомусь із чорних списків;

    __err_too_large__ -- на думку сервера отримувача, лист перевищує допустимий розмір;

    __err_unsubscribed__ -- адресат раніше відписався від ваших розсилок;

    __err_unreachable__ -- адресу позначено як постійно недоступну через багаторазові помилки доставки
    на цю адресу;

    __err_skip_letter__ -- надсилання скасовано, оскільки email-адреса тимчасово недоступна;

    __err_domain_inactive__ -- домен не приймає пошту або не існує;

    __err_destination_misconfigured__ -- домен не приймає пошту через неправильне налаштування на боці
    отримувача, причому відповідь сервера містить інформацію про усувну причину (наприклад,
    використовується непрацюючий блеклист тощо);

    __err_delivery_failed__ -- доставка не вдалася з інших причин;

    __err_spam_skipped__ -- надсилання скасовано через блокування розсилки як спаму;

    __err_lost__ -- лист не було надіслано через неузгодженість його частин, або його було втрачено
    через збій на нашому боці. Відправник має повторно надіслати лист самостійно, оскільки оригінал не
    зберігся;

    Ми залишаємо за собою право змінювати й додавати внутрішні статуси, тому решту
    використовуваних наразі статусів перелічимо лише довідково, без пояснень:
    ok_accepted, ok_sent, ok_delivered, ok_read, ok_link_visited, ok_unsubscribed, ok_resubscribed,
    ok_spam_folder, ok_fbl,
    not_sent, skip_dup_unreachable, skip_dup_temp_unreachable, skip_dup_mailbox_full,
    err_spam_removed, err_resend, err_unknown, err_retry_letter, err_src_invalid,
    err_dest_invalid, err_not_available, err_internal, err_no_dns, err_no_smtp, err_giveup.
    """

    destination_response: Optional[str] = None
    """Відповідь SMTP-сервера."""

    user_agent: Optional[str] = None
    """Рядок user agent отримувача. Присутній лише якщо вдалося його визначити, для статусів "clicked" і
    "opened".
    """

    device_type: Optional[DeviceType] = None
    """Тип пристрою отримувача, визначений за user agent. Присутній для статусів "clicked" і "opened";
    дорівнює "unknown", якщо тип пристрою визначити не вдалося.
    """

    device_brand: Optional[str] = None
    """Марка пристрою отримувача, визначена за user agent. Присутня для статусів "clicked" і "opened", якщо
    її вдалося визначити. Для device_type "mobile" і "tablet" присутня завжди та дорівнює "unknown",
    якщо марку визначити не вдалося.
    """

    os_name: Optional[str] = None
    """Назва операційної системи пристрою отримувача, визначена за user agent. Присутня для статусів
    "clicked" і "opened"; дорівнює "unknown", якщо ОС визначити не вдалося.
    """

    browser_name: Optional[str] = None
    """Назва браузера, у якому було відкрито лист, визначена за user agent. Присутня для статусів "clicked"
    і "opened", лише якщо було визначено браузер, тому ніколи не надходить разом з email_client_name.
    """

    email_client_name: Optional[str] = None
    """Назва поштового клієнта, у якому було відкрито лист, визначена за user agent. Присутня для статусів
    "clicked" і "opened", лише якщо було визначено поштовий клієнт, тому ніколи не надходить разом з
    browser_name.
    """

    traffic_type: Optional[TrafficType] = None
    """Якість трафіку для статусів "opened" і "clicked". "human" — розпізнано звичайний браузер або
    поштовий клієнт без машинних ознак; "machine" — бот, сканер посилань або проксі безпеки; "protected"
    — механізм приватності скриньки/ОС, участь людини підтвердити не можна (Apple Mail Privacy
    Protection / iCloud Private Relay, Gmail Image Proxy; Apple MPP — це protected, не machine);
    "unknown" — User-Agent відсутній, пошкоджений або не розпізнаний.
    """

    ip: Optional[str] = None
    """IP-адреса отримувача. Присутня лише якщо вдалося її визначити, для статусів "clicked" і "opened"."""

    country_code: Optional[str] = None
    """ISO 3166-1 alpha-2 код країни, визначений за IP-адресою отримувача. Присутній для статусів "clicked"
    і "opened".
    """

    country: Optional[str] = None
    """Країна, визначена за IP-адресою отримувача. Присутня для статусів "clicked" і "opened"."""

    city: Optional[str] = None
    """Місто, визначене за IP-адресою отримувача. Присутнє для статусів "clicked" і "opened"."""

    sender_ip: Optional[str] = None
    """IP-адреса SMTP-сервера, з якого було надіслано лист. Присутня лише для статусів "delivered",
    "soft_bounced" і "hard_bounced", якщо доступна.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            delivery_status=data.get("delivery_status"),
            destination_response=data.get("destination_response"),
            user_agent=data.get("user_agent"),
            device_type=to_enum(DeviceType, data.get("device_type")),
            device_brand=data.get("device_brand"),
            os_name=data.get("os_name"),
            browser_name=data.get("browser_name"),
            email_client_name=data.get("email_client_name"),
            traffic_type=to_enum(TrafficType, data.get("traffic_type")),
            ip=data.get("ip"),
            country_code=data.get("country_code"),
            country=data.get("country"),
            city=data.get("city"),
            sender_ip=data.get("sender_ip"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "delivery_status": self.delivery_status,
            "destination_response": self.destination_response,
            "user_agent": self.user_agent,
            "device_type": self.device_type,
            "device_brand": self.device_brand,
            "os_name": self.os_name,
            "browser_name": self.browser_name,
            "email_client_name": self.email_client_name,
            "traffic_type": self.traffic_type,
            "ip": self.ip,
            "country_code": self.country_code,
            "country": self.country,
            "city": self.city,
            "sender_ip": self.sender_ip,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookGetRequest:
    """WebhookGetRequest"""

    url: str
    """URL webhook."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookGetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            url=data.get("url"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "url": self.url,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookGetResponse:
    """WebhookGetResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    object: Optional[WebhookObject] = None
    """Об'єкт з усіма властивостями webhook."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookGetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            object=model_of(WebhookObject, data.get("object")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "object": self.object.to_dict() if self.object is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookListRequest:
    """WebhookListRequest"""

    limit: Optional[int] = None
    """Максимальна кількість webhook, що повертаються за один виклик. Рекомендується 50."""

    offset: Optional[int] = None
    """Індекс першого webhook зі списку, що повертається, рахуючи з нуля.
    За замовчуванням: `0`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookListRequest:
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
class WebhookListResponse:
    """WebhookListResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    objects: Optional[List[WebhookObject]] = None
    """Масив об'єктів з даними про webhook."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            objects=list_of(data.get("objects"), lambda item0: model_of(WebhookObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "objects": [item0.to_dict() for item0 in self.objects] if self.objects is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookDeleteRequest:
    """WebhookDeleteRequest"""

    url: str
    """URL webhook."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            url=data.get("url"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "url": self.url,
        }
        return {k: v for k, v in result.items() if v is not None}
