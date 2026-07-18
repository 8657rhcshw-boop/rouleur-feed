import requests
import time
import xml.etree.ElementTree as ET


URL = "https://www.rouleur.cc/news-sitemap.xml"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Accept": "application/xml,text/xml,*/*"
}


def get_sitemap():
    print("Scarico sitemap...")

    for tentativo in range(3):
        try:
            response = requests.get(
                URL,
                headers=HEADERS,
                timeout=30
            )

            print("STATUS:", response.status_code)

            if response.status_code == 200:
                return response.text

            elif response.status_code == 429:
                print("Troppi tentativi. Aspetto...")
                time.sleep(10)

            else:
                print("Errore HTTP:", response.status_code)

        except Exception as e:
            print("Errore richiesta:", e)

        time.sleep(5)

    return None


def parse_articles(xml_text):
    articles = []

    try:
        root = ET.fromstring(xml_text)

        namespace = {
            "news": "http://www.google.com/schemas/sitemap-news/0.9",
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
        }

        for url in root.findall("sm:url", namespace):
            loc = url.find("sm:loc", namespace)

            if loc is not None:
                articles.append(loc.text)

        return articles

    except Exception as e:
        print("Errore parsing XML:", e)
        return []


def main():

    xml = get_sitemap()

    if not xml:
        print("Nessun XML ricevuto")
        return

    print("\n--- INIZIO XML ---")
    print(xml[:1000])
    print("--- FINE XML ---\n")


    articles = parse_articles(xml)

    print("Articoli trovati:", len(articles))

    for articolo in articles[:10]:
        print("-", articolo)


if __name__ == "__main__":
    main()
