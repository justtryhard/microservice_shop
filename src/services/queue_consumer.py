import pika
import json
import time
import logging


logging.basicConfig(level=logging.INFO)

class QueueConsumer:
    def __init__(self, queue_name: str, host: str = "localhost"):
        self.queue_name = queue_name
        self.host = host
        self.connection = None
        self.channel = None
        self.max_retries = 3
        self.queue_name = "order_processing"

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
            logging.error(f"Connection error: {e}")
            return False

    def process_task(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            task = message["task"]
            retry_count = properties.headers.get('x-retry-count', 0) if properties.headers else 0

            if task == "create_order":
                products = message["data"]["products"]
                logging.info(f"Creating order {message['order_id']}: {products}")
            elif task == "send_email":
                email = message["data"]["email"]
                logging.info(f"Sending email to {email}")
            elif task == "update_stock":
                products = message["data"]["products"]
                logging.info(f"Updating stock for {products}")
            elif task == "generate_report":
                order_id = message["data"]["order_id"]
                logging.info(f"Generating report for {order_id}")
            else:
                logging.error("unknown task")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.info(f"task processed")
        except Exception as e:
            logging.error(f"Processing failure: {e}")

            if retry_count < self.max_retries:
                retry_count += 1
                delay = 2 ** retry_count

                logging.info(f"next retry {retry_count}/{self.max_retries} in {delay} sec")
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
                logging.warning(f"Task send to queue after {self.max_retries} retries")

    def start(self):
        if not self.connect():
            return
        logging.info("consumer is waiting")
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