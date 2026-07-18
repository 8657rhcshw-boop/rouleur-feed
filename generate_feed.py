import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from dateutil import parser
import datetime
import re


BASE = "https://www.rouleur.cc"
SITEMAP = BASE + "/sitemap.xml"

OUTPUT = "rouleur.xml"


HEADERS = {
    "User-Agent": 
    "Mozilla/5.0 (RSS reader)"
}


def get_xml(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.text



def get_article_urls():

    xml = get_xml(SITEMAP)

    soup = BeautifulSoup(xml, "xml")

    urls = []

    for loc in soup.find_all("loc"):

        url = loc.text.strip()

        if "/blogs/news/" in url:
            urls.append(url)


    return list(set(urls))



def parse_article(url):

    html = get_xml(url)

    soup = BeautifulSoup(html, "html.parser")


    # titolo
    title = None

    og_title = soup.find(
        "meta",
        property="og:title"
    )

    if og_title:
        title = og_title.get("content")


    if not title:
        title = soup.title.text


    # immagine
    image = None

    og_image = soup.find(
        "meta",
        property="og:image"
    )

    if og_image:
        image = og_image.get("content")


    # descrizione
    desc = ""

    meta = soup.find(
        "meta",
        property="og:description"
    )

    if meta:
        desc = meta.get("content","")


    # data
    date = datetime.datetime.now()

    time = soup.find(
        "time"
    )

    if time and time.get("datetime"):
        try:
            date = parser.parse(
                time["datetime"]
            )
        except:
            pass


    # premium detection
    premium = False

    text = soup.get_text(
        " ",
        strip=True
    ).lower()


    if (
        "subscriber" in text
        or "members" in text
        or "premium" in text
    ):
        premium = True



    return {
        "title": title,
        "url": url,
        "image": image,
        "description": desc,
        "date": date,
        "premium": premium
    }




def create_feed(items):

    fg = FeedGenerator()

    fg.id(BASE)
    fg.title(
        "Rouleur.cc"
    )

    fg.link(
        href=BASE
    )

    fg.description(
        "All Rouleur articles including subscriber content"
    )

    fg.language(
        "en"
    )


    for item in items:

        fe = fg.add_entry()

        title = item["title"]

        if item["premium"]:
            title = "🔒 " + title


        fe.id(
            item["url"]
        )

        fe.title(
            title
        )

        fe.link(
            href=item["url"]
        )


        fe.description(
            item["description"]
        )

        fe.published(
            item["date"]
        )


    fg.rss_file(
        OUTPUT,
        pretty=True
    )



urls = get_article_urls()


articles = []


for url in urls[:200]:

    try:
        article = parse_article(url)
        articles.append(article)

    except Exception as e:
        print(
            "Errore:",
            url,
            e
        )


articles.sort(
    key=lambda x:x["date"],
    reverse=True
)


create_feed(
    articles
)


print(
    f"Creati {len(articles)} articoli"
)
