import feedparser
from feedgen.feed import FeedGenerator
import datetime


SOURCE_FEED = "https://www.rouleur.cc/feed"

OUTPUT = "rouleur.xml"


def create_feed():

    source = feedparser.parse(SOURCE_FEED)

    fg = FeedGenerator()

    fg.id("https://www.rouleur.cc")
    fg.title("Rouleur.cc - All Articles")
    fg.link(
        href="https://www.rouleur.cc"
    )
    fg.description(
        "Rouleur articles feed"
    )
    fg.language("en")


    for article in source.entries:

        fe = fg.add_entry()

        fe.id(
            article.link
        )

        fe.title(
            article.title
        )

        fe.link(
            href=article.link
        )

        if hasattr(article, "summary"):
            fe.description(
                article.summary
            )

        if hasattr(article, "published_parsed"):

            date = datetime.datetime(
                *article.published_parsed[:6]
            )

            fe.published(
                date
            )


    fg.rss_file(
        OUTPUT,
        pretty=True
    )


create_feed()

print("Feed creato")
