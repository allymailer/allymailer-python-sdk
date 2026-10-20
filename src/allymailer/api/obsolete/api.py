"""ObsoleteApi: API methods of the Obsolete section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from .models import ObsoleteUnsubscribedCheckRequest, ObsoleteUnsubscribedCheckResponse, ObsoleteUnsubscribedListRequest, ObsoleteUnsubscribedListResponse, ObsoleteUnsubscribedSetRequest, ObsoleteUnsubscribedSetResponse


class ObsoleteApi:
    """Застарілі методи роботи з відписками. Ми рекомендуємо користуватися замість них гнучкішими методами
    [suppression](https://docs.allymailer.com.ua/ua/web-api-ref#suppression). Зверніть увагу, що знову
    підписати відписаного адресата через WebAPI не можна. Можна лише надіслати йому email із посиланням
    повторної підписки за допомогою методу email/subscribe.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def unsubscribed_set(self, request: ObsoleteUnsubscribedSetRequest) -> ObsoleteUnsubscribedSetResponse:
        """Внести email до списку відписаних.

        Після внесення email до списку відписаних усі майбутні спроби надіслати на нього повідомлення будуть
        відхилятися. Зауважте, що видалити email зі списку відписаних безпосередньо за допомогою API не
        можна. Але можна надіслати йому повідомлення з посиланням повторної підписки за допомогою методу
        [email/subscribe](https://docs.allymailer.com.ua/ua/web-api-ref#email-subscribe) або видалити його
        зі списку відписаних вручну на сторінці [Пошук email](https://cp.allymailer.com/ua/user/email) у
        панелі керування (але кількість таких видалень на день сильно обмежена).

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#unsubscribed-set

        Raises ApiError when the API returns an error.
        """
        return ObsoleteUnsubscribedSetResponse.from_dict(self._client.call("/unsubscribed/set.json", request.to_dict()))

    def unsubscribed_check(self, request: ObsoleteUnsubscribedCheckRequest) -> ObsoleteUnsubscribedCheckResponse:
        """Перевіряє, чи відписано email.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#unsubscribed-check

        Raises ApiError when the API returns an error.
        """
        return ObsoleteUnsubscribedCheckResponse.from_dict(self._client.call("/unsubscribed/check.json", request.to_dict()))

    def unsubscribed_list(self, request: ObsoleteUnsubscribedListRequest) -> ObsoleteUnsubscribedListResponse:
        """Повертає список адрес, відписаних починаючи з указаної дати.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#unsubscribed-list

        Raises ApiError when the API returns an error.
        """
        return ObsoleteUnsubscribedListResponse.from_dict(self._client.call("/unsubscribed/list.json", request.to_dict()))
