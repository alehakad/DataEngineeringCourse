import os
import re
from datetime import datetime
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
        self.queue_connector = QueueConnector()
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

    @staticmethod
    def find_last_modified_date(html_soup):
        footer_info = html_soup.find("li", id="footer-info-lastmod")
        if footer_info:
            text = footer_info.get_text(strip=True)
            date_pattern = r"\d{1,2} \w+ \d{4}"
            match = re.search(date_pattern, text)

            if match:
                date_str = match.group(0)
                try:
                    # Convert the extracted date string into a datetime object
                    last_modified_date = datetime.strptime(date_str, "%d %B %Y")
                    return last_modified_date
                except ValueError as e:
                    logger.error(f"Error parsing date: {e}")

        logger.error("Element with id 'footer-info-lastmod' not found.")
        return None

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
        page_file_path = self.save_html_to_local(url, html_content)

        html_soup = BeautifulSoup(html_content, "html.parser")
        last_modified_date = self.find_last_modified_date(html_soup)
        # add url with metadata to mongo
        self.mongo_connector.save_url_to_db(url, page_file_path, last_modified_date)
        # find links
        links = self.find_html_links(html_soup)
        # add to next message queues
        for link in links:
            self.queue_connector.publish(link, Fetcher.out_queue)

    @staticmethod
    def find_html_links(html_soup) -> List[str]:
        """
        Extracts all the hyperlinks from the HTML content.
        """

        links = set()
        for a_tag in html_soup.find_all("a", href=True):
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
