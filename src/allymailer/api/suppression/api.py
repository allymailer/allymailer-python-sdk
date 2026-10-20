"""SuppressionApi: API methods of the Suppression section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import SuppressionDeleteRequest, SuppressionGetRequest, SuppressionGetResponse, SuppressionListRequest, SuppressionListResponse, SuppressionSetRequest


class SuppressionApi:
    """Методи для керування адресами, надсилання на які заблоковано з різних причин — відписка,
    недоступність, скарги.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def set(self, request: SuppressionSetRequest) -> SuccessResponse:
        """Додає email-адресу до списку недоступних. Ви завжди зможете пізніше видалити цю адресу зі списку
        недоступних методом
        [suppression/delete](https://docs.allymailer.com.ua/ua/web-api-ref#suppression-delete).

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#suppression-set

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/suppression/set.json", request.to_dict()))

    def get(self, request: SuppressionGetRequest) -> SuppressionGetResponse:
        """Повертає причину й дату блокування email-адреси.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#suppression-get

        Raises ApiError when the API returns an error.
        """
        return SuppressionGetResponse.from_dict(self._client.call("/suppression/get.json", request.to_dict()))

    def list(self, request: SuppressionListRequest) -> SuppressionListResponse:
        """Повертає список недоступних, починаючи з указаної дати.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#suppression-list

        Raises ApiError when the API returns an error.
        """
        return SuppressionListResponse.from_dict(self._client.call("/suppression/list.json", request.to_dict()))

    def delete(self, request: SuppressionDeleteRequest) -> SuccessResponse:
        """Видаляє email-адресу зі списку недоступних (лише записи з is_deletable=true). Якщо жодного запису
        для email не знайдено, повертається помилка API 3003. Якщо записи про недоступність знайдено, але
        жодну з них видалити не можна, повертається помилка API 3004. Якщо перевищено ліміт видалень на
        добу, повертається помилка API 906.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#suppression-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/suppression/delete.json", request.to_dict()))
