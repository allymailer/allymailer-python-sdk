# Project

[До списку розділів](../README.md)

Проєкти дозволяють об'єднати кілька незалежних доменів із webhook, шаблонами та списками відписки. Це дуже корисно, якщо у вас є власні клієнти і ви керуєте їхніми даними з одного облікового запису AllyMailer. Кожен проєкт отримує власний ключ API, а виклики методів API з цим ключем обробляють лише дані цього проєкту. Таким чином, ви можете призначити окремий проєкт для кожного користувача і бути впевненими, що вони не конфліктуватимуть: наприклад, відписка від одного проєкту не вплине на інший.

Методи проєктів за замовчуванням вимкнено через заходи захисту від спаму. Щоб їх увімкнути, вам необхідно звернутися до [служби підтримки](https://cp.allymailer.com/ua/support).

Зверніть увагу: за замовчуванням домени для надсилання підтверджуються та використовуються незалежно для основного облікового запису й кожного з проєктів. Але є можливість увімкнути для проєктів використання доменів, підтверджених в основному обліковому записі. Просто попросіть про це [техпідтримку](https://cp.allymailer.com/ua/support).

`allymailer.api.project.ProjectApi`, `client.project`

| Метод | Ендпоінт | Опис |
|---|---|---|
| [`create`](#create) | `POST /project/create.json` | Створити новий проєкт. |
| [`update`](#update) | `POST /project/update.json` | Змінити властивості проєкту. |
| [`list`](#list) | `POST /project/list.json` | Повертає список проєктів. |
| [`delete`](#delete) | `POST /project/delete.json` | Видалити проєкт. |

## create

`POST /project/create.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#project-create)

Створити новий проєкт.

### Запит: `ProjectCreateRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `project` | `ProjectObject` | так | Об'єкт із властивостями проєкту. |

### Відповідь: `ProjectCreateResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `project_id` | `str` | Унікальний ідентифікатор проєкту, ASCII-рядок до 36 символів завдовжки. |
| `project_api_key` | `str` | API-ключ проєкту. Ви можете використовувати цей ключ замість користувацького api_key у всіх методах, крім project-методів. |

### Приклад

```python
import allymailer
from allymailer.api.project import ProjectCreateRequest, ProjectObject

client = allymailer.client("YOUR_API_KEY")

response = client.project.create(ProjectCreateRequest(
    project=ProjectObject(
        name="Project 1A",
        country="ES",
        backend_domain_id=1234,
        unsubscribe_page_id=1,
    ),
))
print(response.project_id)
```

## update

`POST /project/update.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#project-update)

Змінити властивості проєкту.

### Запит: `ProjectUpdateRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `project_id` | `str` |  | Ідентифікатор проєкту, що оновлюється. Проєкт має бути ідентифіковано або цим полем project_id, або полем project_api_key. Ми рекомендуємо використовувати project_id, це безпечніше. |
| `project_api_key` | `str` |  | Необов'язковий API-ключ проєкту, що оновлюється. Проєкт має бути ідентифіковано або полем project_id, або полем project_api_key. Ми рекомендуємо використовувати project_id, це безпечніше. |
| `project` | `ProjectUpdateObject` | так | Об'єкт із властивостями проєкту. |

### Відповідь: `ProjectUpdateResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `project_api_key` | `str` | API-ключ проєкту. Повертається лише в разі, якщо в параметрі запиту був project_api_key. Якщо ж проєкт було ідентифіковано через project_id, то не повертається. |

### Приклад

```python
import allymailer
from allymailer.api.project import ProjectUpdateRequest, ProjectUpdateObject

client = allymailer.client("YOUR_API_KEY")

response = client.project.update(ProjectUpdateRequest(
    project_id="1234567890",
    project_api_key="your api_key",
    project=ProjectUpdateObject(
        name="Project 1A",
        country="ES",
        backend_domain_id=1234,
        unsubscribe_page_id=1,
    ),
))
print(response.project_api_key)
```

## list

`POST /project/list.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#project-list)

Повертає список проєктів.

### Запит: `ProjectListRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `project_id` | `str` |  | Опціональна можливість указати project_id для включення до списку лише вказаного проєкту. |
| `project_api_key` | `str` |  | Опціональна можливість указати project_api_key для включення до списку лише вказаного проєкту. |

### Відповідь: `ProjectListResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `projects` | `List[ProjectListObject]` | Масив об'єктів, де кожен об'єкт відповідає окремому проєкту. |

### Приклад

```python
import allymailer
from allymailer.api.project import ProjectListRequest

client = allymailer.client("YOUR_API_KEY")

response = client.project.list(ProjectListRequest(
    project_id="1234567890",
    project_api_key="your api_key",
))
print(response.projects)
```

## delete

`POST /project/delete.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#project-delete)

Видалити проєкт.

Деякий час проєкт не видаляється остаточно, і його ще можна відновити — для цього необхідно звернутися в техпідтримку.

### Запит: `ProjectDeleteRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `project_id` | `str` |  | Ідентифікатор проєкту, що видаляється. Проєкт має бути ідентифіковано або цим полем project_id, або полем project_api_key. Ми рекомендуємо використовувати project_id, це безпечніше. |
| `project_api_key` | `str` |  | Необов'язковий API-ключ проєкту, що видаляється. Проєкт має бути ідентифіковано або полем project_id, або полем project_api_key. Ми рекомендуємо використовувати project_id, це безпечніше. |

### Відповідь: `SuccessResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |

### Приклад

```python
import allymailer
from allymailer.api.project import ProjectDeleteRequest

client = allymailer.client("YOUR_API_KEY")

response = client.project.delete(ProjectDeleteRequest(
    project_id="1234567890",
    project_api_key="your api_key",
))
```
