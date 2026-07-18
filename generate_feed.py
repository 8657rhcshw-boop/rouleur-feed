from playwright.sync_api import sync_playwright
import xml.etree.ElementTree as ET


URL = "https://www.rouleur.cc/news-sitemap.xml"


def main():

    print("Avvio browser...")


    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )


        context = browser.new_context(
            viewport={
                "width": 1280,
                "height": 900
            },
            locale="en-US",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            )
        )


        page = context.new_page()


        print("Scarico XML...")


        response = page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )


        xml = response.text()


        print("Primi caratteri XML:")
        print(xml[:500])


        print("\nParsing XML...")


        root = ET.fromstring(xml)


        namespace = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
        }


        articles = []


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


        print(
            "Articoli trovati:",
            len(articles)
        )


        for article in articles[:10]:
            print(
                "-",
                article
            )


        browser.close()



if __name__ == "__main__":
    main()
