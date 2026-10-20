"""EventDumpApi: API methods of the EventDump section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import EventDumpCreateRequest, EventDumpCreateResponse, EventDumpDeleteRequest, EventDumpGetRequest, EventDumpGetResponse, EventDumpListResponse


class EventDumpApi:
    """Методи для отримання списку подій, що сталися, за певний період. Дані зберігаються до 45 днів,
    залежно від вашого тарифу. Це означає, що можна запросити події, починаючи з 00:00:00 45-го дня тому
    і до поточного моменту часу. Для індивідуальних тарифів з великими обсягами за замовчуванням події
    доступні лише за останні 7 днів.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def create(self, request: EventDumpCreateRequest) -> EventDumpCreateResponse:
        """Асинхронний метод, який ініціює підготовку для завантаження файлів дампа у форматі CSV. Максимальна
        кількість збережених/створюваних дампів обмежена десятьма. У разі досягнення ліміту для запиту на
        підготовку нового дампа потрібно видалити старі. Час зберігання сформованого дампа — 8 годин, після
        чого він автоматично видаляється. Якщо період запиту даних більший за добу або подій багато, буде
        сформовано декілька файлів, у кожному з яких буде не більше ніж 100 000 подій. Файл містить колонки
        з такою інформацією — 'event_time', 'job_id', 'from_email', 'email', 'status', 'delivery_status',
        'metadata', 'destination_response', 'user_agent', 'url', 'ip', 'tags' і 'project_id' (якщо у
        користувача увімкнено проєкти). Ви можете відфільтрувати поля та змінити їх порядок, а також додати
        поле 'subject' за допомогою параметра 'dump_fileds'.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#event-dump-create

        Raises ApiError when the API returns an error.
        """
        return EventDumpCreateResponse.from_dict(self._client.call("/event-dump/create.json", request.to_dict()))

    def get(self, request: EventDumpGetRequest) -> EventDumpGetResponse:
        """Повертає властивості дампа за його ідентифікатором.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#event-dump-get

        Raises ApiError when the API returns an error.
        """
        return EventDumpGetResponse.from_dict(self._client.call("/event-dump/get.json", request.to_dict()))

    def list(self) -> EventDumpListResponse:
        """Метод без параметрів, повертає список усіх дампів подій.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#event-dump-list

        Raises ApiError when the API returns an error.
        """
        return EventDumpListResponse.from_dict(self._client.call("/event-dump/list.json"))

    def delete(self, request: EventDumpDeleteRequest) -> SuccessResponse:
        """Видаляє дамп із черги та/або зі сховища.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#event-dump-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/event-dump/delete.json", request.to_dict()))
