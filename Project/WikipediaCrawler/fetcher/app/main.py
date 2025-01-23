import os
from datetime import datetime
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pika.spec import Basic, BasicProperties

from db_api import MongoConnector
from logger_config import logger
from queue_api import QueueConnector


class Fetcher:
    html_storage_path = "/app/html_pages"
    out_queue = os.getenv("OUT_QUEUE")

    def __init__(self):
        logger.info(f"Connect to queue")
        self.queue_connector = QueueConnector()
        self.mongo_connector = MongoConnector()
        os.makedirs(Fetcher.html_storage_path, exist_ok=True)

    @staticmethod
    def fetch_html(url: str) -> tuple[str, dict] | tuple[None, None]:
        """
        Fetches the HTML content of a given URL.
        """
        response = requests.get(url)
        if response.status_code == 200:
            return response.text, response.headers
        else:
            return None, None

    @staticmethod
    def save_html_to_local(url: str, html_content: str):
        """
        Saves the fetched HTML content to a local file.
        """
        sanitized_name = url.replace("http://", "").replace("https://", "").replace("/", "_")
        file_path = os.path.join(Fetcher.html_storage_path, f"{sanitized_name}.html")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        logger.info(f"Page {url} saved to local storage")
        return file_path

    @staticmethod
    def find_last_modified_date(html_headers: dict) -> datetime | None:
        """
        Finds the last modified date from the HTTP headers of the given URL.
        """
        if 'Last-Modified' in html_headers:
            last_modified_str = html_headers['Last-Modified']
            try:
                # Parse the Last-Modified header
                return datetime.strptime(last_modified_str, "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError as e:
                logger.error(f"Error parsing Last-Modified header: {e}")
        else:
            logger.warning("Last-Modified header not found in the response.")

        return None

    def process_message(self, channel, method: Basic.Deliver, properties: BasicProperties, body):
        """
        Processes a message by fetching HTML from the URL, saving it locally,
        extracting links from the HTML content, and publishing them to the out_queue.
        """
        delivery_tag = method.delivery_tag
        url = body.decode()
        retry_count = int(properties.headers.get("x-retry-count", 0)) if properties.headers else 0
        logger.debug(f"Processing URL: {url}, Retry Count: {retry_count}")

        try:
            html_content, html_headers = self.fetch_html(url)
            if not html_content:
                logger.error(f"Failed to fetch HTML from {url}")
                # send to retry queue with delay
                self.queue_connector.nack(delivery_tag)
                return
            # save html to localhost
            page_file_path = self.save_html_to_local(url, html_content)

            last_modified_date = self.find_last_modified_date(html_headers)
            # add url with metadata to mongo
            self.mongo_connector.save_url_to_db(url, page_file_path, last_modified_date)
            # find links
            links = self.find_html_links(url, html_content)

            # add to next message queues
            for link in links:
                self.queue_connector.publish(link, Fetcher.out_queue)

            self.queue_connector.ack(delivery_tag)

        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}, moving to dlx")
            # TODO: handle retries
            self.queue_connector.nack(delivery_tag, requeue=False)

    @staticmethod
    def find_html_links(start_url: str, html_content: str) -> List[str]:
        """
        Extracts all the hyperlinks from the HTML content.
        """
        html_soup = BeautifulSoup(html_content, "html.parser")
        links = set()
        for a_tag in html_soup.find_all("a", href=True):
            href = a_tag['href']
            links.add(urljoin(start_url, href))
        return list(links)

    def start(self):
        """
        Starts the queue consumption.
        """
        logger.info("Starting new fetcher")
        self.queue_connector.consume(os.getenv("IN_QUEUE"), self.process_message, False)

    def close(self):
        """
        Clean up resources.
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
