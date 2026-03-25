from src.models.order import OrderCreate, Order
from src.clients.payment_client import PaymentClient
import queue


task_queue = queue.Queue()

class OrderService:
    payment_client = PaymentClient()

    @classmethod
    async def create_order(cls, order_data: OrderCreate, users_db, products_db, orders_db) -> Order:
        if order_data.user_id not in users_db:
            raise ValueError("User not found")
        user = users_db[order_data.user_id]
        product_list = []
        for elem in order_data.product_ids:
            if elem not in products_db:
                raise ValueError(f"Product {elem} not found")
            product_list.append(products_db[elem])
        new_id = max(orders_db.keys()) + 1 if orders_db else 1
        temp_order = Order(user=user, products=product_list)
        total = temp_order.calculate_total()
        try:
            payment_result = await cls.payment_client.process_payment(
                order_id=new_id,
                cost=total
            )
            if payment_result.get("status") == "ok":
                payment_status = True
            else:
                payment_status = False

        except Exception as e:
            raise Exception(f"Payment processing failed: {e}")
        new_order = Order(user=user, products=product_list, payment_status=payment_status)
        orders_db[new_id] = new_order
        return new_order

    @classmethod
    async def get_order(cls, order_id: int, orders_db) -> Order:
        if order_id not in orders_db:
            raise ValueError("Order not found")
        return orders_db[order_id]



# Архитектура системы с брокером сообщений для проекта SFMShop:
#
# 1. Producer (src/api/main.py или OrderService):
#    При создании заказа отправляет задачи в очередь:
#        - отправка email-уведомления пользователю
#        - обновление остатков товаров на складе
#        - генерация отчетов
#        - логирование
#
#    Пример:
#        task_queue.put({"task": "send_email", "order_id": new_id})
#        task_queue.put({"task": "update_stock", "order_id": new_id})
#
# 2. Очередь сообщений:
#    - Хранит задачи для обработки
#    - Обеспечивает надежность доставки
#
# 3. Consumer (src/services/queue_consumer.py):
#    - Постоянно слушает очередь и получает задачи из неё
#    - Обрабатывает задачи в фоне
#    - Обрабатывает ошибки и retry
#
#    Пример задач:
#        if task == "send_email":
#            send_email(...)
#        elif task == "update_stock":
#            update_stock(...)
#        elif task == "generate_report":
#            generate_report(...)
#
# 4. Надежность:
#    - Сообщения не теряются
#    - Обработки подтверждаются
#    - Retry при ошибках
#
# 5. Преимущества:
#    - Быстрый ответ API
#    - Масштабируемость
#    - Разделение ответственности
#    - Устойчивость к сбоям
#
# 6. Порядок работы:
#    Клиент -> API -> создание заказа -> отправка задач в очередь ->
#    -> Consumer обрабатывает задачи -> пользователь не ждет фоновые операции
#
#
