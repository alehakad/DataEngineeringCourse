import os

from logger_config import logger
from queue_api import QueueConnector
from redis_api import RedisURLHandler


class Filter:

    def __init__(self):
        self.queue_connector = QueueConnector()
        self.redis_connector = RedisURLHandler()

    def check_duplicate(self, url):
        """
        Checks if a given URL was already handled - exists in redis.
        """
        return self.redis_connector.add_url_if_not_exists(url)

    def process_message(self, channel, method, properties, body):
        """
        Processes links adds valid ones to fetcher queue.
        """
        url = body.decode()
        logger.info(f"Checking duplicate url for {url}")
        if not self.check_duplicate(url):
            logger.info(f"Added link {url} to fetcher queue")
            self.queue_connector.publish(url, os.getenv("OUT_QUEUE"))

    def start(self):
        """
        Starts the queue consumption.
        """
        logger.info("Start parser")
        self.queue_connector.consume(os.getenv("IN_QUEUE"), self.process_message)


if __name__ == "__main__":
    filterer = Filter()
    filterer.start()
