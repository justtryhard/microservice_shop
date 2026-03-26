import pika
import json


class QueueProducer:
    def __init__(self, host: str = "localhost"):
        self.connection = None
        self.channel = None
        self.host = host

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue="order_processing", durable=True)
            return True
        except Exception as e:
            print(e)
            return False

    def send_order_task(self, order_id: int, task_type: str, data: dict):
        if not self.channel:
            if not self.connect():
                return False

        try:
            message = {
                "task": task_type,
                "order_id": order_id,
                **data
            }

            self.channel.basic_publish(
                exchange='',
                routing_key='order_processing',
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )

            print(f"task sent to queue: {message}")
            return True

        except Exception as e:
            print(e)
            return False

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()



