from playwright.sync_api import sync_playwright
import xml.etree.ElementTree as ET
import time


URL = "https://www.rouleur.cc/news-sitemap.xml"


def get_xml():

    print("Avvio browser...")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            ),
            locale="en-US"
        )

        page = context.new_page()


        print("Apro sitemap...")

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )


        print("Titolo pagina:")
        print(page.title())


        # Aspetta eventuale controllo Vercel
        for i in range(30):

            title = page.title()

            if "Security Checkpoint" not in title:
                break

            print(
                "Checkpoint Vercel in corso...",
                i + 1
            )

            time.sleep(2)


        content = page.content()


        print("Titolo finale:")
        print(page.title())


        browser.close()

        return content



def parse_articles(xml):

    articles = []

    try:

        root = ET.fromstring(xml)

        namespace = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
        }


        for item in root.findall(
            "sm:url",
            namespace
        ):

            loc = item.find(
                "sm:loc",
                namespace
            )

            if loc is not None:
                articles.append(loc.text)


    except Exception as e:

        print(
            "Errore parsing:",
            e
        )

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
        print(
            "-",
            article
        )



if __name__ == "__main__":
    main()
