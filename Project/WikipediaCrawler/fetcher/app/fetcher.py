import logging
import os
import sys
from typing import List

import requests
from bs4 import BeautifulSoup

from queue_api import RabbitMQConsumer


class Fetcher:
    start_url = "https://en.wikipedia.org/wiki/Main_Page"

    def __init__(self):
        # Set up logger to log to stdout
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create StreamHandler to log to stdout (which Docker uses)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.info(f"Connect to queue")
        self.in_queue = RabbitMQConsumer(
            "html_links", self.process_message, host="rabbitmq"
        )
        self.html_storage_path = "./html_storage"
        os.makedirs(self.html_storage_path, exist_ok=True)

        # TODO: add argument to add only from one container
        self.in_queue.publish(Fetcher.start_url)
        self.logger.info(f"Published start url")

    def fetch_html(self, url: str):
        # TODO: add logger
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def save_html_to_local(self, url, html_content):
        sanitized_name = url.replace("http://", "").replace("https://", "").replace("/", "_")
        file_path = os.path.join(self.html_storage_path, f"{sanitized_name}.html")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        return file_path

    def process_message(self, channel, method, properties, body):
        url = body.decode()
        self.logger.info(f"Fetching HTML from {url}")
        if not url:
            return

        html_content = self.fetch_html(url)
        if not html_content:
            self.logger.error(f"Failed to fetch HTML from {url}")
            return
        # save html to localhost
        self.save_html_to_local(url, html_content)
        # find links
        links = self.find_html_links(html_content)
        # add to next message queue
        for link in links:
            self.add_to_message_queue(link)

    def find_html_links(self, html_content) -> List[str]:
        soup = BeautifulSoup(html_content, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            links.add(href)
        return list(links)

    def add_to_message_queue(self, url):
        pass

    def start(self):
        self.in_queue.consume()


if __name__ == "__main__":
    fetcher = Fetcher()
    fetcher.start()
