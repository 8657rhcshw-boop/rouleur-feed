import asyncio
from playwright.async_api import async_playwright


URL = "https://www.rouleur.cc/sitemap.xml"


async def main():

    print("Avvio browser...")

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            )
        )


        print("Apro sitemap...")

        response = await page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )


        print("STATUS:")
        print(response.status)


        await page.wait_for_timeout(3000)


        text = await page.locator("body").inner_text()


        print("--- RISULTATO ---")
        print(text[:1000])
        print("--- FINE ---")


        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
