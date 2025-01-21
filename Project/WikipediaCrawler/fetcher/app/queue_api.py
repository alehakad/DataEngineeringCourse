from typing import Callable

import pika


class RabbitMQConsumer:
    def __init__(
            self,
            queue_name: str,
            process_message_callback: Callable,
            host: str = "localhost",
            username="user",
            password="password"
    ):
        self.queue_name = queue_name
        self.host = host
        self.process_message_callback = process_message_callback
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=credentials),
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def consume(self):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_message_callback,
            auto_ack=True,
        )
        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def publish(self, message: str | bytes):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message
        )
