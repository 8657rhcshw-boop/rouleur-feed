import requests
import xml.etree.ElementTree as ET
from datetime import datetime


GOOGLE_RSS = "https://news.google.com/rss/search?q=site%3Arouleur.cc"


OUTPUT = "rouleur.xml"


def main():

    print("Scarico Google News RSS...")

    r = requests.get(
        GOOGLE_RSS,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )


    print("STATUS:", r.status_code)


    if r.status_code != 200:
        print("Errore download")
        return


    root = ET.fromstring(r.text)


    items = root.findall(".//item")


    print("Articoli trovati:", len(items))


    rss = ET.Element(
        "rss",
        {
            "version": "2.0"
        }
    )


    channel = ET.SubElement(
        rss,
        "channel"
    )


    ET.SubElement(
        channel,
        "title"
    ).text = "Rouleur RSS"


    ET.SubElement(
        channel,
        "link"
    ).text = "https://www.rouleur.cc"


    ET.SubElement(
        channel,
        "description"
    ).text = "Ultime notizie Rouleur"


    ET.SubElement(
        channel,
        "lastBuildDate"
    ).text = datetime.utcnow().strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )


    for item in items:

        new_item = ET.SubElement(
            channel,
            "item"
        )


        for tag in [
            "title",
            "link",
            "description",
            "pubDate"
        ]:

            value = item.find(tag)

            if value is not None:

                ET.SubElement(
                    new_item,
                    tag
                ).text = value.text


    tree = ET.ElementTree(rss)

    tree.write(
        OUTPUT,
        encoding="utf-8",
        xml_declaration=True
    )


    print("Creato:", OUTPUT)



if __name__ == "__main__":
    main()
