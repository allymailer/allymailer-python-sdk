"""AllyMailer API client."""
from typing import Dict, Optional

from .client import ApiClient, ApiError, Configuration, Transport, TransportLike, UrllibTransport, base_url_for
from .api.email import EmailApi
from .api.email_validation import EmailValidationApi
from .api.confirmed_email import ConfirmedEmailApi
from .api.template import TemplateApi
from .api.webhook import WebhookApi
from .api.suppression import SuppressionApi
from .api.domain import DomainApi
from .api.event_dump import EventDumpApi
from .api.tag import TagApi
from .api.project import ProjectApi
from .api.system import SystemApi
from .api.obsolete import ObsoleteApi

__all__ = ["client", "AllyMailerClient", "ApiClient", "ApiError", "Configuration", "Transport", "UrllibTransport"]
__version__ = "1.1.1"


class AllyMailerClient:
    """Entry point of the AllyMailer API: one attribute per section.

        client = AllyMailerClient("YOUR_API_KEY")
        client.email.send(...)
    """

    def __init__(self, api_key: str, host: Optional[str] = None, timeout: float = 30.0,
            platform: Optional[str] = None, transport: Optional[TransportLike] = None,
            headers: Optional[Dict[str, str]] = None) -> None:
        """host: API host (HOST_* constants of the client package, e.g. "cp.allymailer.com") or a full base
        URL; None: the default one.
        platform: package that uses the SDK and its version (e.g. "django.1.0.0"), sent in the "platform"
        query parameter before the SDK one.
        transport: HTTP layer, an object with send(method, url, headers, body, timeout) -> (status, body) or
        such a function (client.Transport); None: UrllibTransport.
        headers: extra HTTP headers of every request.
        """
        config = Configuration(api_key, timeout=timeout, platform=platform, headers=dict(headers or {}))
        if host:
            config.base_url = base_url_for(host)
        self.api_client = ApiClient(config, transport)
        self.email = EmailApi(self.api_client)
        """Ця група методів пов'язана з надсиланням email."""
        self.email_validation = EmailValidationApi(self.api_client)
        """Методи перевірки email-адрес. Перевірка адреси електронної пошти надає докладну інформацію про
        працездатність email. Це дозволить виключити з надсилання неіснуючі email, знизити показник скарг,
        очистити список підписників і врешті-решт покращити вашу репутацію як відправника. Наприклад, ви
        можете інтегрувати процес перевірки у форму реєстрації вашого сайту і вже на етапі введення адреси
        повідомляти користувачам, що адреса, яку вони ввели у форму, недійсна.
        """
        self.confirmed_email = ConfirmedEmailApi(self.api_client)
        """Керування email-адресами, підтвердженими для надсилання із sandbox-домену. Методи доступні лише з
        API-ключем основного облікового запису.
        """
        self.template = TemplateApi(self.api_client)
        """Ви можете зберегти шаблон на боці AllyMailer і потім посилатися на нього за ідентифікатором. Це не
        обов'язково, але вкрай рекомендовано у разі повторюваних email-повідомлень або за великих обсягів
        надсилання. AllyMailer підтримує два різні синтаксиси для шаблонів, докладніше читайте
        [тут](https://docs.allymailer.com.ua/ua/template-engines).
        """
        self.webhook = WebhookApi(self.api_client)
        """AllyMailer дозволяє вам отримувати сповіщення про зміну статусу доставки листа або спам-блокування.
        Ви надаєте URL, і в разі виникнення події, що вас цікавить, ми сповіщаємо вас, передаючи на цей URL
        JSON-дані про подію.
        """
        self.suppression = SuppressionApi(self.api_client)
        """Методи для керування адресами, надсилання на які заблоковано з різних причин — відписка,
        недоступність, скарги.
        """
        self.domain = DomainApi(self.api_client)
        """Методи для налаштування доменів надсилання та перевірки їх статусів. Корисні, якщо вам недостатньо
        додавання доменів через вебінтерфейс AllyMailer і, наприклад, хочеться автоматизувати додавання
        доменів для ваших власних клієнтів.
        """
        self.event_dump = EventDumpApi(self.api_client)
        """Методи для отримання списку подій, що сталися, за певний період. Дані зберігаються до 45 днів,
        залежно від вашого тарифу. Це означає, що можна запросити події, починаючи з 00:00:00 45-го дня тому
        і до поточного моменту часу. Для індивідуальних тарифів з великими обсягами за замовчуванням події
        доступні лише за останні 7 днів.
        """
        self.tag = TagApi(self.api_client)
        """Методи керування користувацькими мітками. За допомогою міток ви можете класифікувати листи за
        потрібними критеріями. Відокремити маркетингові листи від транзакційних або листи з підтвердженням
        реєстрації від сповіщень про замовлення. AllyMailer дозволяє позначати мітками кожне вихідне
        повідомлення, а потім сегментувати й аналізувати статистику на основі зазначених під час надсилання
        міток.
        """
        self.project = ProjectApi(self.api_client)
        """Проєкти дозволяють об'єднати кілька незалежних доменів із webhook, шаблонами та списками відписки.
        Це дуже корисно, якщо у вас є власні клієнти і ви керуєте їхніми даними з одного облікового запису
        AllyMailer. Кожен проєкт отримує власний ключ API, а виклики методів API з цим ключем обробляють
        лише дані цього проєкту. Таким чином, ви можете призначити окремий проєкт для кожного користувача і
        бути впевненими, що вони не конфліктуватимуть: наприклад, відписка від одного проєкту не вплине на
        інший.
        """
        self.system = SystemApi(self.api_client)
        """Системні методи."""
        self.obsolete = ObsoleteApi(self.api_client)
        """Застарілі методи роботи з відписками. Ми рекомендуємо користуватися замість них гнучкішими методами
        [suppression](https://docs.allymailer.com.ua/ua/web-api-ref#suppression). Зверніть увагу, що знову
        підписати відписаного адресата через WebAPI не можна. Можна лише надіслати йому email із посиланням
        повторної підписки за допомогою методу email/subscribe.
        """


def client(api_key: str, host: Optional[str] = None, timeout: float = 30.0, *,
           platform: Optional[str] = None, transport: Optional[TransportLike] = None,
           headers: Optional[Dict[str, str]] = None) -> AllyMailerClient:
    """Create the API client: ``allymailer.client("YOUR_API_KEY")`` or ``allymailer.client("YOUR_API_KEY",
    "cp.allymailer.com")``; the other arguments: see AllyMailerClient.
    """
    return AllyMailerClient(api_key, host, timeout, platform, transport, headers)
