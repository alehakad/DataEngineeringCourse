import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def fetch(url, session):
    try:
        async with session.get(url, timeout=10) as response:
            # Check if the request was successful
            if response.status == 200:
                return await response.text()
            else:
                print(f"Error: Received status code {response.status} for URL: {url}")
                return None
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_sorted_words(html):
    soup = BeautifulSoup(html, "html.parser")
    page_words = soup.get_text().split()

    # Filter out empty strings and sort words by length
    filtered_words = [word for word in page_words if word.strip()]
    sorted_words = sorted(filtered_words, key=len, reverse=True)

    return sorted_words


async def main():
    url = "https://en.wikipedia.org/wiki/Lyapis_Trubetskoy"

    async with aiohttp.ClientSession() as session:
        html = await fetch(url, session)
        if html:
            sorted_words = extract_sorted_words(html)
            for word in sorted_words[:10]:
                print(word)


if __name__ == "__main__":
    asyncio.run(main())
