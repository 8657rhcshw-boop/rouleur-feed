from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime


SITEMAP = "https://www.rouleur.cc/sitemap.xml"
OUTPUT = "rouleur.xml"


CATEGORIES = [
    "/racing/",
    "/tech/",
    "/culture/",
    "/adventure/",
    "/performance/",
]


def get_sitemap():

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
            SITEMAP,
            wait_until="networkidle",
            timeout=60000
        )

        content = page.content()

        browser.close()


    return content



def get_articles():

    xml = get_sitemap()


    soup = BeautifulSoup(
        xml,
        "xml"
    )


    articles = []


    for url in soup.find_all("url"):

        loc = url.find("loc")

        if not loc:
            continue


        link = loc.text.strip()


        if any(
            cat in link
            for cat in CATEGORIES
        ):

            lastmod = url.find(
                "lastmod"
            )

            date = None

            if lastmod:

                try:

                    date = datetime.fromisoformat(
                        lastmod.text.strip()
                        .replace("Z", "+00:00")
                    )

                except:

                    pass


            articles.append(
                {
                    "url": link,
                    "date": date
                }
            )


    return articles



def create_feed(articles):

    fg = FeedGenerator()

    fg.id(
        "https://www.rouleur.cc"
    )

    fg.title(
        "Rouleur.cc"
    )

    fg.link(
        href="https://www.rouleur.cc"
    )

    fg.description(
        "Rouleur latest articles"
    )

    fg.language(
        "en"
    )


    for article in articles:

        fe = fg.add_entry()

        fe.id(
            article["url"]
        )

        fe.link(
            href=article["url"]
        )

        title = (
            article["url"]
            .split("/")
            [-1]
            .replace("-", " ")
            .title()
        )

        fe.title(
            title
        )


        if article["date"]:

            fe.pubDate(
                article["date"]
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
