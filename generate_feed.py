from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin
import datetime


SOURCE = "https://www.rouleur.cc/"
OUTPUT = "rouleur.xml"


def get_articles():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )
        )

        page.goto(
            SOURCE,
            wait_until="networkidle",
            timeout=60000
        )

        html = page.content()

        browser.close()


    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    articles = {}

    for a in soup.find_all(
        "a",
        href=True
    ):

        href = a["href"]

        if (
            "/stories/" in href
            or "/articles/" in href
            or "/blogs/" in href
        ):

            url = urljoin(
                SOURCE,
                href
            )

            title = a.get_text(
                " ",
                strip=True
            )


            if len(title) > 15:

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
    fg.title("Rouleur.cc")
    fg.link(
        href=SOURCE
    )
    fg.description(
        "Rouleur latest articles"
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
