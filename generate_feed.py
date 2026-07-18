from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


SITEMAP = "https://www.rouleur.cc/news-sitemap.xml"


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

        print("--- TITLE ---")
        print(page.title())

        html = page.content()

        print("\n--- HTML ---")
        print(html[:1000])

        browser.close()

    return html



html = get_sitemap()


soup = BeautifulSoup(
    html,
    "xml"
)


print("\n--- LOC TROVATI ---")

locs = soup.find_all(
    "loc"
)

print(
    "Numero:",
    len(locs)
)


for loc in locs[:20]:
    print(
        loc.text
    )
