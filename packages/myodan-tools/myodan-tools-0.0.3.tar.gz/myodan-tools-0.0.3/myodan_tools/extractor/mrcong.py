import requests
from bs4 import BeautifulSoup

# href="((?:http|https):\/\/mrcong.com\/(?!tag\/)[^"]+)


def extract_post_links(url_str: str):
    current_page = 0
    links = []

    while True:
        current_page += 1
        page = requests.get(url_str + f"/page/{current_page}")

        if page.status_code == 404:
            break

        if page.status_code != 200:
            print("err")

        bs = BeautifulSoup(page.text, "lxml")
        links += bs.select('.post-box-title a[href*="mrcong.com"]')

    return links


def extract_download_links(url_str: str):
    page = requests.get(url_str)
    bs = BeautifulSoup(page.text, "lxml")
    links = bs.select('a[href*="mediafire.com"]')

    return links
