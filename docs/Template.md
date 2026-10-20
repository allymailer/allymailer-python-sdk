# Template

[До списку розділів](../README.md)

Ви можете зберегти шаблон на боці AllyMailer і потім посилатися на нього за ідентифікатором. Це не обов'язково, але вкрай рекомендовано у разі повторюваних email-повідомлень або за великих обсягів надсилання. AllyMailer підтримує два різні синтаксиси для шаблонів, докладніше читайте [тут](https://docs.allymailer.com.ua/en/template-engines).

`allymailer.api.template.TemplateApi`, `client.template`

| Метод | Ендпоінт | Опис |
|---|---|---|
| [`set`](#set) | `POST /template/set.json` | Створити або оновити шаблон. |
| [`get`](#get) | `POST /template/get.json` | Повертає властивості шаблону за його ідентифікатором. |
| [`list`](#list) | `POST /template/list.json` | Повертає повний список або частину списку всіх шаблонів. |
| [`delete`](#delete) | `POST /template/delete.json` | Видаляє шаблон за ідентифікатором. |

## set

`POST /template/set.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#template-set)

Створити або оновити шаблон.

Обмеження:
* Максимальний розмір запиту — 10 MB.
* Кількість шаблонів обмежено 10000.

### Запит: `TemplateSetRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `template` | `TemplateObject` | так | Об'єкт, що містить властивості шаблону. |

### Відповідь: `TemplateSetResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `template` | `TemplateObject` | Об'єкт, що містить властивості шаблону. |

### Приклад

```python
import allymailer
from allymailer.api.template import TemplateSetRequest, TemplateObject, EditorType
from allymailer.common import TemplateEngine

client = allymailer.client("YOUR_API_KEY")

response = client.template.set(TemplateSetRequest(
    template=TemplateObject(
        name="name",
        editor_type=EditorType.HTML,
        template_engine=TemplateEngine.VELOCITY,
        subject="AllyMailer test email ",
        from_email="user@example.com",
        from_name="John Smith",
        reply_to="email@example.com",
        reply_to_name="John Smith",
    ),
))
print(response.template)
```

## get

`POST /template/get.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#template-get)

Повертає властивості шаблону за його ідентифікатором.

### Запит: `TemplateGetRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `id` | `str` | так | Ідентифікатор шаблону. |

### Відповідь: `TemplateGetResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `template` | `TemplateObject` | Об'єкт, що містить властивості шаблону. |

### Приклад

```python
import allymailer
from allymailer.api.template import TemplateGetRequest

client = allymailer.client("YOUR_API_KEY")

response = client.template.get(TemplateGetRequest(
    id="00000000-0000-0000-0000-000000000000",
))
print(response.template)
```

## list

`POST /template/list.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#template-list)

Повертає повний список або частину списку всіх шаблонів.

Ви можете переглядати великий список частинами, використовуючи параметри "offset" і "limit". Якщо повернуто менше ніж "limit" шаблонів — значить, ви досягли кінця списку.

### Запит: `TemplateListRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `limit` | `int` |  | Максимальна кількість шаблонів, що повертаються, за замовчуванням 50. |
| `offset` | `int` |  | Індекс першого шаблону зі списку, що повертається, рахуючи з нуля. |

### Відповідь: `TemplateListResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |
| `templates` | `List[TemplateListObject]` | Масив об'єктів-шаблонів. |

### Приклад

```python
import allymailer
from allymailer.api.template import TemplateListRequest

client = allymailer.client("YOUR_API_KEY")

response = client.template.list(TemplateListRequest())
print(response.templates)
```

## delete

`POST /template/delete.json` · [Документація](https://docs.allymailer.com.ua/ua/web-api-ref#template-delete)

Видаляє шаблон за ідентифікатором.

### Запит: `TemplateDeleteRequest`

| Поле | Тип | Обов'язкове | Опис |
|---|---|---|---|
| `id` | `str` | так | Ідентифікатор шаблону. |

### Відповідь: `SuccessResponse`

| Поле | Тип | Опис |
|---|---|---|
| `status` | `str` | Рядок "success". (`success`) |

### Приклад

```python
import allymailer
from allymailer.api.template import TemplateDeleteRequest

client = allymailer.client("YOUR_API_KEY")

response = client.template.delete(TemplateDeleteRequest(
    id="00000000-0000-0000-0000-000000000000",
))
```
