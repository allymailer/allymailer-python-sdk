"""EmailValidationApi: API methods of the EmailValidation section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from .models import EmailValidationSingleRequest, EmailValidationSingleResponse


class EmailValidationApi:
    """Методи перевірки email-адрес. Перевірка адреси електронної пошти надає докладну інформацію про
    працездатність email. Це дозволить виключити з надсилання неіснуючі email, знизити показник скарг,
    очистити список підписників і врешті-решт покращити вашу репутацію як відправника. Наприклад, ви
    можете інтегрувати процес перевірки у форму реєстрації вашого сайту і вже на етапі введення адреси
    повідомляти користувачам, що адреса, яку вони ввели у форму, недійсна.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def single(self, request: EmailValidationSingleRequest) -> EmailValidationSingleResponse:
        """Допускається не більше ніж два одночасні запити; у разі перевищення буде повернуто помилку. Оскільки
        перевірка має бути швидкою, ми обмежуємо час, що витрачається на перевірку адреси електронної пошти.
        Тому, якщо ми зіткнемося з повільним поштовим сервером, час відповіді якого перевищує 5 секунд,
        результат перевірки може бути невідомим.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#email-validation-single

        Raises ApiError when the API returns an error.
        """
        return EmailValidationSingleResponse.from_dict(self._client.call("/email-validation/single.json", request.to_dict()))
