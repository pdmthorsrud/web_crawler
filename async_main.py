import asyncio
from bs4 import BeautifulSoup
import re
import time

import httpx

base_url = "https://oda.com"
regex = r"(\/no\/categories\/\d+)|(\/no\/products\/\d+)"
category_regex = r"\/no\/categories\/\d+"
product_regex = r"\/no\/products\/\d+"
url_list = ["/"]
crawled_urls = list()
product_file = open("products.txt", "a")


# async def get_content(url: str) -> httpx.Response:
#     async with httpx.AsyncClient(timeout=None) as client:
#         return await client.get(url)
async def get_content(url: str) -> httpx.Response.text:
    async with httpx.AsyncClient(timeout=None) as client:
        print(f"Getting content from {url}")
        response = await client.get(url)
        return response


async def find_all_links_in_url(url_extension: str, pattern: str):
    crawled_urls.append(url_extension)
    complete_url = base_url + url_extension
    match = re.search(product_regex, url_extension)
    if match is not None:
        print(f"Storing product from {complete_url}")
        content = await get_content(complete_url)
        parse_product_data(content)
    else:
        content = await get_content(complete_url)
        print(f"Fetching links from {complete_url}")
        get_links_in_content(content.text, pattern)


def get_links_in_content(content: httpx.Response.text, pattern: str) -> list:
    time.sleep(0.5)
    soup = BeautifulSoup(content, "html.parser")
    filtered_content = soup.find_all("a")
    for line in filtered_content:
        link = line.get("href")
        match = re.search(pattern, str(link))
        if match is not None:
            if link not in url_list:
                url_list.append(link)


def parse_product_data(html_body: str) -> None:
    return
    parsed_body = BeautifulSoup(html_body, "html.parser")
    meta_tags = parsed_body.find_all("meta")
    product_file.write("\n_______________________")
    for meta_tag in meta_tags:
        meta_content = meta_tag.get("content")
        meta_property = meta_tag.get("property")
        if (
                meta_property == "og:title"
                or meta_property == "product:price:amount"
                or meta_property == "product:price:currency"
        ):
            product_file.write("\n" + meta_content)
    product_file.write("\n_______________________\n")


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


async def crawl_url(url: str, pattern: str):
    index = 0
    while len(url_list) != len(crawled_urls):

        tasks = []

        for group in chunker(url_list, 10):
            print("___________________________________________")
            print(f"Found {len(url_list)} links so far")
            print(f"Crawled {len(crawled_urls)} links so far")
            print("___________________________________________")
            for url in group:
                if url not in crawled_urls:
                    tasks.append(asyncio.create_task(find_all_links_in_url(url, pattern)))
            await asyncio.gather(*tasks)

    product_file.close()

if __name__ == '__main__':
    asyncio.run(crawl_url(base_url, regex))
