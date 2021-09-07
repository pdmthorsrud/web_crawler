import asyncio
from bs4 import BeautifulSoup
import re
import time

import httpx

base_url = "https://oda.com"
combined_regex = r"(\/no\/categories\/\d+)|(\/no\/products\/\d+)"
crawl_page_regex = r"\/no\/categories\/\d+"
store_page_regex = r"\/no\/products\/\d+"
to_crawl_urls = ["/"]
crawled_urls = list()
product_file = open("products.txt", "a")


# Get an html_body, let program keep running while waiting
async def get_content(url: str) -> httpx.Response.text:
    async with httpx.AsyncClient(timeout=None) as client:
        print(f"Getting content from {url}")
        response = await client.get(url)
        return response


# Fetch all links, store content if matching store_page_regex, add to to_crawl_urls if matching crawl_page_regex
async def find_all_links_in_url(url_extension: str, pattern: str) -> None:
    crawled_urls.append(url_extension)
    complete_url = base_url + url_extension
    match = re.search(store_page_regex, url_extension)
    # Parse the product's data if it as a page we want to store
    if match is not None:
        print(f"Storing product from {complete_url}")
        content = await get_content(complete_url)
        parse_to_store_page(content)
    # Add the link to to_crawl_urls if it a page we want to crawl
    else:
        content = await get_content(complete_url)
        print(f"Fetching links from {complete_url}")
        parse_to_crawl_page(content, pattern)


# Add all relevant links from page to to_crawl_urls list (if it does not already exist)
def parse_to_crawl_page(content: httpx.Response, pattern: str) -> None:
    # time.sleep(0.5)
    soup = BeautifulSoup(content, "html.parser")
    filtered_content = soup.find_all("a")
    for line in filtered_content:
        link = line.get("href")
        match = re.search(pattern, str(link))
        if match is not None:
            if link not in to_crawl_urls:
                to_crawl_urls.append(link)


# Store relevant information from the page to document
def parse_to_store_page(content: httpx.Response) -> None:
    parsed_body = BeautifulSoup(content, "html.parser")
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


# Divides a list into `size` sized chunks
def chunker(seq, size) -> list:
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


async def crawl():

    while len(to_crawl_urls) != len(crawled_urls):

        tasks = []

        for group in chunker(to_crawl_urls, 10):
            print("\n")
            print("___________________________________________")
            print(f"Found {len(to_crawl_urls)} links so far")
            print(f"Crawled {len(crawled_urls)} links so far")
            print("___________________________________________")
            for url in group:
                if url not in crawled_urls:
                    tasks.append(asyncio.create_task(find_all_links_in_url(url, combined_regex)))
            # Wait for the 10 tasks to finish before moving to next group
            await asyncio.gather(*tasks)

    product_file.close()

if __name__ == '__main__':
    asyncio.run(crawl())
