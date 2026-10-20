"""ConfirmedEmailApi: API methods of the ConfirmedEmail section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from .models import ConfirmedEmailCreateResponse, ConfirmedEmailDeleteResponse, ConfirmedEmailListResponse, ConfirmedEmailRequest


class ConfirmedEmailApi:
    """Керування email-адресами, підтвердженими для надсилання із sandbox-домену. Методи доступні лише з
    API-ключем основного облікового запису.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def create(self, request: ConfirmedEmailRequest) -> ConfirmedEmailCreateResponse:
        """Adds an email address and sends a confirmation link.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#confirmed-email-create

        Raises ApiError when the API returns an error.
        """
        return ConfirmedEmailCreateResponse.from_dict(self._client.call("/confirmed-email/create.json", request.to_dict()))

    def list(self) -> ConfirmedEmailListResponse:
        """Lists confirmed and unconfirmed email addresses for the account.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#confirmed-email-list

        Raises ApiError when the API returns an error.
        """
        return ConfirmedEmailListResponse.from_dict(self._client.call("/confirmed-email/list.json"))

    def delete(self, request: ConfirmedEmailRequest) -> ConfirmedEmailDeleteResponse:
        """Deletes an email address from the account's confirmed email list.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#confirmed-email-delete

        Raises ApiError when the API returns an error.
        """
        return ConfirmedEmailDeleteResponse.from_dict(self._client.call("/confirmed-email/delete.json", request.to_dict()))
