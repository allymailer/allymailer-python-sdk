# ConfirmedEmail

[До списку розділів](../README.md)

Керування email-адресами, підтвердженими для надсилання із sandbox-домену. Методи доступні лише з API-ключем основного облікового запису.

`allymailer.api.confirmed_email.ConfirmedEmailApi`, `client.confirmed_email`

| Метод | Ендпоінт | Опис |
|---|---|---|
| [`create`](#create) | `POST /confirmed-email/create.json` | Adds an email address and sends a confirmation link. |
| [`list`](#list) | `POST /confirmed-email/list.json` | Lists confirmed and unconfirmed email addresses for the account. |
| [`delete`](#delete) | `POST /confirmed-email/delete.json` | Deletes an email address from the account's confirmed email list. |

## create

`POST /confirmed-email/create.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#confirmed-email-create)

Adds an email address and sends a confirmation link.

### Запит: `ConfirmedEmailRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `email` | `str` | так | Email address to add or delete. |

### Відповідь: `ConfirmedEmailCreateResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `confirmed_email` | `ConfirmedEmail` |  |

### Приклад

```python
import allymailer
from allymailer.api.confirmed_email import ConfirmedEmailRequest

client = allymailer.client("YOUR_API_KEY")

response = client.confirmed_email.create(ConfirmedEmailRequest(
    email="dev@example.com",
))
print(response.confirmed_email)
```

## list

`POST /confirmed-email/list.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#confirmed-email-list)

Lists confirmed and unconfirmed email addresses for the account.

### Запит

Метод не має параметрів.

### Відповідь: `ConfirmedEmailListResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `confirmed_emails` | `List[ConfirmedEmail]` |  |

### Приклад

```python
import allymailer

client = allymailer.client("YOUR_API_KEY")

response = client.confirmed_email.list()
print(response.confirmed_emails)
```

## delete

`POST /confirmed-email/delete.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#confirmed-email-delete)

Deletes an email address from the account's confirmed email list.

### Запит: `ConfirmedEmailRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `email` | `str` | так | Email address to add or delete. |

### Відповідь: `ConfirmedEmailDeleteResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `message` | `str` |  |

### Приклад

```python
import allymailer
from allymailer.api.confirmed_email import ConfirmedEmailRequest

client = allymailer.client("YOUR_API_KEY")

response = client.confirmed_email.delete(ConfirmedEmailRequest(
    email="dev@example.com",
))
print(response.message)
```
