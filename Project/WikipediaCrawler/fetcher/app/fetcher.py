import os
from typing import List

import requests
from bs4 import BeautifulSoup

from db_api import MongoConnector
from logger_config import logger
from queue_api import QueueConnector


class Fetcher:
    start_url = "https://en.wikipedia.org/wiki/Main_Page"
    in_queue = "valid_links"
    out_queue = "to_check_links"
    html_storage_path = "/app/html_pages"

    def __init__(self):
        logger.info(f"Connect to queue")
        self.queue_connector = QueueConnector(host="rabbitmq")
        self.mongo_connector = MongoConnector()
        os.makedirs(Fetcher.html_storage_path, exist_ok=True)
        # TODO: add argument to add only from one container
        # seed first url
        self.queue_connector.publish(Fetcher.start_url, Fetcher.in_queue)
        logger.info(f"Published start url")

    @staticmethod
    def fetch_html(url: str):
        """
        Fetches the HTML content of a given URL.
        """
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @staticmethod
    def save_html_to_local(url, html_content):
        """
        Saves the fetched HTML content to a local file.
        """
        sanitized_name = url.replace("http://", "").replace("https://", "").replace("/", "_")
        file_path = os.path.join(Fetcher.html_storage_path, f"{sanitized_name}.html")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        logger.info(f"Page {url} saved to local storage")
        return file_path

    def process_message(self, channel, method, properties, body):
        """
        Processes a message by fetching HTML from the URL, saving it locally,
        extracting links from the HTML content, and publishing them to the out_queue.
        """
        url = body.decode()
        logger.info(f"Fetching HTML from {url}")

        if not url:
            return

        html_content = self.fetch_html(url)
        if not html_content:
            logger.error(f"Failed to fetch HTML from {url}")
            return
        # save html to localhost
        self.save_html_to_local(url, html_content)
        # add url with metadata to mongo
        # TODO: add metadata and filepath
        self.mongo_connector.save_url_to_db(url)
        # find links
        links = self.find_html_links(html_content)
        # add to next message queues
        for link in links:
            self.queue_connector.publish(link, Fetcher.out_queue)

    @staticmethod
    def find_html_links(html_content) -> List[str]:
        """
        Extracts all the hyperlinks from the HTML content.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            links.add(href)
        return list(links)

    def start(self):
        """
        Starts the queue consumption.
        """
        self.queue_connector.consume(Fetcher.in_queue, self.process_message)

    def close(self):
        """
        Clean up resources
        """
        logger.info("Closing resources...")
        self.mongo_connector.close()


if __name__ == "__main__":
    fetcher = Fetcher()
    try:
        fetcher.start()
    except KeyboardInterrupt:
        logger.info("Interrupted. Shutting down")
    finally:
        fetcher.close()
