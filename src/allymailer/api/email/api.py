"""EmailApi: API methods of the Email section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import EmailSendRequest, EmailSendResponse, EmailSubscribeRequest


class EmailApi:
    """Ця група методів пов'язана з надсиланням email."""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def send(self, request: EmailSendRequest) -> EmailSendResponse:
        """Метод для надсилання листів вашим підписникам.

        Під час надсилання ви можете використовувати підстановки змінних, шаблони, увімкнути відстеження
        прочитань або переходів за посиланнями та багато іншого.

        Обмеження:
        * максимальний розмір запиту — 10 MB
        * максимальна кількість отримувачів (recipients) — 500 email
        * у назві вкладень заборонено символ '/'

        Якщо під час надсилання листа у списку отримувачів будуть некоректно введені, неіснуючі, повторювані
        або відписані адреси, вони будуть повернуті у відповіді за допомогою параметра failed_emails, лист
        же буде надіслано на всі інші прийнятні адреси. Якщо всі адреси потраплять до failed_emails,
        надсилання здійснено не буде, буде повернуто помилку з API-кодом 204.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#email-send

        Raises ApiError when the API returns an error.
        """
        return EmailSendResponse.from_dict(self._client.call("/email/send.json", request.to_dict()))

    def subscribe(self, request: EmailSubscribeRequest) -> SuccessResponse:
        """Надіслати посилання на (пере)підписку.

        Метод дозволяє повторно підписати колишнього підписника, який відписався раніше, був заблокований
        через скарги або чия адреса недоступна з якоїсь іншої причини.

        Під час виклику надсилається лист у нейтральному дизайні з посиланням підписки. При переході за
        посиланням з email підписник перестає бути недоступним для користувача та/або перестає бути
        глобально відписаним.

        За замовчуванням дозволено лише одне надсилання листа повторної підписки на добу. Якщо вам потрібно
        більше — напишіть у техпідтримку.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#email-subscribe

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/email/subscribe.json", request.to_dict()))
