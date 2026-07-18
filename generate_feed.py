import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin
import datetime
import re


SOURCE = "https://www.rouleur.cc/"
OUTPUT = "rouleur.xml"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def get_articles():

    r = requests.get(
        SOURCE,
        headers=HEADERS,
        timeout=30
    )

    r.raise_for_status()

    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )


    articles = {}

    for a in soup.find_all(
        "a",
        href=True
    ):

        href = a["href"]

        if (
            "/blogs/" in href
            or "/stories/" in href
            or "/articles/" in href
        ):

            url = urljoin(
                SOURCE,
                href
            )

            title = a.get_text(
                " ",
                strip=True
            )


            if (
                len(title) > 15
                and url not in articles
            ):

                articles[url] = {
                    "title": title,
                    "url": url
                }


    return list(
        articles.values()
    )



def create_feed(items):

    fg = FeedGenerator()

    fg.id(SOURCE)
    fg.title(
        "Rouleur.cc"
    )

    fg.link(
        href=SOURCE
    )

    fg.description(
        "Rouleur latest stories"
    )

    fg.language(
        "en"
    )


    for item in items:

        fe = fg.add_entry()

        fe.id(
            item["url"]
        )

        fe.title(
            item["title"]
        )

        fe.link(
            href=item["url"]
        )

        fe.published(
            datetime.datetime.now()
        )


    fg.rss_file(
        OUTPUT,
        pretty=True
    )



articles = get_articles()

print(
    "Articoli trovati:",
    len(articles)
)


create_feed(
    articles
)
