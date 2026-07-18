import requests
import xml.etree.ElementTree as ET
from datetime import datetime, UTC
from urllib.parse import urlparse, parse_qs


GOOGLE_RSS = "https://news.google.com/rss/search?q=site%3Arouleur.cc"

OUTPUT = "rouleur.xml"


def extract_real_url(url):

    """
    Prova a recuperare il link originale da Google News.
    """

    try:

        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15,
            allow_redirects=True
        )

        final_url = r.url

        if "rouleur.cc" in final_url:
            return final_url

    except Exception:
        pass


    return url



def main():

    print("Scarico Google News RSS...")


    response = requests.get(
        GOOGLE_RSS,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )


    print("STATUS:", response.status_code)


    if response.status_code != 200:
        print("Errore download RSS")
        return



    root = ET.fromstring(response.text)


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
    ).text = datetime.now(UTC).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )



    for item in items:

        new_item = ET.SubElement(
            channel,
            "item"
        )


        title = item.find("title")
        link = item.find("link")
        description = item.find("description")
        pubdate = item.find("pubDate")


        if title is not None:
            ET.SubElement(
                new_item,
                "title"
            ).text = title.text



        if link is not None:

            real_link = extract_real_url(
                link.text
            )

            print(
                "LINK:",
                real_link
            )


            ET.SubElement(
                new_item,
                "link"
            ).text = real_link



        if description is not None:

            ET.SubElement(
                new_item,
                "description"
            ).text = description.text



        if pubdate is not None:

            ET.SubElement(
                new_item,
                "pubDate"
            ).text = pubdate.text



    tree = ET.ElementTree(rss)


    tree.write(
        OUTPUT,
        encoding="utf-8",
        xml_declaration=True
    )


    print("Creato:", OUTPUT)



if __name__ == "__main__":
    main()
