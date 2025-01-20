import aiohttp
from bs4 import BeautifulSoup
import asyncio
from urllib.parse import urljoin
import time


async def fetch_page(session, url):
    """Fetch the content of a page."""
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Error: Received status code {response.status} for URL: {url}")
                return None
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
        return None
    except asyncio.TimeoutError:
        print(f"TimeoutError: The request to {url} timed out.")
        return None


def extract_links(page_content, base_url, all_links):
    """Extract valid Wikipedia links from a page content."""
    if not page_content:
        return []

    soup = BeautifulSoup(page_content, "html.parser")
    links = []

    # All <a> tags with href attributes
    for a_tag in soup.select("a[href]"):
        href = a_tag["href"]
        # Filter for Wikipedia article links
        if href.startswith("/wiki/") and ":" not in href:
            full_url = urljoin(base_url, href)
            if full_url not in all_links:
                links.append(full_url)

    return links


async def collect_page_links(session, url, cur_depth, max_depth, all_links):
    """Collect links and store them with their respective depth in a dictionary."""
    if cur_depth > max_depth or url in all_links:
        return

    print(f"Visiting page {url} with depth {cur_depth}")
    # Fetch page content
    page_content = await fetch_page(session, url)
    if not page_content:
        return

    # Add current URL with its depth to the dictionary
    all_links[url] = cur_depth

    # Extract links from the page
    links = extract_links(page_content, url, all_links)

    # Recursively fetch links for each found link
    tasks = [
        collect_page_links(session, link, cur_depth + 1, max_depth, all_links)
        for link in links
    ]
    await asyncio.gather(*tasks)


async def main():
    start_url = "https://en.wikipedia.org/wiki/Main_Page"
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        all_links = {}  # Dictionary to store links with their depth
        await collect_page_links(
            session, start_url, 1, max_depth=2, all_links=all_links
        )
    total_time = time.time() - start_time
    print(f"Time taken to collect all links: {total_time:.2f} seconds")
    print(f"Total links found: {len(all_links)}")
    for link, depth in all_links.items():
        print(f"{link} - Depth: {depth}")


if __name__ == "__main__":
    asyncio.run(main())
