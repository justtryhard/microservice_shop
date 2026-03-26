import pika
import json
import time


class QueueConsumer:
    def __init__(self, queue_name: str, host: str = "localhost"):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def process_task(self, message: dict):
        task = message.get("task")
        if task == "create_order":
            print(f"creating order {message['order_id']}")
        else:
            print("unknown task")

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        retry_count = message.get("retry", 0)
        try:
            print(f"received: {message}")
            self.process_task(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(e)
            if retry_count < 3:
                message["retry"] = retry_count + 1
                time.sleep(1)
                ch.basic_publish(
                    exchange="",
                    routing_key=self.queue_name,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=2
                    ),
                )
                print(f"retrying {message['retry']}")
            else:
                print("failed aftre all retries:")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        print("consumer is waiting")
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
        )
        self.channel.start_consuming()


if __name__ == "__main__":
    consumer = QueueConsumer("order_tasks")
    consumer.start()