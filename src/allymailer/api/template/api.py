"""TemplateApi: API methods of the Template section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import TemplateDeleteRequest, TemplateGetRequest, TemplateGetResponse, TemplateListRequest, TemplateListResponse, TemplateSetRequest, TemplateSetResponse


class TemplateApi:
    """Ви можете зберегти шаблон на боці AllyMailer і потім посилатися на нього за ідентифікатором. Це не
    обов'язково, але вкрай рекомендовано у разі повторюваних email-повідомлень або за великих обсягів
    надсилання. AllyMailer підтримує два різні синтаксиси для шаблонів, докладніше читайте
    [тут](https://docs.allymailer.com.ua/en/template-engines).
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def set(self, request: TemplateSetRequest) -> TemplateSetResponse:
        """Створити або оновити шаблон.

        Обмеження:
        * Максимальний розмір запиту — 10 MB.
        * Кількість шаблонів обмежено 10000.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#template-set

        Raises ApiError when the API returns an error.
        """
        return TemplateSetResponse.from_dict(self._client.call("/template/set.json", request.to_dict()))

    def get(self, request: TemplateGetRequest) -> TemplateGetResponse:
        """Повертає властивості шаблону за його ідентифікатором.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#template-get

        Raises ApiError when the API returns an error.
        """
        return TemplateGetResponse.from_dict(self._client.call("/template/get.json", request.to_dict()))

    def list(self, request: TemplateListRequest) -> TemplateListResponse:
        """Повертає повний список або частину списку всіх шаблонів.

        Ви можете переглядати великий список частинами, використовуючи параметри "offset" і "limit". Якщо
        повернуто менше ніж "limit" шаблонів — значить, ви досягли кінця списку.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#template-list

        Raises ApiError when the API returns an error.
        """
        return TemplateListResponse.from_dict(self._client.call("/template/list.json", request.to_dict()))

    def delete(self, request: TemplateDeleteRequest) -> SuccessResponse:
        """Видаляє шаблон за ідентифікатором.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#template-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/template/delete.json", request.to_dict()))
