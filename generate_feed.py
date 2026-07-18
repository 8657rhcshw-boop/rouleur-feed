from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


SITEMAP = "https://www.rouleur.cc/sitemap.xml"


def get_sitemap():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )
        )

        page.goto(
            SITEMAP,
            wait_until="networkidle",
            timeout=60000
        )

        print("\n--- TITLE ---")
        print(page.title())

        print("\n--- BODY INIZIO ---")

        body = page.locator("body").inner_text()

        print(
            body[:1000]
        )

        print("\n--- HTML INIZIO ---")

        html = page.content()

        print(
            html[:1000]
        )

        browser.close()


    return html



html = get_sitemap()


soup = BeautifulSoup(
    html,
    "html.parser"
)


print("\n--- URL TROVATI ---")

urls = soup.find_all(
    "loc"
)

print(
    "Numero loc:",
    len(urls)
)


for url in urls[:10]:

    print(
        url.text
    )
