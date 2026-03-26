import pika
import json
import time


class QueueConsumer:
    def __init__(self, queue_name: str, host: str = "localhost"):
        self.queue_name = queue_name
        self.host = host
        self.connection = None
        self.channel = None
        self.max_retries = 3

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.basic_qos(prefetch_count=1)
            return True
        except Exception as e:
            print(e)
            return False

    def process_task(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            task = message["task"]
            retry_count = properties.headers.get('x-retry-count', 0) if properties.headers else 0

            if task == "create_order":
                print(f"creating order {message['order_id']}: {message['products']}")
            else:
                print("unknown task")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"task processed")
        except Exception as e:
            print(f"processing failure {e}")

            if retry_count < self.max_retries:
                retry_count += 1
                delay = 2 ** retry_count

                print(f"next retry {retry_count}/{self.max_retries} in {delay} sec")
                time.sleep(delay)

                ch.basic_publish(
                    exchange='',
                    routing_key='order_processing',
                    body=body,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        headers={'x-retry-count': retry_count}
                    )
                )

                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            else:
                ch.basic_publish(
                    exchange='',
                    routing_key='order_processing_errors',
                    body=body,
                    properties=pika.BasicProperties(delivery_mode=2)
                )

                ch.basic_ack(delivery_tag=method.delivery_tag)
                print(f"task send to queue after {self.max_retries} retries")

    def start(self):
        if not self.connect():
            return
        print("consumer is waiting")
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_task
        )
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.connection.close()

if __name__ == "__main__":
    consumer = QueueConsumer("order_processing")
    consumer.start()