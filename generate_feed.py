from playwright.sync_api import sync_playwright
import time


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
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )


        page = context.new_page()


        print("Apro sito...")


        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )


        print("Titolo iniziale:")
        print(page.title())


        print("Aspetto eventuale verifica...")


        time.sleep(15)


        print("Titolo dopo attesa:")
        print(page.title())


        html = page.content()


        print("\n--- INIZIO ---")
        print(html[:1000])
        print("--- FINE ---")


        browser.close()



if __name__ == "__main__":
    main()
