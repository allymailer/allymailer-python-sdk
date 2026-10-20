"""ProjectApi: API methods of the Project section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import ProjectCreateRequest, ProjectCreateResponse, ProjectDeleteRequest, ProjectListRequest, ProjectListResponse, ProjectUpdateRequest, ProjectUpdateResponse


class ProjectApi:
    """Проєкти дозволяють об'єднати кілька незалежних доменів із webhook, шаблонами та списками відписки.
    Це дуже корисно, якщо у вас є власні клієнти і ви керуєте їхніми даними з одного облікового запису
    AllyMailer. Кожен проєкт отримує власний ключ API, а виклики методів API з цим ключем обробляють
    лише дані цього проєкту. Таким чином, ви можете призначити окремий проєкт для кожного користувача і
    бути впевненими, що вони не конфліктуватимуть: наприклад, відписка від одного проєкту не вплине на
    інший.

    Методи проєктів за замовчуванням вимкнено через заходи захисту від спаму. Щоб їх увімкнути, вам
    необхідно звернутися до [служби підтримки](https://cp.allymailer.com/ua/support).

    Зверніть увагу: за замовчуванням домени для надсилання підтверджуються та використовуються незалежно
    для основного облікового запису й кожного з проєктів. Але є можливість увімкнути для проєктів
    використання доменів, підтверджених в основному обліковому записі. Просто попросіть про це
    [техпідтримку](https://cp.allymailer.com/ua/support).
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def create(self, request: ProjectCreateRequest) -> ProjectCreateResponse:
        """Створити новий проєкт.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#project-create

        Raises ApiError when the API returns an error.
        """
        return ProjectCreateResponse.from_dict(self._client.call("/project/create.json", request.to_dict()))

    def update(self, request: ProjectUpdateRequest) -> ProjectUpdateResponse:
        """Змінити властивості проєкту.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#project-update

        Raises ApiError when the API returns an error.
        """
        return ProjectUpdateResponse.from_dict(self._client.call("/project/update.json", request.to_dict()))

    def list(self, request: ProjectListRequest) -> ProjectListResponse:
        """Повертає список проєктів.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#project-list

        Raises ApiError when the API returns an error.
        """
        return ProjectListResponse.from_dict(self._client.call("/project/list.json", request.to_dict()))

    def delete(self, request: ProjectDeleteRequest) -> SuccessResponse:
        """Видалити проєкт.

        Деякий час проєкт не видаляється остаточно, і його ще можна відновити — для цього необхідно
        звернутися в техпідтримку.

        Документація: https://docs.allymailer.com.ua/ua/web-api-ref#project-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/project/delete.json", request.to_dict()))
