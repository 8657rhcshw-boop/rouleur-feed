import asyncio
import xml.etree.ElementTree as ET
from playwright.async_api import async_playwright


URL = "https://www.rouleur.cc/news-sitemap.xml"


async def main():

    print("Avvio browser...")

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        print("Apro sitemap...")

        await page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        await page.wait_for_timeout(5000)

        print("Leggo contenuto pagina...")

        content = await page.content()

        print("--- PRIMI CARATTERI ---")
        print(content[:500])
        print("--- FINE ---")


        # Prova a prendere il vero XML dal DOM
        text = await page.locator("body").inner_text()


        print("--- TEST XML ---")
        print(text[:500])
        print("--- FINE TEST ---")


        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
