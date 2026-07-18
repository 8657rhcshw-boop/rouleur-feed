import feedparser
import requests
import time
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, ElementTree
from html import unescape
from urllib.parse import quote


# ==========================
# CONFIGURAZIONE
# ==========================

SITE = "rouleur.cc"

GOOGLE_NEWS_RSS = (
    "https://news.google.com/rss/search?q="
    + quote(f"site:{SITE}")
)

OUTPUT_FILE = "rouleur.xml"

MAX_ITEMS = 30


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}


# ==========================
# ESTRAZIONE LINK ORIGINALE
# ==========================

def get_original_url(url):
    """
    Trasforma il link Google News nel link reale dell'articolo.
    """

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )

        final_url = r.url

        # evita eventuali redirect Google rimasti
        if "news.google.com" not in final_url:
            return final_url

        return url

    except Exception:
        return url


# ==========================
# DOWNLOAD GOOGLE NEWS RSS
# ==========================

def download_feed():

    print("Scarico Google News RSS...")
    print(GOOGLE_NEWS_RSS)

    response = requests.get(
        GOOGLE_NEWS_RSS,
        headers=HEADERS,
        timeout=20
    )

    print("STATUS:", response.status_code)

    response.raise_for_status()

    feed = feedparser.parse(response.text)

    print(
        "Articoli trovati:",
        len(feed.entries)
    )

    return feed.entries


# ==========================
# CREAZIONE RSS
# ==========================

def create_rss(entries):

    rss = Element(
        "rss",
        {
            "version": "2.0"
        }
    )

    channel = SubElement(
        rss,
        "channel"
    )

    SubElement(
        channel,
        "title"
    ).text = "Rouleur Cycling News"

    SubElement(
        channel,
        "link"
    ).text = "https://www.rouleur.cc"

    SubElement(
        channel,
        "description"
    ).text = "Latest news from Rouleur"

    SubElement(
        channel,
        "lastBuildDate"
    ).text = datetime.now(
        timezone.utc
    ).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )


    count = 0


    for entry in entries:

        if count >= MAX_ITEMS:
            break


        title = unescape(
            entry.get(
                "title",
                "Rouleur article"
            )
        )


        google_link = entry.get(
            "link",
            ""
        )


        print("Processo:", title)


        original_link = get_original_url(
            google_link
        )


        item = SubElement(
            channel,
            "item"
        )


        SubElement(
            item,
            "title"
        ).text = title


        SubElement(
            item,
            "link"
        ).text = original_link


        SubElement(
            item,
            "guid"
        ).text = original_link


        description = entry.get(
            "description",
            ""
        )


        SubElement(
            item,
            "description"
        ).text = description


        if "published" in entry:
            SubElement(
                item,
                "pubDate"
            ).text = entry.published


        count += 1


        # evita troppe richieste consecutive
        time.sleep(0.2)



    tree = ElementTree(rss)

    tree.write(
        OUTPUT_FILE,
        encoding="utf-8",
        xml_declaration=True
    )


    print()
    print(
        "Creato:",
        OUTPUT_FILE
    )



# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    articles = download_feed()

    create_rss(
        articles
    )
