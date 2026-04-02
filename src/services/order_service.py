from src.models.order import OrderCreate, Order
from src.clients.payment_client import PaymentClient
from src.services.queue_producer import producer1
from src.services.log_service import log_service

class OrderService:
    payment_client = PaymentClient()

    @classmethod
    async def create_order(cls, order_data: OrderCreate, users_db, products_db, orders_db) -> Order:
        if order_data.user_id not in users_db:
            log_service.error("Order creating failed: User not found", user_id=order_data.user_id)
            raise ValueError("User not found")
        user = users_db[order_data.user_id]
        product_list = []
        for elem in order_data.product_ids:
            if elem not in products_db:
                log_service.error("Order creating failed: Product not found", product_id=elem)
                raise ValueError(f"Product {elem} not found")
            product_list.append(products_db[elem])
        new_id = max(orders_db.keys()) + 1 if orders_db else 1
        temp_order = Order(user=user, products=product_list)
        total = temp_order.calculate_total()
        try:
            log_service.info("Checking payment status", order_id=new_id)
            payment_result = await cls.payment_client.process_payment(
                order_id=new_id,
                cost=total
            )
            if payment_result.get("status") == "ok":
                payment_status = True
                log_service.info("Payment successful", order_id=new_id)
            else:
                payment_status = False
                log_service.error("Payment failed", order_id=new_id)

        except Exception as e:
            log_service.error("Payment processing failed", order_id=new_id, error=e)
            raise Exception(f"Payment processing failed: {e}")

        try:
            producer1.send_order_task(new_id, "create_order", {'products': order_data.product_ids})
            producer1.send_order_task(new_id, "send_email", {"user_id": user.name, "email": user.email})
            producer1.send_order_task(new_id, "update_stock", {"products": order_data.product_ids})
            producer1.send_order_task(new_id, "generate_report", {"order_id": new_id})
        except Exception as e:
            log_service.error(f"Failed to send task to RabbitMQ: ", e)
        new_order = Order(user=user, products=product_list, payment_status=payment_status)
        orders_db[new_id] = new_order
        log_service.info("Order created", order_id=new_id, products=[{elem.name: elem.price} for elem in new_order.products], payment_status=new_order.payment_status)
        return new_order

    @classmethod
    async def get_order(cls, order_id: int, orders_db) -> Order:
        if order_id not in orders_db:
            log_service.error("Order not found", order_id=order_id)
            raise ValueError("Order not found")
        log_service.info("Getting order", order_id=order_id)
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
