from playwright.sync_api import sync_playwright
import xml.etree.ElementTree as ET


URL = "https://www.rouleur.cc/news-sitemap.xml"


def get_xml():

    print("Avvio browser...")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        print("Apro sitemap...")

        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        content = page.content()

        print("Pagina caricata")

        browser.close()

        return content



def parse_articles(xml):

    articles = []

    try:

        root = ET.fromstring(xml)

        namespace = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
        }

        for item in root.findall("sm:url", namespace):

            loc = item.find(
                "sm:loc",
                namespace
            )

            if loc is not None:
                articles.append(loc.text)

    except Exception as e:
        print("Errore parsing:", e)

    return articles



def main():

    xml = get_xml()

    print("\n--- RISPOSTA ---")
    print(xml[:500])
    print("--- FINE ---")


    articles = parse_articles(xml)

    print(
        "Articoli trovati:",
        len(articles)
    )

    for article in articles[:10]:
        print(article)



if __name__ == "__main__":
    main()
