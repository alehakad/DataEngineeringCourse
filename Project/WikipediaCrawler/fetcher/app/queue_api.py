import os
from typing import Callable

import pika

from logger_config import logger


# TODO: move to utils
class QueueConnector:
    """
    A class to connect to RabbitMQ, consume messages from a queue,
    and publish messages to a queue.
    """

    def __init__(self):
        """
        Initializes a connection to RabbitMQ using the provided connection parameters.
        """
        self.host = os.getenv("RABBITMQ_HOST")
        credentials = pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"), os.getenv("RABBITMQ_DEFAULT_PASS"))
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=credentials),
        )
        self.channel = self.connection.channel()

    def consume(self, queue_name: str, process_message_callback: Callable, dead_letter_queue: str | None = None):
        """
        Starts consuming messages from the specified queue and processes them
        using the provided callback function.
        """
        if not dead_letter_queue:
            self.channel.queue_declare(queue=queue_name, durable=True)
        else:
            # set up dead letter queue to retry failed messages
            self.channel.queue_declare(queue=queue_name, durable=True,
                                       arguments={'x-dead-letter-exchange': '',
                                                  'x-dead-letter-routing-key': dead_letter_queue,
                                                  })
            # declare dead message queue to send back to urls queue
            self.channel.queue_declare(queue=dead_letter_queue, durable=True, arguments={'x-message-ttl': 5000,
                                                                                         'x-dead-letter-exchange': '',
                                                                                         'x-dead-letter-routing-key': queue_name})
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=process_message_callback,
            auto_ack=False,
        )
        logger.debug("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def publish(self, message: str | bytes, queue_name: str):
        """
        Publishes a message to the specified queue.
        """
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)  # to ensure message persist
        )
        logger.debug(f"Message sent to queue {queue_name}: {message}")

    def nack(self, delivery_tag: int):
        """
        Sending nack about message to the queue to send it to retry dead letter queue
        """
        self.channel.basic_ack(delivery_tag)

    def ack(self, delivery_tag: int):
        """
        Acknowledge in case message is proceeded successfully
        """
        self.channel.basic_ack(delivery_tag)
