import pika
import json


class QueueProducer:
    def __init__(self, host: str = "localhost"):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def send_message(self, queue_name: str, message: dict):
        self.declare_queue(queue_name)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f"message {message} sent!")

    def close(self):
        self.connection.close()




