# Wallet API
API с использованием Django REST Framework для управления кошельками пользователей. 
Кошельки представляют собой виртуальные счета, с помощью которых пользователи могут производить различные операции, такие как пополнение баланса и перевод средств другим пользователям.

---

## Содержание
- [Requirements](#requirements)
- [How to use](#how-to-use)
- [Links](#links)
- [Endpoints](#endpoints)

---
## Requirements
- Django==5.0.4
- djangorestframework==3.15.1
- django-extensions==3.2.3
- drf-yasg==1.21.7
- Werkzeug==3.0.2
- pyOpenSSL==24.1.0
- psycopg2==2.9.9
- django-watchman==1.3.0

---

## How to use

Для запуска с HTTPS необходимо иметь localhost.crt и localhost.key в директории проекта. Сертификат и ключ можно получить с помощью OpenSSL.

```
python manage.py runserver_plus --cert-file localhost.crt --key-file localhost.key
```
---

## Links

Swagger доступен по ссылке:
```
http://127.0.0.1:8000/swagger/
```
Дашборд мониторинга:
```
http://127.0.0.1:8000/api/v1/watchman/dashboard
```
---
## Endpoints
Эндпоинт получения токена. Метод POST, требует ***username*** и ***password***, передать их можно в Postman как query-params. Создать пользователя можно с помощью createsuperuser.
```
http://127.0.0.1:8000/api/v1/token/?username=&password=
```
Эндпоинт создания кошелька с уникальным ключом. Метод POST, требует токен, передать его можно с помощью headers в Postman - `Authorization: Token <your_token>`.
```
http://127.0.0.1:8000/api/v1/create/wallet/
```
Эндпоинт просмотра баланса кошелька. Метод GET, требует ключ кошелька и токен.
```
http://127.0.0.1:8000/api/v1/view/wallet/{key_wallet}/ 
```
Эндпоинт пополнения кошелька. Метод POST, требует ключ кошелька, сумму пополнения (amount) и токен.
```
http://127.0.0.1:8000/api/v1/deposit/wallet/{key_wallet}/?amount=
```
Эндпоинт перевода средств с одного кошелька на другой. Метод POST, требует ключ кошелька отправителя, ключ кошелька получаетля, сумму перевода и токен. 
```
http://127.0.0.1:8000/api/v1/transfer/wallet/?sender_key=&recipient_key=&amount= 
```