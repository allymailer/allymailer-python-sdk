# AllyMailer Python SDK

[![Python](https://img.shields.io/pypi/v/allymailer-python-sdk)](https://pypi.org/project/allymailer-python-sdk/) [![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Офіційна бібліотека Python для API транзакційних листів [AllyMailer](https://allymailer.com.ua).

[Довідник API](https://docs.allymailer.com.ua/ua/web-api-ref) · Документація для LLM: [llms.txt](https://docs.allymailer.com.ua/llms.txt)

> **Django, Flask або FastAPI?** Встановіть [`allymailer-django`](https://github.com/allymailer/allymailer-django) або [`allymailer-flask`](https://github.com/allymailer/allymailer-flask) або [`allymailer-fastapi`](https://github.com/allymailer/allymailer-fastapi): у ньому цей SDK, налаштування, поштовий транспорт і маршрут для вебхуків.

## Встановлення

```bash
pip install allymailer-python-sdk
```

Вимоги: Python 3.8+. Сторонніх залежностей немає.

Отримайте API-ключ у [панелі керування](https://cp.allymailer.com) і зберігайте його у змінній оточення, а не в коді:

```bash
export ALLYMAILER_API_KEY="your-api-key"
```

## Надсилання листа

```python
import os

import allymailer
from allymailer.api.email import EmailSendRequest, MessageObject, MessageObjectRecipientsItem as Recipient
from allymailer.common import BodyObject

client = allymailer.client(os.environ["ALLYMAILER_API_KEY"])

response = client.email.send(EmailSendRequest(
    message=MessageObject(
        recipients=[Recipient.from_address("Олексій <alex@example.com>")],
        from_email="shop@example.com",
        from_name="Магазин",
        subject="Ваше замовлення",
        body=BodyObject.from_html("<p>Вітаємо, {{to_name}}! Ваше замовлення надіслано.</p>"),
    ),
))
print(response.job_id)
```

Адреса відправника має бути на домені, підтвердженому у вашому обліковому записі. Домену ще немає? Надішліть лист із [sandbox-домену](#без-свого-домену-тестовий-sandbox-домен) у три кроки.

## Зміст

- [Рецепти](#рецепти): персоналізація · вкладення · копія і прихована копія · відкладене надсилання · безпечний повтор · помилки · вебхуки
- [Без свого домену: тестовий sandbox-домен](#без-свого-домену-тестовий-sandbox-домен)
- [Запуск у продакшен](#запуск-у-продакшен)
- [Довідник](#довідник)
- [Допомога](#допомога)

## Рецепти

Кожен рецепт продовжує приклад вище: клієнт та імпорти вже є.

### Персоналізація для кожного одержувача

До 500 одержувачів в одному виклику, кожен отримує окрему копію зі своїми підстановками. Метадані одержувача повертаються в його подіях вебхука.

```python
client.email.send(EmailSendRequest(
    message=MessageObject(
        recipients=[
            Recipient.from_address("Олексій <alex@example.com>", {"order": "1001"}).with_metadata({"user_id": "42"}),
            Recipient.from_address("Марія <maria@example.com>", {"order": "1002"}).with_metadata({"user_id": "43"}),
        ],
        from_email="shop@example.com",
        subject="Замовлення №{{order}}",
        body=BodyObject.from_html("<p>{{to_name}}, замовлення №{{order}} надіслано.</p>"),
    ),
))
```

### Вкладення

```python
import base64

from allymailer.common import AttachmentsArrayItem

with open("invoice.pdf", "rb") as file:
    content = base64.b64encode(file.read()).decode()

client.email.send(EmailSendRequest(
    message=MessageObject(
        recipients=[Recipient.from_address("alex@example.com")],
        from_email="shop@example.com",
        subject="Рахунок",
        body=BodyObject.from_html("<p>Рахунок у вкладенні.</p>"),
        attachments=[AttachmentsArrayItem(type="application/pdf", name="invoice.pdf", content=content)],
    ),
))
```

### Копія і прихована копія

Усі адреси передаються в `recipients` (кожна отримує копію), видимі — ще й у заголовках. `audit@example.com` немає в жодному заголовку: це прихована копія. Правила й обмеження: [копія і прихована копія](https://docs.allymailer.com.ua/ua/cc-and-bcc).

```python
from allymailer.common import HeadersObject

client.email.send(EmailSendRequest(
    message=MessageObject(
        recipients=[Recipient.from_address(a) for a in ("alex@example.com", "boss@example.com", "audit@example.com")],
        from_email="shop@example.com",
        subject="Звіт за тиждень",
        body=BodyObject.from_html("<p>Звіт у вкладенні.</p>"),
        headers=HeadersObject(extra={"To": "alex@example.com", "CC": "boss@example.com"}),
    ),
))
```

### Відкладене надсилання

`send_at` — в UTC, не далі ніж на 24 години вперед.

```python
from datetime import datetime, timedelta, timezone

from allymailer.api.email import MessageObjectOptions

# UTC, "YYYY-MM-DD hh:mm:ss"
in_one_hour = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

client.email.send(EmailSendRequest(
    message=MessageObject(
        recipients=[Recipient.from_address("alex@example.com")],
        from_email="shop@example.com",
        subject="Нагадування",
        body=BodyObject.from_text("До зустрічі завтра!"),
        options=MessageObjectOptions(send_at=in_one_hour),
    ),
))
```

### Безпечний повтор

Повтор із тим самим `idempotence_key` протягом хвилини не надішлеться вдруге: з ним повторюйте мережеві помилки, таймаути, 429 і 5xx.

```python
client.email.send(EmailSendRequest(
    message=MessageObject(
        recipients=[Recipient.from_address("alex@example.com")],
        from_email="shop@example.com",
        subject="Скидання пароля",
        body=BodyObject.from_html("<p>Посилання для скидання пароля.</p>"),
        idempotence_key="password-reset-8f3a",
    ),
))
```

### Обробка помилок

Одержувачі, яких API відкинув (відписані, неіснуючі, у стоп-листі), — не помилка: вони у `failed_emails` відповіді, решта лист отримає.

```python
from allymailer import ApiError

try:
    client.email.send(request)
except ApiError as e:
    # HTTP-статус (0: мережева помилка або таймаут), код помилки API, повідомлення
    print(e.http_status, e.error_code, e.message)
```

### Статуси доставки

Зареєструйте свою HTTPS-адресу один раз (`webhook/set`). Потім перевіряйте підпис кожного сповіщення (`auth`: MD5 сирого тіла, у якому значення `auth` замінено на API-ключ; на неправильний — 401) і обробляйте події.

```python
import hashlib
import os

from allymailer.api.webhook import WebhookApi


def handle_webhook(raw_body: str) -> int:
    """raw_body: тіло POST-запиту як надійшло; повертає HTTP-статус відповіді."""
    callback = WebhookApi.parse_callback(raw_body)
    # auth: MD5 сирого тіла, у якому значення auth замінено на ваш API-ключ
    signed = raw_body.replace(callback.auth or "", os.environ["ALLYMAILER_API_KEY"])
    if hashlib.md5(signed.encode()).hexdigest() != callback.auth:
        return 401

    for user in callback.events_by_user or []:
        for event in user.events or []:
            # event.event_data: email, status (delivered, opened, hard_bounced, spam, ...), job_id, metadata
            pass
    return 200
```

> **Відповідайте 200 протягом 3 секунд**, а події обробляйте у фоні (через чергу): інакше AllyMailer повторює запит кожні 10 хвилин протягом доби (зростає `retry_count`), а обробник, на якому за добу не пройшов жоден запит хоча б для 10 подій, вимикається. Обробник має витримувати **щонайменше 5 паралельних запитів до 100 подій у кожному**; повтор надсилає ті самі події ще раз — прибирайте дублікати.

## Без свого домену: тестовий sandbox-домен

Поки ваш домен не підтверджено, листи можна надсилати із **sandbox-домену** — тестового домену, який є в кожного облікового запису: він уже підтверджений, DKIM і SPF налаштовані. Листи з нього доставляються лише на підтверджені вами адреси (посилання для підтвердження приходить листом і діє 48 годин), до 100 на день. Через 31 день після створення sandbox-домен видаляється, але його можна отримати знову: наступний виклик `domain/get-sandbox-domain` створить новий (з іншою назвою, тому беріть її з відповіді, а не прописуйте в коді).

```python
from allymailer.api.confirmed_email import ConfirmedEmailRequest

# 1. Ваш sandbox-домен: створюється під час першого виклику, далі повертається той самий
domain = client.domain.get_sandbox_domain().domain

# 2. Підтвердіть свою скриньку: AllyMailer надішле посилання, перейдіть за ним протягом 48 годин
client.confirmed_email.create(ConfirmedEmailRequest(email="you@example.com"))

# 3. Надішліть із будь-якої адреси sandbox-домену на підтверджену адресу
client.email.send(EmailSendRequest(
    message=MessageObject(
        recipients=[Recipient.from_address("you@example.com")],
        from_email=f"noreply@{domain}",
        subject="Привіт від AllyMailer",
        body=BodyObject.from_html("<p>Працює!</p>"),
    ),
))
```

<details>
<summary>Обмеження sandbox</summary>

- Надсилання лише на підтверджені адреси: до 10 на обліковий запис.
- До 100 листів на день.
- Sandbox-домен спливає через 31 день; знову викличте `domain/get-sandbox-domain`, щоб отримати новий.
- Працює лише з API-ключем облікового запису, не з ключем проєкту.
- Не показується в `domain/list`; інші методи `domain/*` до нього не застосовуються.

Sandbox — для розробки та тестування. Не використовуйте sandbox-домен як відправника на проді.

</details>

<details>
<summary>Те саме через curl</summary>

```bash
BASE=https://cp.allymailer.com/ua/transactional/api/v1

curl -s -X POST $BASE/domain/get-sandbox-domain.json \
  -H "Content-Type: application/json" -H "X-API-KEY: $ALLYMAILER_API_KEY" -d '{}'

curl -s -X POST $BASE/confirmed-email/create.json \
  -H "Content-Type: application/json" -H "X-API-KEY: $ALLYMAILER_API_KEY" \
  -d '{"email": "you@example.com"}'

curl -s -X POST $BASE/email/send.json \
  -H "Content-Type: application/json" -H "X-API-KEY: $ALLYMAILER_API_KEY" \
  -d '{
        "message": {
          "recipients": [
            {
              "email": "you@example.com"
            }
          ],
          "from_email": "noreply@<sandbox-domain>",
          "subject": "Привіт від AllyMailer",
          "body": {
            "html": "<p>Працює!</p>"
          }
        }
      }'
```

</details>

## Запуск у продакшен

**1. Підтвердіть домен надсилання.** `domain/get-dns-records` повертає запис підтвердження, DKIM-ключ і адресу для DMARC; додайте записи у свого DNS-провайдера, потім `domain/validate-verification-record` і `domain/validate-dkim`.

| Тип | Хост | Значення | Звідки взяти |
|---|---|---|---|
| TXT | `@` | `allymailer-validate-hash=…` | поле `verification-record` відповіді, як є |
| TXT | `<селектор>._domainkey` (селектор — на сторінці домену в панелі керування, наприклад `us`) | `v=DKIM1; k=rsa; p=<dkim>` | поле `dkim` відповіді після `v=DKIM1; k=rsa; p=` |
| TXT | `@` | `v=spf1 include:spf.allymailer.com ~all` | у відповіді немає; якщо SPF-запис уже є, додайте include до нього |
| CNAME | `_dmarc` | `<домен>.dmarc.…` | поле `dmarc` відповіді (DMARC-політику публікує AllyMailer); якщо в домену вже є свій TXT-запис DMARC, залиште його |

**2. Надійне надсилання.**

| | |
|---|---|
| Повтори | `429` і `5xx` з backoff і тим самим `idempotence_key`; інші помилки виправляйте, а не повторюйте |
| Ліміти | 500 одержувачів і 10 МБ на запит разом із вкладеннями: у base64 файл стає приблизно на третину більшим |
| Тіло | завжди `html` або `plaintext` (або із шаблону) |
| Статус доставки | вебхук, а не опитування |
| Черга | надсилайте з фонового завдання, а не всередині веб-запиту |
| Налаштування | `from_email` з конфігурації: перехід із sandbox на продакшен без змін у коді |
| Типові налаштування | не прибирайте блок відписки та трекінг; змінити їх можна через підтримку AllyMailer |

## Довідник

### Розділи

| Розділ | Методи | Опис |
|---|---|---|
| [Email](docs/Email.md) | `send`, `subscribe` | Ця група методів пов'язана з надсиланням email. |
| [EmailValidation](docs/EmailValidation.md) | `single` | Методи перевірки email-адрес. Перевірка адреси електронної пошти надає докладну інформацію про працездатність email. Це дозволить виключити з надсилання неіснуючі email, знизити показник скарг, очистити список підписників і врешті-решт покращити вашу репутацію як відправника. Наприклад, ви можете інтегрувати процес перевірки у форму реєстрації вашого сайту і вже на етапі введення адреси повідомляти користувачам, що адреса, яку вони ввели у форму, недійсна. |
| [ConfirmedEmail](docs/ConfirmedEmail.md) | `create`, `list`, `delete` | Керування email-адресами, підтвердженими для надсилання із sandbox-домену. Методи доступні лише з API-ключем основного облікового запису. |
| [Template](docs/Template.md) | `set`, `get`, `list`, `delete` | Ви можете зберегти шаблон на боці AllyMailer і потім посилатися на нього за ідентифікатором. Це не обов'язково, але вкрай рекомендовано у разі повторюваних email-повідомлень або за великих обсягів надсилання. AllyMailer підтримує два різні синтаксиси для шаблонів, докладніше читайте [тут](https://docs.allymailer.com.ua/ua/template-engines). |
| [Webhook](docs/Webhook.md) | `set`, `get`, `list`, `delete` | AllyMailer дозволяє вам отримувати сповіщення про зміну статусу доставки листа або спам-блокування. Ви надаєте URL, і в разі виникнення події, що вас цікавить, ми сповіщаємо вас, передаючи на цей URL JSON-дані про подію. |
| [Suppression](docs/Suppression.md) | `set`, `get`, `list`, `delete` | Методи для керування адресами, надсилання на які заблоковано з різних причин — відписка, недоступність, скарги. |
| [Domain](docs/Domain.md) | `get_dns_records`, `validate_verification_record`, `validate_dkim`, `list`, `get_sandbox_domain`, `delete` | Методи для налаштування доменів надсилання та перевірки їх статусів. Корисні, якщо вам недостатньо додавання доменів через вебінтерфейс AllyMailer і, наприклад, хочеться автоматизувати додавання доменів для ваших власних клієнтів. |
| [EventDump](docs/EventDump.md) | `create`, `get`, `list`, `delete` | Методи для отримання списку подій, що сталися, за певний період. Дані зберігаються до 45 днів, залежно від вашого тарифу. Це означає, що можна запросити події, починаючи з 00:00:00 45-го дня тому і до поточного моменту часу. Для індивідуальних тарифів з великими обсягами за замовчуванням події доступні лише за останні 7 днів. |
| [Tag](docs/Tag.md) | `list`, `delete` | Методи керування користувацькими мітками. За допомогою міток ви можете класифікувати листи за потрібними критеріями. Відокремити маркетингові листи від транзакційних або листи з підтвердженням реєстрації від сповіщень про замовлення. AllyMailer дозволяє позначати мітками кожне вихідне повідомлення, а потім сегментувати й аналізувати статистику на основі зазначених під час надсилання міток. |
| [Project](docs/Project.md) | `create`, `update`, `list`, `delete` | Проєкти дозволяють об'єднати кілька незалежних доменів із webhook, шаблонами та списками відписки. Це дуже корисно, якщо у вас є власні клієнти і ви керуєте їхніми даними з одного облікового запису AllyMailer. Кожен проєкт отримує власний ключ API, а виклики методів API з цим ключем обробляють лише дані цього проєкту. Таким чином, ви можете призначити окремий проєкт для кожного користувача і бути впевненими, що вони не конфліктуватимуть: наприклад, відписка від одного проєкту не вплине на інший. |
| [System](docs/System.md) | `ping`, `info` | Системні методи. |
| [Obsolete](docs/Obsolete.md) | `unsubscribed_set`, `unsubscribed_check`, `unsubscribed_list` | Застарілі методи роботи з відписками. Ми рекомендуємо користуватися замість них гнучкішими методами [suppression](https://docs.allymailer.com.ua/ua/web-api-ref#suppression). Зверніть увагу, що знову підписати відписаного адресата через WebAPI не можна. Можна лише надіслати йому email із посиланням повторної підписки за допомогою методу email/subscribe. |

### Власний HTTP-клієнт / заголовки

`headers` додає HTTP-заголовки до кожного запиту. `transport` замінює HTTP-шар: будь-який об'єкт із `send(method, url, headers, body, timeout) -> (status, body)` (body: bytes; або така функція). Оберніть стандартний `UrllibTransport` для повторів чи логування або викликайте `requests` / `httpx` у власному; виняток транспорту стає `ApiError`.

```python
import time

import allymailer
from allymailer.client import UrllibTransport


class RetryTransport:
    """Logs every request and retries network failures and HTTP 5xx."""

    def __init__(self, inner=None, attempts=3):
        self.inner = inner or UrllibTransport()
        self.attempts = attempts

    def send(self, method, url, headers, body, timeout):
        for attempt in range(1, self.attempts + 1):
            print(method, url)
            try:
                status, raw = self.inner.send(method, url, headers, body, timeout)
            except allymailer.ApiError:
                if attempt == self.attempts:
                    raise
            else:
                if status < 500 or attempt == self.attempts:
                    return status, raw
            time.sleep(attempt)


client = allymailer.client("YOUR_API_KEY", transport=RetryTransport(), headers={"X-Request-Id": "42"})
```

Моделі з довільними ключами (`HeadersObject`) мають словник `extra`: його ключі передаються поруч з іменованими полями.

```python
from allymailer.common import HeadersObject

headers = HeadersObject(extra={
    "X-MyHeader": "some data",
    "CC": "copy@example.com",
    "List-Unsubscribe": "<mailto:unsubscribe@example.com>",
})
```

### Обробка помилок

Кожен метод кидає `ApiError`, якщо API повернув помилку; у ньому є [код помилки API](https://docs.allymailer.com.ua/ua/web-api-ref#api-errors) і HTTP-статус.

## Допомога

- Для ШІ-агентів: [llms.txt](https://docs.allymailer.com.ua/llms.txt), скіли: `npx skills add https://github.com/allymailer/allymailer-skills.git`
- [Підтримка](https://cp.allymailer.com/ua/support) · [Задачі](https://github.com/allymailer/allymailer-python-sdk/issues)
- Розробникам: [AGENTS.md](AGENTS.md) — SDK генерується з OpenAPI-специфікації.
