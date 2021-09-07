import re
from bs4 import BeautifulSoup
import httpx



def get_content(url: str) -> httpx.Response:
    return httpx.get(url).text


def get_links_in_content(content: httpx.Response.text, pattern: str) -> list:
    soup = BeautifulSoup(content, "html.parser")
    filtered_content = soup.find_all("a")
    links: list[str] = []
    for line in filtered_content:
        link = line.get("href")
        match = re.search(pattern, str(link))
        if match is not None:
            links.append(link)
    return links


def add_uniques_to_list(item_list: list[str], unique_list: list):
    for item in item_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def crawl_for_regex_matched_links(base_url: str, unique_list: list[str], regex: str) -> list[str]:
    # Getting first set of links
    content = get_content(base_url)
    no_links_before = len(unique_list)
    category_links = get_links_in_content(content, regex)
    add_uniques_to_list(category_links, unique_list)
    no_links_after = len(unique_list)
    no_new_links = no_links_after - no_links_before
    print("The number of new categories is", no_new_links)

    while no_new_links != 0:
        no_links_before = len(unique_list)
        start_index = len(unique_list) - no_new_links
        print("The start index is", start_index)

        index = start_index
        for link in unique_list[start_index:]:
            print("Scanning index", index, "category " + link)
            content = get_content(base_url + link)
            new_links = get_links_in_content(content, regex)
            add_uniques_to_list(new_links, unique_list)
            index += 1

        no_links_after = len(unique_list)
        no_new_links = no_links_after - no_links_before
        print("The number of new categories is ", no_new_links)
    return unique_list

def parse_product_data(html_body: str) -> None:
    parsed_body = BeautifulSoup(html_body, "html.parser")
    meta_tags = parsed_body.find_all("meta")
    print("_______________________")
    for meta_tag in meta_tags:
        meta_content = meta_tag.get("content")
        meta_property = meta_tag.get("property")
        if (
            meta_property == "og:title"
            or meta_property == "product:price:amount"
            or meta_property == "product:price:currency"
        ):
            print(meta_content)
    print("_______________________")

def main():
    # Instantiating needed variables
    base_url = "https://oda.com"
    unique_categories = []
    unique_products = []
    category_regex = r"\/no\/categories\/\d+"
    product_regex = r"\/no\/products\/\d+"

    crawl_for_regex_matched_links(base_url, unique_categories, category_regex)
    print(unique_categories)

    # for link in unique_categories:
    #     print("Scanning category", base_url + link)
    #     content = get_content(base_url + link)
    #     new_links = get_links_in_content(content, product_regex)
    #     for product_link in new_links:
    #         product_content = get_content(base_url + product_link)
    #         parse_product_data(product_content)
    #     add_uniques_to_list(new_links, unique_products)
    #
    # print(unique_products)

    # no_links_before = len(unique_products)
    # content = get_content(base_url + unique_categories[0])
    # new_links = get_links_in_content(content, product_regex)
    # add_uniques_to_list(new_links, unique_products)
    # no_links_after = len(unique_products)
    # no_new_categories = no_links_after - no_links_before
    # print("The number of new products is", no_new_categories)

    # print("Scanning the category " + category_link)
    # product_content = get_content(category_link)
    # product_links = get_links_in_content(product_content, r"\/no\/products\/\d+")
    # add_uniques_to_list(product_links, unique_products)
    # print(unique_products)


if __name__ == '__main__':
    main()
