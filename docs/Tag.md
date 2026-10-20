# Tag

[До списку розділів](../README.md)

Методи керування користувацькими мітками. За допомогою міток ви можете класифікувати листи за потрібними критеріями. Відокремити маркетингові листи від транзакційних або листи з підтвердженням реєстрації від сповіщень про замовлення. AllyMailer дозволяє позначати мітками кожне вихідне повідомлення, а потім сегментувати й аналізувати статистику на основі зазначених під час надсилання міток.

`allymailer.api.tag.TagApi`, `client.tag`

| Метод | Ендпоінт | Опис |
|---|---|---|
| [`list`](#list) | `POST /tag/list.json` | Метод без параметрів, повертає список усіх користувацьких міток. |
| [`delete`](#delete) | `POST /tag/delete.json` | Видаляє мітку. |

## list

`POST /tag/list.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#tag-list)

Метод без параметрів, повертає список усіх користувацьких міток.

### Запит

Метод не має параметрів.

### Відповідь: `TagListResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `tags` | `List[TagsResponseObject]` | Масив об'єктів з даними користувацьких міток. |

### Приклад

```python
import allymailer

client = allymailer.client("YOUR_API_KEY")

response = client.tag.list()
print(response.tags)
```

## delete

`POST /tag/delete.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#tag-delete)

Видаляє мітку.

### Запит: `TagDeleteRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `tag_id` | `int` | так | Унікальний id мітки. |

### Відповідь: `SuccessResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |

### Приклад

```python
import allymailer
from allymailer.api.tag import TagDeleteRequest

client = allymailer.client("YOUR_API_KEY")

response = client.tag.delete(TagDeleteRequest(
    tag_id=54,
))
```
