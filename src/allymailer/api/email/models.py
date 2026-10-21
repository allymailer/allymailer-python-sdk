"""Models of the Email section."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, map_of, model_of, to_enum

from allymailer.common import AttachmentsArrayItem, BodyObject, HeadersObject, InlineAttachmentsArrayItem, TemplateEngine

__all__ = ["EmailSendRequest", "MessageObject", "MessageObjectRecipientsItem", "MessageObjectOptions", "EmailSendResponse", "EmailSubscribeRequest"]


@dataclass
class EmailSendRequest:
    """EmailSendRequest"""

    message: MessageObject
    """Об'єкт, що містить усі властивості повідомлення, яке надсилається."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailSendRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            message=model_of(MessageObject, data.get("message")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "message": self.message.to_dict() if self.message is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class MessageObject:
    """Об'єкт, що містить усі властивості повідомлення, яке надсилається."""

    recipients: List[MessageObjectRecipientsItem]
    """Масив об'єктів з email-адресами, підстановками та метаданими отримувачів."""

    body: BodyObject
    """Об'єкт, що містить у собі html-, plaintext- і amp-частини листа. Або html-, або plaintext-частина
    має бути присутня обов'язково.
    """

    subject: str
    """Тема листа."""

    template_id: Optional[str] = None
    """Унікальний ідентифікатор шаблону, створеного раніше методом
    [template/set](https://docs.allymailer.com.ua/ua/web-api-ref#template-set). Якщо вказано, то поля
    шаблону підставляються замість пропущених полів email/send. Наприклад, якщо в email/send не вказано
    body — береться тіло листа із шаблону, а якщо не вказано subject — береться тема із шаблону.
    """

    tags: Optional[List[str]] = None
    """Масив із рядків, до 100 символів у кожному. Максимум 4 рядки в масиві, рядки мають бути унікальними.
    Для кожного облікового запису/проєкту дозволено не більше ніж 10 000 міток, у разі перевищення метод
    email/send повертатиме помилку. Мітки можуть використовуватися для категоризації листів за обраними
    вами критеріями. Мітки передаються методами event-dump.
    """

    skip_unsubscribe: Optional[int] = None
    """Пропустити чи не пропускати додавання стандартного блока з посиланням відписки до HTML-частини
    листа. 1=пропустити, 0=додати, за замовчуванням 0. Для использования skip_unsubscribe=1 вам надо
    [попросить техподдержку](https://cp.allymailer.com/ru/support) включить такую возможность.
    Допустимі значення: `0`, `1`.
    """

    global_language: Optional[str] = None
    """Заголовок для вибору мови посилання та сторінки відписки. Припустимі значення "be", "de", "en",
    "es", "fr", "it", "pl", "pt", "ru", "ua", "kz".
    """

    template_engine: Optional[TemplateEngine] = None
    """Параметр для вибору [шаблонізатора](https://docs.allymailer.com.ua/ua/template-engines) — або
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

    from_email: Optional[str] = None
    """Email-адреса відправника. Обов'язковий лише за порожнього template_id."""

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

    bypass_global: Optional[int] = None
    """(0 або 1, за замовчуванням 0) Значення 1=ігнорувати список глобальної недоступності, під час
    надсилання не враховуватимуться дані про недоступність адрес або скарги, отримані під час надсилання
    іншими користувачами AllyMailer. Для деяких системних записів може бути заборонено
    Допустимі значення: `0`, `1`.
    """

    bypass_unavailable: Optional[int] = None
    """(0 або 1, за замовчуванням 0) Значення 1=ігнорувати список недоступних адрес поточного облікового
    запису/проєкту. Указання 1 можливе лише за одночасного вказання bypass_global=1.
    Допустимі значення: `0`, `1`.
    """

    bypass_unsubscribed: Optional[int] = None
    """(0 або 1, за замовчуванням 0) Значення 1=ігнорувати список відписаних від розсилок поточного
    облікового запису/проєкту. Указання 1 можливе лише за одночасного вказання bypass_global=1. Параметр
    доступний лише тим користувачам, яким [техпідтримка](https://cp.allymailer.com/ua/support) схвалила
    вимкнення посилання відписки.
    Допустимі значення: `0`, `1`.
    """

    bypass_complained: Optional[int] = None
    """(0 або 1, за замовчуванням 0) Значення 1=ігнорувати список тих, хто поскаржився на обліковий
    запис/проєкт. Указання 1 можливе лише за одночасного вказання bypass_global=1. Параметр доступний
    лише тим користувачам, яким [техпідтримка](https://cp.allymailer.com/ua/support) схвалила вимкнення
    посилання відписки.
    Допустимі значення: `0`, `1`.
    """

    idempotence_key: Optional[str] = None
    """Рядок до 64 символів завдовжки з унікальним ключем запиту. Може використовуватися для запобігання
    випадковому дублюванню листів. У разі повторного надсилання запиту з тим самим ключем протягом
    хвилини запит буде відхилено. Може створюватися автоматично для кожного листа; щоб увімкнути
    автоматичну генерацію ключа, зв'яжіться з [техпідтримкою](https://cp.allymailer.com/ua/support).
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

    options: Optional[MessageObjectOptions] = None
    """Додаткові опції."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MessageObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            recipients=list_of(data.get("recipients"), lambda item0: model_of(MessageObjectRecipientsItem, item0)),
            body=model_of(BodyObject, data.get("body")),
            subject=data.get("subject"),
            template_id=data.get("template_id"),
            tags=list_of(data.get("tags")),
            skip_unsubscribe=data.get("skip_unsubscribe"),
            global_language=data.get("global_language"),
            template_engine=to_enum(TemplateEngine, data.get("template_engine")),
            global_substitutions=map_of(data.get("global_substitutions")),
            global_metadata=map_of(data.get("global_metadata")),
            from_email=data.get("from_email"),
            from_name=data.get("from_name"),
            reply_to=data.get("reply_to"),
            reply_to_name=data.get("reply_to_name"),
            track_links=data.get("track_links"),
            track_read=data.get("track_read"),
            bypass_global=data.get("bypass_global"),
            bypass_unavailable=data.get("bypass_unavailable"),
            bypass_unsubscribed=data.get("bypass_unsubscribed"),
            bypass_complained=data.get("bypass_complained"),
            idempotence_key=data.get("idempotence_key"),
            headers=model_of(HeadersObject, data.get("headers")),
            attachments=list_of(data.get("attachments"), lambda item0: model_of(AttachmentsArrayItem, item0)),
            inline_attachments=list_of(data.get("inline_attachments"), lambda item0: model_of(InlineAttachmentsArrayItem, item0)),
            options=model_of(MessageObjectOptions, data.get("options")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "recipients": [item0.to_dict() for item0 in self.recipients] if self.recipients is not None else None,
            "template_id": self.template_id,
            "tags": self.tags,
            "skip_unsubscribe": self.skip_unsubscribe,
            "global_language": self.global_language,
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
            "bypass_global": self.bypass_global,
            "bypass_unavailable": self.bypass_unavailable,
            "bypass_unsubscribed": self.bypass_unsubscribed,
            "bypass_complained": self.bypass_complained,
            "idempotence_key": self.idempotence_key,
            "headers": self.headers.to_dict() if self.headers is not None else None,
            "attachments": [item0.to_dict() for item0 in self.attachments] if self.attachments is not None else None,
            "inline_attachments": [item0.to_dict() for item0 in self.inline_attachments] if self.inline_attachments is not None else None,
            "options": self.options.to_dict() if self.options is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class MessageObjectRecipientsItem:
    """MessageObjectRecipientsItem"""

    email: str
    """Email-адреса отримувача"""

    substitutions: Optional[Dict[str, str]] = None
    """Об'єкт, що описує підстановки для конкретного отримувача (наприклад, ім'я, товар для показу саме
    цьому отримувачу — див. [Шаблонізатори](https://docs.allymailer.com.ua/ua/template-engines)).
    Підстановки працюють у параметрах:

    - body.html
    - body.plaintext
    - body.amp
    - subject
    - from_name
    - headers["List-Unsubscribe"]
    - options.unsubscribe_url
    Назви змінних можуть містити літери латинського алфавіту, цифри, символ "_". Першим символом може
    бути лише літера, використання пробілів не допускається. Є спеціальна змінна "to_name", що дозволяє
    задати ім'я отримувача. У разі підстановки туди "Ім'я Прізвище" SMTP-заголовок “To” виглядатиме як
    "Ім'я Прізвище <email@example.com>". Довжина змінної "to_name" обмежена 78 символами.
    """

    metadata: Optional[Dict[str, str]] = None
    """Об'єкт для передачі метаданих, специфічних для окремого отримувача, де "key" — рядок до 64 символів
    завдовжки, "value" — рядок до 1024 символів завдовжки, максимальна кількість ключів — 10. Метадані
    передаються під час виклику [webhook](https://docs.allymailer.com.ua/ua/web-api-ref#webhook) і
    методів [event-dump](https://docs.allymailer.com.ua/ua/web-api-ref#event-dump). Для групування
    листів в одну розсилку може використовуватися системний ключ "campaign_id" зі значенням у вигляді
    невід'ємного десяткового цілого або UUID до 128 біт.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MessageObjectRecipientsItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
            substitutions=map_of(data.get("substitutions")),
            metadata=map_of(data.get("metadata")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
            "substitutions": self.substitutions,
            "metadata": self.metadata,
        }
        return {k: v for k, v in result.items() if v is not None}

    @classmethod
    def from_address(cls, address: str, substitutions: Optional[Dict[str, str]] = None) -> MessageObjectRecipientsItem:
        """A recipient from "email" or "Name <email>": the name goes to the to_name substitution (the name in the
        "To" header); substitutions: more substitutions of the recipient."""
        email, name = address.strip(), ""
        match = re.match(r"^(.*)<([^>]+)>$", email, re.S)
        if match:
            email, name = match.group(2).strip(), match.group(1).strip().strip('"')
        if name:
            substitutions = {"to_name": name, **(substitutions or {})}
        return cls(email=email, substitutions=substitutions)

    def with_metadata(self, metadata: Dict[str, str]) -> MessageObjectRecipientsItem:
        """Sets the metadata of the recipient (returned in its webhook events); returns the recipient."""
        self.metadata = metadata
        return self


@dataclass
class MessageObjectOptions:
    """Додаткові опції."""

    send_at: Optional[str] = None
    """Дата й час у форматі "РРРР-ММ-ДД гг:хх:сс" у часовому поясі UTC. Дозволяє запланувати час надсилання
    на майбутнє, у межах 24 годин від поточного часу.
    """

    unsubscribe_url: Optional[str] = None
    """Користувацьке посилання відписки. Докладніше [тут](https://docs.allymailer.com.ua/unsubscribe-link)."""

    custom_backend_id: Optional[int] = None
    """Ідентифікатор backend-домену, через який надсилається повідомлення. Якщо відсутній — надсилання буде
    від імені backend-домену, призначеного вашому обліковому запису/проєкту за замовчуванням. Ви можете
    придбати один або декілька виділених IP-адрес і використовувати цю опцію для вибору.
    """

    smtp_pool_id: Optional[str] = None
    """Ідентифікатор пулу SMTP, через який надсилається повідомлення. Зазвичай немає необхідності вказувати
    пул явно, оскільки він обирається автоматично або як пул за замовчуванням для вашого облікового
    запису/проєкту, або відповідно до переданого параметра custom_backend_id.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MessageObjectOptions:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            send_at=data.get("send_at"),
            unsubscribe_url=data.get("unsubscribe_url"),
            custom_backend_id=data.get("custom_backend_id"),
            smtp_pool_id=data.get("smtp_pool_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "send_at": self.send_at,
            "unsubscribe_url": self.unsubscribe_url,
            "custom_backend_id": self.custom_backend_id,
            "smtp_pool_id": self.smtp_pool_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EmailSendResponse:
    """EmailSendResponse"""

    status: Optional[str] = None
    """Рядок "success".
    Допустимі значення: `success`.
    """

    job_id: Optional[str] = None
    """Ідентифікатор завдання з надсилання, може виявитися корисним під час з'ясування причин збоїв."""

    emails: Optional[List[str]] = None
    """Масив email-адрес, успішно прийнятих до надсилання."""

    failed_emails: Optional[Dict[str, str]] = None
    """Об'єкт із email-адресами, не прийнятими до надсилання. Email представлено іменем властивості, а його
    статус — значенням властивості, наприклад: {"email1@gmail.com": "temporary_unavailable"}. Можливі
    статуси адрес, на які не вдалося здійснити надсилання:

    - __unsubscribed__ — зазначену адресу відписано;
    - __invalid__ — адреса не існує або введена некоректно;
    - __duplicate__ — адреса повторюється в запиті, повторне надсилання на той самий email запобігнуто;
    - __temporary_unavailable__ — адреса тимчасово недоступна. Це означає, що протягом наступних трьох діб надсилання на цю адресу повертатиме помилку. Email може бути тимчасово недоступним з різних причин, наприклад:

    - попереднє надсилання було відхилено сервером отримувача як спам;
    - поштова скринька отримувача переповнена або не використовується;
    - домен не приймає пошту через неправильне налаштування на боці отримувача або з інших причин;
    - сервер відправника було відхилено через блеклистинг;

    - __permanent_unavailable__ — адреса перманентно недоступна через багаторазові недоставки;
    - __complained__ — в одному з попередніх листів адресат натиснув “Це спам”;
    - __blocked__ — надсилання на цю адресу заборонено адміністрацією AllyMailer.
    У майбутньому можуть з'явитися й інші статуси.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailSendResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            job_id=data.get("job_id"),
            emails=list_of(data.get("emails")),
            failed_emails=map_of(data.get("failed_emails")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "job_id": self.job_id,
            "emails": self.emails,
            "failed_emails": self.failed_emails,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EmailSubscribeRequest:
    """EmailSubscribeRequest"""

    from_email: str
    """Адреса відправника на підтвердженому домені. (Також підтримується іменування поля як
    "email_address_from").
    """

    from_name: str
    """Ім'я відправника. (Також підтримується іменування поля як "name_from")."""

    to_email: str
    """Адреса отримувача. (Також підтримується іменування поля як "email_address_to")."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailSubscribeRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            from_email=data.get("from_email"),
            from_name=data.get("from_name"),
            to_email=data.get("to_email"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "from_email": self.from_email,
            "from_name": self.from_name,
            "to_email": self.to_email,
        }
        return {k: v for k, v in result.items() if v is not None}
