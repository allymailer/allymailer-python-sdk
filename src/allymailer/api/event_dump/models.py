"""Models of the EventDump section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of, to_enum

from allymailer.common import EmailStatus

__all__ = ["EventDumpCreateRequest", "FilterObject", "EventDumpCreateResponse", "EventDumpGetRequest", "EventDumpGetResponse", "EventDumpObject", "EventDumpFilesObject", "EventDumpListResponse", "EventDumpDeleteRequest"]


@dataclass
class EventDumpCreateRequest:
    """EventDumpCreateRequest"""

    start_time: str
    """Дата й час у форматі РРРР-ММ-ДД гг:хх:сс, починаючи з якої необхідно отримати події. Дані
    зберігаються до 45 днів, залежно від вашого тарифу.
    """

    end_time: Optional[str] = None
    """Дата й час у форматі РРРР-ММ-ДД гг:хх:сс, до якої (не включно) запитуються події."""

    limit: Optional[int] = None
    """Максимальна кількість подій, що повертаються, за замовчуванням 50. Якщо це значення перевищує 100
    000, буде створено декілька файлів, кожен з яких містить максимум 100 000 подій.
    """

    all_projects: Optional[bool] = None
    """Якщо у користувача увімкнено проєкти, all_projects=true дозволить отримати дані всіх проєктів.
    За замовчуванням: `False`.
    """

    filter: Optional[FilterObject] = None
    """Об'єкт із властивостями фільтра дампа подій."""

    dump_fields: Optional[List[str]] = None
    """Масив із рядків з переліком назв стовпців, які необхідно отримати у вивантаженні (у порядку
    переліку). Якщо 'dump_fields' відсутній або порожній — застосовується набір і порядок полів за
    замовчуванням. Припустимі значення (у порядку за замовчуванням): 'project_id', 'event_time',
    'job_id', 'from_email', 'email', 'status', 'delivery_status', 'metadata', 'destination_response',
    'user_agent', 'url', 'ip', 'tags'. З метою більшої конфіденційності поле 'subject' не входить до
    набору полів за замовчуванням, але ви можете додати його, вказавши в параметрі 'dump_fields'.
    """

    aggregate: Optional[str] = None
    """Дозволяє отримати агреговану статистику за вказаний період. Може набувати одного з двох значень:

    - __day_status__ - отримати агреговану статистику; за такого значення параметр filter має бути відсутнім або порожнім об'єктом (фільтри неприпустимі);
    - __порожній рядок__ - значення за замовчуванням, еквівалентне відсутності параметра aggregate, і метод event_dump/create у цьому разі працює як раніше.
    """

    delimiter: Optional[str] = None
    """Роздільник полів, за замовчуванням ','. Припустимі значення ',' і ';'."""

    format: Optional[str] = None
    """Формат отримуваного файлу “csv” (за замовчуванням) або “csv_gzip”.
    За замовчуванням: `csv`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpCreateRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            limit=data.get("limit"),
            all_projects=data.get("all_projects"),
            filter=model_of(FilterObject, data.get("filter")),
            dump_fields=list_of(data.get("dump_fields")),
            aggregate=data.get("aggregate"),
            delimiter=data.get("delimiter"),
            format=data.get("format"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "limit": self.limit,
            "all_projects": self.all_projects,
            "filter": self.filter.to_dict() if self.filter is not None else None,
            "dump_fields": self.dump_fields,
            "aggregate": self.aggregate,
            "delimiter": self.delimiter,
            "format": self.format,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class FilterObject:
    """Об'єкт із властивостями фільтра дампа подій."""

    job_id: Optional[str] = None
    """Ідентифікатор завдання, раніше повернутий методом
    [email/send](https://docs.allymailer.com.ua/ua/web-api-ref#email-send).
    """

    status: Optional[EmailStatus] = None
    """Статус email. Можна вказати одне з таких значень:

    __accepted__ — повідомлення прийнято, але ще не надіслано.

    __sent__ — повідомлення надіслано, але ще не доставлено.

    __delivered__ — повідомлення доставлено.

    __opened__ — повідомлення доставлено й зареєстровано його прочитання.

    __clicked__ — повідомлення доставлено, прочитано, було зареєстровано перехід за одним з посилань у
    листі.

    __unsubscribed__ — повідомлення було доставлено отримувачу й прочитано ним, але користувач
    відписався за посиланням у листі.

    __subscribed__ — повідомлення було доставлено отримувачу й прочитано ним, але користувач відписався,
    а потім знову підписався за посиланням у листі.

    __soft_bounced__ — тимчасова недоставка повідомлення. AllyMailer продовжує спроби доставки протягом
    2 діб.

    __hard_bounced__ — доставка не вдалася, спроб доставки більше не буде.

    __spam__ — повідомлення доставлено, але позначено як “спам” отримувачем.
    """

    delivery_status: Optional[str] = None
    """Внутрішній детальний статус доставки AllyMailer. Можна вказати декілька статусів через кому. Ось
    деякі з можливих статусів:

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

    email: Optional[str] = None
    """Адреса отримувача"""

    email_from: Optional[str] = None
    """Адреса відправника"""

    domain: Optional[str] = None
    """Домен отримувача"""

    campaign_id: Optional[str] = None
    """Ідентифікатор розсилки, невід'ємне десяткове ціле або UUID до 128 біт, передане в метаданих у полі з
    іменем "campaign_id" (ім'я можна налаштувати через техпідтримку).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> FilterObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            job_id=data.get("job_id"),
            status=to_enum(EmailStatus, data.get("status")),
            delivery_status=data.get("delivery_status"),
            email=data.get("email"),
            email_from=data.get("email_from"),
            domain=data.get("domain"),
            campaign_id=data.get("campaign_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "job_id": self.job_id,
            "status": self.status,
            "delivery_status": self.delivery_status,
            "email": self.email,
            "email_from": self.email_from,
            "domain": self.domain,
            "campaign_id": self.campaign_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpCreateResponse:
    """EventDumpCreateResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    dump_id: Optional[str] = None
    """Ідентифікатор дампа. Використовується для виклику методу
    [event-dump/get](https://docs.allymailer.com.ua/ua/web-api-ref#event-dump-get).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpCreateResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            dump_id=data.get("dump_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "dump_id": self.dump_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpGetRequest:
    """EventDumpGetRequest"""

    dump_id: str
    """Ідентифікатор дампа, отриманий методом
    [event-dump/create](https://docs.allymailer.com.ua/ua/web-api-ref#event-dump-create).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpGetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            dump_id=data.get("dump_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "dump_id": self.dump_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpGetResponse:
    """EventDumpGetResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    event_dump: Optional[EventDumpObject] = None
    """Об'єкт із властивостями дампа подій."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpGetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            event_dump=model_of(EventDumpObject, data.get("event_dump")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "event_dump": self.event_dump.to_dict() if self.event_dump is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpObject:
    """Об'єкт із властивостями дампа подій."""

    dump_id: Optional[str] = None
    """Ідентифікатор дампа, отриманий методом
    [event-dump/create](https://docs.allymailer.com.ua/ua/web-api-ref#event-dump-create).
    """

    dump_status: Optional[str] = None
    """Статус задачі. Одне з чотирьох значень:

    - __queued__ - очікує в черзі, обробка ще не починалася;
    - __in_process__ - триває обробка;
    - __ready__ - обробку завершено, файли доступні для завантаження;
    - __failed__ - обробку перервано з помилкою.
    """

    files: Optional[List[EventDumpFilesObject]] = None
    """Масив об'єктів, кожен з яких позначає готовий до завантаження файл. Навіть якщо
    "dump_status"="in_process", уже можна завантажувати ті файли, які вказані в "files". У разі
    відсутності подій за заданими параметрами буде повернуто порожній масив.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            dump_id=data.get("dump_id"),
            dump_status=data.get("dump_status"),
            files=list_of(data.get("files"), lambda item0: model_of(EventDumpFilesObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "dump_id": self.dump_id,
            "dump_status": self.dump_status,
            "files": [item0.to_dict() for item0 in self.files] if self.files is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpFilesObject:
    """Об'єкт із властивостями файлу дампа подій."""

    url: Optional[str] = None
    """Унікальний URL для завантаження файлу з розширенням .csv або .csv.gz, залежно від запитаного
    формату.
    """

    size: Optional[int] = None
    """Розмір файлу."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpFilesObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            url=data.get("url"),
            size=data.get("size"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "url": self.url,
            "size": self.size,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpListResponse:
    """EventDumpListResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    event_dumps: Optional[List[EventDumpObject]] = None
    """Масив об'єктів, що описують дампи подій. Кожен об'єкт містить ті самі властивості, що й об'єкт
    'event_dump', який повертає метод
    [event-dump/get](https://docs.allymailer.com.ua/ua/web-api-ref#event-dump-get).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            event_dumps=list_of(data.get("event_dumps"), lambda item0: model_of(EventDumpObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "event_dumps": [item0.to_dict() for item0 in self.event_dumps] if self.event_dumps is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpDeleteRequest:
    """EventDumpDeleteRequest"""

    dump_id: str
    """Ідентифікатор дампа, отриманий методом
    [event-dump/create](https://docs.allymailer.com.ua/ua/web-api-ref#event-dump-create).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            dump_id=data.get("dump_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "dump_id": self.dump_id,
        }
        return {k: v for k, v in result.items() if v is not None}
