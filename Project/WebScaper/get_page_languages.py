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


def extract_languages_from_html(html):
    # doesnt include original language
    all_languages = []
    soup = BeautifulSoup(html, "html.parser")
    links_with_lang = soup.find_all("a", attrs={"lang": True})
    for language_link in links_with_lang:

        # extarct lamguage link
        language_page_url = language_link.get("href")
        # extract language name from span text
        language_name = language_link.find("span")
        language_name = (
            language_name.get_text() if language_name else "Unknown Language"
        )
        all_languages.append((language_page_url, language_name))

    return all_languages


async def main():
    url = "https://en.wikipedia.org/wiki/Lyapis_Trubetskoy"

    async with aiohttp.ClientSession() as session:
        html = await fetch(url, session)
        if html:
            all_languages = extract_languages_from_html(html)
            for language in all_languages:
                print(language)


if __name__ == "__main__":
    asyncio.run(main())
