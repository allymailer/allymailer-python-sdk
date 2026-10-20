"""TagApi: API methods of the Tag section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import TagDeleteRequest, TagListResponse


class TagApi:
    """Методи керування користувацькими мітками. За допомогою міток ви можете класифікувати листи за
    потрібними критеріями. Відокремити маркетингові листи від транзакційних або листи з підтвердженням
    реєстрації від сповіщень про замовлення. AllyMailer дозволяє позначати мітками кожне вихідне
    повідомлення, а потім сегментувати й аналізувати статистику на основі зазначених під час надсилання
    міток.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def list(self) -> TagListResponse:
        """Метод без параметрів, повертає список усіх користувацьких міток.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#tag-list

        Raises ApiError when the API returns an error.
        """
        return TagListResponse.from_dict(self._client.call("/tag/list.json"))

    def delete(self, request: TagDeleteRequest) -> SuccessResponse:
        """Видаляє мітку.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#tag-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/tag/delete.json", request.to_dict()))
