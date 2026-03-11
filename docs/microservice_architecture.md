# Структура

- src/api/main.py - точка входа FastAPI (8001)
- src/api/routes/orders.py - эндпойнты для заказов
- src/models/ - pydantic модели
- src/clients/payment_client.py - бизнес логика обработки платежей
- src/services/order_service.py - бизнес логика заказов
- data.py - хранилище данных для тестирования
- payment_service/main.py - точка входа FastAPI для работы с платежами (8002)


# Ответственность микросервиса
- приём запросов на проведение платежа от других сервисов 
- валидация входящих данных (сумма, идентификатор заказа)
- имитация обработки платежа
- Возврат  ошибок в случае некорректных запросов или внутренних сбоев

# Эндпойнты

1. Создание платежа (/payments)
2. Получение информации о платеже (/payments/{payment_id})
3. Проверка состояния (/test)

# Взаимодействие с order service

1. order service получает запрос на создание заказа
2. проверяет юзера и товары, вычисляет итоговую сумму
3. отправляет post-запрос в payment-service на /api/v1/payments
4. payment service обрабатывает запрос, имитирует успешный платёж и возвращает "status": "ok"
5. order service обрабатывает ответ: если "ok", то заказ оплачен (True). Если статус иной - заказ сохраняется, но как неоплаченный (False)

# Обработка ошибок

- таймаут payment-service - order service возвращает клиенту 502 с пояснением
- http-ошибка от payment-service - аналогично 502 от order service
- невалидные данные - payment-service возвращает 400, order service перебрасывает как 502


# Развёртывание
order service:
python -m uvicorn src.api.main:app --reload --port 8001

payment service:
python -m uvicorn payment_service.main:app --reload --port 8002

