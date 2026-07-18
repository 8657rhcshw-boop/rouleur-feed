import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
from email.utils import format_datetime


SITEMAP = "https://www.rouleur.cc/sitemap.xml"
OUTPUT = "rouleur.xml"


CATEGORIES = [
    "/racing/",
    "/tech/",
    "/culture/",
    "/adventure/",
    "/performance/",
]


def get_articles():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(
        SITEMAP,
        headers=headers,
        timeout=30
    )

    r.raise_for_status()


    soup = BeautifulSoup(
        r.text,
        "xml"
    )


    articles = []


    for url in soup.find_all("url"):

        loc = url.find("loc")

        if not loc:
            continue


        link = loc.text.strip()


        if any(
            category in link
            for category in CATEGORIES
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
