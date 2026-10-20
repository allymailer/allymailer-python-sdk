"""SystemApi: API methods of the System section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from .models import SystemInfoResponse, SystemPingResponse


class SystemApi:
    """Системні методи."""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def ping(self) -> SystemPingResponse:
        """Перевіряє валідність API-ключа та повертає ідентифікатор користувача.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#system-ping

        Raises ApiError when the API returns an error.
        """
        return SystemPingResponse.from_dict(self._client.call("/system/ping.json"))

    def info(self) -> SystemInfoResponse:
        """Повертає інформацію про користувача або проєкт за API-ключем.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#system-info

        Raises ApiError when the API returns an error.
        """
        return SystemInfoResponse.from_dict(self._client.call("/system/info.json"))
