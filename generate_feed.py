from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin


SOURCE = "https://www.rouleur.cc/"


def get_articles():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            )
        )

        page.goto(
            SOURCE,
            wait_until="networkidle",
            timeout=60000
        )

        html = page.content()

        browser.close()


    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    print("\n--- LINK TROVATI ---\n")


    links = []

    for a in soup.find_all(
        "a",
        href=True
    ):

        text = a.get_text(
            " ",
            strip=True
        )

        href = urljoin(
            SOURCE,
            a["href"]
        )

        if text:

            links.append(
                {
                    "text": text,
                    "href": href
                }
            )


    for link in links[:100]:

        print(
            link["text"],
            "=>",
            link["href"]
        )


    print(
        "\nTotale link:",
        len(links)
    )


    return []



articles = get_articles()

print(
    "Articoli trovati:",
    len(articles)
)
