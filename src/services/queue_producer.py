import pika
import json
import logging


class QueueProducer:
    def __init__(self, host: str = "localhost"):
        self.connection = None
        self.channel = None
        self.host = host
        self.queue_name = "order_processing"

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue="order_processing", durable=True)
            return True
        except Exception as e:
            logging.error(f"Connection error: {e}")
            return False

    def send_order_task(self, order_id: int, task_type: str, data: dict):
        if not self.channel:
            if not self.connect():
                return False


        message = {
            "task": task_type,
            "order_id": order_id,
            "data": data
        }
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )

            logging.info(f"Task sent to queue: {message}")
            return True

        except Exception as e:
            logging.error(f"Error: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()



producer1 = QueueProducer()
producer1.connect()